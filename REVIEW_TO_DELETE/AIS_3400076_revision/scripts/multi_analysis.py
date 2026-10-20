"""MULTI arm, original test split (seed 42): pose CNN (Table 1 / S6 check, robust
stats, error vs bending) and curvature CNNs (per-point Fig. 7b errors vs labels,
and section-end points vs mocap tip markers)."""
import json
import numpy as np
from scipy.stats import spearmanr
from scipy.spatial.transform import Rotation as R
from common import *

tr, va, te = original_split()
d = load_fields(MULTI_SHARDS, ["X_images", "tip_1", "tip_2", "tip_3", "X_quad", "X_affine", "X_const"], te)
img = d["X_images"]
lab = np.concatenate([d["tip_1"].numpy(), d["tip_2"].numpy(), d["tip_3"].numpy()], axis=1)
res = {"n_test": int(len(te))}

pred = run_model(jit(f"{REPO}/MULTI/models/vision/helyx_model.pt"), img, batch=8)
sec = {"I": 0, "II": 6, "III": 12}
abs_pos, abs_rot, rel_pos, rel_rot, bend = {}, {}, {}, {}, {}
for k, o in sec.items():
    abs_pos[k] = np.linalg.norm(pred[:, o:o + 3] - lab[:, o:o + 3], axis=1)
    abs_rot[k] = ang_dist_deg(pred[:, o + 3:o + 6], lab[:, o + 3:o + 6])
prev = {"I": None, "II": 0, "III": 6}
for k, o in sec.items():
    p = prev[k]
    if p is None:
        rel_pos[k], rel_rot[k] = abs_pos[k], abs_rot[k]
        bend[k] = bending_from_euler(lab[:, 3:6])
        continue
    rel_pos[k] = np.linalg.norm((pred[:, o:o + 3] - pred[:, p:p + 3]) - (lab[:, o:o + 3] - lab[:, p:p + 3]), axis=1)
    Rp = R.from_euler("zyx", pred[:, o + 3:o + 6]) * R.from_euler("zyx", pred[:, p + 3:p + 6]).inv()
    Rt = R.from_euler("zyx", lab[:, o + 3:o + 6]) * R.from_euler("zyx", lab[:, p + 3:p + 6]).inv()
    rel_rot[k] = np.degrees(np.linalg.norm((Rt * Rp.inv()).as_rotvec(), axis=1))
    Rloc = R.from_euler("zyx", lab[:, p + 3:p + 6]).inv() * R.from_euler("zyx", lab[:, o + 3:o + 6])
    bend[k] = np.degrees(np.arccos(np.clip(Rloc.as_matrix()[:, 2, 2], -1, 1)))


def stats(x):
    return {"mean": x.mean(), "std": x.std(), "median": np.median(x), "q1": np.percentile(x, 25),
            "q3": np.percentile(x, 75), "p95": np.percentile(x, 95), "max": x.max()}


for k in sec:
    res[f"abs_{k}"] = {"pos": stats(abs_pos[k]), "rot": stats(abs_rot[k])}
    res[f"rel_{k}"] = {"pos": stats(rel_pos[k]), "rot": stats(rel_rot[k])}
    rp, pp = spearmanr(bend[k], abs_pos[k]); rr, prr = spearmanr(bend[k], abs_rot[k])
    res[f"bend_{k}"] = {"rho_pos": rp, "p_pos": pp, "rho_rot": rr, "p_rot": prr, "max": bend[k].max()}
    # outliers driving the std
    res[f"outliers_rot_{k}"] = {"n_gt_30deg": int((abs_rot[k] > 30).sum()), "n_gt_90deg": int((abs_rot[k] > 90).sum())}

# ---- curvature CNNs f_C^3 ----
models = {"const": "constant_model.pt", "affine": "affine_model.pt", "quad": "quadratic_model.pt"}
labels = {"const": d["X_const"].numpy(), "affine": d["X_affine"].numpy(), "quad": d["X_quad"].numpy()}
tips_mocap = np.stack([lab[:, 0:3], lab[:, 6:9], lab[:, 12:15]], axis=1)
curv = {}
for m, fn in models.items():
    p = run_model(jit(f"{REPO}/MULTI/models/curvature/{fn}"), img, batch=8)
    e_lab, e_tip, e_labtip = [], [], []
    for i in range(len(te)):
        P = points_multi(pad_params(p[i], m, 3))
        G = points_multi(pad_params(labels[m][i], m, 3))
        e_lab.append(np.linalg.norm(P - G, axis=1))
        e_tip.append(np.linalg.norm(P[[2, 5, 8]] - tips_mocap[i], axis=1))
        e_labtip.append(np.linalg.norm(G[[2, 5, 8]] - tips_mocap[i], axis=1))
    e_lab, e_tip, e_labtip = map(np.array, (e_lab, e_tip, e_labtip))
    curv[m] = {"vs_label": e_lab, "tips_vs_mocap": e_tip, "labeltips_vs_mocap": e_labtip}
    res[f"curv_{m}"] = {
        "per_point_mean_vs_label": e_lab.mean(0).tolist(), "per_point_rmse_vs_label": np.sqrt((e_lab**2).mean(0)).tolist(),
        "per_point_median_vs_label": np.median(e_lab, 0).tolist(),
        "sum_mean_vs_label": e_lab.sum(1).mean(), "sum_std_vs_label": e_lab.sum(1).std(ddof=1),
        "tips_mean_vs_mocap": e_tip.mean(0).tolist(), "tips_median_vs_mocap": np.median(e_tip, 0).tolist(),
        "labeltips_mean_vs_mocap": e_labtip.mean(0).tolist(), "labeltips_median_vs_mocap": np.median(e_labtip, 0).tolist(),
    }

np.savez_compressed(f"{DATA}/multi_test.npz", te=te, pred_pose=pred, lab=lab,
                    **{f"abs_pos_{k}": v for k, v in abs_pos.items()}, **{f"abs_rot_{k}": v for k, v in abs_rot.items()},
                    **{f"rel_pos_{k}": v for k, v in rel_pos.items()}, **{f"rel_rot_{k}": v for k, v in rel_rot.items()},
                    **{f"bend_{k}": v for k, v in bend.items()},
                    **{f"{m}_{k}": v for m in curv for k, v in curv[m].items()})
json.dump(res, open(f"{DATA}/multi_summary.json", "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=lambda x: round(float(x), 3)))
