"""
Offline ablation of the null-space secondary objective for the model-based
controller (Eq. 8-10 / Algorithm 1 in the paper).

The real closed-loop logs (results/ControlWorkspaceJacobian.npz etc.) only
ever store the final camera/mocap pose per target, never the tendon lengths
or motor current, so H(l) cannot be recovered from hardware telemetry after
the fact. This script instead *replays* the resolved-motion-rate control law
against the PCC forward-kinematics model, driving through the same 20
k-medoids targets in the same order, with and without the null-space term
N @ (DELTAL_mean - DELTAL) -- reusing the exact Jacobian/pseudo-inverse/
null-space math from MULTIController, but against a simulated forward model
instead of real cameras and motors.

This is a simulated/offline comparison, not a hardware measurement: it shows
what the null-space objective is doing to the tendon configuration for a
given target sequence, holding the target sequence identical between the two
conditions, which is not something the hardware logs support on their own.

Run from within MULTI/.
"""
import numpy as np
import torch
from scipy.spatial.transform import Rotation as R, Slerp

from MULTI_jacobians import q2tendon, q2coordinates

Q2TENDON = q2tendon()
Q2COORDS = q2coordinates()

DAMPING = 0.1       # lambda, matches MULTIController.PseudoInverse default
CONVERGENCE = 10.0  # gamma, matches MULTIController default convergence=10
DISCR_WP = 1.0      # epsilon, matches the paper's 1 mm waypoint spacing


def integrate_forward(DELTAL0, DxDyDl0, coords0, d_DELTAL, step_size=2.0):
    """Numerically integrates the PCC forward map DELTAL -> (DxDyDl, coords)
    for a tendon-length increment d_DELTAL, using local-Jacobian sub-stepping.
    Same logic as MULTI_kinematics.tendon2coordinates, but reuses the
    module-level Q2TENDON/Q2COORDS instead of re-deriving the symbolic
    Jacobians via sympy on every call -- that re-derivation is cheap for a
    single real hardware iteration but makes a multi-thousand-iteration
    offline replay intractable.
    """
    if np.linalg.norm(DxDyDl0) < 1e-4:
        DxDyDl0 = np.full(9, 1e-4)

    N = max(int(np.ceil(np.linalg.norm(d_DELTAL) / step_size)), 5)
    d_DELTAL_step = d_DELTAL / N

    DELTAL, DxDyDl, coords = np.copy(DELTAL0), np.copy(DxDyDl0), np.copy(coords0)
    for _ in range(N):
        J_tendon = Q2TENDON(*DxDyDl)
        J_coords = Q2COORDS(*DxDyDl)
        d_DxDyDl = np.linalg.pinv(J_tendon) @ d_DELTAL_step
        DxDyDl = DxDyDl + d_DxDyDl
        coords = coords + J_coords @ d_DxDyDl
        DELTAL = DELTAL + d_DELTAL_step
    return DELTAL, DxDyDl, coords


def kinematics(DELTAL):
    """DELTAL (9,) -> DxDyDl (9,), same formula as MULTIController.kinematics."""
    deltas = [
        np.radians([0, 120, -120]),
        np.radians([60, 180, -60]),
        np.radians([150, 270, 30]),
    ]
    DxDyDl = []
    for i in range(3):
        section = DELTAL[i * 3:(i + 1) * 3]
        delta = deltas[i]
        Dl = np.mean(section)
        Dx = (2 / 3) * np.sum(-section * np.cos(delta))
        Dy = (2 / 3) * np.sum(-section * np.sin(delta))
        DxDyDl.extend([Dx, Dy, Dl])
    return np.array(DxDyDl)


def analytic_jacobian(DELTAL):
    DxDyDl = kinematics(DELTAL)
    return Q2COORDS(*DxDyDl) @ np.linalg.pinv(Q2TENDON(*DxDyDl)), DxDyDl


def pseudo_inverse(J, k=DAMPING):
    return J.T @ np.linalg.pinv(J @ J.T + k**2 * np.eye(J.shape[0]))


def null_space_proj(J, J_pseudo):
    return np.eye(J.shape[1]) - J_pseudo @ J


def angular_distance(euler_a, euler_b):
    r_a = R.from_euler('zyx', euler_a)
    r_b = R.from_euler('zyx', euler_b)
    return np.linalg.norm((r_b * r_a.inv()).as_rotvec())


def get_next_waypoint(current_pose, target_pose, discr_wp=DISCR_WP):
    curr_pos, curr_euler = current_pose[:3], current_pose[3:]
    targ_pos, targ_euler = target_pose[:3], target_pose[3:]
    trans_dist = np.linalg.norm(targ_pos - curr_pos)
    rot_dist_mm = np.rad2deg(angular_distance(curr_euler, targ_euler))
    N_waypoints = int(np.ceil((trans_dist + rot_dist_mm / 5.0) / discr_wp)) + 1
    if N_waypoints < 2:
        return target_pose.copy()
    t_values = np.linspace(0, 1, N_waypoints)
    positions = np.linspace(curr_pos, targ_pos, N_waypoints)
    slerp = Slerp([0, 1], R.from_euler('zyx', [curr_euler, targ_euler]))
    orientations = slerp(t_values).as_euler('zyx')
    return np.column_stack([positions, orientations])[1:][0]


def compute_pose_error(pose_a, pose_b):
    pos_error = np.linalg.norm(pose_a[:3] - pose_b[:3])
    rot_error_deg = np.rad2deg(angular_distance(pose_a[3:], pose_b[3:]))
    return pos_error + rot_error_deg / 5.0


def simulate_sequence(targets, DELTAL_mean, with_null=True, max_iters_per_target=3000):
    """Replays the resolved-motion-rate law sequentially through `targets`
    (in the recorded order), starting from the straight configuration and
    carrying state across targets, exactly as the real persistent
    MULTIController object does across a run of the target-reaching suite."""

    DELTAL = np.full(9, 1e-4)
    DxDyDl = np.full(9, 1e-4)
    coords = np.array([1e-4, 1e-4, 145 * 3, 1e-4, 1e-4, 1e-4])

    final_poses, final_deltals, n_iters_list, converged_list = [], [], [], []

    for target in targets:
        n_iters = 0
        while compute_pose_error(coords, target) > CONVERGENCE and n_iters < max_iters_per_target:
            p_ref = get_next_waypoint(coords, target)
            J, DxDyDl = analytic_jacobian(DELTAL)
            J_pseudo = pseudo_inverse(J)
            d_DELTAL = J_pseudo @ (p_ref - coords)
            if with_null:
                N = null_space_proj(J, J_pseudo)
                d_DELTAL = d_DELTAL + N @ (DELTAL_mean - DELTAL)
            DELTAL, DxDyDl, coords = integrate_forward(DELTAL, DxDyDl, coords, d_DELTAL)
            n_iters += 1

        final_poses.append(coords.copy())
        final_deltals.append(DELTAL.copy())
        n_iters_list.append(n_iters)
        converged_list.append(compute_pose_error(coords, target) <= CONVERGENCE)

    return (np.array(final_poses), np.array(final_deltals),
            np.array(n_iters_list), np.array(converged_list))


def H(deltal, DELTAL_mean):
    return 0.5 * np.sum((deltal - DELTAL_mean) ** 2, axis=-1)


def rms_dev(deltal, DELTAL_mean):
    return np.sqrt(np.mean((deltal - DELTAL_mean) ** 2, axis=-1))


if __name__ == "__main__":
    DELTAL_mean = torch.load("models/kinematics/DELTAL_stats.pt")["mean"].numpy()

    d = np.load("results/ControlWorkspaceJacobian.npz")
    targets = d["target"].astype(np.float64)
    real_mocap = d["mocap"]

    print("Simulating WITH null-space objective...")
    poses_with, deltals_with, iters_with, conv_with = simulate_sequence(targets, DELTAL_mean, with_null=True)
    print(f"  converged: {conv_with.sum()}/{len(targets)}, mean iters: {iters_with.mean():.0f}")

    print("Simulating WITHOUT null-space objective...")
    poses_without, deltals_without, iters_without, conv_without = simulate_sequence(targets, DELTAL_mean, with_null=False)
    print(f"  converged: {conv_without.sum()}/{len(targets)}, mean iters: {iters_without.mean():.0f}")

    pos_err = np.linalg.norm(poses_with[:, :3] - real_mocap[:, :3], axis=1)
    print(f"\nSanity check vs real hardware mocap (with-null sim): "
          f"mean pos diff {pos_err.mean():.1f} mm, max {pos_err.max():.1f} mm")

    h_with, h_without = H(deltals_with, DELTAL_mean), H(deltals_without, DELTAL_mean)
    r_with, r_without = rms_dev(deltals_with, DELTAL_mean), rms_dev(deltals_without, DELTAL_mean)
    primary_with = np.array([compute_pose_error(p, t) for p, t in zip(poses_with, targets)])
    primary_without = np.array([compute_pose_error(p, t) for p, t in zip(poses_without, targets)])

    print(f"\nH(l):               with-null {h_with.mean():.1f}+/-{h_with.std():.1f}   "
          f"without-null {h_without.mean():.1f}+/-{h_without.std():.1f}")
    print(f"RMS tendon dev [mm]: with-null {r_with.mean():.2f}+/-{r_with.std():.2f}   "
          f"without-null {r_without.mean():.2f}+/-{r_without.std():.2f}")
    print(f"Primary task error:  with-null {primary_with.mean():.2f}+/-{primary_with.std():.2f}   "
          f"without-null {primary_without.mean():.2f}+/-{primary_without.std():.2f}")

    np.savez_compressed(
        "results/NullSpaceAblation.npz",
        targets=targets,
        poses_with=poses_with, deltals_with=deltals_with, iters_with=iters_with, conv_with=conv_with,
        poses_without=poses_without, deltals_without=deltals_without, iters_without=iters_without, conv_without=conv_without,
        DELTAL_mean=DELTAL_mean,
    )
    print("\nSaved results/NullSpaceAblation.npz")
