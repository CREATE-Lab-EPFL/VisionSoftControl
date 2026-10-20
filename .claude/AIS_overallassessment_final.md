# AIS 3400076 — Reply to the reviewer's "Overall assessment" (draft)

Local-only file (git-excluded). Rules: one plain continuous block, no bold, no numbers, no quoted manuscript text.
Reviewer's overall assessment, in short: technically interesting integration; originality lies in distributed markerless internal cameras plus model-based and learned redundancy-aware control on a multisection arm, to be defined precisely and compared directly; several claims extend beyond the evidence (curvature estimate not used for control, scalability only with separately trained networks, learned-surrogate curvature labels, no quantitative evidence for the secondary objective, limited targets and planar trajectories without repeated trials); related work, reproducibility details, curvature formulation and figures need significant improvement.

Statements below map to: Comment 2 (contribution, comparison; DONE), Comment 1 (curvature separate; DONE), Comment 3 (retrained per arm; drafted), Comment 4 (model-constrained reconstruction; pending), Comments 6 to 8 (secondary objective, coverage, data independence; pending), Comments 5, 9, 10 (curvature formulation, reproducibility, figures; pending).
RE-CHECK this reply once those replies are final, and delete the todo.

## Letter block (replaces the placeholder reply under "Overall assessment" in `response_letter.tex`)

```latex
\begin{reply}
We thank the reviewer for the careful and constructive assessment. We agree that the originality of the work lies in the integration of distributed internal-camera sensing, which requires no markers at inference, with model-based and learned redundancy-aware control on a multi-section arm, and the contribution is now defined in these terms and compared directly with the closest prior systems. We have also aligned the claims with the evidence: the manuscript now states that the curvature estimate is evaluated separately from the controllers, that the networks are retrained for each arm, and that the multi-section reconstruction is model-constrained. The effect of the secondary objective, the coverage of the control evaluation and the independence of the training and evaluation data are now addressed through additional offline analyses of the existing data, and the related-work discussion, reproducibility details, curvature formulation and figures have been revised. Where a point could not be addressed with the existing data, such as repeated trials, we narrowed the corresponding claim and listed the limitation. Detailed responses follow. \todo{re-check once all point-by-point replies are final}
\end{reply}
```
