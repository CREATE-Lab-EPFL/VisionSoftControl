"""
Comment 7 (MULTI half): bending-angle coverage of the control evaluation vs.
the training workspace, per section.

Training-workspace bending angle comes directly from the stored curvature
labels (X_quad), same as the SINGLE analysis (see SINGLE_workspace_coverage
notebook). For the control-evaluation targets, this reuses the already-
computed, PCC-consistent tendon lengths from MULTI_nullspace_ablation.py's
"with-null" simulation (results/NullSpaceAblation.npz) rather than
re-deriving them -- those were obtained by replaying the actual model-based
control law against the PCC forward model, so they're a faithful (if
idealized) stand-in for "what configuration these targets correspond to."
Requires MULTI_nullspace_ablation.py to have been run first.

For the tracked trajectories (many more points), a full PCC-consistent
replay would be too slow; the data-driven IK network (models/kinematics/
IK_model.pt) is used instead as a fast approximate inverse. This is a
coverage CHARACTERIZATION, not a per-controller comparison (unlike the
null-space ablation, where mixing models would bias the comparison), so
using the network here is a reasonable, lower-stakes shortcut -- flagged
here and in the notebook as an estimate, not a measurement.

Run from within MULTI/.
"""
import glob
import numpy as np
import torch

D_SECTION = 30.0  # mm, section radius (diameter=60 in MULTI_jacobians.py)


def kinematics(DELTAL):
    deltas = [
        np.radians([0, 120, -120]),
        np.radians([60, 180, -60]),
        np.radians([150, 270, 30]),
    ]
    DxDyDl = []
    for i in range(3):
        section = DELTAL[..., i*3:(i+1)*3]
        delta = deltas[i]
        Dl = np.mean(section, axis=-1)
        Dx = (2/3) * np.sum(-section * np.cos(delta), axis=-1)
        Dy = (2/3) * np.sum(-section * np.sin(delta), axis=-1)
        DxDyDl.append(np.stack([Dx, Dy, Dl], axis=-1))
    return np.concatenate(DxDyDl, axis=-1)


def per_section_bending_deg(DxDyDl):
    """DxDyDl: (..., 9) -> (..., 3) bending angle per section, in degrees."""
    out = []
    for i in range(3):
        Dx, Dy = DxDyDl[..., i*3], DxDyDl[..., i*3+1]
        Delta = np.sqrt(Dx**2 + Dy**2)
        out.append(np.rad2deg(Delta / D_SECTION))
    return np.stack(out, axis=-1)


if __name__ == "__main__":
    print("Loading MULTI training dataset curvature labels...")
    files = sorted(glob.glob("data/MULTI_dataset/DatasetMulti*.pt"))
    all_quad = []
    for f in files:
        d = torch.load(f, map_location="cpu")
        all_quad.extend(d["X_quad"])
        del d
    X_quad = torch.stack(all_quad).numpy()  # (N, 15) = 3 x [s, c0, c1, c2, phi]

    theta_train = np.zeros((len(X_quad), 3))
    for sec in range(3):
        off = sec * 5
        s, c0, c1, c2 = X_quad[:, off], X_quad[:, off+1], X_quad[:, off+2], X_quad[:, off+3]
        theta_train[:, sec] = np.rad2deg(np.abs(c0*s + 0.5*c1*s**2 + (1/3)*c2*s**3))

    for sec in range(3):
        t = theta_train[:, sec]
        print(f"Section {sec+1} training bending angle: mean {t.mean():.1f}  p95 {np.percentile(t,95):.1f}  "
              f"(max {t.max():.1f} -- unreliable, polynomial-fit outlier)")

    nsa = np.load("results/NullSpaceAblation.npz")
    deltals_with = nsa["deltals_with"]  # (20, 9), PCC-consistent tendon config per target
    DxDyDl_targets = kinematics(deltals_with)
    theta_targets = per_section_bending_deg(DxDyDl_targets)
    for sec in range(3):
        t = theta_targets[:, sec]
        print(f"Section {sec+1} 20-target control eval bending angle: mean {t.mean():.1f}  max {t.max():.1f}")

    device = torch.device("cpu")
    IK = torch.jit.load("models/kinematics/IK_model.pt", map_location=device)
    IK.eval()

    poly_files = sorted(glob.glob("results/Polygon*30sides*.npz"))
    poly_files = [f for f in poly_files if "OpenLoop" not in f]  # closed-loop only, real camera pose
    print(f"\nFound {len(poly_files)} closed-loop 30-sided MULTI trajectory files")
    all_theta_traj = []
    with torch.no_grad():
        for f in poly_files:
            d = np.load(f)
            mocap = d["mocap"][::20]  # subsample
            pose = torch.tensor(mocap, dtype=torch.float32)
            deltal_est = IK(pose).numpy()
            DxDyDl_traj = kinematics(deltal_est)
            all_theta_traj.append(per_section_bending_deg(DxDyDl_traj))
    theta_traj = np.concatenate(all_theta_traj, axis=0)
    for sec in range(3):
        t = theta_traj[:, sec]
        print(f"Section {sec+1} trajectory (IK-net estimate, N={len(t)}): mean {t.mean():.1f}  max {t.max():.1f}")

    np.savez_compressed(
        "results/MULTI_workspace_coverage.npz",
        theta_train=theta_train, theta_targets=theta_targets, theta_traj=theta_traj,
    )
    print("\nSaved results/MULTI_workspace_coverage.npz")
