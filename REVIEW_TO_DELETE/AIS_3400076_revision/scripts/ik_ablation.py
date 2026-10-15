"""C6, data-driven controller: offline ablation of the secondary objective in the
IK training loss (Eq. 11). Trains N_l^3 twice with the paper's loss through the
frozen FK network (MULTI/models/kinematics/FK_model.pt): zeta = 0.01 (paper) and
zeta = 0 (no secondary objective), same data/split/seed, and compares
primary-task error FK(IK(p)) vs p and H(l) = 0.5||l - l_bar||^2 on the test poses
and on the 20 control targets. Offline/simulated through the learned FK model."""
import json
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from common import *

torch.manual_seed(42); np.random.seed(42)
fk = jit(f"{REPO}/MULTI/models/kinematics/FK_model.pt")
for p in fk.parameters():
    p.requires_grad_(False)
d = torch.load(f"{REPO}/MULTI/data/FKdata.pt", map_location="cpu")
L = torch.stack(list(d["DELTAL"])).float(); P = torch.stack(list(d["tip3_pose"])).float()
idx = np.arange(len(L)); tr, tmp = train_test_split(idx, test_size=0.15, random_state=42); va, te = train_test_split(tmp, test_size=1 / 3, random_state=42)
pm, ps = P[tr].mean(0), P[tr].std(0); lm, ls = L[tr].mean(0), L[tr].std(0)
lbar = torch.load(f"{REPO}/MULTI/models/kinematics/DELTAL_stats.pt")["mean"].float()


def net():
    return nn.Sequential(nn.Linear(6, 128), nn.ELU(), nn.Linear(128, 128), nn.ELU(), nn.Linear(128, 128), nn.ELU(),
                         nn.Linear(128, 128), nn.ELU(), nn.Linear(128, 9))


def loss_fn(model, pn, zeta):
    ln = model(pn); l = ln * ls + lm
    pp = (fk(l) - pm) / ps
    return nn.functional.huber_loss(pp, pn, delta=1.0) + zeta * torch.mean(ln ** 2)


def train(zeta, epochs=1500, patience=50):
    torch.manual_seed(42)
    m = net(); opt = torch.optim.Adam(m.parameters(), lr=1e-3, weight_decay=5e-6)
    sch = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, factor=0.9, patience=15)
    Xtr, Xva = (P[tr] - pm) / ps, (P[va] - pm) / ps
    best, state, c = 1e9, None, 0
    for ep in range(epochs):
        m.train(); perm = torch.randperm(len(Xtr))
        for i in range(0, len(perm), 64):
            b = perm[i:i + 64]; opt.zero_grad(); l = loss_fn(m, Xtr[b], zeta); l.backward()
            nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        m.eval()
        with torch.no_grad():
            v = loss_fn(m, Xva, zeta).item()
        sch.step(v)
        if v < best - 1e-6:
            best, state, c = v, {k: t.clone() for k, t in m.state_dict().items()}, 0
        else:
            c += 1
            if c > patience:
                break
    m.load_state_dict(state); m.eval()
    return m, ep


def evaluate(m, poses):
    with torch.no_grad():
        l = m((poses - pm) / ps) * ls + lm; pr = fk(l)
    pos = torch.linalg.norm(pr[:, :3] - poses[:, :3], dim=1).numpy()
    rot = ang_dist_deg(pr[:, 3:].numpy(), poses[:, 3:].numpy())
    H = 0.5 * ((l - lbar) ** 2).sum(1).numpy(); rms = torch.sqrt(((l - lbar) ** 2).mean(1)).numpy()
    return {"pos_mean": pos.mean(), "pos_std": pos.std(), "rot_mean": rot.mean(), "rot_std": rot.std(),
            "H_mean": H.mean(), "H_std": H.std(), "rms_dev_mean": rms.mean(), "rms_dev_std": rms.std()}


targets = torch.tensor(np.load(f"{REPO}/MULTI/results/ControlWorkspace.npz")["pose"], dtype=torch.float32)
res = {}
for z in (0.01, 0.0):
    m, ep = train(z)
    res[f"zeta={z}"] = {"epochs": ep, "test": evaluate(m, P[te]), "control_targets": evaluate(m, targets)}
json.dump(res, open(f"{DATA}/ik_ablation.json", "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=lambda x: round(float(x), 3)))
