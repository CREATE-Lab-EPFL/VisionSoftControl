"""Remaining numbers for the response: Table S6 robust stats (paper's method),
outliers, trajectory start/direction/cycles, control-target coverage table,
tendon ranges and acquisition sessions. Reads repo files only."""
import json, glob, zipfile, datetime
import numpy as np
import torch
from scipy.spatial import ConvexHull, Delaunay
from scipy.spatial.transform import Rotation as R
from common import *

res = {}

# ---------- Table S6 (relative transforms, paper's Method 3) + outliers ----------
m = np.load(f"{DATA}/multi_test.npz")
P, L = m["pred_pose"], m["lab"]
def rel(a, b):
    Ra, Rb = R.from_euler("zyx", a[3:]).as_matrix(), R.from_euler("zyx", b[3:]).as_matrix()
    return Ra.T @ Rb, Ra.T @ (b[:3] - a[:3])
base = np.zeros(6)
relp, relr = np.zeros((len(P), 3)), np.zeros((len(P), 3))
for i in range(len(P)):
    pp = [base] + [P[i, 6 * k:6 * k + 6] for k in range(3)]
    ll = [base] + [L[i, 6 * k:6 * k + 6] for k in range(3)]
    for k in range(3):
        Rp, tp = rel(pp[k], pp[k + 1]); Rl, tl = rel(ll[k], ll[k + 1])
        relp[i, k] = np.linalg.norm(tp - tl)
        relr[i, k] = np.degrees(np.linalg.norm((R.from_matrix(Rl) * R.from_matrix(Rp).inv()).as_rotvec()))
def st(x):
    return {"mean": x.mean(), "std": x.std(), "median": np.median(x), "q1": np.percentile(x, 25), "q3": np.percentile(x, 75),
            "p95": np.percentile(x, 95), "max": x.max()}
res["tableS6"] = {s: {"pos": st(relp[:, k]), "rot": st(relr[:, k])} for k, s in enumerate(["I", "II", "III"])}
absrot = np.stack([m["abs_rot_I"], m["abs_rot_II"], m["abs_rot_III"]], 1)
# outliers: samples with any tip orientation error > 30 deg
out = np.where((absrot > 30).any(1))[0]
lab_bend = np.stack([bending_from_euler(L[:, 3:6]), m["bend_II"], m["bend_III"]], 1)
res["outliers"] = {
    "n_samples_any_rot_gt30": int(len(out)), "indices": out.tolist(),
    "label_pitch_deg": [np.degrees(L[i, [4, 10, 16]]).round(1).tolist() for i in out],
    "label_bend_deg": [lab_bend[i].round(1).tolist() for i in out],
    "abs_rot_err": [absrot[i].round(1).tolist() for i in out],
    "tableS6_without_outliers": {s: {"pos_mean": np.delete(relp[:, k], out).mean(), "pos_std": np.delete(relp[:, k], out).std(),
                                     "rot_mean": np.delete(relr[:, k], out).mean(), "rot_std": np.delete(relr[:, k], out).std()}
                                 for k, s in enumerate(["I", "II", "III"])},
    "table1_without_outliers": {s: {"pos_mean": np.delete(m[f"abs_pos_{s}"], out).mean(), "pos_std": np.delete(m[f"abs_pos_{s}"], out).std(),
                                    "rot_mean": np.delete(m[f"abs_rot_{s}"], out).mean(), "rot_std": np.delete(m[f"abs_rot_{s}"], out).std()}
                                for s in ["I", "II", "III"]},
    "label_bend_p99_by_section": np.percentile(lab_bend, 99, axis=0).round(1).tolist(),
}

# ---------- trajectories: start, direction, cycles ----------
def fit_circle(xy):
    A = np.column_stack([2 * xy[:, 0], 2 * xy[:, 1], np.ones(len(xy))]); b = (xy**2).sum(1)
    s, *_ = np.linalg.lstsq(A, b, rcond=None); return s[0], s[1], np.sqrt(s[2] + s[0]**2 + s[1]**2)
traj = {}
files = sorted(glob.glob(f"{REPO}/SINGLE/results/PolygonWS_30_*.npz")) + sorted(glob.glob(f"{REPO}/MULTI/results/Polygon*30sides*.npz"))
for f in files:
    d = np.load(f); mo = d["mocap"]
    tgt = d["target"] if "target" in d.files else None
    if tgt is None:  # SINGLE open-loop logs: reuse matching closed-loop target
        b = f.split("/")[-1].replace(".npz", "").split("_")
        tgt = np.load(f"{REPO}/SINGLE/results/PolygonWS_30_{b[2]}_{b[-1]}_mocap.npz")["target"]
    cx, cy, r = fit_circle(tgt[:, :2])
    a_t = np.unwrap(np.arctan2(tgt[:, 1] - cy, tgt[:, 0] - cx))
    a_m = np.unwrap(np.arctan2(mo[:, 1] - cy, mo[:, 0] - cx))
    traj[f.split("/")[-1]] = {
        "radius": r, "z": float(tgt[:, 2].mean()), "n_vertices": int(len(tgt)), "n_logged": int(len(mo)),
        "first_vertex_angle_deg": float(np.degrees(np.arctan2(tgt[0, 1] - cy, tgt[0, 0] - cx))),
        "vertex_order": "CCW" if (a_t[-1] - a_t[0]) > 0 else "CW",
        "logged_start_angle_deg": float(np.degrees(a_m[0]) % 360), "logged_sweep_deg": float(np.degrees(a_m[-1] - a_m[0])),
        "cycles": float(abs(a_m[-1] - a_m[0]) / (2 * np.pi)),
    }
res["trajectories"] = traj

# ---------- control targets: coordinates, bending/compression, coverage ----------
cov = {}
ws1 = np.load(f"{REPO}/SINGLE/data/Workspace.npz")["xyz"]
t1 = np.load(f"{REPO}/SINGLE/results/ControlWorkspace.npz")["xyz"]
sc = np.load(f"{REPO}/SINGLE/results/SINGLE_workspace_coverage.npz")
ws3 = np.load(f"{REPO}/MULTI/data/Workspace.npz")
t3 = np.load(f"{REPO}/MULTI/results/ControlWorkspace.npz")["pose"]
mc = np.load(f"{REPO}/MULTI/results/MULTI_workspace_coverage.npz")
nsa = np.load(f"{REPO}/MULTI/results/NullSpaceAblation.npz")
deltas = [np.radians([0, 120, -120]), np.radians([60, 180, -60]), np.radians([150, 270, 30])]
Dl3 = np.stack([nsa["deltals_with"][:, 3 * k:3 * k + 3].mean(1) for k in range(3)], 1)
for name, ws, tg in [("SINGLE", ws1, t1[:, :3]), ("MULTI", ws3["tip3"], t3[:, :3])]:
    hw, ht = ConvexHull(ws), ConvexHull(tg)
    inside = Delaunay(tg).find_simplex(ws) >= 0
    nn = np.min(np.linalg.norm(ws[:, None, :] - tg[None, :, :], axis=2), axis=1)
    cov[name] = {"ws_points": int(len(ws)), "hull_volume_ratio": ht.volume / hw.volume, "frac_ws_inside_target_hull": inside.mean(),
                 "z_filter_mm": 115 if name == "SINGLE" else 200, "frac_ws_above_filter": float((ws[:, 2] > (115 if name == "SINGLE" else 200)).mean()),
                 "median_dist_ws_to_nearest_target": np.median(nn), "p95_dist_ws_to_nearest_target": np.percentile(nn, 95)}
cov["SINGLE"]["targets"] = [{"id": i + 1, "x": float(p[0]), "y": float(p[1]), "z": float(p[2]), "bend_deg": float(sc["theta_targets_deg"][i])}
                            for i, p in enumerate(t1)]
cov["SINGLE"]["train_bend"] = {"mean": float(sc["theta_train_deg"].mean()), "p95": float(np.percentile(sc["theta_train_deg"], 95)), "max": float(sc["theta_train_deg"].max())}
cov["SINGLE"]["target_bend_max"] = float(sc["theta_targets_deg"].max()); cov["SINGLE"]["traj_bend_max"] = float(sc["all_traj_theta"].max())
cov["MULTI"]["targets"] = [{"id": i + 1, "x": float(p[0]), "y": float(p[1]), "z": float(p[2]), "yaw": float(np.degrees(p[3])),
                            "pitch": float(np.degrees(p[4])), "roll": float(np.degrees(p[5])),
                            "bend_deg": mc["theta_targets"][i].round(1).tolist(), "dL_mm": Dl3[i].round(1).tolist()} for i, p in enumerate(t3)]
cov["MULTI"]["train_bend_p95"] = np.percentile(mc["theta_train"], 95, axis=0).round(1).tolist()
cov["MULTI"]["train_bend_mean"] = mc["theta_train"].mean(0).round(1).tolist()
cov["MULTI"]["target_bend_max"] = mc["theta_targets"].max(0).round(1).tolist()
cov["MULTI"]["traj_bend_max"] = mc["theta_traj"].max(0).round(1).tolist()
res["coverage"] = cov

# ---------- tendon ranges, dataset sizes, sessions ----------
s_all = load_all_small(SINGLE_SHARDS, ["X_DELTAL"])["X_DELTAL"]
m_all = load_all_small(MULTI_SHARDS, ["X_DELTAL"])["X_DELTAL"]
res["tendon_recorded_range_mm"] = {"SINGLE_min": s_all.min(0).round(1).tolist(), "SINGLE_max": s_all.max(0).round(1).tolist(),
                                   "MULTI_min": m_all.min(0).round(1).tolist(), "MULTI_max": m_all.max(0).round(1).tolist()}
res["tendon_commanded_range_mm"] = {"SINGLE": "U(-45, 10) per tendon", "MULTI": "independent mode: I U(-25,10), II U(-35,10), III U(-40,10); coupled modes via SamplingSolver"}
sess = {}
for name, zp in [("SINGLE", f"{REPO}/SINGLE/data/SINGLE_dataset.zip"), ("MULTI", f"{REPO}/MULTI/data/MULTI_dataset.zip")]:
    with zipfile.ZipFile(zp) as z:
        sess[name] = sorted({f"{i.date_time[0]:04d}-{i.date_time[1]:02d}-{i.date_time[2]:02d}" for i in z.infolist() if i.filename.endswith(".pt")})
fk = torch.load(f"{REPO}/MULTI/data/FKdata.pt", map_location="cpu")
ts = np.array([float(t) for t in fk["timestamps"]])
gaps = np.diff(np.sort(ts))
sess["FK_n"] = int(len(ts)); sess["FK_sessions_gap_gt_1h"] = int((gaps > 3600).sum() + 1)
sess["FK_dates"] = sorted({datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in ts})
res["sessions"] = sess

json.dump(res, open(f"{DATA}/misc_summary.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in res.items() if k != "coverage"}, indent=1, default=lambda x: round(float(x), 3)))
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "targets"} for k, v in cov.items()}, indent=1, default=lambda x: round(float(x), 3)))
