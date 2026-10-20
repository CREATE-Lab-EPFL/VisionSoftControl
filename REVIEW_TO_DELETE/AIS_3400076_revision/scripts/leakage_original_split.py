"""C8: nearest training neighbour (tendon space) of each test sample, original split."""
import json, numpy as np
from scipy.spatial import cKDTree
from common import *
out = {}
for name, shards in [("SINGLE", SINGLE_SHARDS), ("MULTI", MULTI_SHARDS)]:
    D = load_all_small(shards, ["X_DELTAL"])["X_DELTAL"]
    tr, va, te = original_split(len(D))
    nn, _ = cKDTree(D[tr]).query(D[te], k=1)
    out[name] = {"mean": nn.mean(), "median": np.median(nn), "frac_lt_0.5": (nn < 0.5).mean(), "frac_lt_1": (nn < 1).mean(),
                 "frac_lt_2": (nn < 2).mean(), "frac_exact": (nn < 1e-6).mean(), "n_test": len(te)}
json.dump(out, open(f"{DATA}/leakage_original_split.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=lambda x: round(float(x), 3)))
