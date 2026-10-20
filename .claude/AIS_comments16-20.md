# AIS 3400076 — Minor comments 16 to 20 (Pages 5-7) (draft)

Local-only (git-excluded). Rules: short edits, reply = one plain block, no numbers, no bold, no quoted manuscript text.

---
## Comment 16: angle decoding and loss balancing

Facts (notebooks): the networks regress angles directly in radians (no sin/cos output, so there is nothing to decode). Sine and cosine of angles are used only inside the loss, to avoid the wrap-around discontinuity: curvature phi (single-section curvature networks) and yaw/pitch/roll (multi-section pose network). The single-section pose network does NOT use sin/cos: its six outputs (position and yaw/pitch/roll) are all standardized and trained with MSE. Balancing: targets are standardized with training-set mean and standard deviation (positions, lengths, curvature coefficients); the loss is one mean-reduced MSE (single-section) or Huber, delta = 1 (multi-section) over the concatenation [standardized non-angle outputs, sin(angles), cos(angles)], i.e. equal weights, no per-term weighting.

### Edit (SI, "CNN Architecture and Training Parameters"; replace the sentence on normalization/sine-cosine)
Find:
```latex
During training, outputs were normalized for stability, with all angular quantities reparameterized using sine and cosine.
```
Replace:
```latex
During training, the targets were standardized with the training-set mean and standard deviation. The networks regress angles directly, in radians, so no decoding is needed at inference; sine and cosine of the angles enter only the loss, to avoid the wrap-around discontinuity, for the curvature angle $\phi$ of the single-section networks and for the yaw, pitch, and roll of the multi-section pose network. The single-section pose network regresses standardized yaw, pitch, and roll without this reparameterization. All terms (standardized positions, lengths and curvature coefficients, and the sine and cosine of the angles) have equal weight in a single mean-reduced loss.
```
(The Huber/MSE statement is fixed in Comment 9, E1; the sentence "The regressors were trained using the Huber loss ..." in the same SI paragraph should be changed to "The multi-section regressors were trained using the Huber loss ..., and the single-section regressors using the mean squared error.")

### Letter
```latex
\begin{point}[Angle decoding and loss balancing]\label{c:16}
Explain how angular sine/cosine outputs are converted back to angles and how losses for position, orientation, length, and curvature are balanced after normalization.
\end{point}
\begin{reply}
We thank the reviewer and clarified this in the Supporting Information. The networks do not output sine and cosine: they regress the angles directly, so no conversion back to angles is needed, and the sine and cosine of the angles are used only inside the loss to avoid the wrap-around discontinuity. The targets are standardized with the training-set mean and standard deviation, and all terms enter a single mean-reduced loss with equal weights, without per-term weighting. We also corrected the description of which networks use this reparameterization and which loss each network was trained with.
\end{reply}
```

---
## Comment 17: sign in Eq. S11 and Grad-CAM pixels

Facts (code, `SINGLE_helyx_testing.ipynb`, Grad-CAM cells): the score passed to Grad-CAM is `MSETarget` = minus the SUM of squared errors between the (denormalized) prediction and the ground-truth pose; Grad-CAM weights are the pixel-averaged gradients of that score; target layer = last convolution; map = ReLU of the weighted sum, normalized by its maximum, upsampled and overlaid. So (a) the minus sign comes from using the negative loss as the score, so positive weights mark features whose increase reduces the error; (b) the loss is the squared error, NOT the Huber loss as the SI says; (c) the map uses the ground-truth label, so it shows features supporting a correct pose, not a causal attribution.

### Edit 1 (SI, "Spatial Attention Formulation")
Find:
```latex
by backpropagating the Huber loss $\mathcal{L}$ to the last convolutional layer.
```
Replace:
```latex
by backpropagating the sum of squared errors $\mathcal{L}$ between the prediction and the ground-truth pose, computed on the denormalized outputs, to the last convolutional layer; the score is $-\mathcal{L}$, which explains the negative sign in the channel weights below.
```

### Edit 2 (SI, after the Grad-CAM equation)
```latex
 Channels with positive weight are those whose activation increases the score, that is, reduces the pose error; the map keeps only these contributions through the ReLU, is normalized by its maximum, and is upsampled to the image size. The highlighted pixels therefore indicate the image regions whose features most support reducing the error with respect to the ground-truth label, which is a sensitivity of the prediction and not a causal attribution.
```

### Letter
```latex
\begin{point}[Sign in Eq.~S11 and Grad-CAM regions]\label{c:17}
Clarify the negative sign in Eq. S11 and clarify how the highlighted pixels are the regions used for prediction.
\end{point}
\begin{reply}
We thank the reviewer. The negative sign arises because the score used for Grad-CAM is the negative of the loss, so that channels with positive weights are those whose activation reduces the pose error; we also corrected the loss, which is the squared error between the prediction and the ground-truth pose and not the Huber loss, as previously written. We clarified that the highlighted pixels are the regions whose features most support reducing the error with respect to the ground-truth label, a sensitivity measure and not a causal attribution of which pixels were used for the prediction.
\end{reply}
```

---
## Comment 18: Algorithm 1 initial line
No new edit: answered by the Comment 1 package (line rewritten as "Calibrate encoder zero to ... via PCC" and explained in the controller section).
```latex
\begin{point}[Algorithm 1 initialization line]\label{c:18}
In Algorithm 1, the initial line that estimates tendon lengths from intermediate positions via PCC appears unused because tendon lengths are read from encoders inside the loop. Remove it or explain its role.
\end{point}
\begin{reply}
We thank the reviewer. The line is needed and its role is now explained: it calibrates the zero of the encoders to the tendon lengths given by the PCC kinematics for the camera-estimated tip positions at start-up, which determines how the encoder readings are converted to tendon lengths at every iteration. The line has been rewritten and explained as described in our reply to the first major comment.
\end{reply}
```

---
## Comment 19: Jacobian notation (NO redraw: Fig. S3 already uses J_{l2p}(l) and \hat{J}_{p2l}; the text is aligned to it)

Convention (kept from the figure): a subscript "a2b" means the map from a to b. J_{l2p}(l) is the analytic FORWARD Jacobian (tendon lengths to pose), J^# its damped pseudoinverse, and \hat{J}_{p2l} the derivative of the learned INVERSE network N_l (pose to tendon lengths), i.e. the learned counterpart of J^#. The only inconsistent place is the single-section text, which calls the forward Jacobian J_{t2l}(l) although it maps lengths to position.

### Edits (main2.tex; search by text)
Find: `the forward derivative $J$ is computed as $J_{t2l}(l)$.`
Replace: `the forward Jacobian $J = J_{l2t}(l)$ is computed.`

Add at the end of the "General control scheme" paragraph (Section 3.3), after the sentences added for Comment 1:
```latex
 Throughout, a subscript a2b denotes the map from a to b: $J_{l2p}(l)$ is the analytic forward Jacobian, $J^{\#}$ its regularized pseudoinverse, and $\hat{J}_{p2l}$ the derivative of the learned inverse network, i.e. the learned counterpart of $J^{\#}$.
```
Algorithms 1 and 2 and Eq. for the data-driven Jacobian are unchanged ($J_{l2p}(l)$, $\hat{J}_{t2l}$, $\hat{J}_{p2l}$).

### notation.tex
Find: `$J, J^\#$ & Analytical Jacobian matrix and its regularized Moore-Penrose pseudoinverse. \\`
Replace: `$J_{l2p}, J^\#$ & Analytical forward Jacobian (tendon lengths to pose; $J_{l2t}$ for the position only) and its regularized Moore-Penrose pseudoinverse. \\`
Find: `$\hat{J}_{t2l}, \hat{J}_{p2l}$ & Estimated Jacobians derived from the data-driven mappings $N_l^1$ and $N_l^3$. \\`
Replace: `$\hat{J}_{t2l}, \hat{J}_{p2l}$ & Learned counterparts of $J^\#$: derivatives of the data-driven inverse mappings $N_l^1$ and $N_l^3$. \\`
(The Comment 1 edit in the Fig. S3 caption already writes $J_{l2p}(l)$: no change.)

### Letter
```latex
\begin{point}[Jacobian notation]\label{c:19}
Use consistent Jacobian notation. J_t2l, J_l2p, and their learned representations currently alternate between a forward Jacobian, an inverse Jacobian, and a derivative of an inverse network. These might be confusing to follow for the readers.
\end{point}
\begin{reply}
We thank the reviewer. We now define the convention explicitly: a subscript denotes the map from the first to the second quantity, the analytic Jacobian is always the forward Jacobian of the pose with respect to the tendon lengths, its regularized pseudoinverse is the corresponding inverse, and the learned controller uses the derivative of the learned inverse network, which we identify as the learned counterpart of the pseudoinverse. The single-section text, where the forward Jacobian carried the subscripts of the inverse map, has been corrected, and the algorithms, the block diagrams and the nomenclature follow the same convention.
\end{reply}
```

---
## Comment 20: open-loop baselines and terminology

Facts (code): same straight-line Cartesian / SE(3) planner with 1 mm waypoint spacing and slerp for the orientation; multi-section damping 0.1 in both; single-section closed-loop damping 0.1 (regularization 0.01 on the product); open-loop does the same null-space term for the model-based law. Differences: closed-loop starts from the camera estimate, re-plans from the current camera estimate at every iteration, and stops when the pose error falls below the threshold; open-loop starts from the pose measured by motion capture at the start, plans the full waypoint sequence once, executes it without feedback and without a convergence check, and updates its state with the internal model (PCC or learned forward network). CONFIRM: the damping of the SINGLE open-loop class and that the stored open-loop runs used these settings.

### Edit 1 (single-section controller paragraph "In both cases, ...")
Find:
```latex
The same algorithms are also employed in open-loop control as a baseline, where robot states are internally updated through either model-based or data-driven forward kinematics.
```
Replace:
```latex
The same planner, waypoint spacing, and damping are also employed in open-loop control as a baseline, which differs only in that it starts from the pose measured by the motion capture system, plans the full waypoint sequence once, executes it without feedback or convergence check, and updates the robot state internally through either model-based or data-driven forward kinematics.
```

### Edit 2 (terminology: replace "feedforward" by "open-loop")
Fig. 6 caption: "(c) Model-based feedforward controller. (d) Data-driven feedforward controller." -> "(c) Model-based open-loop controller. (d) Data-driven open-loop controller."
Fig. 9 caption: same replacement. Fig. 10 caption: "(b) Model-based feedforward controller." -> "(b) Model-based open-loop controller."
Text: "the data-driven feedforward controller (7.3 ...)" -> "open-loop"; "feedforward accuracy is lower" -> "open-loop accuracy is lower". Keep "feedforward" only in the related-work sentence on iterative learning control (a different meaning). The panels of Figs. 6 and 9 already read "open-loop".

### Letter
```latex
\begin{point}[Open-loop baselines and terminology]\label{c:20}
State whether the open-loop baselines use the same measured initial pose, planner, gains, stopping limits, and commanded waypoint sequence as the closed-loop methods. 'Open-loop' and 'feedforward' should be used consistently.
\end{point}
\begin{reply}
We thank the reviewer and now state this explicitly. The open-loop baselines use the same planner, waypoint spacing and damping as the closed-loop methods. They differ in that they start from the pose measured by the motion capture system, plan the complete waypoint sequence once and execute it without feedback and without a convergence check, updating the robot state with the internal forward model, whereas the closed-loop methods start from the camera estimate, re-plan from the current estimate at every step and stop when the error falls below the convergence threshold. The term open-loop is now used consistently in place of feedforward in the text and in the captions.
\end{reply}
```
