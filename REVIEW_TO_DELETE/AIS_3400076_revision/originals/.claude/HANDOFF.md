# Handoff: AIS revision — reviewer response analysis

Read this whole file before doing anything. It's a self-contained status
snapshot of an in-progress task: addressing every comment in a major-revision
reviewer letter for the paper in this repo, with code-verified corrections
and real data re-analysis (not just text edits).

## The task

- `REVIEW_TO_DELETE/Revision_letter.pdf` — the **real, authoritative** reviewer
  letter (an emailed PDF export). This is ground truth for what the reviewer
  actually asked; read it directly, don't rely on paraphrase.
- `REVIEW_TO_DELETE/AIS_3400076_detailed_response.pdf` — a **draft** response
  written before any code/data was checked. It is not reliable on its own —
  several of its claims turned out to be wrong when checked against the
  actual code (see "Corrections to the draft response" below). Use it only
  as an index of which comments exist, not as a source of truth for what the
  code/data actually do.
- `REVIEW_TO_DELETE/vision_based_soft_control_AIS-Main.pdf` /
  `-Supporting.pdf` — the submitted manuscript + SI.
- Goal: for every major/minor/SI comment, either (a) find the code-verified
  correct explanation, (b) re-analyze real data to produce the number the
  reviewer asked for, or (c) confirm it's something only the user (Lorenzo)
  can answer (e.g. camera model, random seeds never recorded).
- The user said explicitly: **"go on, but trust the data"** — when analysis
  contradicts a manuscript claim (see the 85°/56.8° item below), trust the
  data, not the manuscript text, and flag the correction.

## One-time environment setup (needed on a fresh machine/session)

No Python environment on this machine had `torch` before this session (no
GPU available either — `nvidia-smi` reports no devices, so CPU-only is
correct, not a compromise). Set up with:

```bash
source ~/miniconda3/etc/profile.d/conda.sh   # or wherever conda lives
conda create -y -n visioncontrol python=3.10
conda activate visioncontrol
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install numpy scikit-learn scipy pandas matplotlib nbformat nbclient ipykernel
python3 -m ipykernel install --user --name visioncontrol --display-name "visioncontrol"
```

`casadi` is deliberately **not** installed — `SINGLE_reconstruction_utility.py`
imports it at module level but only for the `curvature_reconstruction`
method (CasADi/IPOPT fitting), which nothing in this analysis calls. If you
reimplement the `N_C` surrogate again, its `theta2R`/`theta2t` math only
needs `scipy.integrate.quad`, not casadi.

## Data

Two datasets were uploaded by the user as zips and extracted here:

- `SINGLE/data/SINGLE_dataset/Dataset0-9.pt` (10 shards × 1000 samples,
  ~2.9GB). Each shard is a `torch.load`-able dict with **lists** (not
  stacked tensors) under keys: `X_images` (1×480×640 uint8), `y` (6:
  x,y,z,yaw,pitch,roll — pose label), `X_DELTAL` (3), `backbones` (19, raw
  OptiTrack subsection Euler angles + arc length), `X_quad` (5: `[s(=L), c0,
  c1, c2, phi]`), `X_affine` (4), `X_const` (3), `X_poly`.
- `MULTI/data/MULTI_dataset/DatasetMulti0-9.pt` (10 shards × 1000, ~9.4GB).
  Keys: `X_images` (3×480×640 uint8), `X_DELTAL` (9), `X_quad` (15 = 3
  sections × `[s,c0,c1,c2,phi]`), `X_affine` (12), `X_const` (9), `tip_1`,
  `tip_2`, `tip_3` (each 6).

**Both are `.gitignore`d — they only exist locally on this machine, not in
git.** If you're on a different machine, you need to re-obtain them
(originals were user-uploaded zips named `SINGLE_dataset.zip` /
`MULTI_dataset.zip`; the README also points to a Zenodo DOI for the
published dataset). Everything else (notebooks, scripts, `results/*.npz`,
model checkpoints in `models/`) **is** committed to git.

**Important**: there's an automated process in this environment that
auto-commits and auto-pushes to `origin/main` (the public
`CREATE-Lab-EPFL/VisionSoftControl` repo) under generic "Update `<date>`"
messages — not something either you or the user triggers manually. Don't be
surprised by a clean `git status` after work was clearly done, and don't try
to diagnose it as a bug; just know your edits will show up on `origin/main`
on their own. The user is aware and was told the commit history may want
cleanup later, before this becomes part of the permanent paper-adjacent
record — don't do that rewrite unprompted.

## What's already done (committed, on origin/main)

All of these executed with **zero errors** (verified via nbformat error-cell
scan). Read a notebook before redoing its analysis.

| File | Addresses | Headline result |
|---|---|---|
| `MULTI/MULTI_nullspace_ablation.py` + `.ipynb` | Comment 6 | Offline replay of the resolved-motion-rate law, with/without the null-space term, against the PCC forward model, through the real 20-target sequence. H(l): 269±135 (with) vs 693±396 (without); RMS tendon dev 7.48±1.96mm vs 12.00±3.18mm; primary-task error basically unchanged (5.25 vs 5.84mm) — the objective works "for free." 2/20 targets stop just above the convergence threshold under both conditions — a ZYX-Euler gimbal-lock-adjacent artifact near pitch ±75-90°, not a real failure (see notebook cell 9 for the diagnosis). |
| `SINGLE/SINGLE_test_reconstruction.ipynb` | C24, C25 | Recomputed test-set error (4.02±2.25mm, 3.13±2.02°) matches published (3.99±2.23mm, 3.11±1.96°) almost exactly despite a different random split — good external validation of the whole pipeline. Bending-vs-accuracy correlation: r=-0.20 (real, modest, supports the qualitative claim). |
| `MULTI/MULTI_test_reconstruction.ipynb` | C23, C24, S29 | Table 1 reproduces almost exactly (4.42/14.03/26.12mm vs published 4.44/14.01/26.45mm). Confirms the "std > mean" skew in Table 1/S6 is real (e.g. Section I orientation max 175.64°) — very likely the same Euler-angle artifact as above. Has both absolute (Table 1) and relative (S6) conventions, plus median/IQR/p95. |
| `SINGLE/SINGLE_workspace_coverage.ipynb` | C7 (SINGLE half) | **The manuscript's "up to 85°" claim does not match the shipped data.** Three independent methods (fitted polynomial integral, raw OptiTrack backbone rotation matrix, pose-label rotation-vector norm) all agree exactly: max 56.8°, mean 19.3°, p95 35.6°, N=10000. User confirmed: "85 deg was more of an assumption" — trust the data. Control targets reach 59-72% of the *real* range, not ~40%. |
| `SINGLE/SINGLE_NC_surrogate_validation.ipynb` (model at `SINGLE/models/kinematics/NC_surrogate_reconstructed.pt`) | C4, S28 | `N_C` (pose→curvature surrogate for MULTI ground truth) has **no checkpoint or training code anywhere in the repo** — reconstructed an equivalent from the SINGLE dataset per the SI's own description ("treating the robot as a modular extension of the single-section unit"). Sum-of-3D-errors: 2.11±2.95mm (median 1.41, p95 5.74, N=500) — small relative to the CNN's own error, consistent with the SI's existing qualitative claim. |
| `SINGLE/SINGLE_path_error_metrics.ipynb`, `MULTI/MULTI_path_error_metrics.ipynb` | C26 | Real RMS radial/height path-error numbers (Kasa circle fit to each file's own target vertices) for every SINGLE/MULTI trajectory file, closed/open-loop, with/without 50g disturbance. |
| `SINGLE/SINGLE_MULTI_leakage_check.ipynb` | C8 | Quantified, not just flagged: 53.4% of SINGLE test samples are within 1mm (tendon space) of a training sample (92.4% within 2mm) — network's own reported error is ~4mm, so this is a real concern. MULTI has **exact zero-distance duplicates** — plausibly from the SI's coupled-module sampling (Algorithm 1). |

**Note on generating scripts**: the notebooks above have markdown cells that
name the `.py` script that generated their underlying `results/*.npz` (e.g.
"See `nc_surrogate.py`"). By explicit user preference, those generating
scripts have **not** been persisted to the repo — they lived only in an
ephemeral scratchpad that's since been cleared. **Don't try to reconstruct
them.** The `.npz`/`.pdf` outputs and the notebooks that read them are the
durable record; if you need to redo one of these analyses, write it fresh
rather than trying to recover the exact original script, and don't turn
that into a project of persisting every intermediate helper — the user
explicitly pushed back on that once already ("too much... don't do this
huge refactor").

### Corrections to the draft response (code-verified, not yet in any doc except this one and the chat transcript)

- **C1**: the draft response says the pre-loop PCC tendon estimate "never
  reaches J, N, or δl." This is **wrong**. In `MULTI_controller.py`
  `__init__` (~L141-144) and identically in `SINGLE_controller.py`
  (~L131-132), the camera/PCC estimate computes `self.DELTAL_reference`, a
  **one-time calibration offset** between the motor's absolute encoder zero
  and the physical PCC tendon-length origin. Every `read_DELTAL_from_motors()
  - self.DELTAL_reference` call inside the control loop depends on it,
  feeding directly into the Jacobian and null-space term. It's a real,
  necessary calibration, not dead code.
- **C5**: main-text Eq. 4's normalized-`s` vs SI's dimensional-`x` — checked
  `SINGLE_reconstruction_utility.py`/`MULTI_jacobians.py`: the **code uses
  dimensional arc length throughout**, matching the SI, not the main text.
  Fixing the main text to match the SI (as the draft response proposes) is
  correct.
- **Minor "simultaneous" cameras (pp.3-5)**: confirmed false —
  `MULTI_cameras_utility.py`'s `ThreadedCameraSystem` runs each camera in an
  independent free-running thread (`time.sleep(0.27)` between reads, no
  shared trigger), so frames are never truly simultaneous.
- **Minor sine/cosine decode (pp.5-7)**: the draft guesses "presumably
  atan2 of the predicted sin/cos pair." Wrong — checked the training
  notebooks: the network head **directly regresses raw angle values**;
  sin/cos is only used transiently inside the loss (Huber loss on
  `sin(pred)` vs `sin(true)` etc., for wraparound-safety), never as an
  output representation. There is no atan2 decode step because there's
  nothing to decode.
- **C8 split mechanics**: confirmed directly from
  `*_helyx_testing.ipynb`'s (disabled `if False:`) split cell:
  `train_test_split(all_indices, test_size=0.15)` then `(temp, test_size=
  1/3)`, **no `random_state`** — a pure random shuffle pooled across all
  shards, not session-blocked. The 20 k-medoids control targets are drawn
  from `data/Workspace.npz`, which pools `train+val+test` together — **the
  control-evaluation targets were never excluded from training.**
- Minor open-loop/closed-loop gains (Minor 20): confirmed `discr_wp=1` for
  both `MULTIController` and `MULTIOpenLoop` (same value, code-checked, not
  assumed).

### Confirmed new citations (from the real letter's exact wording — draft response's guesses for two of these were wrong until checked)

```bibtex
@article{hoferVisionBasedSensingApproach2021,
  title = {A {{Vision-Based Sensing Approach}} for a {{Spherical Soft Robotic Arm}}},
  author = {Hofer, Matthias and Sferrazza, Carmelo and D'Andrea, Raffaello},
  year = 2021, journal = {Frontiers in Robotics and AI}, volume = {8}, pages = {630935},
  doi = {10.3389/frobt.2021.630935}
}
@article{thuruthelLearningClosedLoop2017,
  title = {Learning {{Closed Loop Kinematic Controllers}} for {{Continuum Manipulators}} in {{Unstructured Environments}}},
  author = {Thuruthel, Thomas George and Falotico, Egidio and Manti, Mariangela and Pratesi, Andrea and Cianchetti, Matteo and Laschi, Cecilia},
  year = 2017, journal = {Soft Robotics}, volume = {4}, number = {3}, pages = {285--296},
  doi = {10.1089/soro.2016.0051}
}
@article{hanAnchoringMorphologicalRepresentations2025,
  title = {Anchoring {{Morphological Representations Unlocks Latent Proprioception}} in {{Soft Robots}}},
  author = {Han, Xudong and Guo, Ning and Xu, Ruoyu and Wan, Fang and Song, Chaoyang},
  year = 2025, journal = {Advanced Intelligent Systems}, volume = {7}, number = {12}, pages = {e202500444},
  doi = {10.1002/aisy.202500444}
}
@article{luAdaptiveOnlineLearning2024,
  title = {Adaptive {{Online Learning}} and {{Robust}} 3-{{D Shape Servoing}} of {{Continuum}} and {{Soft Robots}} in {{Unstructured Environments}}},
  author = {Lu, Yiang and Chen, Wei and Lu, Bo and Zhou, Jianshu and Chen, Zhi and Dou, Qi and Liu, Yun-Hui},
  year = 2024, journal = {Soft Robotics}, volume = {11}, number = {2}, pages = {320--337},
  doi = {10.1089/soro.2022.0158}
}
```

(`Yoo et al.` is already `Ref. [15]` in the manuscript — not new.)

## MULTI workspace coverage, S31 — done; S30 done-then-reverted (see below)

- `MULTI/MULTI_workspace_coverage.py` + `.ipynb` — Comment 7's MULTI half,
  done, both committed. Section-by-section: targets reach 23-43° max vs.
  training p95 of 30-34° (roughly comparable range, unlike SINGLE's clearer
  under-coverage); trajectories reach up to 57° for Section III (IK-net
  estimate).
- `MULTI/MULTI_S31_sample_regimes.py` + `.ipynb` — **run, but did NOT settle
  S31.** Important finding, not just an inconclusive result:
  `MULTI_data_acquire.py` implements a `config = np.random.randint(0,3)`
  scheme where `config==0` couples all 3 sections and `config==1` couples
  sections I-II via `SamplingSolver` (an exact 3×3 linear solve). The
  detection method (checking whether sections' curvature coordinates match)
  was verified correct via a self-check against a synthetic coupled pair
  (max diff 5.33e-15, machine precision). Despite that, **essentially none
  of the 10,000 shipped samples show any matched-section signature** —
  median inter-section distance is 10-14 (curvature-coordinate units),
  nowhere near the ~0.09mm-equivalent encoder tolerance that would explain a
  genuinely-coupled-but-noisy sample. **The shipped dataset does not show
  the trace `MULTI_data_acquire.py`'s current coupling scheme should leave
  if it generated this data.** Likely explanation: an earlier/different
  acquisition script (possibly fully-independent sampling throughout) was
  actually used. **This needs confirmation from whoever ran the original
  acquisition sessions (ask Lorenzo directly) before S31 can be answered —
  do not report regime counts as fact.**
- S30 (matched target IDs + shared color scale for the Fig S4-S6-style
  control-error scatter plots) — **done, then removed.** The 3 output PDFs
  were produced by `S30_matched_figures.py`, which was deleted along with
  the other unwanted root-level helper scripts; with no generating script
  left anywhere, the PDFs were orphaned and were removed too (unlike
  `MULTI_workspace_coverage.ipynb`/`MULTI_S31_sample_regimes.ipynb`, whose
  underlying data-generating scripts are still in `MULTI/` and kept). **S30
  is back to not-addressed** — if it's wanted, it needs redoing from
  scratch, not recovering.

## Not started (bigger, lower priority)

- **Fig 7b full 9-point backbone reconstruction** (deeper version of
  Comment 23 for MULTI): would require running the MULTI curvature CNNs
  (`models/curvature/quadratic_for_MULTI_model.pt` etc.) and composing the
  3-section forward chain (rotation/translation composition per section,
  analogous to `MULTI_jacobians.py`'s `q2coordinates` but for the
  polynomial `c0,c1,c2` model instead of the `Dx,Dy,Dl` parameterization).
  The Table 1/S6 pose-CNN-based re-analysis already substantively answers
  Comment 23's core ask (define the statistic precisely, make SINGLE/MULTI
  comparable) — this would be a deepening, not a gap-fill.
- Manuscript text edits themselves (the actual prose changes for Comments
  1-10, minor comments, SI comments) — everything above produces the
  *evidence*; nobody has drafted the response-letter prose or manuscript
  diffs yet. The manuscript source isn't in this repo (only compiled PDFs in
  `REVIEW_TO_DELETE/`) — it lives wherever Lorenzo actually writes the paper
  (Overleaf/Word), so edits need to happen there, not here.

## Working preference (learned the hard way)

The user pushed back explicitly on persisting a growing pile of standalone
`.py` "helper" scripts (especially ones living outside `SINGLE/`/`MULTI/` at
the repo root, like a shared notebook-builder or figure-fixer): "too
much... don't do this huge refactor." Preference going forward:
- Don't create supporting infrastructure/helper scripts proactively.
- It's fine for a notebook to reference a `.py` script that no longer
  exists in the repo (e.g. "see `nc_surrogate.py`") — leave it, don't
  "fix" it by recreating the file.
- Favor one-off, inline analysis over building reusable tooling, unless
  asked for the latter directly.

## How to resume

The user asked to switch modes: **address the reviewer's comments one
question at a time from here**, rather than another broad automated sweep.
Don't launch into another multi-notebook batch unprompted — wait for
direction on which comment to take next.

In a new chat: point Claude at this file (`.claude/HANDOFF.md`) for full
context, then work question by question per the preference above.
Everything needed to pick up cleanly is either in this file, in the
committed notebooks, or in the conversation transcript this file
summarizes.
