"""Shared helpers for the revision analyses. Read-only w.r.t. the repo."""
import glob
import os

import numpy as np
import torch
from scipy.integrate import cumulative_trapezoid
from scipy.spatial.transform import Rotation as R
from sklearn.model_selection import train_test_split

REPO = "/home/vigno0405/github/VisionSoftControl"
OUT = "/home/vigno0405/github/VisionSoftControl/REVIEW_TO_DELETE/AIS_3400076_revision"
FIG = os.path.join(OUT, "figures")
DATA = os.path.join(OUT, "data")
os.makedirs(FIG, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

SINGLE_SHARDS = sorted(glob.glob(f"{REPO}/SINGLE/data/SINGLE_dataset/Dataset*.pt"))
MULTI_SHARDS = sorted(glob.glob(f"{REPO}/MULTI/data/MULTI_dataset/DatasetMulti*.pt"))


def original_split(n=10000):
    """Reproduces the notebooks' split: global np.random.seed(42) set in cell 0,
    then train_test_split(test_size=0.15) and (temp, test_size=1/3) with the
    default random_state=None, which draws from that global stream."""
    np.random.seed(42)
    idx = np.arange(n)
    tr, tmp = train_test_split(idx, test_size=0.15)
    va, te = train_test_split(tmp, test_size=1 / 3)
    return np.sort(tr), np.sort(va), np.sort(te)


def load_fields(shards, keys, indices):
    """Loads only the requested global indices (shards are 1000 samples each)."""
    indices = np.sort(np.asarray(indices))
    out = {k: [] for k in keys}
    per = 1000
    for s, f in enumerate(shards):
        sel = indices[(indices >= s * per) & (indices < (s + 1) * per)] - s * per
        if len(sel) == 0:
            continue
        d = torch.load(f, map_location="cpu")
        for k in keys:
            out[k].extend([d[k][i] for i in sel])
        del d
    return {k: torch.stack(v) for k, v in out.items()}


def load_all_small(shards, keys):
    out = {k: [] for k in keys}
    for f in shards:
        d = torch.load(f, map_location="cpu")
        for k in keys:
            out[k].extend(d[k])
        del d
    return {k: torch.stack(v).numpy() for k, v in out.items()}


def ang_dist_deg(a, b):
    return np.degrees(np.linalg.norm((R.from_euler("zyx", b) * R.from_euler("zyx", a).inv()).as_rotvec(), axis=-1))


def jit(path):
    m = torch.jit.load(path, map_location="cpu")
    m.eval()
    return m


def run_model(model, x, batch=16):
    outs = []
    with torch.no_grad():
        for i in range(0, len(x), batch):
            outs.append(model(x[i:i + batch].float()).numpy())
    return np.concatenate(outs)


# ---- PPC backbone reconstruction (same discretisation as MULTI_helyx_testing cells 20-21) ----
def _section(S, c0, c1, c2, phi, n=1000):
    v = np.linspace(0, S, n)
    th = c0 * v + 0.5 * c1 * v**2 + (1 / 3) * c2 * v**3
    tz = cumulative_trapezoid(np.cos(th), v, initial=0.0)
    pi = cumulative_trapezoid(np.sin(th), v, initial=0.0)
    t = np.array([np.cos(phi) * pi, np.sin(phi) * pi, tz])
    the = th[-1]
    cp, sp, ct, st = np.cos(phi), np.sin(phi), np.cos(the), np.sin(the)
    Rend = np.array([[cp**2 * (ct - 1) + 1, cp * sp * (ct - 1), cp * st],
                     [sp * cp * (ct - 1), sp**2 * (ct - 1) + 1, sp * st],
                     [-cp * st, -sp * st, ct]])
    return t, Rend


FRACS = (1 / 3, 2 / 3, 1.0)


def points_single(S, c0, c1, c2, phi):
    t, _ = _section(S, c0, c1, c2, phi)
    return np.array([t[:, int(f * 999)] for f in FRACS])


def points_multi(p15):
    """p15 = (S,c0,c1,c2,phi) x 3 sections -> (9,3) chained points, as in the paper."""
    pts = []
    Rcum, tcum = np.eye(3), np.zeros(3)
    for k in range(3):
        S, c0, c1, c2, phi = p15[5 * k:5 * k + 5]
        t, Rend = _section(S, c0, c1, c2, phi)
        tg = (Rcum @ t) + tcum[:, None]
        pts += [tg[:, int(f * 999)] for f in FRACS]
        tcum = tg[:, -1]
        Rcum = Rcum @ Rend
    return np.array(pts)


def pad_params(arr, model, sections):
    """Labels/preds -> (S,c0,c1,c2,phi) per section with zeros for missing coefficients."""
    out = []
    w = {"quad": 5, "affine": 4, "const": 3}[model]
    for k in range(sections):
        p = arr[w * k:w * k + w]
        if model == "quad":
            out += list(p)
        elif model == "affine":
            out += [p[0], p[1], p[2], 0.0, p[3]]
        else:
            out += [p[0], p[1], 0.0, 0.0, p[2]]
    return np.array(out, dtype=float)


def bending_from_euler(e):
    """Bending angle (deg) of a frame given ZYX Euler angles relative to its parent."""
    return np.degrees(np.arccos(np.clip(R.from_euler("zyx", e).as_matrix()[..., 2, 2], -1, 1)))
