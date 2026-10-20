# AIS 3400076 — Comment 1: FINAL (approved by the user)

Local-only file (git-excluded via `.git/info/exclude`): it contains unpublished peer-review replies.
Context: `.claude/HANDOFF.md` (data/code analyses) and the auto-memory note `project_ais_revision_workflow`.

Conventions (decided with the user):
- Letter = `response_letter.tex` (Overleaf), one "Reviewer 1" section, comments numbered 1-31 continuously
  (major 1-10, minor 11-27, SI 28-31), macros `point` / `reply` / `newtext` / `\todo{}`, labels `\label{c:N}`.
- Manuscript = Overleaf `main2.tex` + `supporting_information.tex`; user applies edits by hand. `diff.tex` builds latexdiff markup
  (needs `--append-textcmd=abstract,transabstract`).
- KEEP the manuscript's existing notation and wording. No new symbols (the user rejected an `o` offset symbol).
- Fig. 4c is NOT redrawn: caption + pointer to SI Fig. S3a instead.

Code facts behind this comment (verified): controllers load only the pose CNN + FK/IK MLPs (`MULTI_controller.py:334-338`); the model-based
Jacobian/null-space use l = encoder - DELTAL_reference (`:506-511, :591`); DELTAL_reference = encoder - PCC(camera tips) at start-up
(`MULTI_controller.py:137-144`, `SINGLE_controller.py:126-132`); data-driven Jacobian uses pose only (`:494-497`); dataset DELTAL uses the same
convention with OptiTrack instead of the camera (`*_data_acquire.py`); `xyz2tendon` integrates PCC kinematics from the straight configuration
(`MULTI_kinematics.py:144`), so l is referenced to the straight configuration, not "absolute".

---

## Part A: manuscript changes (search by the Find text)

### A1. Abstract: replace the whole body of BOTH `\abstract[ABSTRACT]{...}` and `\transabstract[transABSTRACT]{...}`

```latex
Soft continuum robotic arms offer unparalleled dexterity and compliance. However, their virtually infinite degrees of freedom and nonlinear deformations pose significant challenges for sensing and control. This paper proposes a vision-based framework for distributed state estimation and closed-loop control of tendon-driven soft robotic arms. Miniature cameras embedded in each section provide dense proprioceptive feedback. Convolutional neural networks map multi-view images to the tip pose, which closes the control loop, and to the full-body shape through a polynomial curvature model, which is evaluated as a separate sensing capability. Two alternative controllers are designed and evaluated. The first is a model-based null-space velocity controller that regulates tip pose from camera feedback while shaping tendon configurations, using motor encoders for its Jacobian and null-space term. The second is a data-driven inverse kinematics neural network that maps task-space goals to tendon commands without encoders, with explicit secondary-objective optimization during training. Both approaches are validated in open- and closed-loop settings on single- and multi-section manipulators in quasi-static regimes. Experiments demonstrate that embedded vision enables accurate full-body state reconstruction, reliable redundancy resolution, and robust regulation even under external disturbances.
```

### A2. Introduction, "Research problem and hypothesis" paragraph

Find:
```latex
The reconstructed state is then used as feedback in both model-based and data-driven controllers, enabling tip regulation while reducing actuation effort.
```
Replace:
```latex
The estimated tip pose is then used as feedback in both model-based and data-driven controllers, enabling tip regulation while reducing actuation effort; the full-body reconstruction is evaluated as a separate sensing capability and does not enter the control law.
```

### A3. Contribution list, items 1-3 (item 4 unchanged)

Find:
```latex
\item A distributed and scalable vision-based sensing strategy for soft arms that uses miniature cameras embedded in each section of the robot. It provides dense, markerless feedback for full-body state reconstruction, and scales to arms with different numbers of sections through modular hardware design and a lightweight CNN architecture.
\item Integration of embedded vision with model-based null-space control. We close the loop by combining camera-based state estimation with a Jacobian-based Piecewise Constant Curvature velocity controller.
\item A data-driven framework for both sensing and control. We train learning-based inverse kinematics models to generate actuation commands while optimizing redundancy objectives.
```
Replace:
```latex
\item A distributed and scalable vision-based sensing strategy for soft arms that uses miniature cameras embedded in each section of the robot. It provides dense, markerless feedback for two outputs: the tip pose, which is the feedback signal used for control, and the full-body state reconstruction, which is evaluated as a separate sensing capability. It scales to arms with different numbers of sections through modular hardware design and a lightweight CNN architecture.
\item Integration of embedded vision with model-based null-space control. We close the loop with the camera-based tip pose estimate and a Jacobian-based Piecewise Constant Curvature velocity controller, whose Jacobian and null-space term are computed from motor encoder measurements.
\item A data-driven framework for both sensing and control. We train learning-based inverse kinematics models to generate actuation commands while optimizing redundancy objectives; this controller relies on camera feedback only and does not use encoders.
```

### A4. Section 3.3 Controller Design

(a) General control scheme paragraph: after "...falls below a given threshold $\gamma$." append:
```latex
 In the model-based controller, motor encoders additionally provide the tendon lengths $l$ from which the Jacobian and the null-space term are computed (Fig.~S3a of the Supporting Information); the data-driven controller uses no encoders. The curvature networks $f_C^1$ and $f_C^3$ are not part of this loop.
```

(b) Single-section controller. Find:
```latex
Once $l$ is measured from the motor encoders, the forward derivative
```
Replace:
```latex
Once $l$ is measured from the motor encoders (using the same start-up calibration as in Alg.~\ref{alg:model_based_controller}), the forward derivative
```

(c) Algorithm 1, ONE line (everything else, including the in-loop "Measure $l$ from motor encoders", stays as is):
```latex
Find:    \State Estimate $l \gets l (t_I, t_{II}, t_{III})$ via PCC
Replace: \State Calibrate encoder zero to $l(t_I, t_{II}, t_{III})$ via PCC
```

(d) Paragraph after Algorithm 1. Find the tail of the sentence:
```latex
and the PCC-based Jacobian is estimated from encoders.
```
Replace:
```latex
and the PCC-based Jacobian is evaluated at the tendon lengths $l$ measured from the encoders, whose zero is calibrated at start-up to the tendon lengths given by the PCC kinematics for the camera-estimated tip positions.
```

### A5. Fig. 4 caption (no redraw)

Find:
```latex
(c) High-level kinematic closed-loop controller employing CNN-based feedback. Tendons can be actuated using either model-based or data-driven approaches.
```
Replace:
```latex
(c) High-level kinematic closed-loop controller employing CNN-based feedback; tendons can be actuated using either model-based or data-driven approaches. In both controllers, the tip pose $p$ estimated by the CNN closes the loop. The model-based controller additionally uses motor-encoder readings of the tendon lengths $l$ to compute the Jacobian and the null-space term, whereas the data-driven controller uses no encoders. The full-body curvature estimate does not enter the control loop.
```

### A6. Conclusion (one replacement; the reviewer explicitly asks for the conclusion to distinguish the three roles)

Find:
```latex
Miniature cameras embedded in each segment feed deep learning algorithms that reconstruct the full shape of the robot, enabling closed-loop control strategies, both model-based and data-driven, which explicitly exploit kinematic redundancy to accomplish secondary tasks within the null space.
```
Replace:
```latex
Miniature cameras embedded in each section feed deep learning algorithms that estimate the tip poses and reconstruct the full shape of the robot. The tip poses close the loop of both model-based and data-driven controllers that explicitly exploit kinematic redundancy to accomplish secondary tasks within the null space; the model-based controller also uses motor encoders for its Jacobian and null-space term, and the full-shape reconstruction is evaluated separately.
```

Only this one conclusion edit is made for Comment 1. The other conclusion sentences are left alone on purpose.
CARRIED TO COMMENT 27: the sentence "In such settings, full-body curvature feedback from embedded cameras enables null-space control to actively shape the arm for obstacle avoidance while maintaining the desired tip pose." overstates (the curvature estimate is not in the control loop); rewrite it there as "could enable ... ; this is a future direction and was not evaluated here."

### A7. Supporting Information (`supporting_information.tex`)

(a) Fig. S3 caption, two replacements.

Find:
```latex
This approach uses model-based null-space optimization to translate observed poses into actuator commands.
```
Replace:
```latex
This approach uses model-based null-space optimization to translate observed poses into actuator commands. The camera-based pose $p$ enters the task-space error, whereas the encoders provide $l$ for the Jacobian $J_{l2p}(l)$ and the null-space term.
```

Find:
```latex
This approach uses data-driven kinematics learning to translate observed poses into actuator commands.
```
Replace:
```latex
This approach uses data-driven kinematics learning to translate observed poses into actuator commands. The Jacobian is obtained from the pose $p$ alone; no encoder signal is used.
```

(b) "Control Blocks Diagrams" text: after "...detailing the signal flow from camera feedback to actuator commands." append:
```latex
 The curvature networks do not appear in either diagram because they are evaluated separately from the controllers.
```

### After applying
- Recompile `diff.tex` (with `--append-textcmd=abstract,transabstract`) and check the abstract is marked.
- SI markup: a second main file `diff_si.tex` with `\ShellEscape{latexdiff --type=CFONT supporting_information.tex supporting_information2.tex > supporting_information-d.tex}` and `\input{supporting_information-d}` (never redirect into an existing source file).
- Wording deliberately left for later comments: "scalable"/"scales" (Comment 3), "markerless" (11), "reducing actuation effort" (6),
  "reliable redundancy resolution" and "robust regulation even under external disturbances" (6 and 7).

---

## Part B: response letter block (replaces the Comment 1 block in `response_letter.tex`)

```latex
\begin{point}[Clarify the role of visual sensing in closed-loop control]\label{c:1}
The manuscript presents pose estimation and full-body piecewise-polynomial-curvature (PPC) reconstruction as parts of a unified sensing-and-control framework. However, Algorithms 1 and 2 and Fig.~S3 indicate that both controllers use feedback from the pose network, while the curvature network is evaluated separately and does not enter either control law.

Algorithm 1 also uses a PCC inverse calculation to initialize tendon lengths from section-tip positions. This is not the same as using the image-based PPC curvature estimate. Moreover, the resulting estimate appears to be replaced by the motor-encoder measurement at the first control iteration, before it affects the control command. The authors should explain this initialization or remove it.

The abstract, contribution list, Fig.~4c, and conclusion should clearly distinguish:
(i) camera-based pose estimation used for control;
(ii) encoder measurements used to calculate the Jacobian and null-space term; and
(iii) image-based PPC reconstruction evaluated as a separate sensing capability.
If the curvature estimate is intended to contribute to control, the manuscript should explicitly show where it enters the control law.
\end{point}
\begin{reply}
We thank the reviewer for this comment. The reviewer's reading is correct: the camera closes the control loop through a single signal, the tip pose estimated by the pose network $f_p^3$, while the curvature networks are evaluated as a separate sensing capability and do not enter either control law. The original text did not state this clearly, and in places it suggested that the full-body reconstruction was used as feedback. The manuscript now distinguishes three roles consistently: (i) the camera-based tip pose is the feedback used for the task-space error in both controllers; (ii) motor-encoder measurements are used only by the model-based controller, to compute the Jacobian and the null-space term, while the data-driven controller uses no encoders; and (iii) the image-based PPC reconstruction is a separate sensing capability that does not enter the control law. This is stated in the abstract, the introduction, the contribution list, the controller design section, the conclusion, and the captions of Fig.~4c and SI Fig.~S3, whose block diagram shows the encoder path. Regarding Algorithm 1, the line is needed, but we agree it was unclear. It does not initialize the loop variable $l$; it calibrates the zero of the encoders to the tendon lengths given by the PCC kinematics for the camera-estimated tip positions at start-up, so it is not overwritten by the encoder measurement but determines how the encoder readings are converted to $l$ at every iteration. We have rewritten this line of Algorithm 1 and added a sentence explaining the calibration to the controller design section, where the single-section controller is also stated to use the same calibration.
\end{reply}
```

FORMAT RULE (user): every reply is ONE continuous plain block: no bold, no medskip or paragraph breaks, no quoted manuscript paragraph (newtext); refer to sections instead. Comment 18 (same Algorithm 1 line) should only cite this reply.
