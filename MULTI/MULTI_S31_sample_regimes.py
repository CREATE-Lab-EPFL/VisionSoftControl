"""
S31: sample counts per acquisition/sampling regime for the MULTI dataset.

SI Algorithm 1 describes three regimes: (I) all modules driven to the same
q-configuration via the Bending Solver BS, (II) modules I+II coupled/sampled,
III set via BS(II), (III) all three independent. This isn't stored as an
explicit label in the shipped dataset, but it leaves a detectable signature:
under regime I, all three sections' curvature coordinates (Dx,Dy,Dl) should
match (the Bending Solver enforces this by construction); under regime II,
only sections II and III match; under regime III, none do (near-zero chance
of an accidental match under continuous random sampling).

This infers regime membership from that signature directly on X_DELTAL, via
the same kinematics() tendon->curvature map used throughout this analysis.

Caveat: this is inferred post-hoc from the geometric signature, not read
from an explicit stored label -- check that the printed pairwise-distance
histogram is cleanly bimodal (a near-zero cluster well separated from the
bulk) before quoting these counts as exact.

Run from within MULTI/.
"""
import glob
import numpy as np
import torch


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


if __name__ == "__main__":
    print("Loading MULTI dataset tendon lengths...")
    files = sorted(glob.glob("data/MULTI_dataset/DatasetMulti*.pt"))
    all_dl = []
    for f in files:
        d = torch.load(f, map_location="cpu")
        all_dl.extend(d["X_DELTAL"])
        del d
    DELTAL = torch.stack(all_dl).numpy()
    print("Total samples:", len(DELTAL))

    DxDyDl = kinematics(DELTAL)
    sec1, sec2, sec3 = DxDyDl[:, 0:3], DxDyDl[:, 3:6], DxDyDl[:, 6:9]

    d12 = np.linalg.norm(sec1 - sec2, axis=1)
    d23 = np.linalg.norm(sec2 - sec3, axis=1)
    d13 = np.linalg.norm(sec1 - sec3, axis=1)

    print("\nPairwise section-to-section curvature-coordinate distance distribution:")
    for name, d in [("I-II", d12), ("II-III", d23), ("I-III", d13)]:
        print(f"  {name}: median {np.median(d):.3f}  p10 {np.percentile(d,10):.3f}  "
              f"fraction < 0.05: {100*(d<0.05).mean():.1f}%  fraction < 0.5: {100*(d<0.5).mean():.1f}%")

    # Sanity check the detection method itself before trusting a "no coupling
    # found" conclusion: MULTI_data_acquire.py's SamplingSolver and this
    # script's kinematics() should be exactly equivalent (same 3x3 linear
    # system, closed-form vs. np.linalg.solve) for a genuinely coupled pair.
    def _sampling_solver(delta_old, deltaL_old, delta_new):
        s1, s2, s3 = delta_old
        n1, n2, n3 = delta_new
        A_old = np.array([[np.cos(s1), np.sin(s1), -1],
                           [np.cos(s2), np.sin(s2), -1],
                           [np.cos(s3), np.sin(s3), -1]])
        sol = np.linalg.solve(A_old, -deltaL_old)
        A_new = np.array([[np.cos(n1), np.sin(n1), -1],
                           [np.cos(n2), np.sin(n2), -1],
                           [np.cos(n3), np.sin(n3), -1]])
        return -A_new @ sol

    deltas = [np.radians([0, 120, -120]), np.radians([60, 180, -60]), np.radians([150, 270, 30])]
    rng = np.random.default_rng(0)
    dl1_test = rng.uniform(-25, 10, size=3)
    dl2_test = _sampling_solver(deltas[0], dl1_test, deltas[1])
    q1_test = kinematics(np.concatenate([dl1_test, np.zeros(6)]))[:3]
    q2_test = kinematics(np.concatenate([np.zeros(3), dl2_test, np.zeros(3)]))[3:6]
    self_check_gap = np.max(np.abs(q1_test - q2_test))
    print(f"\nSelf-check: kinematics() vs. SamplingSolver on a synthetic coupled pair -> "
          f"max diff {self_check_gap:.2e} (should be ~machine epsilon; if not, the detection "
          f"method itself is broken, not the data)")

    TOL = 0.5
    all_match = (d12 < TOL) & (d23 < TOL) & (d13 < TOL)
    # config==1 in MULTI_data_acquire.py couples I<->II (SamplingSolver(delta1, DELTAL_first, delta2)),
    # leaving III independent -- so the "two-coupled" signature is d12 small, not d23.
    two_match_12_only = (d12 < TOL) & ~all_match
    independent = ~all_match & ~two_match_12_only

    print(f"\nInferred regime counts (tolerance={TOL}):")
    print(f"  Regime I   (all sections matched, config==0):     {all_match.sum()}  ({100*all_match.mean():.1f}%)")
    print(f"  Regime II  (I & II matched only, config==1):      {two_match_12_only.sum()}  ({100*two_match_12_only.mean():.1f}%)")
    print(f"  Regime III (fully independent, config==2):        {independent.sum()}  ({100*independent.mean():.1f}%)")
    print(f"  (SI / MULTI_data_acquire.py describe a nominal 1/3-1/3-1/3 split via np.random.randint(0,3))")

    if self_check_gap < 1e-6 and all_match.sum() == 0 and two_match_12_only.sum() == 0:
        print("\n*** FINDING: self-check confirms the detection method is correct (near-zero gap on a")
        print("    synthetic coupled pair), yet ZERO samples in the shipped dataset show ANY matched-section")
        print("    signature, at a tolerance far looser than mechanical/encoder precision could explain")
        print("    (median inter-section distance is ~10-14, vs. ~0.09mm-equivalent encoder tolerance).")
        print("    This means the shipped 10,000-sample MULTI dataset does NOT show the trace that")
        print("    MULTI_data_acquire.py's current config==0/1/2 coupling scheme should leave. Most likely")
        print("    explanation: this script is not the exact version that generated the shipped data (an")
        print("    earlier/different acquisition script may have been used, e.g. fully independent sampling")
        print("    throughout). This needs confirmation from whoever ran the original acquisition sessions --")
        print("    do NOT report regime counts from this script as fact without that confirmation.")

    np.savez_compressed("results/S31_sample_regime_counts.npz",
                         d12=d12, d23=d23, d13=d13, self_check_gap=self_check_gap,
                         all_match=all_match, two_match_12_only=two_match_12_only, independent=independent)
    print("\nSaved results/S31_sample_regime_counts.npz")
