"""Same metrics as ik_ablation.py for the deployed IK_model.pt (reference)."""
import json, numpy as np, torch
from sklearn.model_selection import train_test_split
from common import *
fk = jit(f"{REPO}/MULTI/models/kinematics/FK_model.pt"); ik = jit(f"{REPO}/MULTI/models/kinematics/IK_model.pt")
d = torch.load(f"{REPO}/MULTI/data/FKdata.pt", map_location="cpu")
P = torch.stack(list(d["tip3_pose"])).float()
idx = np.arange(len(P)); tr, tmp = train_test_split(idx, test_size=0.15, random_state=42); va, te = train_test_split(tmp, test_size=1/3, random_state=42)
lbar = torch.load(f"{REPO}/MULTI/models/kinematics/DELTAL_stats.pt")["mean"].float()
targets = torch.tensor(np.load(f"{REPO}/MULTI/results/ControlWorkspace.npz")["pose"], dtype=torch.float32)
def ev(poses):
    with torch.no_grad():
        l = ik(poses); pr = fk(l)
    pos = torch.linalg.norm(pr[:, :3] - poses[:, :3], dim=1).numpy(); rot = ang_dist_deg(pr[:, 3:].numpy(), poses[:, 3:].numpy())
    H = 0.5 * ((l - lbar) ** 2).sum(1).numpy(); rms = torch.sqrt(((l - lbar) ** 2).mean(1)).numpy()
    return {"pos_mean": pos.mean(), "pos_std": pos.std(), "rot_mean": rot.mean(), "H_mean": H.mean(), "H_std": H.std(), "rms_dev_mean": rms.mean(), "rms_dev_std": rms.std()}
r = {"test": ev(P[te]), "control_targets": ev(targets)}
json.dump(r, open(f"{DATA}/ik_deployed_eval.json", "w"), indent=1, default=float)
print(json.dumps(r, indent=1, default=lambda x: round(float(x), 2)))
