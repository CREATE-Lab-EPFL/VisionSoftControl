# AIS 3400076 — Comment 2: FINAL DRAFT (all claims verified against the PDFs, 2026-10-20)

Local-only file (git-excluded): it contains unpublished peer-review replies.
Reviewer's heading: "Establish originality claims through direct comparison with prior work".
Rules: short manuscript additions (here ONE sentence citing the table); reply = one continuous plain block (no bold, no spacing, no quoted paragraph); keep existing notation.

## Verification (the comparison table `tab:S10_comparison` in main2 needs NO corrections)
- Hofer 2021 (full text): 3 bellows actuators each with a camera, white pattern, LED board; 2 rotational DOF; CNN ~1 deg at 30 Hz; two decoupled PI loops (50 Hz); stiffness adjustment "not explored".
- Thuruthel 2017 (PDF): 6-DoF cable-driven manipulator (six servos); position and orientation from an Aurora electromagnetic tracker, 6-DoF probe at the tip; learned IK, redundancy handled implicitly (multiple solutions possible, no explicit secondary objective); tested with and without external forces.
- Han 2025 (PDF): one miniature camera tracks one internal marker; fill/indicator lights are LED PCBs; motion replay on a tendon-driven platform and contact reasoning; control only as a prospect, no closed loop.
- Pei 2024 (PDF): model-based closed-loop control from IMUs plus encoders; no mention of redundancy, null space or secondary objective.
- Lu 2024 (journal PDF): multicore FBGs, colonoscope and multisection manipulators; no redundancy, null space or secondary objective.
- Almanzor 2023 (PDF): colour camera for feedback, fixed relative to the robot (external). ConTac 2024 (PDF): fish-eye camera on top of the arm observing the marked skin, LEDs inside the skin, admittance control.
- Wang 2020 and Yoo 2023: abstracts only (sensing only, no control).

## Manuscript edits

Note: the table sits in the Introduction, so it becomes Table 1 and the old Table 1 (`table:abs_errors`, Comment 24) becomes Table 2, the control table Table 3. Replies to Comment 24 must say "original Table 1, now Table 2".

### E1. ONE sentence, between the control related-work paragraph (ends "...relies only on motor encoder feedback~\cite{chenVersatileNeuralNetwork2025}.") and "Research problem and hypothesis"

```latex
Table~\ref{tab:S10_comparison} compares closely related systems in terms of their sensing modality, the region of the arm that is sensed, the estimated quantity, whether the estimate closes a control loop, and whether redundancy is exploited.
```

### E2. Narrow the broad claim ("Research problem and hypothesis" paragraph)

Find:
```latex
To the best of our knowledge, no framework has yet combined such sensing with closed-loop null-space control of continuum robots, either through model-based or learning-based approaches.
```
Replace:
```latex
To the best of our knowledge, and as summarized in Table~\ref{tab:S10_comparison}, no framework has yet combined internal sensing distributed along the arm with closed-loop control that exploits kinematic redundancy, either through model-based or learning-based approaches.
```

### E3. Contribution list lead-in

Find:
```latex
The contributions of this paper include:
```
Replace:
```latex
The contribution of this paper lies in integrating internal-camera sensing distributed along the arm, which requires no markers at inference, with redundancy-aware control on a multi-section arm. Specifically, the contributions include:
```
("no markers at inference" anticipates Comment 11; harmonize there.)

## Letter block (replaces the Comment 2 block in `response_letter.tex`)

```latex
\begin{point}[Establish originality claims through direct comparison with prior work]\label{c:2}
The individual sensing and control elements of this paper have appeared in many papers. Novelty can't be based solely on combining internal vision, learned kinematics, and closed-loop control at a general level. The paper's contribution appears to lie more specifically in integrating distributed markerless internal cameras with model-based and learned redundancy-aware control on a multisection arm. This contribution should be defined precisely and compared directly with prior systems.

Several particularly relevant studies are missing or insufficiently discussed:

Hofer et al. (2021), A Vision-Based Sensing Approach for a Spherical Soft Robotic Arm, integrated cameras into three soft actuators, used a CNN to estimate arm orientation, and demonstrated camera-based closed-loop control. The paper reported approximately 1 deg orientation accuracy at 30 Hz, compared with the present manuscript's $3.11^\circ \pm 1.96^\circ$ single-section error and 8 Hz update rate.

Thuruthel et al. (2017), Learning Closed Loop Kinematic Controllers for Continuum Manipulators in Unstructured Environments, demonstrated learned inverse kinematics with feedback on a redundant tendon-driven continuum arm, including evaluation under external loads.

Han et al. (2025), Anchoring Morphological Representations Unlocks Latent Proprioception in Soft Robots, used an internal camera to estimate full-body deformation and force.

Lu et al. (2024), Adaptive Online Learning and Robust 3-D Shape Servoing of Continuum and Soft Robots in Unstructured Environments, is context for learned shape servoing and robustness, although it uses FBG sensing.

Yoo et al., Toward Zero-Shot Sim-to-Real Transfer Learning for Pneumatic Soft Robot 3D Proprioceptive Sensing, has internal-camera soft-robot proprioception.

The authors should explain what each close prior study established and identify the specific capability added here. The claim that no prior framework combines comparable sensing with closed-loop null-space control is too broad without this analysis.
\end{point}
\begin{reply}
We thank the reviewer for this comment and agree that the originality claim was too broad. The contribution is now stated as the integration of internal-camera sensing distributed along the arm, which requires no markers at inference, with redundancy-aware control on a multi-section arm (end of the introduction), and the claim that no framework combines such sensing with closed-loop null-space control has been qualified and tied to a new comparison table in the introduction. The table compares Hofer et al., Thuruthel et al., Han et al.\ and Lu et al.\ with Yoo et al., which was already cited, and with further related systems, in terms of sensing modality, sensed region of the arm, estimated quantity, closed-loop use of the estimate and exploitation of redundancy. We acknowledge that Hofer et al.\ reach a higher orientation accuracy and update rate than our single-section estimator, for a single two-degree-of-freedom joint rather than the full pose, and that our update rate limits the framework to quasi-static operation, as stated in the conclusion.
\end{reply}
```

(The editor's email asks for a response to reviewer-suggested references inside the letter: this reply answers it.)
