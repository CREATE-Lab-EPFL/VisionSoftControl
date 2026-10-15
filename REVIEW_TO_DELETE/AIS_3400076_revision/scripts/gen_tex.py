"""Generates LaTeX snippets (tables/lists) from the analysis outputs so numbers
are not transcribed by hand."""
import json, re, shutil, os
OUT = "/home/vigno0405/github/VisionSoftControl/REVIEW_TO_DELETE/AIS_3400076_revision"
REPO = "/home/vigno0405/github/VisionSoftControl"
B = f"{OUT}/build"; os.makedirs(B, exist_ok=True)
misc = json.load(open(f"{OUT}/data/misc_summary.json"))
cov = misc["coverage"]

rows = "\n".join(f"{t['id']} & {t['x']:.1f} & {t['y']:.1f} & {t['z']:.1f} & {t['bend_deg']:.1f} \\\\" for t in cov["SINGLE"]["targets"])
open(f"{B}/targets_single.tex", "w").write(rows)
rows = "\n".join(f"{t['id']} & {t['x']:.0f} & {t['y']:.0f} & {t['z']:.0f} & {t['yaw']:.0f} & {t['pitch']:.0f} & {t['roll']:.0f} & "
                 f"{t['bend_deg'][0]:.0f}/{t['bend_deg'][1]:.0f}/{t['bend_deg'][2]:.0f} & {t['dL_mm'][0]:.1f}/{t['dL_mm'][1]:.1f}/{t['dL_mm'][2]:.1f} \\\\"
                 for t in cov["MULTI"]["targets"])
open(f"{B}/targets_multi.tex", "w").write(rows)

def pe(path, label_fn):
    d = json.load(open(path)); out = []
    for k, v in d.items():
        out.append(f"{label_fn(k.split('/')[-1])} & {v['radius']:.1f} & {v['z_ref']:.0f} & {v['radial_rms']:.2f} & {v['height_rms']:.2f} & {v['n_points']} \\\\")
    return out
def lab_single(f):
    b = f.replace(".npz", "").split("_")
    ctrl = "Model-based" if "jacobian" in f else "Data-driven"; loop = "open" if "_OL_" in f else "closed"
    return f"Single & {ctrl} & {loop}"
def lab_multi(f):
    ctrl = "Model-based" if "Jacobian" in f else "Data-driven"; loop = "open" if "OpenLoop" in f else "closed"
    w = " + 50 g" if "W50g" in f else ""
    return f"Multi & {ctrl}{w} & {loop}"
rows = pe(f"{REPO}/SINGLE/results/PathErrorMetrics_closed.json", lab_single) + pe(f"{REPO}/SINGLE/results/PathErrorMetrics_open.json", lab_single) + \
       pe(f"{REPO}/MULTI/results/PathErrorMetrics.json", lab_multi)
open(f"{B}/path_errors.tex", "w").write("\n".join(rows))

# pages where 'segment' wording occurs (for the section/segment comment)
def seg_pages(fn):
    pages = open(f"{OUT}/pages/{fn}").read().split("<page ")[1:]
    out = []
    for i, p in enumerate(pages, 1):
        ws = re.findall(r">([^<]*)</word>", p)
        n = sum(1 for w in ws if re.search(r"(?i)segment", w))
        if n: out.append(f"p.\\,{i} ({n})")
    return ", ".join(out)
open(f"{B}/segment_pages.tex", "w").write(f"Main text: {seg_pages('main_bbox.html')}. SI: {seg_pages('si_bbox.html')}.")

for src, dst in [(f"{REPO}/MULTI/results/nullspace_ablation.pdf", "repo_nullspace_ablation.pdf"),
                 (f"{REPO}/SINGLE/results/single_workspace_coverage.pdf", "repo_single_workspace_coverage.pdf"),
                 (f"{REPO}/MULTI/results/multi_workspace_coverage.pdf", "repo_multi_workspace_coverage.pdf")]:
    shutil.copy(src, f"{OUT}/figures/{dst}")
print(open(f"{B}/segment_pages.tex").read())
