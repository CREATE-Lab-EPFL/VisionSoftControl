"""Bar chart for the data-driven secondary-objective ablation (from data/ik_ablation.json),
same layout as the repo's null-space ablation figure."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import DATA, FIG
r = json.load(open(f"{DATA}/ik_ablation.json"))
a, b = r["zeta=0.01"]["control_targets"], r["zeta=0.0"]["control_targets"]
plt.rcParams.update({"font.size": 7, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.0))
for k, (m, s, t, yl) in enumerate([("H_mean", "H_std", "Secondary objective $H(l)$", "$H(l)$"),
                                   ("rms_dev_mean", "rms_dev_std", "RMS tendon deviation from $\\bar l$", "[mm]"),
                                   ("pos_mean", "pos_std", "Position error through $N_p^3$", "[mm]")]):
    ax[k].bar([0, 1], [a[m], b[m]], yerr=[a[s], b[s]], capsize=3, color=["tab:blue", "tab:red"])
    ax[k].set_xticks([0, 1], ["$\\zeta=0.01$ (paper)", "$\\zeta=0$"]); ax[k].set_title(t); ax[k].set_ylabel(yl)
fig.suptitle("Data-driven controller: IK network trained with / without the secondary term (20 control targets, offline)", fontsize=7.5)
plt.tight_layout(); plt.savefig(f"{FIG}/ik_ablation.pdf"); plt.close()
print("ok")
