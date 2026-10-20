# AIS 3400076 — Comment 6: "Quantitatively evaluate the secondary objective" (draft)

Local-only (git-excluded). Rules: short edits, reply = one plain block, no numbers, no bold.

## What exists (from `MULTI/MULTI_nullspace_ablation.ipynb`, results in `MULTI/results/NullSpaceAblation.npz`)
- OFFLINE replay of the model-based resolved-motion-rate law on the PCC forward model over the same 20 real targets, with and without the null-space term. SIMULATED, not hardware; the replay differs from the hardware runs by 27.6 mm on average in final position (idealized: no camera noise, cable stretch, compliance), so only the relative comparison is meaningful.
- With vs without null-space term: H(l) 269 +- 135 vs 693 +- 396; RMS tendon deviation 7.48 +- 1.96 mm vs 12.00 +- 3.18 mm; final position error 5.25 +- 2.23 mm vs 5.84 +- 1.85 mm; converged targets 18/20 vs 20/20 (two targets stopped just above the threshold, orientation residuals near gimbal lock of the Euler stopping metric).
- NOT done: data-driven controller without the secondary term (needs a retrained inverse network and hardware runs); real tendon distributions from hardware (the logged `ControlWorkspace*.npz` hold only targets and mocap poses, no tendon lengths). Motor current/energy was not measured, so no effort claim is made.

## Manuscript edits (search by Find text)

### E1. Section 3.3.2, description of H(l)
Find:
```latex
Reducing the deviation from mid-range values keeps the manipulator away from its physical limits, preserving flexibility for future tasks, and promotes smooth, coordinated joint motions by distributing control effort evenly across the tendons.
```
Replace:
```latex
This is an actuator-range-centering objective: it keeps the tendons away from their limits, preserving flexibility for future tasks, and it does not directly minimize force, motor current, or energy.
```

### E2. Introduction, "Research problem and hypothesis" paragraph (sentence edited for Comment 1)
Find:
```latex
enabling tip regulation while reducing actuation effort;
```
Replace:
```latex
enabling tip regulation while keeping the tendons close to mid-range;
```

### E3. Abstract and `\transabstract` (last sentence; also covers Comment 7)
Find:
```latex
Experiments demonstrate that embedded vision enables accurate full-body state reconstruction, reliable redundancy resolution, and robust regulation even under external disturbances.
```
Replace:
```latex
Experiments demonstrate that embedded vision enables accurate state reconstruction, redundancy resolution that keeps the tendons close to mid-range, and accurate regulation, including under a constant tip payload.
```

### E4. Conclusion, wording of the secondary objective
Find:
```latex
In this paper, redundancy was exploited to balance tendon effort,
```
Replace:
```latex
In this paper, redundancy was exploited to keep the tendons close to mid-range,
```
(If the sentence breaks differently in Overleaf, search for "balance tendon effort".)

### E5. Section 4.2.4 (multi-section target control), add one sentence at the end of the paragraph
Find:
```latex
though with superior orientation tracking and lower variance than the model-based open-loop controller.
```
Replace:
```latex
though with superior orientation tracking and lower variance than the model-based open-loop controller. An offline replay of the model-based law on the PCC forward model over the same targets (simulated, not measured on hardware) shows that the null-space term reduces the RMS deviation of the tendons from $\bar{l}$ from $12.0 \pm 3.2$ to $7.5 \pm 2.0$~mm at comparable final position error (Supporting Information).
```

### E6. SI, new subsection (place after the control-workspace subsections)
```latex
\subsection{Null-Space Ablation}
To isolate the effect of the secondary objective, the model-based control law was replayed offline on the PCC forward model over the same twenty targets, with and without the null-space term. This replay is simulated, not measured on hardware: it omits camera noise, cable stretch, and compliance, and differs from the hardware runs by $27.6$~mm in final position on average, so only the relative comparison is meaningful. Table~\ref{tab:nullspace_ablation} reports the secondary-task metrics, the value of $H(l)$ and the RMS deviation of the tendons from $\bar{l}$, together with the primary-task error. With the null-space term, two targets stopped just above the convergence threshold, owing to orientation residuals close to gimbal lock of the Euler representation used in the stopping metric. For the data-driven controller, the secondary objective enters through the training loss; a network trained without it was not available, so its effect is not isolated here.

\begin{table}[ht]
\centering
\caption{Offline null-space ablation of the model-based controller over the twenty control targets (mean $\pm$ standard deviation across targets; simulated).}
\label{tab:nullspace_ablation}
\renewcommand{\arraystretch}{1.3}
\begin{tabular*}{\linewidth}{@{\extracolsep\fill}lcc}
\toprule
 & \textbf{With null space} & \textbf{Without null space} \\
\midrule
$H(l)$ [mm$^2$] & $269 \pm 135$ & $693 \pm 396$ \\
RMS tendon deviation [mm] & $7.48 \pm 1.96$ & $12.00 \pm 3.18$ \\
Final position error [mm] & $5.25 \pm 2.23$ & $5.84 \pm 1.85$ \\
Converged targets & 18 of 20 & 20 of 20 \\
\bottomrule
\end{tabular*}
\end{table}
```

### E7. Conclusion future work (hardware ablation, repeated trials, ...)
Defined once in `AIS_comments21-27.md`, edit C27-E1. Do not add a second sentence here.

## Letter block

```latex
\begin{point}[Quantitatively evaluate the secondary objective]\label{c:6}
The control contribution is framed as redundancy-aware null-space control, but the manuscript reports no quantitative experimental results isolating the effect of the secondary objective. No reported experiment shows the objective $H(l)$, tendon-limit margins, tendon distributions, or configurations obtained with and without the secondary objective. Furthermore, $H(l)$ penalizes displacement from the mean sampled tendon vector. It does not directly minimize tendon force, motor current, energy, or control effort. The objective should therefore might described as actuator-range centering unless effort is measured.

For both controllers, an ablation with the secondary objective disabled using identical targets would be helpful. Results should report both primary-task error and a quantitative secondary-task metric. A useful experiment could compare multiple configurations reaching the same tip pose and show the resulting tendon margins or values of $H(l)$.
\end{point}
\begin{reply}
We thank the reviewer for this comment and agree that the secondary objective needs quantitative support and a more precise description. We now describe it as actuator-range centering: it penalizes the deviation of the tendon lengths from their mean sampled values, and we no longer claim that it minimizes force, current or energy, which were not measured. To isolate its effect, we replayed the model-based control law offline on the forward model over the same targets with and without the null-space term, and report the primary-task error together with the secondary-task metrics, the value of the objective and the RMS deviation of the tendons from their mean, in the Supporting Information, clearly labeled as simulated rather than measured on hardware. The null-space term markedly reduces the tendon deviation at comparable position error. For the data-driven controller the secondary objective enters through the training loss, and a network trained without it would require new training and hardware evaluation, which we did not perform; we state this in the Supporting Information and list a hardware ablation as future work.
\end{reply}
```
