# AIS 3400076 revision: status

Last update: 2026-10-15

Everything for the revision lives in the repository folder `REVIEW_TO_DELETE/` (untracked; not committed).

## Deliverables (in REVIEW_TO_DELETE/)
- `AIS_3400076_revision_guide.pdf`: the workbook (every comment, steps, copyable LaTeX, responses).
- `AIS_3400076_response_letter_draft.pdf`: compiled response letter (source: `AIS_3400076_revision/snippets/response_letter.tex`).
- `AIS_3400076_revision_guide_v1.pdf`: earlier version (no copyable LaTeX), kept for reference.
- The four original review PDFs (decision letter, manuscript, SI, first draft response).

## Graphs (all from notebooks in the repository)
- `SINGLE/SINGLE_revision_figures.ipynb` -> `SINGLE/results/fig5b_equal_axes.pdf`, `figS4_matched_ids.pdf`, `revision_single_test.npz`.
- `MULTI/MULTI_revision_figures.ipynb` (run after the SINGLE one) -> `MULTI/results/fig7_per_point.pdf`, `bending_error.pdf`, `figS5_matched_ids.pdf`, `figS6_matched_ids.pdf`, `ik_ablation.json/.pdf`, `fig3_network_map.pdf`, `fig4c_signal_flow.pdf`, `revision_multi_test.npz`.
- Already in the repo: `MULTI_nullspace_ablation.ipynb` (Fig. S8a), `SINGLE_workspace_coverage.ipynb` and `MULTI_workspace_coverage.ipynb` (Fig. S9).

## In AIS_3400076_revision/
- `snippets/`: every LaTeX snippet shown in the guide, plus `response_letter.tex`. Regenerate with `python scripts/snippets.py` (visioncontrol env).
- `figures_for_SI/`: copies of the notebook outputs referenced by the new SI figures S7-S9.
- `figures/`: earlier drafts of the proposed figures (superseded by the notebook outputs).
- `crops/`: annotated crops of the current figures. `pages/`, `text/`: rendered pages and extracted text of the manuscript and SI.
- `scripts/`, `data/`: analyses and their outputs; `scripts/build_notebooks.py` writes and executes the two revision notebooks.
- `build/main.tex`: guide source (`pdflatex` twice from `build/`).
- `originals/.claude/HANDOFF.md`: the old handoff note (its folder was removed from the repo).

## Open items (need the author)
- [FILL] camera model/lens/size/mass, exposure, pretension criterion, current limit, tendon material/diameter, removed samples, FK dataset details, Sec. 4.2.3 denominator.
- [CONFIRM] one build per arm; S_I-S_III in Fig. 1b; Huber vs MSE for the single-section networks.
- Check unverified cells of the comparison table (Thuruthel sensor, Han closed loop, Lu "--").
