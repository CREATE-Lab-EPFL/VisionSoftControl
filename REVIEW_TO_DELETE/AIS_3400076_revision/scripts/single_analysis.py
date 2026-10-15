"""SINGLE arm, original test split (seed 42): pose CNN (Table S5 check, robust
stats, error vs bending) and curvature CNNs (per-point Fig. 7a errors, vs
fitted labels and vs mocap subsection markers)."""
import json
import numpy as np
from scipy.stats import spearmanr
from common import *

tr, va, te = original_split()
d = load_fields(SINGLE_SHARDS, ["X_images", "y", "X_quad", "X_affine", "X_const", "backbones"], te)
img = d["X_images"]
y = d["y"].numpy()
res = {"n_test": int(len(te))}

# ---- pose CNN f_p^1 ----
pred = run_model(jit(f"{REPO}/SINGLE/models/vision/helyx_model.pt"), img)
pos_err = np.linalg.norm(pred[:, :3] - y[:, :3], axis=1)
rot_err = ang_dist_deg(pred[:, 3:], y[:, 3:])
res["pose"] = {
    "pos_mean": pos_err.mean(), "pos_std": pos_err.std(), "rot_mean": rot_err.mean(), "rot_std": rot_err.std(),
    "pos_median": np.median(pos_err), "pos_p95": np.percentile(pos_err, 95), "pos_max": pos_err.max(),
    "rot_median": np.median(rot_err), "rot_p95": np.percentile(rot_err, 95), "rot_max": rot_err.max(),
    "per_axis_mm": [float(np.abs(pred[:, i] - y[:, i]).mean()) for i in range(3)],
    "per_axis_std_mm": [float(np.abs(pred[:, i] - y[:, i]).std()) for i in range(3)],
}
bend = bending_from_euler(y[:, 3:])
rho_p, pp = spearmanr(bend, pos_err)
rho_r, pr = spearmanr(bend, rot_err)
res["bending"] = {"rho_pos": rho_p, "p_pos": pp, "rho_rot": rho_r, "p_rot": pr,
                  "bend_min": bend.min(), "bend_max": bend.max()}

# ---- curvature CNNs f_C^1 ----
models = {"const": "const_model.pt", "affine": "affine_model.pt", "quad": "quadratic_model.pt"}
labels = {"const": d["X_const"].numpy(), "affine": d["X_affine"].numpy(), "quad": d["X_quad"].numpy()}
bb = d["backbones"].numpy()
markers = np.stack([bb[:, 0:3], bb[:, 6:9], bb[:, 12:15]], axis=1)  # subsection markers, base frame
curv = {}
for m, fn in models.items():
    p = run_model(jit(f"{REPO}/SINGLE/models/curvature/{fn}"), img)
    e_lab, e_mk, e_labmk = [], [], []
    for i in range(len(te)):
        P = points_single(*pad_params(p[i], m, 1))
        G = points_single(*pad_params(labels[m][i], m, 1))
        e_lab.append(np.linalg.norm(P - G, axis=1))
        e_mk.append(np.linalg.norm(P - markers[i], axis=1))
        e_labmk.append(np.linalg.norm(G - markers[i], axis=1))
    e_lab, e_mk, e_labmk = map(np.array, (e_lab, e_mk, e_labmk))
    curv[m] = {"vs_label": e_lab, "vs_marker": e_mk, "label_vs_marker": e_labmk}
    res[f"curv_{m}"] = {
        "per_point_mean_vs_label": e_lab.mean(0).tolist(), "per_point_rmse_vs_label": np.sqrt((e_lab**2).mean(0)).tolist(),
        "per_point_std_vs_label": e_lab.std(0).tolist(),
        "sum_mean_vs_label": e_lab.sum(1).mean(), "sum_std_vs_label": e_lab.sum(1).std(ddof=1),
        "per_point_mean_vs_marker": e_mk.mean(0).tolist(), "per_point_rmse_vs_marker": np.sqrt((e_mk**2).mean(0)).tolist(),
        "per_point_mean_label_vs_marker": e_labmk.mean(0).tolist(),
    }

np.savez_compressed(f"{DATA}/single_test.npz", te=te, pred_pose=pred, y=y, pos_err=pos_err, rot_err=rot_err, bend=bend,
                    **{f"{m}_{k}": v for m in curv for k, v in curv[m].items()})
json.dump(res, open(f"{DATA}/single_summary.json", "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=lambda x: round(float(x), 3)))
