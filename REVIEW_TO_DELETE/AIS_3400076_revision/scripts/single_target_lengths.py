"""Comment 7 (compression range, single section): the 20 control targets were snapped to sampled
workspace points, so each target is matched to its dataset sample by tip position and its length
change is the mean recorded tendon displacement (Eq. 2), as for the multi-section table.
Adds `dL_mm` and `match_dist_mm` to each single-section target, and the training range `train_dL`, in data/misc_summary.json."""
import json
import numpy as np
from common import *

d = load_all_small(SINGLE_SHARDS, ["y", "X_DELTAL"])
pos, dl = d["y"][:, :3], d["X_DELTAL"]
targets = np.load(f"{REPO}/SINGLE/results/ControlWorkspace.npz")["xyz"]
misc = json.load(open(f"{DATA}/misc_summary.json"))
for t, rec in zip(targets, misc["coverage"]["SINGLE"]["targets"]):
    dist = np.linalg.norm(pos - t, axis=1); i = int(np.argmin(dist))
    rec["dL_mm"] = float(dl[i].mean()); rec["match_dist_mm"] = float(dist[i])
m_tr = dl.mean(1)  # length change of every training sample
misc["coverage"]["SINGLE"]["train_dL"] = {"p5": float(np.percentile(m_tr, 5)), "p95": float(np.percentile(m_tr, 95)),
                                       "min": float(m_tr.min()), "max": float(m_tr.max())}
json.dump(misc, open(f"{DATA}/misc_summary.json", "w"), indent=1, default=float)
r = misc["coverage"]["SINGLE"]["targets"]
print("max match distance [mm]:", max(x["match_dist_mm"] for x in r))
print("single dL range [mm]:", min(x["dL_mm"] for x in r), max(x["dL_mm"] for x in r))
m = np.array([x["dL_mm"] for x in misc["coverage"]["MULTI"]["targets"]])
print("multi dL range per section [mm]:", m.min(0), m.max(0))
