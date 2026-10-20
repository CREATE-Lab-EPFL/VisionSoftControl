"""Fig. S2b / C4 / S28: validation of the ORIGINAL N_C models
(MULTI/models/curvature/*_for_MULTI_model.pt).
(1) the 20 full-marker configurations in MULTI/data/CurvatureDataCheck.npz
    (mocap-fitted curvature vs N_C output), same 9-point metric as the paper;
(2) N_C on the held-out SINGLE test split (pose -> curvature labels)."""
import json
import numpy as np
from common import *

res = {}
cd = np.load(f"{REPO}/MULTI/data/CurvatureDataCheck.npz")
pairs = {"const": ("const_mocap", "const_ANN"), "affine": ("aff_mocap", "aff_ANN"), "quad": ("quad_mocap", "quad_ANN")}
per = {}
for m, (gk, pk) in pairs.items():
    G, P = cd[gk], cd[pk]
    e = np.array([np.linalg.norm(points_multi(pad_params(P[i], m, 3)) - points_multi(pad_params(G[i], m, 3)), axis=1)
                  for i in range(len(G))])
    per[m] = e
    w = {"quad": 5, "affine": 4, "const": 3}[m]
    names = {"quad": ["S", "c0", "c1", "c2", "phi"], "affine": ["S", "c0", "c1", "phi"], "const": ["S", "c0", "phi"]}[m]
    par = {}
    for j, nm in enumerate(names):
        diff = np.abs(np.concatenate([P[:, w * k + j] - G[:, w * k + j] for k in range(3)]))
        if nm == "phi":
            diff = np.degrees(np.abs((diff + np.pi) % (2 * np.pi) - np.pi))
        par[nm] = {"mae": diff.mean(), "std": diff.std()}
    s = e.sum(1)
    res[f"check20_{m}"] = {
        "N": int(len(G)), "sum_mean": s.mean(), "sum_std_ddof1": s.std(ddof=1), "sum_median": np.median(s),
        "per_point_mean": e.mean(0).tolist(), "per_point_std": e.std(0, ddof=1).tolist(),
        "per_point_rmse": np.sqrt((e**2).mean(0)).tolist(), "max_point_error": e.max(), "params": par,
    }

# N_C on the SINGLE held-out test split
tr, va, te = original_split()
d = load_fields(SINGLE_SHARDS, ["y", "X_quad", "X_affine", "X_const"], te)
y = d["y"].float()
lab = {"const": d["X_const"].numpy(), "affine": d["X_affine"].numpy(), "quad": d["X_quad"].numpy()}
fn = {"const": "constant_for_MULTI_model.pt", "affine": "affine_for_MULTI_model.pt", "quad": "quadratic_for_MULTI_model.pt"}
single = {}
for m in fn:
    p = run_model(jit(f"{REPO}/MULTI/models/curvature/{fn[m]}"), y, batch=256)
    e = np.array([np.linalg.norm(points_single(*pad_params(p[i], m, 1)) - points_single(*pad_params(lab[m][i], m, 1)), axis=1)
                  for i in range(len(te))])
    single[m] = e
    res[f"singletest_{m}"] = {"N": int(len(te)), "per_point_mean": e.mean(0).tolist(), "per_point_std": e.std(0).tolist(),
                              "sum_mean": e.sum(1).mean(), "sum_std_ddof1": e.sum(1).std(ddof=1)}

np.savez_compressed(f"{DATA}/nc_validation.npz", **{f"check20_{m}": v for m, v in per.items()},
                    **{f"singletest_{m}": v for m, v in single.items()})
json.dump(res, open(f"{DATA}/nc_summary.json", "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=lambda x: round(float(x), 3)))
