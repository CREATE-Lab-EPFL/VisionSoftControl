"""C8: does near-duplicate leakage inflate the reported accuracy? Test error with
vs without test samples whose tendon configuration also appears in training."""
import json, numpy as np
from scipy.spatial import cKDTree
from common import *
out = {}
M = np.load(f"{DATA}/multi_test.npz"); S = np.load(f"{DATA}/single_test.npz")
for name, shards, D in [("MULTI", MULTI_SHARDS, M), ("SINGLE", SINGLE_SHARDS, S)]:
    X = load_all_small(shards, ["X_DELTAL"])["X_DELTAL"]
    tr, va, te = original_split(len(X))
    assert np.array_equal(te, D["te"])
    nn, _ = cKDTree(X[tr]).query(X[te], k=1)
    thr = 1e-6 if name == "MULTI" else 1.0
    dup = nn < thr
    r = {"threshold_mm": thr, "n_dup": int(dup.sum()), "n_rest": int((~dup).sum())}
    keys = [("pos_I", "abs_pos_I"), ("pos_II", "abs_pos_II"), ("pos_III", "abs_pos_III"), ("rot_I", "abs_rot_I"), ("rot_II", "abs_rot_II"), ("rot_III", "abs_rot_III")] if name == "MULTI" else [("pos", "pos_err"), ("rot", "rot_err")]
    for k, f in keys:
        e = D[f]
        r[k] = {"all_mean": e.mean(), "dup_mean": e[dup].mean(), "rest_mean": e[~dup].mean(), "dup_median": np.median(e[dup]), "rest_median": np.median(e[~dup])}
    out[name] = r
json.dump(out, open(f"{DATA}/leakage_effect.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=lambda x: round(float(x), 2)))
