# AIS 3400076 revision: status

Last update: 2026-10-15. Everything lives in the repository folder `REVIEW_TO_DELETE/` (committed by you in 84bc19c and pushed to origin; the clean-up after that is not committed yet).

## REVIEW_TO_DELETE/
- `AIS_3400076_response_letter.pdf`: the response letter (source: `AIS_3400076_revision/snippets/response_letter.tex`).
- `AIS_3400076_revision_guide.pdf`: what to change, step by step, with copyable LaTeX and the response to each comment.
- Original review PDFs: `Revision_letter.pdf`, `vision_based_soft_control_AIS-Main.pdf`, `vision_based_soft_control_AIS-Supporting.pdf`.

## Graphs (all from notebooks in the repository, PDFs in results/)
- `SINGLE/SINGLE_revision_figures.ipynb`: Fig. 5b equal axes, Fig. S4 target IDs.
- `MULTI/MULTI_revision_figures.ipynb` (run after the SINGLE one): Fig. 7 per point, Fig. S7 error vs bending, Figs. S5/S6 target IDs, Fig. S8b IK ablation, Fig. 3/4c diagrams.
- Already in the repo: `MULTI_nullspace_ablation.ipynb` (Fig. S8a), `SINGLE_workspace_coverage.ipynb` and `MULTI_workspace_coverage.ipynb` (Fig. S9).

## Sources (AIS_3400076_revision/)
- `snippets/`: every LaTeX snippet and `response_letter.tex`; regenerate with `python scripts/snippets.py` (visioncontrol env).
- `build/main.tex` + `crops/`: guide source (`pdflatex` twice from `build/`).
- `scripts/` + `data/`: analyses behind the numbers and tables; `scripts/build_notebooks.py` writes and executes the two revision notebooks.

## Open items (need the author)
- [FILL] camera model/lens/size/mass, exposure, pretension criterion, current limit, tendon material/diameter, removed samples, FK dataset details, Sec. 4.2.3 denominator.
- [CONFIRM] one build per arm; S_I-S_III in Fig. 1b; Huber vs MSE for the single-section networks.
- Check unverified cells of the comparison table (Thuruthel sensor, Han closed loop, Lu "--").
