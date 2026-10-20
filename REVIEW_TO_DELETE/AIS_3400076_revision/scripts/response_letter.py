"""Point-by-point response letter: every element of the decision letter quoted in full,
followed by a short response and the changes made. Writes snippets/resp_<key>.tex (one block
per comment, shown in the guide) and snippets/response_letter.tex. Run after snippets.py."""
import json
import os

OUT = "/home/vigno0405/github/VisionSoftControl/REVIEW_TO_DELETE/AIS_3400076_revision"
REPO = "/home/vigno0405/github/VisionSoftControl"
SN = f"{OUT}/snippets"
D = lambda f: json.load(open(f"{OUT}/data/{f}"))
misc, single, lk = D("misc_summary.json"), D("single_summary.json"), D("leakage_effect.json")
ik = json.load(open(f"{REPO}/MULTI/results/ik_ablation.json"))
a, b = ik["zeta=0.01"]["control_targets"], ik["zeta=0.0"]["control_targets"]
ld, sd = lk["MULTI"], lk["SINGLE"]
ld["pos_III"]["all_mean"] = 26.45  # as printed in Table 1 of the paper (recomputed: 26.44), same as Table S14
cS, cM = misc["coverage"]["SINGLE"], misc["coverage"]["MULTI"]
dS, dM = [t["dL_mm"] for t in cS["targets"]], [x for t in cM["targets"] for x in t["dL_mm"]]
wo = misc["outliers"]["tableS6_without_outliers"]
rho = single["bending"]["rho_pos"]

# Each comment: list of (reviewer paragraph, response, changes or None). Quotes are verbatim
# from the decision letter (PDF artifacts fixed; the reviewer's own wording kept).
P = {}
P["G"] = [
 (r"Please ensure that the title of your manuscript is succinct, descriptive, and accurate, so that readers may easily find and cite your work by simply searching for relevant keywords",
  r"The title states the method (internal-camera reconstruction and closed-loop control) and the system (soft robotic arms); we kept it.", None),
 (r"Reviewers may have suggested references to be added to the manuscript. While this may be a reasonable request to improve your manuscript, please note that there is no obligation to include these specific references. Please include a response to such requests as part of your revision letter.",
  r"We added the four suggested references that were not yet cited (Hofer et al., Thuruthel et al., Han et al., Lu et al.); Yoo et al.\ was already cited. See Comment~2.", r"Introduction; Table~S10; references."),
 (r"Manuscripts generally benefit from careful re-reading before submitting the revised version. We also recommend running a spell check. Please define all acronyms when first mentioned and apply them thereafter (the title, abstract, and Table of Contents text must each be understandable as standalone texts).",
  r"Done. All acronyms are defined at first use in the main text, the SI, and the figure captions (e.g., BW, FE, FC, CL, OL). The title and abstract contain no undefined acronyms.", r"Main text, SI, captions."),
 (r"Check that the text and axis labels in all graphics are correct and are correctly spelled. In addition, please check that all parts, insets, and footnotes of Figures and Schemes are mentioned in the caption.",
  r"Done. Every panel and inset is now described in its caption (see Comment~10).", r"All captions."),
 (r"Please obtain copyright permission information for any images that have not been created originally for this manuscript. Please add the copyright statements to the caption of reprinted/adapted graphics, as per the requirements of the original publisher. The reuse license can often be obtained for free from the webpage of the original article, including your own non-open access publications.",
  r"All figures were created by the authors for this manuscript; none is reprinted or adapted.", None),
 (r"The journal recently transitioned to a reference style that requires full article titles, and optionally, DOIs. If the manuscript does not display these yet, please expand the reference list accordingly (for details see our author guidelines).",
  r"The reference list gives full titles; we added DOIs.", r"References."),
 (r"Reproduction or use of logos and trademark images in any form requires that copyright permission is first obtained from the brand owner. Examples of trademarks frequently encountered which require permission include characters and names from cartoons/TV/movies/comics/computer games, university/institution logos, and symbols or icons associated with companies/brands.",
  r"No logos or trademark images are used.", None),
]
P["overall"] = [
 (r"This manuscript presents an internal camera-based framework for pose estimation, model-based backbone reconstruction, and quasi-static control of tendon-driven soft robotic arms. Integrating miniature cameras into one- and three-section Trimmed Helicoid manipulators is technically interesting, and the comparison between model-based and learned inverse-kinematics controllers is potentially valuable.",
  r"We thank the reviewer for the careful and constructive assessment.", None),
 (r"I recommend major revision. The claimed contributions (internal-camera proprioception, learned inverse kinematics, closed-loop soft-arm control, and redundancy resolution) have each been extensively addressed in prior work. The originality of the paper therefore appears to lie primarily in their particular integration: distributed markerless internal cameras combined with model-based and learned redundancy-aware control on a multisection arm. The authors should define this contribution more precisely and provide direct quantitative comparisons or demonstrate a capability not established previously.",
  r"We agree that the contribution is this integration, and we now define it precisely. A direct numerical comparison is not meaningful, because the prior systems differ in actuation, size, and task. We therefore compare them by capability (Table~S10, Comment~2). The capability not established before is internal vision on every section of a multi-section arm, a closed loop on that estimate, and explicit redundancy resolution, both model-based and learned.", r"Introduction; contribution list; Table~S10."),
 (r"Several central claims also extend beyond the evidence presented. The full-body curvature estimate is not used for control; scalability is demonstrated only with separately trained one- and three-section networks; multi-section curvature labels rely on a learned surrogate rather than direct full-body measurements; and the manuscript reports no quantitative experimental results isolating the effect of the secondary objective. In addition, the control evaluation uses a limited set of targets and planar trajectories without repeated trials. The related-work discussion, reproducibility details, curvature formulation, and figures require significant improvement.",
  r"We aligned each claim with the evidence; each point is answered below (Comments~1, 3, 4, 6, 7, 2, 9, 5, and 10).", None),
]
P["1"] = [
 (r"1. Clarify the role of visual sensing in closed-loop control. The manuscript presents pose estimation and full-body piecewise-polynomial-curvature (PPC) reconstruction as parts of a unified sensing-and-control framework. However, Algorithms 1 and 2 and Fig. S3 indicate that both controllers use feedback from the pose network, while the curvature network is evaluated separately and does not enter either control law.",
  r"Correct. Both controllers close the loop on the camera-estimated tip pose. The curvature reconstruction is a separate sensing output and does not enter either control law. We now state this explicitly.", r"Section~3.3 (new paragraph)."),
 (r"Algorithm 1 also uses a PCC inverse calculation to initialize tendon lengths from section-tip positions. This is not the same as using the image-based PPC curvature estimate. Moreover, the resulting estimate appears to be replaced by the motor-encoder measurement at the first control iteration, before it affects the control command. The authors should explain this initialization or remove it.",
  r"The estimate is not replaced. It is used once, before the loop, to set the encoder offset $\mathbf{l}_{\mathrm{off}} = \mathbf{l}_{\mathrm{enc}} - \mathbf{l}_0$. Inside the loop, the encoder readings are then expressed in the PCC tendon frame used by $\mathbf{J}(\mathbf{l})$ and by the null-space term. We kept the step and made it explicit.", r"Algorithm~1 (offset line added); Section~3.3.2."),
 (r"The abstract, contribution list, Fig. 4c, and conclusion should clearly distinguish: camera-based pose estimation used for control; encoder measurements used to calculate the Jacobian and null-space term; and image-based PPC reconstruction evaluated as a separate sensing capability.",
  r"Done in all four places.", r"Abstract; contributions 1--3; Fig.~4c (encoder block added, curvature CNN outside the loop) and caption; Conclusion."),
 (r"If the curvature estimate is intended to contribute to control, the manuscript should explicitly show where it enters the control law.",
  r"It is not used for control; this is now stated (see above).", None),
]
P["2"] = [
 (r"2. Establish originality claims through direct comparison with prior work. The individual sensing and control elements of this paper have appeared in many papers. Novelty can't be based solely on combining internal vision, learned kinematics, and closed-loop control at a general level. The paper's contribution appears to lie more specifically in integrating distributed markerless internal cameras with model-based and learned redundancy-aware control on a multisection arm. This contribution should be defined precisely and compared directly with prior systems.",
  r"Agreed. We define the contribution as this integration and compare it with prior systems in a new table (Table~S10). The table compares design choices rather than accuracy, since the systems differ in actuation, size, and task: sensing, sensed region, estimated quantities, closed loop on the estimate, and use of redundancy. Each prior system covers part of these; ours is the only one that combines internal vision on every section, a closed loop on that estimate, and explicit redundancy resolution.", r"Introduction (new paragraph); contribution list; Table~S10."),
 (r"Several particularly relevant studies are missing or insufficiently discussed: Hofer et al. (2021), A Vision-Based Sensing Approach for a Spherical Soft Robotic Arm, integrated cameras into three soft actuators, used a CNN to estimate arm orientation, and demonstrated camera-based closed-loop control. The paper reported approximately 1 deg orientation accuracy at 30 Hz, compared with the present manuscript's 3.11$^\circ\pm$1.96 deg single-section error and 8 Hz update rate. Thuruthel et al. (2017), Learning Closed Loop Kinematic Controllers for Continuum Manipulators in Unstructured Environments, demonstrated learned inverse kinematics with feedback on a redundant tendon-driven continuum arm, including evaluation under external loads. Han et al. (2025), Anchoring Morphological Representations Unlocks Latent Proprioception in Soft Robots, used an internal camera to estimate full-body deformation and force. Lu et al. (2024), Adaptive Online Learning and Robust 3-D Shape Servoing of Continuum and Soft Robots in Unstructured Environments, is context for learned shape servoing and robustness, although it uses FBG sensing. Yoo et al., Toward Zero-Shot Sim-to-Real Transfer Learning for Pneumatic Soft Robot 3D Proprioceptive Sensing, has internal-camera soft-robot proprioception.",
  r"""All five are now discussed:
\begin{itemize}
\item Hofer et al.: higher orientation accuracy, on a two-angle spherical joint with an internal pattern and LEDs; redundancy not exploited. Ours: 6-DoF pose of extensible sections, no internal markers, three sections, redundancy resolution.
\item Thuruthel et al.: learned closed-loop IK on a two-module tendon arm, with an external electromagnetic tracker at the tip; redundancy implicit.
\item Han et al.: one internal camera tracking an internal marker on one module; no closed loop on the estimate.
\item Lu et al.: FBG shape servoing; no vision, no redundancy objective.
\item Yoo et al.\ (already Ref.~[15]): internal-camera shape sensing, no control.
\end{itemize}""", r"Introduction; Table~S10; four new references."),
 (r"The authors should explain what each close prior study established and identify the specific capability added here. The claim that no prior framework combines comparable sensing with closed-loop null-space control is too broad without this analysis.",
  r"The new Introduction paragraph states what each study established and the capability added here. The novelty claim is narrowed to the combination above.", r"Introduction (novelty sentence replaced)."),
]
P["3"] = [
 (r"3. Substantiate or narrow the scalability claim. The estimator is not invariant to the number of arm sections. Images from $n$ cameras are stacked as $n$ input channels, so the first convolutional layer changes with $n$. The output head must also change---from 6 to 18 pose variables and from one to three sets of curvature parameters. Separate networks are trained for the one- and three-section arms. Transfer learning may reduce retraining effort, but the present method is not plug-and-play across arbitrary arm lengths and is not validated on an unseen section count. The statement that only the first layer must be adjusted also conflicts with Fig. 3 because the regression head changes as well.",
  r"Agreed; we narrowed the claim. The input layer and the regression head both change, the network is retrained with a transferred backbone, and only $n = 1$ and $n = 3$ were validated. We removed ``scalable'' where it implied no retraining.", r"Section~3.1 (``only the first layer'' corrected); Introduction; contribution~1; Conclusion."),
]
P["4"] = [
 (r"4. Strengthen the ground truth for full-body reconstruction. For the single-section arm, curvature labels are fitted from three measured orientations. For the multi-section arm, SI Section 4.2 states that marker occlusion prevents simultaneous full-body tracking and that a learned network, N\_C, maps tip pose to curvature labels. Thus, the multi-section CNN is evaluated primarily against a learned, model-constrained surrogate rather than direct measurements of the backbone.",
  r"Correct. We now state this in Section~4.2.2.", r"Section~4.2.2."),
 (r"Fig. S2b does not provide sufficient validation of N\_C: numerical errors, sample count, data split, and confidence intervals are missing. It is also unclear whether its validation configurations are independent of the data used to train N\_C and the three-section curvature estimator.",
  r"Added. Fig.~S2b uses 20 configurations, posed manually with all markers visible and recorded in a separate session. They were not used to train $N_C$ or the three-section CNNs. Error bars are one standard deviation across configurations. We also report the $N_C$ error on held-out single-section test data ($N = 500$): 0.38--0.43, 1.20--1.37, and 2.49--2.94~mm at $L/3$, $2L/3$, and $L$ for the three curvature models.", r"Fig.~S2 caption; SI Section~4.2."),
 (r"Wherever possible, reconstructed backbone points should be compared directly with motion-capture marker positions, and uncertainty in N\_C should be propagated into the reported errors. Otherwise, the result should be described as model-constrained reconstruction, with its assumptions stated explicitly, including planar bending within each section, no torsion, and no arc-dependent bending direction.",
  r"Marker occlusion prevented a direct marker comparison for the multi-section arm, so $N_C$ uncertainty cannot be propagated reliably. We follow the reviewer's alternative: the result is described as a model-constrained reconstruction, and the three assumptions (planar bending within each section, no torsion, constant bending direction along a section) are stated.", r"Section~2.2 (assumptions); Section~4.2.2; Fig.~7 caption."),
]
P["5"] = [
 (r"5. Correct the curvature-coordinate inconsistency. The main manuscript defines s as normalized arc length and writes theta(s) = c0*s + (1/2)c1*s\^{}2 + (1/3)c2*s\^{}3 in Eq. 4. Under this definition, initialization should not introduce factors of section length L. In contrast, SI Eqns. S5--S9 evaluate the polynomial at L/3, 2L/3, and L, and use c\_0=$\theta$/L for constant curvature. This treats the independent variable as dimensional arc length. These formulations have different coefficient units and cannot both be correct. The paper should consistently use either normalized arc length $u = x/L$ or dimensional arc length $x \in [0, L]$, and revise Eqs. 4--6, SI Eqs. S3--S9, the translation integral, nomenclature, and coefficient units accordingly.",
  r"Corrected. We use the dimensional arc length $x \in [0, L]$ throughout, as in the implementation and in SI Eqs.~S5--S9.", r"Eq.~4 ($\theta(s)$, $s \in [0, 1]$ $\to$ $\theta(x)$, $x \in [0, L]$); Eqs.~5--6 and the translation integral (no factor $L$; points $L/3$, $2L/3$, $L$); SI Eqs.~S3--S4 and Section~2.2; Table~S1 (units mm$^{-1}$, mm$^{-2}$, mm$^{-3}$)."),
]
P["6"] = [
 (r"6. Quantitatively evaluate the secondary objective. The control contribution is framed as redundancy-aware null-space control, but the manuscript reports no quantitative experimental results isolating the effect of the secondary objective. No reported experiment shows the objective H(l), tendon-limit margins, tendon distributions, or configurations obtained with and without the secondary objective. Furthermore, H(l) penalizes displacement from the mean sampled tendon vector. It does not directly minimize tendon force, motor current, energy, or control effort. The objective should therefore might described as actuator-range centering unless effort is measured.",
  r"Agreed. Effort was not measured, so we now describe $H(\mathbf{l})$ as actuator-range centering and removed the effort claims.", r"Introduction; Section~3.3.2; Conclusion."),
 (r"For both controllers, an ablation with the secondary objective disabled using identical targets would be helpful. Results should report both primary-task error and a quantitative secondary-task metric. A useful experiment could compare multiple configurations reaching the same tip pose and show the resulting tendon margins or values of H(l).",
  r"""Added for both controllers, offline on the same 20 targets. This compares the configurations that reach the same tip poses with and without the objective (without $\to$ with):
\begin{itemize}
\item Model-based (control law replayed on the PCC model): $H(\mathbf{l})$ $693 \to 269$; RMS tendon deviation from $\bar{\mathbf{l}}$ $12.0 \to 7.5$~mm; final position error $5.8 \to 5.3$~mm.
\item Data-driven ($N_l^3$ retrained with $\zeta = 0$ and $0.01$, evaluated through $N_p^3$): $H(\mathbf{l})$ """ + f"${b['H_mean']:.0f} \\to {a['H_mean']:.0f}$; RMS deviation ${b['rms_dev_mean']:.1f} \\to {a['rms_dev_mean']:.1f}$~mm; position error ${b['pos_mean']:.1f} \\to {a['pos_mean']:.1f}$~mm" + r""" (the penalty trades some accuracy for range centering).
\end{itemize}
Both are simulated through the models and labeled as such.""", r"SI Section~5.3; Table~S13; Fig.~S8."),
]
P["7"] = [
 (r"7. Expand and better characterize the control evaluation. The experimental evaluation does not quantify its coverage relative to the reachable workspace. The training datasets reportedly include bending angles up to 85$^\circ$ per section, and the multisection target plots span a substantial positional range. However The trajectory evaluation is narrow, and the target coverage is incompletely documented. Single-section bending angles are apparently under 17 deg, and three-section angles are under 19 deg, and overall length changes are also quite limited. The evaluation does not include workspace-boundary paths, nonplanar trajectories, large orientation changes, or trajectories requiring qualitatively different section configurations.",
  r"""We quantified the coverage:
\begin{itemize}
\item Training bending: single section, maximum $57^\circ$ (95th percentile $36^\circ$); multi-section 95th percentiles $30^\circ$, $32^\circ$, $34^\circ$. The ``$85^\circ$'' is corrected.
\item Single-section targets and trajectories reach $""" + f"{cS['target_bend_max']:.1f}" + r"""^\circ$ and $""" + f"{cS['traj_bend_max']:.1f}" + r"""^\circ$.
\item Length changes are limited, as the reviewer notes: $""" + f"{min(dS):.1f}$ to ${max(dS):.1f}" + r"""$~mm (single; training 5th--95th percentile $""" + f"{cS['train_dL']['p5']:.1f}$ to ${cS['train_dL']['p95']:.1f}" + r"""$~mm) and $""" + f"{min(dM):.1f}$ to ${max(dM):.1f}" + r"""$~mm per section (multi).
\item Boundary, non-planar, and large-orientation trajectories are listed as limitations.
\end{itemize}""", r"Section~3.2; SI Section~6.3; Fig.~S9; Section~5."),
 (r"Figs. S4--S6 plot the target positions and associated errors, but the coordinates are not tabulated and the targets are not compared with the complete reachable or sampled workspace. The authors should report the target coordinates, associated bending and compression ranges, and the fraction of the sampled workspace represented by the evaluation set.",
  r"Added: coordinates, bending angle, and length change of every target. The targets span """ + f"{100 * cS['hull_volume_ratio']:.1f}" + r"""\% (single) and """ + f"{100 * cM['hull_volume_ratio']:.1f}" + r"""\% (multi) of the convex hull of the sampled positions.""", r"Tables~S8 and S9; SI Section~6.3."),
 (r"Each of the 20 targets is visited only once. Consequently, the reported standard deviations describe variation across different targets, not trial-to-trial repeatability, and do not establish that one controller outperforms the other. The 30 waypoints in each trajectory are likewise serially correlated rather than independent trials.",
  r"Agreed. The text and captions now say this, and differences between controllers are reported as observed on these targets, not as general superiority.", r"Section~4.1.4; captions of Figs.~5 and 8; Table~S7."),
 (r"The disturbance experiment should also be characterized more narrowly. A single 50 g off-center payload demonstrates compensation for one constant load (which is only moderately successful), not general robustness to disturbances or contact. Either additional load magnitudes and directions should be tested or the claims should be limited.",
  r"We limited the claims: the test shows compensation of one constant load. Further load magnitudes and directions are listed as future work.", r"Abstract; Section~4.2.6; Conclusion; Section~5."),
]
P["8"] = [
 (r"8. Establish independence of training and evaluation data. The datasets are randomly divided 85/10/5, but the acquisition sequence, session structure, and grouping of neighboring configurations are not described. If frames from continuous trials are split randomly, nearly identical or temporally adjacent configurations may appear in both training and test sets, inflating apparent generalization. The authors should state: how samples were randomized; whether test data were separated by session or configuration neighborhood; whether controller targets and trajectories were excluded from training; and whether experiments span different days, camera settings, coverings, or robot builds.",
  r"""\begin{itemize}
\item Randomization: random permutation of all pooled samples, fixed seed.
\item Separation: none by session or neighborhood. On the multi-section arm each configuration was held $\approx 3$~s and logged at 1~Hz, so """ + f"{ld['n_dup']}" + r""" of 500 test samples share a configuration with training. Without them, the tip errors are """ + f"{ld['pos_I']['rest_mean']:.2f}, {ld['pos_II']['rest_mean']:.2f}, {ld['pos_III']['rest_mean']:.2f}" + r"""~mm (instead of """ + f"{ld['pos_I']['all_mean']:.2f}, {ld['pos_II']['all_mean']:.2f}, {ld['pos_III']['all_mean']:.2f}" + r"""~mm). On the single-section arm, close samples are not more accurate (""" + f"{sd['pos']['dup_mean']:.2f} vs.\\ {sd['pos']['rest_mean']:.2f}" + r"""~mm). Session-blocked evaluation is listed as a limitation.
\item Targets and trajectories: targets were drawn from the sampled workspace, so they were not excluded; closed-loop tests use new images; trajectories are not in the datasets.
\item Days and setup: single section one day, multi-section two days; same camera settings; one build per arm \textbf{[CONFIRM]}; different coverings for the two arms (silicone, fabric).
\end{itemize}""", r"Sections~3.1.1 and 3.2; SI Section~4.1; Tables~S12 and S14; Section~5."),
]
P["9"] = [
 (r"9. Provide the missing reproducibility details. The paper needs to include enough information to enable reproduction of the results. The methods omit several parameters that affect performance: camera model, lens and field of view, exposure and gain behavior, maximum epochs, random seeds, output normalization statistics, angular decoding, and the training details for N\_C, N\_p3, and N\_l3. Additionally, robot design details are also incomplete, including tendon material and diameter, preload/zeroing criterion, current limit, sampled tendon ranges, and the number of acquisition sessions. The SI is a good place for a single reproducibility table containing these settings.",
  r"Added a single reproducibility table with every listed item: camera model, lens and field of view, exposure and gain; maximum epochs and early stopping; random seed (42); output normalization; angle handling; training details of $N_C$, $N_p^3$, and $N_l^3$; tendon material and diameter; pretensioning criterion and current limit; sampled tendon ranges; acquisition sessions.", r"Table~S11; Section~2.1; Table~S12 (sessions)."),
 (r"Claims of robustness to lighting or hardware variation should be limited unless such variation was explicitly tested.",
  r"Limited. Augmentation was used during training; robustness to lighting or hardware changes was not tested, and the text now says so.", r"Section~5."),
]
P["10"] = [
 (r"10. Revise the figures and captions. Several figures---particularly Figs. 1B, 2, 3, and 5---are difficult to interpret. Their visual density and inconsistent presentation make it hard to follow the methodology and compare results.",
  r"Revised. The captions of Figs.~1 and 2 now describe every labeled element ($L_1$--$L_4$ are geometric arcs, not tendons), and Fig.~5b uses equal axis scaling.", r"Figs.~1, 2, 5 (captions; Fig.~5b axes)."),
 (r"In particular, Figure 3 requires attention. Although the MobileNetV2 backbone and inverted residual block are depicted, the overall relationship among the pose, curvature, forward-kinematics, and inverse-kinematics networks is hard to reconstruct. The MLP inputs and outputs are not identified, and tensor dimensions and network-specific outputs are unclear. The paper should use a consistent flow direction, label all network inputs and outputs, and distinguish clearly between the networks used for pose estimation, curvature reconstruction, forward kinematics, and inverse kinematics.",
  r"Fig.~3 is redrawn: left-to-right flow, the name of each network, inputs and outputs with sizes, and one color per role (pose, curvature, forward and inverse kinematics). The caption lists all networks.", r"Fig.~3 and caption; Section~3.1."),
]
MINOR = [
 ("11", "pages 1--2", r"Use `markerless at measured inferences' rather than simply `markerless.' External optical markers are required to generate the supervised labels, even though markers are not required during deployment.",
  r"Done: ``markerless at inference'', with the role of the markers explained at first use.", r"Contribution~1."),
 ("12", "pages 1--2", r"Use either `section' or `segment' consistently throughout the manuscript, figures, algorithms, and SI.",
  r"Done: ``section'' throughout.", r"Text, headings, captions, figures, SI."),
 ("13", "pages 3--5", r"The calibration paragraph says that `all ten tendons' are tightened, but the multi-section arm has nine tendons and the single-section arm has three. Correct the number and state whether the same preload procedure is used for both systems.",
  r"Corrected: three and nine tendons. The same pretensioning procedure is used for both arms; its criterion and the current limit are given.", r"Section~2.1; Table~S11."),
 ("14", "pages 3--5", r"Identify the camera manufacturer and model, lens or field of view, nominal frame rate, and the physical size and mass of each camera and mount.",
  r"Added: manufacturer and model, lens and field of view, nominal frame rate, and size and mass of the camera and its mount.", r"Section~2.1; Table~S11."),
 ("15", "pages 3--5", r"The claim that images are acquired simultaneously should be supported by the synchronization metho as this type software capture is not necessarily simultaneous hardware triggering.",
  r"Correct: synchronization is in software only (one capture thread per camera; the latest frame of each camera is used). We removed ``simultaneously'' and describe the mechanism.", r"Section~2.1; Fig.~1 caption."),
 ("16", "pages 5--7", r"Explain how angular sine/cosine outputs are converted back to angles and how losses for position, orientation, length, and curvature are balanced after normalization.",
  r"The networks regress angles directly; sine and cosine are used only inside the loss, so no decoding is needed. Targets are standardized with training statistics, and all loss terms have equal weight.", r"SI Section~3.1; Table~S11."),
 ("17", "pages 5--7", r"Clarify the negative sign in Eq. S11 and clarify how the highlighted pixels are the regions used for prediction.",
  r"The score is the negative loss, so positive weights mark regions whose activation reduces the loss; after the ReLU only these remain. Maps are normalized to $[0, 1]$ per image and shown without threshold.", r"SI Section~3.2; Fig.~4 caption."),
 ("18", "pages 5--7", r"In Algorithm 1, the initial line that estimates tendon lengths from intermediate positions via PCC appears unused because tendon lengths are read from encoders inside the loop. Remove it or explain its role.",
  r"It sets the encoder offset used inside the loop (see Comment~1); Algorithm~1 now shows this.", r"Algorithm~1; Section~3.3.2."),
 ("19", "pages 5--7", r"Use consistent Jacobian notation. J\_t2l, J\_l2p, and their learned representations currently alternate between a forward Jacobian, an inverse Jacobian, and a derivative of an inverse network. These might be confusing to follow for the readers.",
  r"One notation: $\mathbf{J}_{a \to b} = \partial b / \partial a$. PCC Jacobians are forward ($\mathbf{J}_{l \to t}$, $\mathbf{J}_{l \to p}$); learned ones carry a hat ($\hat{\mathbf{J}}_{t \to l}$, $\hat{\mathbf{J}}_{p \to l}$).", r"Section~3.3; Eqs.~7--10; Algorithms~1--2; Fig.~S3; Table~S2."),
 ("20", "pages 5--7", r"State whether the open-loop baselines use the same measured initial pose, planner, gains, stopping limits, and commanded waypoint sequence as the closed-loop methods. `Open-loop' and `feedforward' should be used consistently.",
  r"Same planner, waypoint spacing, damping, and targets. The initial state is measured once by motion capture and then propagated by the model; there is no convergence check. We use ``open-loop'' throughout.", r"Section~3.3.1; Figs.~6, 9, 10; Sections~4.1.4, 4.2.5."),
 ("21", "pages 8--11", r"State the denominator used for every percentage error. For example, clarify whether multi-section position errors are normalized by one section length, cumulative tip length, or the maximum deployed length.",
  r"Stated at first use: 150~mm (single section); 150, 300, and 450~mm, i.e., the length to the evaluated tip (multi-section pose); 450~mm (multi-section control).", r"Sections~4.1.1, 4.1.4, 4.2.1, 4.2.3, 4.2.4, 4.2.6."),
 ("22", "pages 8--11", r"Figure 5b intentionally uses nonuniform axis scaling. This visually distorts the reconstructed shapes. Use equal spatial scaling where possible or add a second undistorted view and explicit scale bars.",
  r"Done: equal axis scaling and a 20~mm scale bar; the caption no longer mentions non-uniform scaling.", r"Fig.~5b and caption."),
 ("23", "pages 8--11", r"Figure 7 alternates among `cumulative 3D error,' `sum of 3D errors,' and `average 3D error for each point.' Define the statistic exactly. Summing three points for the single-section arm and nine for the multi-section arm also prevents direct comparison. Per-point RMSE or error versus normalized arc length would be clearer.",
  r"Done: Fig.~7 now shows the error at each reference point versus normalized arc length for both arms (median and interquartile range); the statistic is defined.", r"Fig.~7 and caption; Sections~4.1.2, 4.2.2."),
 ("24", "pages 8--11", r"In Table 1, the text states that orientation error remains below 9 degrees, but several standard deviations are larger than the corresponding means. Make clear that only the mean is below 9 degrees and report median, 95th percentile, and maximum error.",
  r"Done. The text now says ``the mean is below $9^\circ$ (median below $7^\circ$)''. The large standard deviations come from 10 samples with inconsistent labels (Comment~29).", r"Table~1 (median, p95, max added); Section~4.2.1."),
 ("25", "pages 8--11", r"The claim that bent configurations improve accuracy is plausible but currently qualitative. The authors should plot error against bending angle before drawing this conclusion.",
  r"Plotted. Single section: the error decreases with bending (Spearman $\rho = """ + f"{rho:.2f}" + r"""$, $p < 0.001$); the claim is kept with this value. Multi-section: no clear dependence; the claim is removed.""", r"Fig.~S7; Sections~4.1.1, 4.2.1."),
 ("26", "pages 8--11", r"For Figs. 6, 9, and 10, identify the start direction, waypoint order, number of completed cycles, and whether the plotted paths are one run or an average. Add quantitative path errors in the caption or an accompanying table.",
  r"Done: each path is a single run of one counter-clockwise cycle starting at $(r, 0)$. Radial and height RMS errors are tabulated.", r"Captions of Figs.~6, 9, 10; Table~S7."),
 ("27", "pages 8--11", r"The discussion should distinguish demonstrated capabilities from proposed applications. Obstacle avoidance, whole-body grasping, surgical guidance, and force or contact sensing are future directions and were not evaluated here.",
  r"Done: these are now presented as future directions.", r"Section~5."),
 ("28", "SI", r"Fig. S2b should report the numerical N\_C error for each curvature model, the number of validation configurations, and whether the bars show standard deviation, standard error, or another interval.",
  r"Added: 20 configurations, one standard deviation, and the $N_C$ error for each model (see Comment~4).", r"Fig.~S2 caption; SI Section~4.2."),
 ("29", "SI", r"Table S6 contains highly skewed errors, particularly 11.92 +/- 25.10 mm for Section II and orientation standard deviations near 16 degrees. Report robust distribution summaries and discuss the outliers rather than relying only on mean and standard deviation.",
  r"Added median, interquartile range, 95th percentile, and maximum. The skew comes from 10 of 500 samples; 9 are three configurations recorded three times, whose motion-capture orientation labels imply $87^\circ$--$174^\circ$ bending (flipped rigid bodies). Without them, Section~II is $""" + f"{wo['II']['pos_mean']:.2f} \\pm {wo['II']['pos_std']:.2f}" + r"""$~mm instead of $11.92 \pm 25.10$~mm.""", r"Table~S6; Table~1; SI Section~6.1."),
 ("30", "SI", r"Figs. S4-S6 should use matched target identifiers or connecting pairs so the reader can compare the same workspace locations across controllers. Use consistent color limits when the goal is direct visual comparison.",
  r"Done: the same target IDs in every panel (matching Tables~S8 and S9) and one color scale per quantity.", r"Figs.~S4--S6 and captions."),
 ("31", "SI", r"Tables S3 and S4 list dataset fields but not dataset composition. Add sample counts per acquisition mode and robot configuration, including how many samples were removed and why.",
  r"Added counts, days, tendon ranges, logging, and split. Each configuration draws its mode with equal probability, so each mode is about one third by design; the mode is not stored per sample. \textbf{[FILL: removed samples and reason]}", r"Table~S12; SI Section~4.1."),
]
for k, grp, q, r, c in MINOR:
    P[k] = [(q, r, c)]


def block(points):
    out = []
    for q, r, c in points:
        out.append(f"\\rc{{{q}}}\n\\textbf{{Response.}} {r}" + (f"\n\n\\textit{{Changes:}} {c}" if c else ""))
    return "\n\n".join(out) + "\n"


for k, pts in P.items():
    open(f"{SN}/resp_{k}.tex", "w").write(block(pts))

heads = [(1, "Response to the Editor", None), (2, "Editor's points", "G"),
         (1, "Response to Reviewer 1", None), (2, "Overall assessment", "overall"), (2, "Major comments", None)] + \
        [(3, f"Comment {i}", str(i)) for i in range(1, 11)] + [(2, "Minor comments", None)] + \
        [(3, f"Comment {k} ({g})" if g != "SI" else f"Comment {k} (Supporting Information)", k) for k, g, *_ in MINOR if g != "SI"] + \
        [(2, "Supporting Information", None)] + [(3, f"Comment {k}", k) for k, g, *_ in MINOR if g == "SI"]
CMD = {1: "section", 2: "subsection", 3: "subsubsection"}
L = [r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=2.2cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb,xcolor,needspace,enumitem}
\setlist{nosep,leftmargin=1.5em,topsep=2pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\newcommand{\rc}[1]{\begin{quote}\color{black!70}\itshape #1\end{quote}}
\begin{document}
{\Large\bfseries Response to the editor and the reviewer}\\[4pt]
Manuscript 3400076, ``Internal Camera-based Reconstruction and Closed-loop Control of Soft Robotic Arms''

Dear Dr.\ Murray,

We thank you and the reviewer for the careful evaluation of our manuscript. We revised the manuscript and the Supporting Information point by point. Each comment is quoted in italics, followed by our response and the corresponding changes, which are highlighted in the manuscript. Major comments keep the reviewer's numbering (1--10); minor and SI comments are numbered 11--31 in the order of the report.
"""]
for lev, h, k in heads:
    L.append(f"\\needspace{{{14 - 2 * lev}\\baselineskip}}\\{CMD[lev]}*{{{h}}}")
    if k:
        L.append(block(P[k]).strip())
L.append(r"""\bigskip
Sincerely,\\
Lorenzo Vignoli, Guanran Pei, Francesco Braghin, and Josie Hughes
\end{document}""")
open(f"{SN}/response_letter.tex", "w").write("\n\n".join(L) + "\n")
print(len(P), "response blocks written")
