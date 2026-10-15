"""Proposed (revised) figures for the response. Uses the analysis outputs in
data/ and the repo's control-result files (read-only)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from common import *

plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
COL = {"const": "tab:red", "affine": "tab:green", "quad": "tab:blue"}
LBL = {"const": "Constant", "affine": "Affine", "quad": "Quadratic"}
S = np.load(f"{DATA}/single_test.npz")
M = np.load(f"{DATA}/multi_test.npz")

# ---------- Fig. 7 proposed: per-point error vs normalised arc length ----------
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.7))
for a, (D, n, title) in zip(ax, [(S, 3, "(a) Single-section"), (M, 9, "(b) Multi-section")]):
    x = np.arange(1, n + 1) / n
    for k, m in enumerate(["const", "affine", "quad"]):
        e = D[f"{m}_vs_label"]
        off = (k - 1) * 0.008
        a.errorbar(x + off, np.median(e, 0), yerr=[np.median(e, 0) - np.percentile(e, 25, 0), np.percentile(e, 75, 0) - np.median(e, 0)],
                   fmt="o-", ms=3, lw=1, capsize=2, color=COL[m], label=LBL[m])
    if n == 9:
        for b in (1 / 3, 2 / 3):
            a.axvline(b + 1 / 18, color="0.7", lw=0.6, ls=":")
    a.set_xlabel("Normalised arc length $s/L_{tot}$"); a.set_ylabel("3D error per point [mm]"); a.set_title(title, fontsize=9)
    a.set_xlim(0, 1.05); a.grid(alpha=0.2)
ax[0].legend(frameon=False, fontsize=8)
plt.tight_layout(); plt.savefig(f"{FIG}/fig7_proposed.pdf"); plt.close()

# ---------- error vs bending ----------
def binned(ax, x, y, edges, color):
    c = 0.5 * (edges[1:] + edges[:-1]); med, q1, q3 = [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        s = y[(x >= lo) & (x < hi)]
        med.append(np.median(s) if len(s) > 5 else np.nan); q1.append(np.percentile(s, 25) if len(s) > 5 else np.nan); q3.append(np.percentile(s, 75) if len(s) > 5 else np.nan)
    ax.plot(c, med, "-o", color=color, ms=3, lw=1.2); ax.fill_between(c, q1, q3, color=color, alpha=0.2)

from scipy.stats import spearmanr
fig, ax = plt.subplots(1, 4, figsize=(9.5, 2.5))
x, y = S["bend"], S["pos_err"]
ax[0].scatter(x, y, s=4, alpha=0.3, color="tab:blue"); binned(ax[0], x, y, np.arange(0, 55, 5), "k")
r, p = spearmanr(x, y); ax[0].set_title(f"Single: position\nSpearman $\\rho$={r:.2f}, p<0.001", fontsize=8)
ax[0].set_xlabel("Bending angle [deg]"); ax[0].set_ylabel("Tip position error [mm]")
for i, k in enumerate(["I", "II", "III"]):
    xb, yb = M[f"bend_{k}"], M[f"abs_pos_{k}"]
    keep = xb <= 60
    ax[i + 1].scatter(xb[keep], yb[keep], s=4, alpha=0.3, color="tab:orange"); binned(ax[i + 1], xb, yb, np.arange(0, 65, 5), "k")
    r, p = spearmanr(xb, yb)
    ax[i + 1].set_title(f"Multi: tip {k} position\n$\\rho$={r:.2f}, p={p:.2f}", fontsize=8); ax[i + 1].set_xlabel(f"Section {k} bending [deg]")
    ax[i + 1].set_xlim(0, 60)
plt.tight_layout(); plt.savefig(f"{FIG}/bending_error.pdf"); plt.close()

# ---------- S4–S6 proposed: matched IDs, shared colour limits ----------
def load_ctrl(path):
    d = np.load(path); t, m = d["target"], d["mocap"]
    pe = np.linalg.norm(t[:, :3] - m[:, :3], axis=1)
    re_ = ang_dist_deg(t[:, 3:], m[:, 3:]) if t.shape[1] == 6 else None
    return t, pe, re_

def scatter_panel(fig, pos, t, err, vmin, vmax, cmap, title):
    a = fig.add_subplot(pos, projection="3d")
    sc = a.scatter(t[:, 0], t[:, 1], t[:, 2], c=err, cmap=cmap, vmin=vmin, vmax=vmax, s=18, depthshade=False)
    for i, p in enumerate(t[:, :3]):
        a.text(p[0], p[1], p[2], f" {i + 1}", fontsize=5.5)
    a.set_xlabel("X [mm]", fontsize=7, labelpad=-6); a.set_ylabel("Y [mm]", fontsize=7, labelpad=-6); a.set_zlabel("Z [mm]", fontsize=7, labelpad=-6)
    a.tick_params(labelsize=5, pad=-2); a.set_title(title, fontsize=8); a.view_init(elev=22, azim=-60)
    return sc

R1 = f"{REPO}/SINGLE/results"; R3 = f"{REPO}/MULTI/results"
# S4
tA, eA, _ = load_ctrl(f"{R1}/ControlWorkspace_jacobian.npz"); tB, eB, _ = load_ctrl(f"{R1}/ControlWorkspace_datadriven.npz")
vmax = np.ceil(max(eA.max(), eB.max()))
fig = plt.figure(figsize=(6.4, 2.8))
scatter_panel(fig, 121, tA, eA, 0, vmax, "viridis", "(a) Model-based CL")
sc = scatter_panel(fig, 122, tB, eB, 0, vmax, "viridis", "(b) Data-driven CL")
fig.colorbar(sc, ax=fig.axes, shrink=0.7, label="Position error [mm]"); plt.savefig(f"{FIG}/figS4_proposed.pdf"); plt.close()
# S5 and S6
for name, pa, pb, la, lb in [("figS5", "ControlWorkspaceJacobian.npz", "ControlWorkspaceDatadriven.npz", "(a) Model-based CL", "(b) Data-driven CL"),
                             ("figS6", "ControlWorkspaceJacobian_W50g.npz", "ControlWorkspaceOpenLoopJacobian_W50g.npz", "(a) Closed-loop, 50 g", "(b) Open-loop, 50 g")]:
    tA, pA, rA = load_ctrl(f"{R3}/{pa}"); tB, pB, rB = load_ctrl(f"{R3}/{pb}")
    vp, vr = np.ceil(max(pA.max(), pB.max())), np.ceil(max(rA.max(), rB.max()))
    fig = plt.figure(figsize=(6.4, 5.2))
    scatter_panel(fig, 221, tA, pA, 0, vp, "viridis", la + " - position"); s1 = scatter_panel(fig, 222, tB, pB, 0, vp, "viridis", lb + " - position")
    scatter_panel(fig, 223, tA, rA, 0, vr, "plasma", la + " - orientation"); s2 = scatter_panel(fig, 224, tB, rB, 0, vr, "plasma", lb + " - orientation")
    fig.colorbar(s1, ax=fig.axes[:2], shrink=0.7, label="Position error [mm]"); fig.colorbar(s2, ax=fig.axes[2:4], shrink=0.7, label="Orientation error [deg]")
    plt.savefig(f"{FIG}/{name}_proposed.pdf"); plt.close()

# ---------- Fig. 5b proposed: equal axis scaling ----------
te = S["te"]; bend = S["bend"]
pick = [int(np.argmin(np.abs(bend - np.percentile(bend, q)))) for q in (10, 45, 75, 97)]
d = load_fields(SINGLE_SHARDS, ["X_images", "X_quad", "X_affine", "X_const"], te[pick])
order = np.argsort(te[pick]); pick_sorted = np.array(pick)[order]
models = {"quad": "quadratic_model.pt", "affine": "affine_model.pt", "const": "const_model.pt"}
preds = {m: run_model(jit(f"{REPO}/SINGLE/models/curvature/{f}"), d["X_images"]) for m, f in models.items()}
labs = {"quad": d["X_quad"].numpy(), "affine": d["X_affine"].numpy(), "const": d["X_const"].numpy()}
def curve(p):
    S_, c0, c1, c2, phi = p; v = np.linspace(0, S_, 400)
    th = c0 * v + 0.5 * c1 * v**2 + c2 * v**3 / 3
    return cumulative_trapezoid(np.sin(th), v, initial=0), cumulative_trapezoid(np.cos(th), v, initial=0)
fig, ax = plt.subplots(1, 2, figsize=(6.0, 3.6), gridspec_kw={"width_ratios": [1, 1.6]})
for j in range(len(pick)):
    for m in ["quad", "affine", "const"]:
        xg, zg = curve(pad_params(labs[m][j], m, 1)); xp, zp = curve(pad_params(preds[m][j], m, 1))
        for a in ax:
            a.plot(xg, zg, color=COL[m], lw=1); a.plot(xp, zp, color=COL[m], lw=1, ls="--")
ax[0].set_title("Current style (non-uniform axes)", fontsize=8); ax[0].set_xlim(0, 60); ax[0].set_ylim(0, 150)
ax[1].set_title("Proposed: equal axis scaling", fontsize=8); ax[1].set_aspect("equal"); ax[1].set_xlim(0, 80); ax[1].set_ylim(0, 150)
for a in ax:
    a.set_xlabel("In-plane projection [mm]"); a.set_ylabel("Z [mm]"); a.grid(alpha=0.2)
ax[1].plot([55, 75], [10, 10], "k-", lw=2); ax[1].text(65, 14, "20 mm", ha="center", fontsize=7)
plt.tight_layout(); plt.savefig(f"{FIG}/fig5b_proposed.pdf"); plt.close()
print("figures done")
