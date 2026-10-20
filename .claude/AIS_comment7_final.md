# AIS 3400076 — Comment 7: "Expand and better characterize the control evaluation" (draft)

Local-only (git-excluded). Rules: short edits, reply = one plain block, no numbers, no bold. No new hardware experiments: claims are narrowed and coverage is quantified from logged data.

## Data (from `SINGLE/SINGLE_workspace_coverage.ipynb`, `MULTI/MULTI_workspace_coverage.ipynb`, `results/ControlWorkspace*.npz`)
- The manuscript says training data cover "bending angles up to 85 deg". The shipped single-section data give max 56.8 deg (mean 19.3, p95 35.6, N=10000) by three independent methods; the user confirmed 85 deg "was more of an assumption", so the data win.
- Single-section: control targets mean 20.2 / max 33.7 deg; tracked trajectories mean 24.7 / max 40.9 deg, i.e. about 59% and 72% of the trained maximum.
- Multi-section, per section (I / II / III): training p95 29.7 / 31.7 / 34.0 deg (the polynomial-fit max is unreliable for sections II and III, degenerate fits up to 136 to 178 deg); targets max 23.1 / 43.4 / 25.5; trajectories max 29.0 / 27.0 / 57.4. Target bending angles are from the PCC-consistent tendon configurations of the targets (model-based, not measured).
- Target z (single): 120.8 to 135.8 mm for a 150 mm rest length (compression about 14 to 29 mm).
- Each target and trajectory was run once (`ControlWorkspace*.npz`, `PolygonWS_*`/`Polygon*`), so no repeatability data exist.

NOTE: the reviewer estimates single-section bending under about 17 deg and three-section under about 19 deg. From the logged poses, the single-section targets reach 34 deg (trajectories 41 deg) and the multi-section targets 23, 43 and 26 deg per section; the reviewer's figures are probably read from the plots. The reply does not dispute them.

## Manuscript edits (search by Find text)

### E1. Section 3.2 (Workspace Sampling), corrected training range
Find:
```latex
covering bending angles up to $85^\circ$ per section.
```
Replace:
```latex
covering bending angles up to $57^\circ$ for the single-section arm and up to about $34^\circ$ per section (95th percentile) for the multi-section arm.
```

### E2. Section 4.1.4 (single-section targets): after the sentence "...each target was visited once, and errors are reported as the final position error at convergence." add
```latex
 The targets reach bending angles up to $34^\circ$ and the trajectories up to $41^\circ$, about $60\%$ and $70\%$ of the trained range, and the reported standard deviations describe variation across targets, not trial-to-trial repeatability.
```

### E3. Section 4.2.4 (multi-section targets): after "The same $k$-medoids algorithm used for the single-section arm defined $20$ target poses." add
```latex
 The targets reach up to $23^\circ$, $43^\circ$, and $26^\circ$ in sections I to III, comparable to the trained 95th percentiles, and, as before, each target was visited once, so the standard deviations describe variation across targets rather than repeatability.
```

### E4. Trajectories (single-section paragraph "Two circular trajectories ..." and multi-section paragraph "Two circular trajectories with horizontal end-effector orientation ..."): append to each
```latex
 Each trajectory was executed once, and its waypoints are serially correlated, so the reported errors do not establish repeatability.
```
(Put it once, in the single-section paragraph, and write "As before, ..." in the multi-section paragraph if you want it shorter.)

### E5. Section 4.2.6 (payload): reframe
Find:
```latex
serving as a proxy for evaluating closed-loop robustness under persistent external interactions.
```
Replace:
```latex
as a single-condition demonstration of closed-loop compensation for a constant off-center load, not of general robustness to disturbances or contact.
```

### E6. Conclusion, robustness wording
Find:
```latex
while being robust to external disturbances.
```
Replace:
```latex
including under a constant tip payload.
```
(The sentence becomes: "Closed-loop control achieves near-sensing performance and outperforms open-loop alternatives, including under a constant tip payload." Make sure the preceding "and" is removed or the comma kept consistent.)

### E7. Abstract: done in `AIS_comment6_final.md`, E3 (the last sentence).

### E8. Conclusion future work (repeated trials, non-planar and boundary trajectories, several loads, ...): defined once in `AIS_comments21-27.md`, edit C27-E1.

### E9. SI, new subsection "Control Evaluation Coverage" (after "Control Workspace Definition")
```latex
\subsection{Coverage of the Control Evaluation}
Table~\ref{tab:coverage} compares the bending angles of the control targets and trajectories with those of the training data, and Tables~\ref{tab:targets_single} and~\ref{tab:targets_multi} list the target coordinates. For the multi-section arm, the bending angles of the targets are those of the corresponding PCC-consistent tendon configurations, and the trained range is summarized by the 95th percentile because polynomial fits of sections II and III occasionally degenerate.

\begin{table}[ht]
\centering
\caption{Bending angle [$^\circ$] of the training data, control targets, and tracked trajectories.}
\label{tab:coverage}
\renewcommand{\arraystretch}{1.3}
\begin{tabular*}{\linewidth}{@{\extracolsep\fill}lcccc}
\toprule
 & \textbf{Training (max / p95)} & \textbf{Targets (max)} & \textbf{Trajectories (max)} \\
\midrule
Single-section & 56.8 / 35.6 & 33.7 & 40.9 \\
Multi-section, I & -- / 29.7 & 23.1 & 29.0 \\
Multi-section, II & -- / 31.7 & 43.4 & 27.0 \\
Multi-section, III & -- / 34.0 & 25.5 & 57.4 \\
\bottomrule
\end{tabular*}
\end{table}

\begin{table}[ht]
\centering
\caption{Single-section control targets (tip position in the base frame, mm).}
\label{tab:targets_single}
\renewcommand{\arraystretch}{1.1}
\begin{tabular*}{\linewidth}{@{\extracolsep\fill}cccc}
\toprule
\textbf{ID} & $x$ & $y$ & $z$ \\
\midrule
1 & -19.8 & -25.4 & 122.6 \\
2 & -10.2 & -16.0 & 129.0 \\
3 & -7.3 & 32.8 & 121.8 \\
4 & -0.7 & -8.2 & 133.9 \\
5 & -1.1 & 18.3 & 128.2 \\
6 & 22.4 & 2.6 & 128.7 \\
7 & -24.8 & 5.9 & 123.2 \\
8 & 26.6 & -10.3 & 120.8 \\
9 & 12.8 & 14.2 & 125.8 \\
10 & -0.8 & -25.5 & 123.3 \\
11 & 27.7 & 18.1 & 120.8 \\
12 & 11.9 & -6.7 & 129.6 \\
13 & 13.6 & 28.8 & 122.8 \\
14 & 11.6 & -19.6 & 121.9 \\
15 & 5.6 & 6.5 & 135.8 \\
16 & 36.7 & 5.2 & 121.9 \\
17 & 2.4 & 2.0 & 122.8 \\
18 & -22.5 & -8.6 & 121.1 \\
19 & -19.6 & 19.5 & 122.6 \\
20 & -10.0 & 6.0 & 127.9 \\
\bottomrule
\end{tabular*}
\end{table}

\begin{table*}[ht]
\centering
\caption{Multi-section control targets: tip position [mm], orientation as yaw, pitch, roll [$^\circ$], and bending angle of sections I / II / III [$^\circ$].}
\label{tab:targets_multi}
\renewcommand{\arraystretch}{1.1}
\begin{tabular}{ccccccc c}
\toprule
\textbf{ID} & $x$ & $y$ & $z$ & yaw & pitch & roll & bending I / II / III \\
\midrule
1 & 81.7 & -167.2 & 307.9 & -15.2 & 21.4 & 62.5 & 13.3 / 30.9 / 25.5 \\
2 & -219.1 & 28.3 & 269.4 & 30.2 & -56.6 & 23.9 & 18.5 / 43.4 / 17.2 \\
3 & 128.9 & 103.2 & 331.5 & 13.5 & 25.0 & -37.0 & 14.2 / 25.0 / 15.8 \\
4 & 136.9 & 11.5 & 347.8 & -3.5 & 20.8 & 9.5 & 11.1 / 20.3 / 18.4 \\
5 & 4.4 & -123.1 & 352.7 & -0.5 & -1.6 & 39.0 & 5.5 / 21.3 / 20.7 \\
6 & 4.9 & -21.9 & 382.6 & 0.8 & 17.5 & 4.7 & 2.1 / 7.3 / 14.2 \\
7 & -71.9 & -71.9 & 366.2 & 6.1 & -33.9 & 26.4 & 5.5 / 17.3 / 14.9 \\
8 & -116.8 & -159.4 & 312.6 & 17.2 & -24.4 & 51.5 & 18.5 / 27.6 / 17.9 \\
9 & -67.9 & 140.8 & 344.0 & -5.8 & -20.6 & -47.3 & 14.7 / 22.8 / 0.7 \\
10 & 27.0 & 133.5 & 350.3 & 6.2 & 20.0 & -46.4 & 11.8 / 21.6 / 7.4 \\
11 & -140.1 & -17.0 & 351.8 & 4.8 & -38.3 & 10.5 & 11.4 / 21.6 / 11.0 \\
12 & -124.6 & 71.0 & 351.1 & 0.1 & -30.0 & -13.4 & 13.0 / 22.0 / 6.5 \\
13 & 80.8 & -56.4 & 359.1 & -9.6 & 36.7 & 30.5 & 4.1 / 19.0 / 22.0 \\
14 & -56.7 & 210.1 & 292.3 & -6.7 & -8.3 & -65.3 & 21.6 / 33.1 / 6.7 \\
15 & -179.2 & -65.9 & 308.5 & 9.1 & -55.9 & 19.3 & 14.9 / 34.3 / 17.8 \\
16 & 69.9 & 200.6 & 282.0 & 16.6 & 21.7 & -71.9 & 17.4 / 39.8 / 16.5 \\
17 & -67.9 & 7.1 & 379.3 & 4.4 & -11.3 & 8.7 & 5.8 / 12.3 / 9.0 \\
18 & -46.8 & 75.0 & 377.9 & 0.3 & -6.1 & -20.6 & 9.2 / 11.8 / 5.2 \\
19 & 52.3 & 48.1 & 376.4 & 2.9 & 2.0 & -8.1 & 7.1 / 8.6 / 11.0 \\
20 & -169.0 & 142.9 & 290.9 & -27.6 & -25.2 & -68.4 & 23.1 / 33.9 / 6.7 \\
\bottomrule
\end{tabular}
\end{table*}
```
(Orientation columns assume the stored values are radians in ZYX order and were converted to degrees; the largest stored magnitude is 1.25, below pi. CONFIRM the convention before submission. Compression is visible through the z column; the training z range was not recomputed because the dataset is not on this machine.)

## Letter block

```latex
\begin{point}[Expand and better characterize the control evaluation]\label{c:7}
The experimental evaluation does not quantify its coverage relative to the reachable workspace. The training datasets reportedly include bending angles up to 85$^\circ$ per section, and the multisection target plots span a substantial positional range. However The trajectory evaluation is narrow, and the target coverage is incompletely documented. Single-section bending angles are apparently under 17 deg, and three-section angles are under 19 deg, and overall length changes are also quite limited. The evaluation does not include workspace-boundary paths, nonplanar trajectories, large orientation changes, or trajectories requiring qualitatively different section configurations.

Figs.~S4--S6 plot the target positions and associated errors, but the coordinates are not tabulated and the targets are not compared with the complete reachable or sampled workspace. The authors should report the target coordinates, associated bending and compression ranges, and the fraction of the sampled workspace represented by the evaluation set.

Each of the 20 targets is visited only once. Consequently, the reported standard deviations describe variation across different targets, not trial-to-trial repeatability, and do not establish that one controller outperforms the other. The 30 waypoints in each trajectory are likewise serially correlated rather than independent trials.

The disturbance experiment should also be characterized more narrowly. A single 50 g off-center payload demonstrates compensation for one constant load (which is on ly moderately successful), not general robustness to disturbances or contact. Either additional load magnitudes and directions should be tested or the claims should be limited.
\end{point}
\begin{reply}
We thank the reviewer for this comment. We now report the coordinates of all control targets and the bending angles of the targets and trajectories relative to the trained range in the Supporting Information, computed from the logged poses, and we corrected the stated training range, which was overstated: the measured maximum bending angle of the single-section dataset is lower than previously written. We agree that each target and trajectory was executed once, so the reported standard deviations describe variation across targets and waypoints rather than repeatability and do not establish that one controller outperforms the other; this is now stated in the results, and repeated trials, non-planar and boundary trajectories, and several load magnitudes and directions are listed as future work. The payload experiment is now described as a single-condition demonstration of compensation for a constant off-center load, and the claims of robustness to disturbances in the abstract and the conclusion have been limited accordingly. No new hardware experiments were run for this revision.
\end{reply}
```
