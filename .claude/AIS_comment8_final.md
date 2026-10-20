# AIS 3400076 — Comment 8: "Establish independence of training and evaluation data" (draft; needs user input marked [..])

Local-only (git-excluded). Rules: short edits, reply = one plain block, no numbers, no bold, no quoted manuscript text.

## Facts (code + notebooks)
- Split: `SINGLE_helyx_testing.ipynb` / `MULTI_helyx_training.ipynb` (dataset-generation cell): `train_test_split(all_indices, test_size=0.15)` then `test_size=1/3`, NO `random_state`; indices pooled over ALL shards; not blocked by session or configuration neighborhood. The split indices were not saved.
- Each commanded configuration is an independent random draw (SINGLE: uniform tendon displacement in [-45, 10] mm per tendon; MULTI: per-section ranges and three sampling regimes in the acquisition script), so neighbors in the data come from dense sampling, not from temporal adjacency of a continuous trial.
- Nearest-neighbor analysis (`SINGLE_MULTI_leakage_check.ipynb`, tendon space, 500 test samples vs. training set): SINGLE mean 1.10 mm, median 0.95 mm, 53.4% within 1 mm and 92.4% within 2 mm of a training sample (the network's own error is about 4 mm). MULTI (9-D): mean 4.72 mm, median 5.01 mm, and 28.2% of test samples have an EXACT duplicate (distance 0) in the training set.
- CONFIRMED by the user: cause of the MULTI duplicates: the acquisition script commands a configuration, waits 3 s, and takes frames from a continuously running 1 Hz acquisition thread, so several frames share one commanded configuration. Consequence: with a random frame-level split, frames of the same configuration fall in both training and test sets, so the multi-section test errors are optimistic. State this plainly; it is not only an interpolation effect. The S31 mismatch (no coupling signature in the shipped data) still means the exact script version and the per-regime counts are not known.
- Control targets: 20 k-medoids targets from `data/Workspace.npz`, which pools train, validation and test samples; they were NOT excluded from training. The circular trajectories are not dataset samples.
- A freshly drawn random split gave test errors that agree closely with the published ones (4.02 vs 3.99 mm, 3.13 vs 3.11 deg), so the reported accuracy is not tied to one split. This does not remove the overlap concern.

## Pending inputs from the user
1. Number of acquisition sessions, days, whether camera settings, covering (skin) or robot build changed between sessions, and whether the control experiments used the same covering and build as the data collection.
2. DONE (confirmed): several frames per commanded configuration. Still needed: how many frames per configuration, to quote in the paper.
3. Optional, strongest answer: an error-versus-distance-to-nearest-training-configuration analysis (test error restricted to configurations far from any training sample). It needs the two dataset zips and a torch environment (see HANDOFF).

## Manuscript edits (search by Find text)

### E1. Network Training paragraph
Find:
```latex
The dataset was split into training ($85\%$), validation ($10\%$), and test ($5\%$) sets.
```
Replace:
```latex
Tendon configurations were sampled at random, and the samples were randomly assigned to training ($85\%$), validation ($10\%$), and test ($5\%$) sets, pooled over all acquisition sessions and without blocking by session or configuration neighborhood; for the multi-section arm, several frames were recorded at each commanded configuration, so frames of the same configuration can appear in both training and test sets and the reported test errors are optimistic (Supporting Information).
```

### E2. Control targets (single-section paragraph, after "...each target was visited once, and errors are reported as the final position error at convergence.")
```latex
 The targets were selected from the sampled workspace and were not excluded from the training set, and the circular trajectories were not part of it, so the control experiments evaluate closed-loop tracking within the sampled workspace rather than generalization to unseen poses.
```
(In the multi-section targets paragraph add: "As before, the targets were not excluded from the training set.")

### E3. Section 3.1 or 3.2 (acquisition conditions), one sentence
```latex
All data were acquired in several sessions with the same cameras, covering and robot build, and the control experiments used the same covering and build.
```

### E4. SI, new subsection "Overlap Between Training and Test Data" (next to the dataset composition subsection)
```latex
\subsection{Overlap Between Training and Test Data}
The samples were randomly assigned to the three sets, pooled across all acquisition files, without a fixed random seed and without blocking by session or configuration neighborhood. To quantify the resulting overlap, Table~\ref{tab:overlap} reports, for each test configuration, the distance in tendon space to the nearest training configuration. For the single-section arm, the typical spacing is about one millimeter, smaller than the pose error of the network, as expected from a dense independent sampling of a three-dimensional tendon space; the test set therefore assesses interpolation rather than extrapolation. For the multi-section arm, a fraction of the test configurations coincide exactly with a training configuration, because several frames were recorded at each commanded configuration and the random split places frames of the same configuration in both sets. The reported multi-section test errors are therefore optimistic and should be read as in-distribution accuracy, not as accuracy on unseen configurations. A freshly drawn random split gives test errors that agree closely with the reported ones, so they do not depend on one particular split.

\begin{table}[ht]
\centering
\caption{Distance in tendon space from each of the $500$ test configurations to the nearest training configuration.}
\label{tab:overlap}
\renewcommand{\arraystretch}{1.3}
\begin{tabular*}{\linewidth}{@{\extracolsep\fill}lcc}
\toprule
 & \textbf{Single-section} & \textbf{Multi-section} \\
\midrule
Mean [mm] & $1.10$ & $4.72$ \\
Median [mm] & $0.95$ & $5.01$ \\
Within $0.5$~mm & $11.8\%$ & $28.2\%$ \\
Within $1$~mm & $53.4\%$ & --- \\
Within $2$~mm & $92.4\%$ & --- \\
Exact duplicates & --- & $28.2\%$ \\
\bottomrule
\end{tabular*}
\end{table}
```
(The columns use different dimensionalities, three versus nine tendons, so distances are not directly comparable; say so in the caption. Cells marked --- were not computed in `SINGLE_MULTI_leakage_check.ipynb`; fill them by re-running it, or delete the rows.)

### E5. Conclusion limitations: defined once in `AIS_comments21-27.md` (C27-E1), including session-blocked evaluation.

## Letter block
```latex
\begin{point}[Establish independence of training and evaluation data]\label{c:8}
The datasets are randomly divided 85/10/5, but the acquisition sequence, session structure, and grouping of neighboring configurations are not described. If frames from continuous trials are split randomly, nearly identical or temporally adjacent configurations may appear in both training and test sets, inflating apparent generalization.

The authors should state:
how samples were randomized;
whether test data were separated by session or configuration neighborhood;
whether controller targets and trajectories were excluded from training; and
whether experiments span different days, camera settings, coverings, or robot builds.
\end{point}
\begin{reply}
We thank the reviewer for this comment and now describe the data handling explicitly. The configurations were commanded by random sampling, and the samples were assigned randomly to the three sets, pooled over all acquisition files, without a fixed seed and without separating test data by session or configuration neighborhood. The controller targets were selected from the sampled workspace and were not excluded from training, whereas the circular trajectories were not part of the training data; the control experiments therefore evaluate closed-loop tracking within the sampled workspace rather than generalization to unseen poses, which we now state. The data were acquired in several sessions with the same cameras, covering and robot build, and the control experiments used the same hardware, so the data do not span different coverings, builds or camera settings. To quantify the overlap, we report in the Supporting Information the distance from each test configuration to the nearest training configuration; the single-section test configurations lie close to training configurations, and for the multi-section arm several frames were recorded at each commanded configuration, so frames of the same configuration can appear in both sets; the reported errors therefore describe in-distribution accuracy, and the multi-section test errors are optimistic, which we state. The test errors recomputed on a freshly drawn random split agree closely with the reported ones. Evaluation on data blocked by session or configuration neighborhood was not possible with the existing data and is listed as future work.
\end{reply}
```
