# AIS 3400076 — Comment 9: "Provide the missing reproducibility details" (draft; hardware cells use the user's answers: commercial USB camera, standard tendon cable, several sessions)

Local-only (git-excluded). Rules: reply = one plain block, no numbers, no bold.
Everything below marked "code" was read from the notebooks/scripts in this repo (the version saved here: confirm the shipped models were trained with it).

## Corrections the code forces on the text
- Main text says Huber loss was used for all regressors; the notebooks use MSE for the single-section pose and curvature networks, the single-section kinematics MLP and N_C, and Huber (delta = 1) for the multi-section pose/curvature CNNs and the FK/IK MLPs.
- SI says "all angular quantities reparameterized using sine and cosine": in the code the networks regress angles directly; sine and cosine appear only inside the loss (curvature phi for the single-section arm; yaw/pitch/roll for the multi-section arm). The single-section pose network standardizes yaw/pitch/roll like the other outputs, with no sin/cos. See Comment 16 file.
- Seeds: none fixed for splitting or training; control scripts use seed 42.

## Manuscript edits

### E1. Network Training paragraph (main text)
Find:
```latex
We employed Huber loss ($\mathcal{L}$) to train all regressors to compensate for ground-truth noise and outliers~\cite{meyerAlternativeProbabilisticInterpretation2021}.
```
Replace (confirmed: the single-section networks were trained with the mean squared error):
```latex
We employed the Huber loss ($\mathcal{L}$) for the multi-section networks, to compensate for ground-truth noise and outliers~\cite{meyerAlternativeProbabilisticInterpretation2021}, and the mean squared error for the single-section networks. All settings needed for reproduction are listed in the Supporting Information.
```

### E2. Augmentation sentence (main text, same paragraph)
Find:
```latex
to account for residual variations through the diffusive skin.
```
Replace:
```latex
to account for residual variations through the diffusive skin; robustness to such variations was not tested experimentally.
```

### E3. Conclusion, lighting claim
Find:
```latex
and variability is mitigated through image augmentations during training.
```
Replace:
```latex
and variability was addressed only through image augmentations during training; robustness to lighting and hardware variation was not tested.
```

### E4. SI: new subsection "Reproducibility Settings" with one table (place after "Dataset Composition")
```latex
\subsection{Reproducibility Settings}
Table~\ref{tab:repro} lists the settings needed to reproduce the results.

\begin{table*}[ht]
\centering
\caption{Reproducibility settings. Entries marked $^\dagger$ were read from the released code.}
\label{tab:repro}
\renewcommand{\arraystretch}{1.25}
\footnotesize
\begin{tabular}{p{3.6cm}p{6.2cm}p{6.2cm}}
\toprule
 & \textbf{Single-section} & \textbf{Multi-section} \\
\midrule
\multicolumn{3}{l}{\textit{Hardware and acquisition}} \\
Cameras & commercial off-the-shelf USB camera & three cameras of the same type \\
Image format$^\dagger$ & $480\times640$ grayscale (converted from color) & $480\times640$ grayscale, three stacked channels \\
Exposure and gain$^\dagger$ & camera defaults (not set in software) & camera defaults (not set in software) \\
Capture$^\dagger$ & software capture, no hardware trigger & independent free-running capture threads, no hardware trigger \\
Motors$^\dagger$ & Dynamixel servo motors, 6~mm pulley, 4096 ticks per revolution, extended position control & same \\
Tendons & standard tendon cable; preload as in Section~\ref{sec:setup} & standard tendon cable \\
Current limit$^\dagger$ & motor default (not set in software) & motor default (not set in software) \\
Acquisition sessions & several sessions, same hardware & several sessions, same hardware \\
Samples$^\dagger$ & $10{,}000$ & $10{,}000$ \\
Sampled tendon displacement$^\dagger$ [mm] & uniform in $[-45, 10]$ per tendon & uniform per section: I $[-25, 10]$, II $[-35, 10]$, III $[-40, 10]$ \\
\midrule
\multicolumn{3}{l}{\textit{Pose and curvature networks}} \\
Backbone$^\dagger$ & MobileNetV2, ImageNet-pretrained, first convolution replaced by a one-channel convolution & MobileNetV2 features, ImageNet-pretrained, native three-channel input \\
Head$^\dagger$ & linear layer to 6 (pose) or 5 / 4 / 3 (quadratic / affine / constant curvature) & linear $1280\to512$, LeakyReLU, linear to 18 (pose) or 15 / 12 / 9 (curvature) \\
Augmentation$^\dagger$ & blur, Gaussian noise (std up to 30 gray levels), brightness and contrast jitter ($\pm40\%$), brightness shift, vignette, cutout; training only & same \\
Loss$^\dagger$ & mean squared error on standardized targets; $\sin\phi,\cos\phi$ for the curvature angle & Huber ($\delta=1$) on standardized positions and $\sin,\cos$ of the angles \\
Angular output & angles regressed directly in radians; no decoding step & same \\
Normalization & targets standardized with the training-set mean and standard deviation, embedded in the released models & same \\
Optimizer$^\dagger$ & Adam, learning rate $10^{-3}$, weight decay $5\cdot10^{-6}$, linear warm-up over 10 iterations & same \\
Schedule$^\dagger$ & plateau scheduler (factor 0.5, patience 5), early stopping (patience 30), at most 500 epochs, batch 16, gradient accumulation & plateau factor 0.6, patience 5, otherwise same \\
Seeds & none fixed for splitting and training & same \\
\midrule
\multicolumn{3}{l}{\textit{Auxiliary networks}} \\
$N_C$ ($p, l \mapsto C$)$^\dagger$ & MLP $9\to128$, three residual blocks of width 128 (batch normalization, LeakyReLU), output 5 / 4 / 3; MSE; Adam, weight decay $10^{-5}$; early stopping; trained on single-section data only & --- \\
Forward network $N_p^3$$^\dagger$ & --- & same MLP, $9\to6$, Huber, Adam ($10^{-3}$, $5\cdot10^{-6}$), plateau factor 0.9, patience 5 \\
Inverse network $N_l^1$, $N_l^3$$^\dagger$ & MLP $3\to128$, three residual blocks, $128\to64\to32\to3$; MSE; weight decay $10^{-5}$ & MLP $6\to9$; loss: Huber error of the frozen $N_p^3$ plus $\zeta\|\bar{l}-N_l^3(p)\|_2^2$, $\zeta=0.01$; plateau factor 0.9, patience 15 \\
\midrule
\multicolumn{3}{l}{\textit{Control}} \\
Parameters$^\dagger$ & damping $\lambda=0.1$, waypoint spacing 1~mm, convergence threshold 3~mm & same damping and spacing, convergence threshold 10 (position in mm plus orientation in degrees divided by 5) \\
Target selection$^\dagger$ & 20 k-medoids targets (random state 42) & same \\
\bottomrule
\end{tabular}
\end{table*}
```
(Single-section kinematics MLP and N_C weight decay are 1e-5 in the notebooks; FK weight decay is 5e-6. The IK optimizer line was not printed, so it is assumed to match the FK settings. The k-medoids random state 42 is from `MULTI_try_motion.py`.)

## Letter block
```latex
\begin{point}[Provide the missing reproducibility details]\label{c:9}
The paper needs to include enough information to enable reproduction of the results. The methods omit several parameters that affect performance: camera model, lens and field of view, exposure and gain behavior, maximum epochs, random seeds, output normalization statistics, angular decoding, and the training details for N_C, N_p3, and N_l3. Additionally, robot design details are also incomplete, including tendon material and diameter, preload/zeroing criterion, current limit, sampled tendon ranges, and the number of acquisition sessions. The SI is a good place for a single reproducibility table containing these settings.

Claims of robustness to lighting or hardware variation should be limited unless such variation was explicitly tested.
\end{point}
\begin{reply}
We thank the reviewer for this comment and added a single reproducibility table to the Supporting Information, as suggested. It lists the cameras, image format, capture method, motors, tendons, preload and current limit, the number of acquisition sessions, the sampled tendon ranges, the architecture, augmentation, loss, optimizer, schedule, early stopping and maximum epochs of every network, including the surrogate and the forward and inverse kinematic networks, the normalization of the outputs, the handling of angles, and the seeds. In preparing it we also corrected the main text, which stated that the Huber loss was used for all regressors: the single-section networks were trained with the mean squared error. The networks regress angles directly, so no decoding step is needed, and the sine and cosine of the angles enter only the loss. No random seed was fixed for splitting and training, which we state. The claims about lighting and hardware variation have been limited: these variations were addressed only through data augmentation and were not tested.
\end{reply}
```
