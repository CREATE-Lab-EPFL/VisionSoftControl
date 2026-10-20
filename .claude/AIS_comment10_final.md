# AIS 3400076 — Comment 10: "Revise the figures and captions" (NO figure is redrawn; the figures are complemented by captions and one SI table)

Local-only (git-excluded). Rules: short edits, reply = one plain block, no numbers, no bold.
Comments 22 (Fig. 5b) and 23 (Fig. 7) are in `AIS_comments21-27.md`; the regenerated Figs. S4-S6 (Comment 30) are optional copies in `.claude/AIS_figures/` and need no drawing work from you.

## What the figures show (checked on the rendered figures)
- Fig. 3a shows the MobileNetV2 pipeline with no tensor sizes; its left "Transfer Learning" arrow runs from the one-image to the three-image input; panel b shows the MLP blocks without inputs or outputs.
- Fig. 2 shows the four boundary arcs L1 to L4 as unexplained colored dashes (L1 green, L2 blue, L3 yellow, L4 red) and uses x for two different axes.
- Fig. 5c uses CL / OL without definition (fixed in Comment 22).

## Edit 1: Fig. 3 caption (replace the last sentence of (a) and the first of (b); the transfer sentence is already rewritten in Comment 3, E6)
Find: `This representation is used to predict tip poses (6 outputs for the single-section, 18 for the multi-section) or curvature parameters for each section, using dedicated networks for different approximations.`
Replace:
```latex
This representation is used to predict tip poses (6 outputs for the single-section arm, 18 for the multi-section arm, one 6-vector per section tip) or curvature parameters (5, 4 or 3 outputs per section for the quadratic, affine and constant models, that is 15, 12 or 9 for three sections), using dedicated networks for each. The inputs, outputs and role of every network, including the kinematic networks of (b) and the curvature surrogate $N_C$, are listed in the network table of the Supporting Information.
```
Find: `(b) Multi-layer perceptron (MLP) architecture used for kinematics approximations.`
Replace: `(b) Multi-layer perceptron (MLP) architecture shared by the kinematic networks $N_l^1$, $N_p^3$, $N_l^3$ and the curvature surrogate $N_C$ (input and output dimensions in the network table of the Supporting Information).`

## Edit 2: Fig. 2 caption (append)
```latex
 The colored dashed lines mark the four boundary arcs $L_1$ (green), $L_2$ (blue), $L_3$ (yellow), and $L_4$ (red).
```

## Edit 3: SI, new table (place at the start of "Deep Learning Architecture Details")
```latex
\begin{table*}[ht]
\centering
\caption{Networks used in this work with their inputs, outputs, and role. Numbers in parentheses are dimensions.}
\label{tab:networks}
\renewcommand{\arraystretch}{1.25}
\footnotesize
\begin{tabular}{p{1.3cm}p{3.6cm}p{4.2cm}p{1.9cm}p{4.2cm}}
\toprule
\textbf{Network} & \textbf{Input} & \textbf{Output} & \textbf{Arm} & \textbf{Role} \\
\midrule
$f_p^1$ & image $480\times640\times1$ & tip pose (6) & single & pose feedback for control \\
$f_C^1$ & image $480\times640\times1$ & curvature parameters (5, 4, or 3 for the quadratic, affine, or constant model) & single & separate sensing capability; not used in control \\
$f_p^3$ & three stacked images $480\times640\times3$ & three tip poses (18) & multi & pose feedback for control \\
$f_C^3$ & three stacked images $480\times640\times3$ & curvature parameters of three sections (15, 12, or 9) & multi & separate sensing capability; not used in control \\
$N_l^1$ & tip position (3) & tendon lengths (3) & single & learned inverse kinematics of the data-driven controller \\
$N_p^3$ & tendon lengths (9) & tip pose (6) & multi & learned forward kinematics; open-loop state update and training of $N_l^3$ \\
$N_l^3$ & tip pose (6) & tendon lengths (9) & multi & learned inverse kinematics with the secondary term, data-driven controller \\
$N_C$ & tip pose (6) and tendon lengths (3) of a module & curvature parameters (5, 4, or 3) & trained on single-section data, applied to each module & generates the multi-section curvature labels; not used in control \\
\bottomrule
\end{tabular}
\end{table*}
```
(Dimensions are from the notebooks: pose heads 6 and 18, curvature heads 5/4/3 and 15/12/9, kinematic MLPs 3 to 3, 9 to 6, 6 to 9, N_C input 9 = 6 + 3.)

## Letter block
```latex
\begin{point}[Revise the figures and captions]\label{c:10}
Several figures---particularly Figs. 1B, 2, 3, and 5---are difficult to interpret. Their visual density and inconsistent presentation make it hard to follow the methodology and compare results.

In particular, Figure 3 requires attention. Although the MobileNetV2 backbone and inverted residual block are depicted, the overall relationship among the pose, curvature, forward-kinematics, and inverse-kinematics networks is hard to reconstruct. The MLP inputs and outputs are not identified, and tensor dimensions and network-specific outputs are unclear. The paper should use a consistent flow direction, label all network inputs and outputs, and distinguish clearly between the networks used for pose estimation, curvature reconstruction, forward kinematics, and inverse kinematics.
\end{point}
\begin{reply}
We thank the reviewer. Rather than redrawing the figures, we complemented them where the information was missing. A new table in the Supporting Information lists every network, the pose, curvature, forward-kinematics and inverse-kinematics networks and the curvature surrogate, with its input and output dimensions, the arm it belongs to and its role, including whether it enters the control loop, and the caption of the network figure now gives the output dimensions and points to this table. The caption of the network figure also corrects how the networks are initialized and explains the transfer-learning arrow, and the caption of the geometry figure now identifies the four boundary arcs. The abbreviations and the axis scaling of the reconstruction figure are explained in its caption, and the statistic plotted in the error figure is now defined exactly. We also corrected figure captions where the text and the figures disagreed. We kept the layouts of the figures, and we regenerated the supporting control-error figures with matched color scales and target identifiers.
\end{reply}
```
