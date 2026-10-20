# AIS 3400076 — Minor comments 21 to 27 (Pages 8-11) (draft; red/[..] items need the user)

Local-only (git-excluded). Rules: short edits, reply = one plain block, no numbers, no bold, no quoted manuscript text.
Generated figures are in `.claude/AIS_figures/` (local-only, copy them into Overleaf).

---
## Comment 21: denominator of percentage errors

Verified from the logged data: published percentages reproduce exactly with the nominal rest length of 150 mm per section: single-section 3.99 mm / 150 = 2.66%; multi-section Module I 4.44 / 150 = 2.96%, Module II 14.01 / 300 = 4.67%, Module III 26.45 / 450 = 5.88% (cumulative nominal length up to each tip); control errors: single 4.63 mm / 150 = 3.1%; multi 25.32 mm / 450 = 5.6% (full arm). All six control percentages in the text reproduce.

### Edit 1 (Static Pose Reconstruction, single-section, first sentences)
Find:
```latex
The final position accuracy corresponds to $2.66 \pm 1.49 \%$ of the robot length
```
Replace:
```latex
The final position accuracy corresponds to $2.66 \pm 1.49 \%$ of the nominal robot length ($150~\text{mm}$)
```

### Edit 2 (Static Pose Reconstruction, multi-section)
Find:
```latex
Position error for Module I ($2.96 \pm 1.79\%$ of section length)
```
Replace:
```latex
Position error for Module I ($2.96 \pm 1.79\%$ of the nominal section length of $150~\text{mm}$)
```
Find:
```latex
reaching $4.67 \pm 2.93\%$ and $5.88 \pm 3.66\%$ up to the respective tips,
```
Replace:
```latex
reaching $4.67 \pm 2.93\%$ and $5.88 \pm 3.66\%$ of the cumulative nominal length up to the respective tips ($300$ and $450~\text{mm}$),
```

### Edit 3 (control performance, one sentence in each of the two target paragraphs)
Single-section (after "...Fig.~\ref{fig:Figure_5}\textbf{c}."): ` Control errors are expressed as a percentage of the nominal robot length ($150~\text{mm}$).`
Multi-section (after the position-error sentence): ` Control errors are expressed as a percentage of the nominal length of the full arm ($450~\text{mm}$).`

### Small fix found on the way
Payload paragraph: "compared to $14.5 \pm 3.5 \%$" does not match the table (64.56 mm / 450 mm = 14.3%): change to `$14.3 \pm 3.5 \%$`. (Recomputed from the logged data: 14.3 +- 3.5.)

### Letter
```latex
\begin{point}[Denominator of percentage errors]\label{c:21}
State the denominator used for every percentage error. For example, clarify whether multi-section position errors are normalized by one section length, cumulative tip length, or the maximum deployed length.
\end{point}
\begin{reply}
We thank the reviewer. The denominator is now stated for every percentage: the nominal rest length of the arm, which is one section length for the single-section arm and for the first module of the multi-section arm, the cumulative nominal length up to the respective tip for the other modules, and the nominal length of the full arm for the control errors of the multi-section arm. We also corrected one percentage in the payload paragraph that did not match the table.
\end{reply}
```

---
## Comment 22: Fig. 5b axis scaling (NO redraw: explained in the caption)

Measured on the rendered figure: in the shape plots the horizontal axis is stretched by about a factor of 2.7 relative to the vertical axis. Fig. 5c also uses the abbreviations CL and OL, which the caption does not define.

### Caption edits (Fig. 5)
Find: `Axes scaling is not uniform to emphasize the bending effect.`
Replace:
```latex
The horizontal axis is stretched by about a factor of $2.7$ with respect to the vertical axis to emphasize the bending effect, so the shapes appear more bent than they are; the tick labels give the true scale of each axis.
```
Find: `(c) Performance of the proposed controllers on the control workspace of the single-segment arm, reporting both average errors and standard deviations.`
Replace:
```latex
(c) Performance of the proposed controllers on the control workspace of the single-segment arm (CL: closed-loop, OL: open-loop), reporting both average errors and standard deviations.
```
(If you applied the Comment 12 replacement of "single-segment" first, search for "single-section arm, reporting".)

### Letter
```latex
\begin{point}[Fig.~5b axis scaling]\label{c:22}
Figure 5b intentionally uses nonuniform axis scaling. This visually distorts the reconstructed shapes. Use equal spatial scaling where possible or add a second undistorted view and explicit scale bars.
\end{point}
\begin{reply}
We thank the reviewer. We kept the stretched view, because with equal scaling the differences between the curvature models would be barely visible, but the caption now states the stretch factor, warns that the shapes appear more bent than they are, and refers to the tick labels for the true scale of each axis. We also defined the abbreviations used in the panel on the control errors.
\end{reply}
```

---
## Comment 23: Fig. 7 statistic (NO redraw: defined exactly in the caption and the text)

Verified on the rendered Fig. 7 and Fig. S2: the vertical axis of every panel is "Sum of 3D errors [mm]": per test configuration, the sum over the reference points (three in Fig. 7a, nine in Fig. 7b and Fig. S2) of the Euclidean distance between the predicted and the measured backbone point. Bar = mean over the test set, error bar = +- one standard deviation (bar height sits at the middle of the whisker), lines inside the bars = percentiles. The bar heights are about 7.7 to 7.9 mm (single-section) and 199 to 203 mm (multi-section), i.e. about 2.6 mm and 22 mm per reference point. The text calls the plotted quantity "average 3D error for each point" and the caption "cumulative", which is inconsistent with the axis; the three phrases should be replaced by one.

### Edit 1: Fig. 7 caption
Find: `Cumulative 3D reconstruction error of the curvature models.`
Replace:
```latex
Sum of the 3D reconstruction errors of the curvature models, that is, for each test configuration, the sum over the reference points of the Euclidean distance between predicted and measured backbone points; bars show the mean, error bars one standard deviation, and horizontal lines inside the bars percentiles of the distribution over the test set. Dividing the mean by the number of reference points gives about $2.6$~mm per point in (a) and about $22$~mm per point in (b).
```
(Keep the rest of the caption: reference points, "Note the different vertical scales".)

### Edit 2: text, single-section curvature paragraph
Find: `reports the average 3D error for each point, as well as the cumulative standard deviations across all curvature models.`
Replace: `reports, for each curvature model, the mean and the standard deviation over the test set of the sum of the 3D errors at the three points.`

### Edit 3: text, multi-section curvature paragraph
Find: `We evaluate reconstruction accuracy at nine uniformly spaced backbone reference points in Fig.~\ref{fig:Figure_7}\textbf{b}.`
Replace: `We evaluate reconstruction accuracy at nine uniformly spaced backbone reference points, using the sum of the 3D errors at these points as in Fig.~\ref{fig:Figure_7}\textbf{a}, in Fig.~\ref{fig:Figure_7}\textbf{b}; the sums of the single-section and multi-section arms are not directly comparable because they run over three and nine points.`

### Edit 4: SI, Fig. S2 caption
Replace the whole caption by:
```latex
(a) Sum of the 3D errors of the curvature models over the reference points placed every ninth of the manipulator length. (b) Sum of the 3D errors induced by the $N_C$ approximation with respect to the motion-capture ground truth. In both panels, bars show the mean, error bars one standard deviation, and horizontal lines inside the bars percentiles of the distribution over the test configurations.
```

### Letter
```latex
\begin{point}[Fig.~7 error statistic]\label{c:23}
Figure 7 alternates among 'cumulative 3D error,' 'sum of 3D errors,' and 'average 3D error for each point.' Define the statistic exactly. Summing three points for the single-section arm and nine for the multi-section arm also prevents direct comparison. Per-point RMSE or error versus normalized arc length would be clearer.
\end{point}
\begin{reply}
We thank the reviewer. The statistic is now defined exactly and used consistently in the text, the caption and the Supporting Information: for each test configuration, the sum over the reference points of the Euclidean distance between the predicted and the measured backbone point, with the bars showing the mean over the test set and the error bars one standard deviation. Because the sums run over a different number of points, the caption also gives the corresponding mean error per reference point for both arms, which makes them comparable; we kept the figure itself unchanged.
\end{reply}
```

---
## Comment 24: Table 1 orientation error (recomputed robust statistics)

Source: `MULTI/MULTI_test_reconstruction.ipynb` (500 test configurations of a RE-DRAWN random split; the original split was not saved, so means differ slightly from the originally reported ones: orientation I 6.78 -> 5.65, II 6.45 -> 6.54, III 8.74 -> 8.53). The maxima near 176 deg are single samples; they are most likely wrap-around or ambiguity of the Euler-angle representation, not regression failure (flagged as a hypothesis in the notebook).
DECISION for the user: replace the whole Table 1 by the recomputed one below (all columns from one split, recommended) or keep the published means and only add the other columns from the recomputation (inconsistent).

### Edit 1: replace the table (the old Table 1, label `table:abs_errors`; with the new comparison table in the Introduction it becomes Table 2)
```latex
\begin{table*}[ht]
\centering
\caption{Pose errors for the multi-section arm on $500$ randomly drawn test configurations (mean $\pm$ standard deviation, median, 95th percentile, and maximum).\label{table:abs_errors}}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{lcccc|cccc}
\toprule
 & \multicolumn{4}{c|}{\textbf{Position [mm]}} & \multicolumn{4}{c}{\textbf{Orientation [°]}} \\
\textbf{Section} & mean $\pm$ SD & median & p95 & max & mean $\pm$ SD & median & p95 & max \\
\midrule
I   & $4.42 \pm 2.56$ & $3.93$ & $8.61$ & $17.48$ & $5.65 \pm 8.85$ & $4.63$ & $10.31$ & $175.64$ \\
II  & $14.03 \pm 10.26$ & $12.02$ & $28.58$ & $147.37$ & $6.54 \pm 7.54$ & $5.69$ & $12.64$ & $155.81$ \\
III & $26.12 \pm 16.00$ & $23.26$ & $55.63$ & $140.29$ & $8.53 \pm 11.07$ & $7.07$ & $16.12$ & $176.78$ \\
\bottomrule
\end{tabular}
\end{table*}
```

### Edit 2: text after the table's first reference
Find:
```latex
while orientation remains below $9^\circ$.
```
Replace:
```latex
while the mean orientation error remains below $9^\circ$ (median below $8^\circ$, 95th percentile below $17^\circ$). The standard deviations exceed the means in part because of rare outliers, most likely owing to the wrap-around of the Euler-angle representation, with maxima above $150^\circ$.
```
Add to the Network Training or table text: "Statistics are recomputed on a re-drawn random test split, because the original split was not stored."
Optional: add median/p95/max for the single-section arm to SI Table S5 (recomputed: translation 4.02 +- 2.25 mm, median 3.57, p95 8.48, max 15.04; rotation 3.13 +- 2.02 deg, median 2.66, p95 7.06, max 13.41).

### Letter
```latex
\begin{point}[Table 1 orientation error]\label{c:24}
In Table 1, the text states that orientation error remains below 9 degrees, but several standard deviations are larger than the corresponding means. Make clear that only the mean is below 9 degrees and report median, 95th percentile, and maximum error.
\end{point}
\begin{reply}
We thank the reviewer. The text now states that only the mean orientation error is below the stated value, and the table reports the median, the 95th percentile and the maximum in addition to the mean and standard deviation. The large standard deviations are caused by rare outliers, which we discuss and attribute most likely to the wrap-around of the Euler-angle representation. Because the original test split was not stored, the statistics were recomputed on a freshly drawn random split of the same size, and the means agree closely with the previous ones; this is stated in the table caption.
\end{reply}
```

---
## Comment 25: "bent configurations improve accuracy"

Evidence (single-section, 500 test configurations; bending angle = rotation of the ground-truth pose; figure `.claude/AIS_figures/Figure_S_error_vs_bending.pdf`): Spearman rho = -0.21 (translation) and -0.20 (rotation), both significant; binned median translation error 3.91, 3.75, 3.40, 2.82, 4.44 mm for bending 0-10, 10-20, 20-30, 30-40, 40-60 deg (n = 81, 183, 166, 55, 15); the highest bin has only 15 samples and no improvement. Multi-section (tip error vs. tip rotation): rho = -0.08, -0.04, -0.05 (translation) and +0.04, +0.08, +0.12 (rotation) for tips I to III, mostly not significant: the multi-section claim is NOT supported.

### Edit 1 (single-section static pose results)
Find:
```latex
Overall, accuracy improves in bent configurations, where helicoidal deformations provide stronger visual cues for state estimation. Compared to IMU-based approaches~\cite{peiIMUBasedPose2024}, which have reported degradation at high bending, these results suggest that embedded vision may be advantageous at workspace boundaries.
```
Replace:
```latex
The error decreases moderately with the bending angle (Spearman correlation of about $-0.2$ for both translation and rotation, Fig.~S7 of the Supporting Information), consistent with stronger visual cues from helicoidal deformations, although the few test samples beyond $40^\circ$ show no further improvement. Compared to IMU-based approaches~\cite{peiIMUBasedPose2024}, which have reported degradation at high bending, accuracy is maintained at moderate bending; the most strongly bent configurations are sparsely represented.
```

### Edit 2 (multi-section static pose results): remove the unsupported sentence
Find:
```latex
Bent configurations, however, partially offset accumulation by providing more distinctive image features.
```
Replace: (delete; or) `The error shows no clear dependence on the bending angle.`

### Edit 3 (conclusion)
Find: `with preserved accuracy at workspace boundaries.`
Replace: `with accuracy maintained at moderate bending.`

### Edit 4: new SI figure (copy the PDF) and caption
```latex
\begin{figure}[htb]
\centering
\includegraphics[width=\linewidth]{Figures/Figure_S7.pdf}
\caption{Reconstruction error of the single-section pose network versus the bending angle of the ground-truth pose on the $500$ test configurations. Orange: binned median and interquartile range; the Spearman correlation is reported in each panel.}
\label{fig:Figure_S7}
\end{figure}
```
(Copy `.claude/AIS_figures/Figure_S_error_vs_bending.pdf` as `Figures/Figure_S7.pdf`; change "Fig.~S7" to `Fig.~\ref{fig:Figure_S7}` if you cross-reference in the SI.)

### Letter
```latex
\begin{point}[``Bent configurations improve accuracy'']\label{c:25}
The claim that bent configurations improve accuracy is plausible but currently qualitative. The authors should plot error against bending angle before drawing this conclusion.
\end{point}
\begin{reply}
We thank the reviewer. We plotted the error against the bending angle for the single-section test set and added the figure to the Supporting Information. The error decreases moderately with bending, with a weak but significant negative correlation for both translation and rotation, and the few most strongly bent configurations show no further improvement, so we reworded the claim and removed the statement that vision is advantageous at the workspace boundaries. For the multi-section arm the error shows no clear dependence on the bending angle, and the corresponding sentence has been removed.
\end{reply}
```

---
## Comment 26: Figs. 6, 9, 10 trajectory details and path errors

Facts (logged data): every trajectory is a regular 30-sided polygon visited once, counter-clockwise seen from +z, starting on the positive x-axis of the base frame, 30 vertices (single-section: waypoints every 1 mm along the polygon); the plotted paths are the motion-capture records of ONE run (no averaging); about one lap each (0.99 to 1.01).
Path errors (radial and height RMS in mm, from a circle fit to each trajectory's target vertices, `*_path_error_metrics.ipynb`, results in `results/PathErrorMetrics*.json`):

Single-section (radius about 35 / 25 mm; heights 115 / 125 mm):
| Controller | R35 z115 radial / height | R25 z125 radial / height |
|---|---|---|
| Closed-loop model-based | 1.46 / 2.65 | 1.32 / 1.23 |
| Closed-loop data-driven | 1.71 / 2.49 | 1.83 / 1.54 |
| Open-loop model-based | 8.06 / 8.74 | 5.71 / 4.30 |
| Open-loop data-driven | 2.27 / 5.48 | 1.61 / 4.41 |

Multi-section (R120 z350 / R80 z380):
| Controller | R120 radial / height | R80 radial / height |
|---|---|---|
| Closed-loop model-based | 7.78 / 5.74 | 6.25 / 3.43 |
| Closed-loop data-driven | 7.63 / 2.10 | 5.85 / 2.72 |
| Open-loop model-based | 12.64 / 8.10 | 10.60 / 5.24 |
| Open-loop data-driven | 10.86 / 4.41 | 5.53 / 7.67 |
| Closed-loop model-based, 50 g | 11.46 / 6.46 | 5.35 / 1.63 |
| Open-loop model-based, 50 g | 27.10 / 28.46 | 20.64 / 11.22 |

### Edit 1: captions of Figs. 6 and 9 (append) and Fig. 10
```latex
Each path is the motion-capture record of a single run of one lap, starting on the positive $x$-axis of the base frame and following the $30$ waypoints in counter-clockwise order (seen from $+z$); radial and height errors are reported in the Supporting Information.
```

### Edit 2: SI table (new subsection "Path Errors")
```latex
\subsection{Path Errors for the Circular Trajectories}
Table~\ref{tab:path_errors} reports, for each trajectory, the root-mean-square radial deviation from the circle fitted to the target waypoints and the root-mean-square deviation of the height from the nominal height, from the single run of each controller.

\begin{table*}[ht]
\centering
\caption{Root-mean-square path errors [mm] (radial / height) for the circular trajectories.}
\label{tab:path_errors}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{lcccc}
\toprule
 & \multicolumn{2}{c}{\textbf{Single-section}} & \multicolumn{2}{c}{\textbf{Multi-section}} \\
 & $35$~mm, $115$~mm & $25$~mm, $125$~mm & $120$~mm, $350$~mm & $80$~mm, $380$~mm \\
\midrule
Closed-loop, model-based & $1.46$ / $2.65$ & $1.32$ / $1.23$ & $7.78$ / $5.74$ & $6.25$ / $3.43$ \\
Closed-loop, data-driven & $1.71$ / $2.49$ & $1.83$ / $1.54$ & $7.63$ / $2.10$ & $5.85$ / $2.72$ \\
Open-loop, model-based & $8.06$ / $8.74$ & $5.71$ / $4.30$ & $12.64$ / $8.10$ & $10.60$ / $5.24$ \\
Open-loop, data-driven & $2.27$ / $5.48$ & $1.61$ / $4.41$ & $10.86$ / $4.41$ & $5.53$ / $7.67$ \\
Closed-loop, model-based, $50$~g & --- & --- & $11.46$ / $6.46$ & $5.35$ / $1.63$ \\
Open-loop, model-based, $50$~g & --- & --- & $27.10$ / $28.46$ & $20.64$ / $11.22$ \\
\bottomrule
\end{tabular}
\end{table*}
```
(Header radii/heights are radius and height of each trajectory. The notebooks use the circle fitted to each file's own target vertices; the fitted radii differ by a few mm from the nominal ones, e.g. 31.4 vs 35 mm for one single-section run: say "fitted" in the caption if the reviewer asks.)

### Letter
```latex
\begin{point}[Figs.~6, 9, 10: trajectory details and path errors]\label{c:26}
For Figs. 6, 9, and 10, identify the start direction, waypoint order, number of completed cycles, and whether the plotted paths are one run or an average. Add quantitative path errors in the caption or an accompanying table.
\end{point}
\begin{reply}
We thank the reviewer. The captions now state that every plotted path is the record of a single run of one lap, that it starts on the positive horizontal axis of the base frame, and that the waypoints are followed in counter-clockwise order seen from above. The root-mean-square radial and height path errors of every controller and trajectory, including the payload experiment, are reported in a new table in the Supporting Information.
\end{reply}
```

---
## Comment 27: demonstrated capabilities vs proposed applications

### Edit 1 (Conclusion "What this sensing strategy can do" paragraph; replace the whole paragraph)
Find: the paragraph starting "This sensing and control framework endows soft robots with accurate motion capabilities." through "...while maintaining the desired tip pose." (if you applied the Comment 1 variant of the last sentence, replace that too).
Replace:
```latex
This sensing and control framework provides accurate quasi-static pose regulation of soft arms, as demonstrated here. Applications such as search-and-rescue, inspection in confined environments, and minimally invasive surgery, as well as using full-body curvature feedback for null-space obstacle avoidance or whole-body grasping, and force or contact sensing, are proposed directions and were not evaluated in this work.
```

### Edit 2 (limitations, same section; "suitable for applications such as inspection or surgical guidance")
Find: `suitable for applications such as inspection or surgical guidance;`
Replace: `which may suit applications such as inspection or surgical guidance, not evaluated here;`

### C27-E1 (limitations sentence referenced by Comments 6, 7 and 8; add at the end of the "Limitations and future work" paragraph)
```latex
The control evaluation is limited to a single execution of each target and trajectory, two planar circular trajectories with a fixed orientation, and a single constant tip payload, and the training and evaluation data were drawn from the same acquisition sessions; repeated trials, workspace-boundary and non-planar trajectories, several loads, a hardware ablation of the secondary objective, and evaluation on session-blocked data are left for future work.
```

### Letter
```latex
\begin{point}[Discussion: demonstrated vs.\ proposed]\label{c:27}
The discussion should distinguish demonstrated capabilities from proposed applications. Obstacle avoidance, whole-body grasping, surgical guidance, and force or contact sensing are future directions and were not evaluated here.
\end{point}
\begin{reply}
We thank the reviewer and agree. The discussion now separates what was demonstrated, accurate quasi-static pose regulation, from the proposed applications, search-and-rescue, inspection, surgery, obstacle avoidance, whole-body grasping, and force or contact sensing, which are stated to be future directions that were not evaluated. We also added the limitations of the evaluation, namely single executions, planar trajectories, one payload, and data from the same acquisition sessions.
\end{reply}
```
