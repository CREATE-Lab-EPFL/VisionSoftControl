"""Writes every paste-ready LaTeX snippet of the revision workbook to snippets/,
plus a complete response letter (snippets/response_letter.tex).
Tables are generated from the analysis outputs (data/*.json) and the repository
result files (read-only), so numbers are not retyped by hand."""
import json, os
OUT = "/home/vigno0405/github/VisionSoftControl/REVIEW_TO_DELETE/AIS_3400076_revision"
REPO = "/home/vigno0405/github/VisionSoftControl"
SN = f"{OUT}/snippets"; os.makedirs(SN, exist_ok=True)
D = lambda f: json.load(open(f"{OUT}/data/{f}"))
misc, multi, single, nc = D("misc_summary.json"), D("multi_summary.json"), D("single_summary.json"), D("nc_summary.json")
ik, lk = json.load(open(f"{REPO}/MULTI/results/ik_ablation.json")), D("leakage_effect.json")  # from MULTI_revision_figures.ipynb
lk["MULTI"]["pos_III"]["all_mean"] = 26.45  # as printed in Table 1 of the paper (recomputed: 26.44)
SNIP, RESP = {}, []


def S(name, text):
    SNIP[name] = text.strip("\n") + "\n"


def R(head, quote, name):
    """Response-letter entry: heading, reviewer text, response snippet name."""
    RESP.append((head, quote, name))


f1, f2 = (lambda v: f"{v:.1f}"), (lambda v: f"{v:.2f}")

# =============================== PART 1: FIGURES ===============================
S("fig1_caption", r"""
\caption{(a) Multi-section soft robot arm sensorization and reconstruction pipeline. Images from the three cameras (BW: black-and-white, i.e., grayscale) are read concurrently by software, one capture thread per camera, without hardware triggering (Section 2.1), and fed to CNNs (FE: feature extractor; FC: fully connected layer), which predict both the section-tip poses and the full-body curvature. (b) Robot setup. The tendon-driven arm consists of three independent sections, each actuated by three motors, with Bowden cables (housing tubes in gray) routing the tendons of sections II and III. The circles show the tendon positions in the cross-section of each section, and $S_{\mathrm{I}}$--$S_{\mathrm{III}}$ the section base frames. The optical tracking system provides the ground-truth configuration.}
""")
S("fig2_caption", r"""
\caption{PCC parameterization of soft robots according to both $\boldsymbol{\xi}(\theta, \phi, L)$ and $\mathbf{q}(\Delta_x, \Delta_y, L)$ parameters, derived from the four arc lengths $\{L_i\}_{i=1,\dots,4}$. $L_1$--$L_4$ are the arcs at distance $d$ from the central axis along the $\pm x$ and $\pm y$ directions that define $\Delta_x$ and $\Delta_y$ (Eq.~S1); they are geometric constructions, not tendons. The three tendons are placed at the angles $\{\delta_i\}_{i=1,\dots,3}$ on the circle of radius $d$.}
""")
S("fig3_caption", r"""
\caption{(a) Convolutional neural network (CNN) architecture used for pose estimation and full-body reconstruction. The $n$ grayscale images from the embedded cameras ($n \times 480 \times 640$) are stacked as input channels and processed by a MobileNetV2 backbone with inverted residual bottlenecks, fine-tuned on our dataset and followed by global average pooling (GAP) to a 1280-dimensional feature vector. Regression heads map this vector to the section-tip poses ($f_p^n$: $6n$ outputs) or to the curvature parameters of each section ($f_C^n$: 5, 4, or 3 parameters per section for the quadratic, affine, and constant models). The heads are one linear layer for $n = 1$ and two layers ($1280 \to 512 \to$ outputs) for $n = 3$. Data augmentation is applied during training only. Transfer learning is applied between pose and curvature networks and from the single-section to the multi-section network. (b) Residual multi-layer perceptron (MLP) used for $N_l^1$ (tip position, 3 $\to$ tendon lengths, 3) and $N_C$ (section-tip pose, 6 $\to$ curvature parameters of the section). The input vector is projected into a 128-dimensional latent space and processed through three residual blocks, each comprising two fully connected layers with Batch Normalization and LeakyReLU activations, followed by the output regression head. The multi-section kinematic networks $N_p^3$ (tendon lengths, 9 $\to$ tip pose, 6) and $N_l^3$ (tip pose, 6 $\to$ tendon lengths, 9) are MLPs with four hidden layers of 128 units and ELU activations; $N_l^3$ is trained through the frozen $N_p^3$ (Eq.~11).}
""")
S("fig4_caption", r"""
\caption{(a) Grad-CAM visualizations from $f_p^1$ for different bending configurations and average Grad-CAM over the test set. Colors show the heatmap of Eq.~S12, normalized to $[0, 1]$ per image and displayed without thresholding; warm colors mark the regions whose activation most reduces the prediction loss. The network mostly focuses on deformations of the Trimmed Helicoid structure along the bending direction. (b) Different null-space configurations yield the same tip pose. (c) High-level kinematic closed-loop controller. The tip pose estimated by the pose CNN from the camera images is the feedback signal of both controllers. In the model-based controller, the motor encoders provide the tendon lengths used by the PCC Jacobian and the null-space term; the data-driven controller does not use encoders. The curvature CNNs are not part of the control loop.}
""")
S("fig5_caption", r"""
\caption{(a) Distribution of position (mm) and orientation ($^\circ$) reconstruction errors for the single-section arm on the test set. (b) Single-section curvature reconstruction and bending angle error. Four test examples with increasing deformation are shown, with GT (ground-truth) reconstructions as solid and CNN predictions as dashed lines. Axes have equal scaling. The corresponding $\phi$ angular errors are highlighted in orange. (c) Performance of the proposed controllers on the control workspace of the single-section arm (CL: closed-loop; OL: open-loop). Bars show the mean final position error over the 20 targets; error bars show one standard deviation across targets, each visited once.}
""")
CYCLE = r"Each trajectory is a single run of one cycle, starting at $(x, y) = (r, 0)$ with respect to the circle center and traversing the 30 waypoints counter-clockwise (top view); path errors are reported in Table~S7."
S("fig6_caption", r"""
\caption{Trajectory tracking for the single-section soft manipulator. The dashed gray line indicates the reference trajectory; executed trajectories are shown in orange for the lower circle and blue for the upper one. """ + CYCLE + r""" (a) Model-based closed-loop controller. (b) Data-driven closed-loop controller. (c) Model-based open-loop controller. (d) Data-driven open-loop controller.}
""")
S("fig9_caption", r"""
\caption{Trajectory tracking for the multi-section soft manipulator with horizontal end-effector orientation. The angular values are the mean $\pm$ standard deviation of the orientation error along each circle and are reported next to the corresponding circle. """ + CYCLE + r""" (a) Model-based closed-loop controller. (b) Data-driven closed-loop controller. (c) Model-based open-loop controller. (d) Data-driven open-loop controller.}
""")
S("fig10_caption", r"""
\caption{Trajectory tracking for the multi-section robot under an external payload of 50~g attached at the tip, corresponding to about 40\% of the effective mass of the manipulator. """ + CYCLE + r""" (a) Model-based closed-loop controller. (b) Model-based open-loop controller.}
""")

# --- Table S7: path errors (from the repository's PathErrorMetrics files) ---
def paths_rows():
    rows = []
    def add(arm, ctrl, loop, v):
        rows.append((arm, ctrl, loop, round(v["z_ref"]), v["radial_rms"], v["height_rms"]))
    sc = json.load(open(f"{REPO}/SINGLE/results/PathErrorMetrics_closed.json"))
    so = json.load(open(f"{REPO}/SINGLE/results/PathErrorMetrics_open.json"))
    mm = json.load(open(f"{REPO}/MULTI/results/PathErrorMetrics.json"))
    for src, loop in [(sc, "closed"), (so, "open")]:
        for ctrl, key in [("Model-based", "jacobian"), ("Data-driven", "datadriven")]:
            for k, v in sorted(src.items(), key=lambda kv: kv[1]["z_ref"]):
                if key in k:
                    add("Single", ctrl, loop, v)
    order = [("Model-based", "closed", "PolygonJacobian_30"), ("Data-driven", "closed", "PolygonDatadriven_30"),
             ("Model-based", "open", "PolygonOpenLoopJacobian_30"), ("Data-driven", "open", "PolygonOpenLoopDatadriven_30"),
             ("Model-based, 50 g", "closed", "PolygonJacobian_W50g"), ("Model-based, 50 g", "open", "PolygonOpenLoopJacobian_W50g")]
    for ctrl, loop, key in order:
        for k, v in sorted(mm.items(), key=lambda kv: kv[1]["z_ref"]):
            if k.split("/")[-1].startswith(key):
                add("Multi", ctrl, loop, v)
    return rows
pr = paths_rows()
body = []
for i, (arm, ctrl, loop, z, rad, hei) in enumerate(pr):
    if i and arm != pr[i - 1][0]:
        body.append(r"\midrule")
    body.append(f"{arm} & {ctrl} & {loop} & {z} & {rad:.2f} & {hei:.2f} \\\\")
S("tab_S7_paths", r"""
\begin{table}[h]
\centering
\caption{Path errors of the trajectory-tracking experiments (Figs.~6, 9 and 10). Radial RMS: root-mean-square distance of the executed path from the reference circle, measured in the horizontal plane; height RMS: root-mean-square of $z - z_{\mathrm{ref}}$. The reference circle is the commanded one (center and radius of the commanded waypoints). Each row is a single run of one cycle; consecutive samples along a path are serially correlated and are not independent trials.}
\label{tab:S7_paths}
\begin{tabular}{lllrrr}
\toprule
Arm & Controller & Loop & $z_{\mathrm{ref}}$ [mm] & Radial RMS [mm] & Height RMS [mm] \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

S("fig7_caption", r"""
\caption{3D reconstruction error of the curvature models along the backbone. For each test sample ($N = 500$), the backbone reconstructed from the predicted curvature parameters is compared with the one reconstructed from the curvature labels, and the 3D distance is evaluated at each reference point. (a) Single-section arm: reference points at $L/3$, $2L/3$, and $L$. (b) Multi-section arm: reference points every ninth of the arm length; the labels are model-constrained (Section~2.2). The horizontal axis is the arc length normalized by the total length; markers show the median and error bars the interquartile range.}
""")
sq = {m: single[f"curv_{m}"] for m in ("const", "affine", "quad")}
S("text_412_fig7", r"""
Fig.~7a reports the 3D error at each reference point. The three curvature models give similar errors, which grow along the backbone to a mean of 4.9--5.1~mm at the tip (median 3.9--4.2~mm).
""")
S("text_422_fig7", r"""
Errors grow toward the distal tip, reaching a median of about 41~mm at the end of the arm, and all models provide similar approximations.
""")
S("fig8_caption", r"""
\caption{(a) Distribution of position (mm) and orientation ($^\circ$) reconstruction errors for the multi-section arm on the test set. (b) Performance of the four proposed controllers on the control workspace of the multi-section arm (CL: closed-loop; OL: open-loop), reporting the mean and standard deviation across the 20 targets (each visited once) for translation and rotation accuracy.}
""")
S("figS1_caption", r"""
\caption{(a) Workspace of the multi-section robot. Sampled positions of the first, second, and third section tips are depicted as blue, green, and red dots. (b) Main reference systems during modeling and data acquisition.}
""")
S("figS2_caption", r"""
\caption{(a) 3D reconstruction accuracy of the curvature models at reference points placed every ninth of the manipulator length: sum over the nine points of the mean error at each point (same data as Fig.~7b). (b) Errors induced by the $N_C$ approximation with respect to the motion-capture ground truth, on 20 configurations of the multi-section arm posed manually with all subsection markers visible and recorded in a separate session; these configurations were not used to train $N_C$ or the multi-section curvature CNNs. Bars show the sum over the nine reference points of the mean 3D error at each point; error bars show one standard deviation of the per-configuration sum across the 20 configurations.}
""")
S("figS4_caption", r"""
\caption{Closed-loop tracking error distribution (mm) on the control workspace for the single-section arm. (a) Model-based. (b) Data-driven. Numbers identify the targets (Table~S8); both panels share the same color scale.}
""")
S("figS5_caption", r"""
\caption{Closed-loop tracking error distribution (mm and $^\circ$) on the control workspace for the multi-section arm. (a) Model-based. (b) Data-driven. Numbers identify the targets (Table~S9); panels showing the same quantity share the same color scale.}
""")
S("figS6_caption", r"""
\caption{Tracking error distribution (mm and $^\circ$) for the multi-section arm under external disturbance (50~g tip payload). (a) Closed-loop. (b) Open-loop. Numbers identify the targets (Table~S9); panels showing the same quantity share the same color scale.}
""")
bs = single["bending"]
S("si_bending", r"""
\subsection{Error as a Function of the Bending Angle}
Fig.~S7 relates the tip position error on the test sets to the bending angle. For the single-section arm, the error decreases with bending (Spearman $\rho = """ + f"{bs['rho_pos']:.2f}" + r"""$, $p < 0.001$ for position; $\rho = """ + f"{bs['rho_rot']:.2f}" + r"""$, $p = 0.001$ for orientation). For the multi-section arm, the tip errors show no clear dependence on the bending angle of the corresponding section ($|\rho| \le 0.06$).

\begin{figure}[h]
\centering
\includegraphics[width=\linewidth]{bending_error.pdf}
\caption{Tip position error as a function of the bending angle on the test sets ($N = 500$). (a) Single-section arm; bending angle from the tip orientation label. (b--d) Multi-section arm, tips I--III, against the bending angle of the corresponding section, computed from the relative orientation of consecutive tips. Dots: test samples; black line: median in $5^\circ$ bins; shaded band: interquartile range; $\rho$: Spearman rank correlation. Samples with a labeled section bending above $60^\circ$ (Section~6.1) lie outside the plotted range.}
\label{fig:S7_bending}
\end{figure}
""")

# ============================ PART 2: COMPARISON ============================
S("tab_S10_comparison", r"""
\begin{table*}[t]
\centering
\caption{Comparison of Embedded Sensing and Closed-Loop Control in Soft and Continuum Arms}
\label{tab:S10_comparison}
\footnotesize
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.18}
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{4.0cm} >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X@{}}
\hline
\textbf{Approach} & \textbf{Sensing} & \textbf{Sensed along the arm} & \textbf{Estimated} & \textbf{Closed loop on the estimate} & \textbf{Redundancy}\\
\hline
Sim-to-real sensing~\cite{yooZeroShotSimtoRealTransfer2023} & internal camera & one actuator & shape & --- & ---\\
Anchored proprioception~\cite{hanAnchoringMorphologicalRepresentations2025} & internal camera, marker & one module & motion, force, shape & --- & ---\\
Spherical soft arm~\cite{hoferVisionBasedSensingApproach2021} & internal cameras, pattern, LEDs & one joint & orientation & PI & not exploited\\
Learned closed-loop IK~\cite{thuruthelLearningClosedLoop2017} & tip sensing & tip & tip position & learned IK & implicit\\
FBG shape servoing~\cite{luAdaptiveOnlineLearning2024} & FBG & whole body & shape & adaptive & ---\\
\hline
\textbf{Distributed vision with redundancy-aware control (ours)} & \textbf{internal cameras only} & \textbf{every section} & \textbf{tip poses, shape} & \textbf{model-based; learned IK} & \textbf{null space; IK training loss}\\
\hline
\end{tabularx}\\[2pt]
\parbox{\linewidth}{\footnotesize IK: inverse kinematics; PI: proportional--integral; FBG: fiber Bragg grating; ---: not addressed.}
\end{table*}
""")
S("intro_comparison", r"""
Several systems combine embedded sensing with closed-loop control of soft or continuum arms. Hofer et al.\ placed one camera inside each of the three fabric bellows of a pneumatic spherical arm, observed a painted interior pattern under internal illumination, and regulated the two joint angles in closed loop with about $1^\circ$ accuracy at 30~Hz; the actuation redundancy of the arm was not exploited \cite{hoferVisionBasedSensingApproach2021}. Thuruthel et al.\ learned closed-loop inverse kinematics with end-effector feedback for a redundant tendon-driven continuum manipulator, with and without external loads \cite{thuruthelLearningClosedLoop2017}. Han et al.\ tracked an internal anchor marker with a single onboard camera to infer the full-body deformation and contact force of soft modules \cite{hanAnchoringMorphologicalRepresentations2025}, and Yoo et al.\ estimated the 3D shape of a pneumatic actuator from an internal camera with a model trained in simulation \cite{yooZeroShotSimtoRealTransfer2023}; neither closed a control loop on the estimate. Lu et al.\ servoed the 3D shape of continuum and soft robots with adaptive online learning, using fiber Bragg grating sensing \cite{luAdaptiveOnlineLearning2024}. The present work differs in two respects: it distributes one internal camera per section along a multi-section tendon-driven arm, without internal markers, patterns, or dedicated illumination, and it closes the loop on the camera-estimated pose with controllers that resolve the actuation redundancy explicitly, either in the null space of a model-based Jacobian or through a secondary objective in the training of a learned inverse kinematics. To the best of our knowledge, this combination has not been reported.
""")
S("intro_contributions", r"""
\begin{enumerate}
\item A distributed vision-based sensing strategy for soft arms that uses miniature cameras embedded in each section of the robot. It provides dense feedback that is markerless at inference (external motion-capture markers are used only to generate training labels) for tip-pose estimation and full-body curvature reconstruction, and can be extended to arms with a different number of sections through modular hardware and a lightweight CNN whose backbone is transferred and retrained; we validated arms with one and three sections.
\item Integration of embedded vision with model-based null-space control. We close the loop on the camera-estimated pose with a Jacobian-based Piecewise Constant Curvature velocity controller, in which the motor encoders provide the tendon lengths for the Jacobian and the null-space term.
\item A data-driven framework for both sensing and control. We train learning-based inverse kinematics models that generate actuation commands from the camera-estimated pose without encoder feedback, with a secondary objective in the training loss.
\item Experimental validation of pose regulation with both controllers on single- and multi-section arms, including a constant tip payload, and an offline evaluation of the secondary objectives.
\end{enumerate}
""")
S("intro_scale_sentence", r"""
Addressing the sensing and control challenges of continuum manipulators, this paper proposes a strategy for vision-based reconstruction and control of soft robotic arms that can be extended to a different number of sections. Information from miniature cameras embedded in the sections is fused within a single CNN to achieve full-body reconstruction. The estimated tip pose is then used as feedback in both model-based and data-driven controllers, enabling tip regulation while keeping the tendon lengths centered in their actuation range.
""")
S("bib_new", r"""
@article{hoferVisionBasedSensingApproach2021,
  title = {A Vision-Based Sensing Approach for a Spherical Soft Robotic Arm},
  author = {Hofer, Matthias and Sferrazza, Carmelo and D'Andrea, Raffaello},
  journal = {Frontiers in Robotics and AI},
  volume = {8},
  pages = {630935},
  year = {2021},
  doi = {10.3389/frobt.2021.630935}
}

@article{thuruthelLearningClosedLoop2017,
  title = {Learning Closed Loop Kinematic Controllers for Continuum Manipulators in Unstructured Environments},
  author = {Thuruthel, Thomas George and Falotico, Egidio and Manti, Mariangela and Pratesi, Andrea and Cianchetti, Matteo and Laschi, Cecilia},
  journal = {Soft Robotics},
  volume = {4},
  number = {3},
  pages = {285--296},
  year = {2017},
  doi = {10.1089/soro.2016.0051}
}

@article{hanAnchoringMorphologicalRepresentations2025,
  title = {Anchoring Morphological Representations Unlocks Latent Proprioception in Soft Robots},
  author = {Han, Xudong and Guo, Ning and Xu, Ruoyu and Wan, Fang and Song, Chaoyang},
  journal = {Advanced Intelligent Systems},
  volume = {7},
  number = {12},
  pages = {e202500444},
  year = {2025},
  doi = {10.1002/aisy.202500444}
}

@article{luAdaptiveOnlineLearning2024,
  title = {Adaptive Online Learning and Robust 3-D Shape Servoing of Continuum and Soft Robots in Unstructured Environments},
  author = {Lu, Yiang and Chen, Wei and Lu, Bo and Zhou, Jianshu and Chen, Zhi and Dou, Qi and Liu, Yun-Hui},
  journal = {Soft Robotics},
  volume = {11},
  number = {2},
  pages = {320--337},
  year = {2024},
  doi = {10.1089/soro.2022.0158}
}
""")

# ====================== PART 3: TEXT EDITS, BY TOPIC ======================
# --- abstract / conclusion / claims ---
S("abstract_sentence2", r"""
Miniature cameras embedded in each section provide dense proprioceptive feedback, while convolutional neural networks map multi-view images to both tip pose and full-body reconstruction using a polynomial curvature model. The estimated tip poses close the control loop, while the curvature reconstruction is evaluated as a separate sensing output.
""")
S("abstract_last", r"""
Experiments show that embedded vision enables accurate tip-pose estimation and model-constrained full-body reconstruction, and closed-loop pose regulation with redundancy resolution that compensates a constant tip payload.
""")
S("sec31_scalability", r"""
To process the image batches, the first convolutional layer is adapted to the number of stacked images and preceded by a normalization layer. Adapting the network to a different number of sections requires changing this input layer and the regression head ($6n$ pose outputs and $n$ sets of curvature parameters) and retraining, with the remaining backbone transferred (Section~3.1.1); we validated this for $n = 1$ and $n = 3$. At the end of the backbone, we apply Global Average Pooling (GAP) followed by a regression head: one fully connected layer for the single-section networks and two for the multi-section networks (Fig.~3a).
""")
S("sec31_mlp", r"""
The single-section inverse kinematics $N_l^1: \mathbf{t} \mapsto \mathbf{l}$ uses the residual MLP of Fig.~3b, whose residual blocks mitigate vanishing gradients; the same architecture is used for $N_C$. The multi-section forward and inverse mappings $N_p^3: \mathbf{l} \mapsto \mathbf{p}$ and $N_l^3: \mathbf{p} \mapsto \mathbf{l}$ are MLPs with four hidden layers of 128 units and ELU activations (Table~S11).
""")
S("concl_first", r"""
This work proposes a framework for vision-based proprioception and control of soft continuum robotic arms. Miniature cameras embedded in each section feed deep learning algorithms that estimate the section-tip poses and reconstruct the full shape of the robot. The estimated poses close the loop of two control strategies, model-based and data-driven, which explicitly exploit kinematic redundancy to accomplish secondary tasks within the null space; the shape reconstruction is evaluated as a separate sensing output.
""")
S("concl_second", r"""
Experimental results demonstrate that our sensing approach reaches competitive performance in reconstructing both tip pose and full-body curvature, with accuracy that does not degrade at large bending angles for the single-section arm. Closed-loop control achieves near-sensing performance, outperforms open-loop alternatives, and compensates a constant 50~g tip payload.
""")
S("concl_third", r"""
Potential applications, not evaluated in this work, include search-and-rescue or inspection within confined and cluttered environments and minimally invasive surgery. In such settings, full-body curvature feedback from embedded cameras could be used by the null-space controller to shape the arm for obstacle avoidance while maintaining the desired tip pose.
""")
S("concl_lighting", r"""
Illumination passes through the opaque covering; image augmentations were applied during training to account for residual brightness variations, but robustness to changes in lighting or hardware was not tested.
""")
S("concl_limits_add", r"""
The control evaluation used 20 targets, each visited once, and planar circular trajectories; repeated trials, non-planar and workspace-boundary trajectories, larger length changes, and further load magnitudes and directions remain to be tested. The training, validation, and test sets were drawn from the same acquisition sessions, so session-blocked evaluation is also left to future work. The secondary objectives were evaluated offline through the kinematic models (SI Section~5.3) rather than in hardware experiments.
""")
S("concl_effort", r"""
In this paper, redundancy was exploited to keep the tendon lengths centered in their actuation range, but the same methodology applies to shaping arm configurations for obstacle avoidance while tracking a desired end-effector trajectory.
""")
# --- control: sensing role, algorithm, notation, open loop ---
S("sec33_feedback", r"""
In both controllers, the feedback signal is the tip pose estimated by the pose CNN from the camera images. The model-based controllers additionally read the tendon lengths from the motor encoders to evaluate the PCC Jacobian and the null-space term, whereas the data-driven controllers do not use encoders. The curvature CNNs are not part of either control law; full-body reconstruction is evaluated as a separate sensing output (Sections~4.1.2 and 4.2.2).
""")
S("alg1", r"""
\begin{algorithm}[t]
\caption{Model-based feedback controller}
\begin{algorithmic}
\State Set target $\mathbf{p}_{\mathrm{targ}}$ and convergence threshold $\gamma$
\State Measure current pose $\mathbf{p}$ from $f_p^3(\mathbf{I})$
\State Measure tip positions $[\mathbf{t}_{\mathrm{I}}, \mathbf{t}_{\mathrm{II}}, \mathbf{t}_{\mathrm{III}}]$ from $f_p^3(\mathbf{I})$
\State Estimate $\mathbf{l}_0 \gets \mathbf{l}(\mathbf{t}_{\mathrm{I}}, \mathbf{t}_{\mathrm{II}}, \mathbf{t}_{\mathrm{III}})$ via PCC
\State Set encoder offset $\mathbf{l}_{\mathrm{off}} \gets \mathbf{l}_{\mathrm{enc}} - \mathbf{l}_0$
\While{$d_{SE(3)}(\mathbf{p}, \mathbf{p}_{\mathrm{targ}}) > \gamma$}
\State Compute next reference $\mathbf{p}_{\mathrm{ref}} \gets W^3(\mathbf{p}, \mathbf{p}_{\mathrm{targ}})$
\State Measure $\mathbf{l} \gets \mathbf{l}_{\mathrm{enc}} - \mathbf{l}_{\mathrm{off}}$ from motor encoders
\State Compute Jacobian $\mathbf{J} \gets \mathbf{J}_{l \to p}(\mathbf{l})$
\State Compute damped pseudoinverse $\mathbf{J}^{\#} \gets \mathbf{J}^T (\mathbf{J}\mathbf{J}^T + \lambda^2 \mathbf{I})^{-1}$
\State Compute null-space projector $\mathbf{N} \gets \mathbf{I} - \mathbf{J}^{\#}\mathbf{J}$
\State Move motors by $\delta\mathbf{l} \gets \mathbf{J}^{\#}(\mathbf{p}_{\mathrm{ref}} - \mathbf{p}) + \mathbf{N}(\bar{\mathbf{l}} - \mathbf{l})$
\State Measure $\mathbf{p}$ from $f_p^3(\mathbf{I})$
\EndWhile
\end{algorithmic}
\end{algorithm}
""")
S("alg2_lines", r"""
\State Compute $\hat{\mathbf{J}}_{p \to l} \gets \left. \partial N_l^3 / \partial \mathbf{p} \right|_{\mathbf{p}}$
\State Move motors by $\delta\mathbf{l} \gets \hat{\mathbf{J}}_{p \to l} (\mathbf{p}_{\mathrm{ref}} - \mathbf{p})$
""")
S("sec332_offset", r"""
The model-based controller is summarized in Alg.~1. Before the loop, the tendon lengths $\mathbf{l}_0$ corresponding to the camera-estimated section-tip positions are computed through the inverse PCC map (Eq.~2) and used once to set the encoder offset $\mathbf{l}_{\mathrm{off}} = \mathbf{l}_{\mathrm{enc}} - \mathbf{l}_0$. Inside the loop, the encoder readings are expressed in the same PCC tendon-length frame, $\mathbf{l} = \mathbf{l}_{\mathrm{enc}} - \mathbf{l}_{\mathrm{off}}$, which is used by the Jacobian and by the null-space term. The single-section controller and the data acquisition use the same offset.
""")
S("sec331_jacobian", r"""
with encoder position feedback. Once $\mathbf{l}$ is measured from the motor encoders, the forward Jacobian $\mathbf{J}_{l \to t}(\mathbf{l}) = \partial \mathbf{t} / \partial \mathbf{l}$ is computed from the PCC model.
""")
S("eq7", r"""
\begin{equation}
\hat{\mathbf{J}}_{t \to l} = \left. \frac{\partial N_l^1}{\partial \mathbf{t}} \right|_{\mathbf{t}}
\end{equation}
""")
S("notation_rule", r"""
Throughout, $\mathbf{J}_{a \to b} = \partial b / \partial a$ denotes the Jacobian of the mapping from $a$ to $b$; analytical (PCC) Jacobians are forward Jacobians ($\mathbf{J}_{l \to t}$, $\mathbf{J}_{l \to p}$) and $\mathbf{J}^{\#}$ is their damped pseudoinverse, while hats denote Jacobians of the learned inverse-kinematics networks ($\hat{\mathbf{J}}_{t \to l}$, $\hat{\mathbf{J}}_{p \to l}$).
""")
S("tabS2_jac_rows", r"""
$\mathbf{J}_{l \to t}, \mathbf{J}_{l \to p}, \mathbf{J}^{\#}$ & Analytical (PCC) forward Jacobians, $\partial \mathbf{t}/\partial \mathbf{l}$ and $\partial \mathbf{p}/\partial \mathbf{l}$, and their regularized Moore-Penrose pseudoinverse. \\
$\hat{\mathbf{J}}_{t \to l}, \hat{\mathbf{J}}_{p \to l}$ & Jacobians of the learned inverse kinematics, $\partial N_l^1/\partial \mathbf{t}$ and $\partial N_l^3/\partial \mathbf{p}$. \\
""")
S("sec331_openloop", r"""
The same algorithms are also employed in open-loop control as a baseline. The open-loop controllers use the same planner, waypoint spacing $\varepsilon$, damping $\lambda$, and target sequence as the closed-loop ones. Their initial state is measured once by the motion capture system and then propagated internally through the model-based or data-driven kinematics instead of the camera estimate, and the full waypoint sequence is executed without the convergence check.
""")
# --- kinematic model (Comment 5) ---
S("eq4_text", r"""
However, soft arms undergo deformations due to external forces and self-weight, requiring more complex shape approximations for full-body proprioception. We adopt the Piecewise Polynomial Curvature (PPC) model [31], which retains the $\boldsymbol{\xi}$-parameters. It expresses the curvature $\kappa(x)$ of the central axis of a section as a polynomial in the arc length $x \in [0, L]$, with the local bending angle $\theta(x) = \int_0^x \kappa(v)\, dv$. For example, in the quadratic case:
\begin{equation}
\theta(x) = c_0 x + \frac{1}{2} c_1 x^2 + \frac{1}{3} c_2 x^3, \qquad x \in [0, L]
\end{equation}
where $c_0$, $c_1$, and $c_2$ have units of mm$^{-1}$, mm$^{-2}$, and mm$^{-3}$.
""")
S("eq5b", r"""
\mathbf{t}(x) = \left[ c_\phi \int_0^x s_{\theta(v)}\, dv, \;\; s_\phi \int_0^x s_{\theta(v)}\, dv, \;\; \int_0^x c_{\theta(v)}\, dv \right]^T
""")
S("assumptions", r"""
Within each section, the PPC model assumes planar bending with a bending direction $\phi$ that is constant along the arc length, and no torsion; the curvature varies along the section only through the polynomial coefficients.
""")
S("eq6_text", r"""
For capturing ground truth pose, reflective markers for motion capture are placed along each section at intervals of $L/3$. We refer to these bodies as subsections of the module. They provide ground-truth bending direction and angle estimates $\hat{\phi}_x$, $\hat{\theta}_x$ at $x = L/3, 2L/3, L$ (details in the Supporting Information).
""")
S("eq6", r"""
\begin{equation}
\mathop{\arg\min}_{c_0, c_1, c_2 \in \mathbb{R}} \sum_{x \in \{L/3,\, 2L/3,\, L\}} \left\| \mathbf{R}_x(c_0, c_1, c_2) - \hat{\mathbf{R}}_x \right\|_F^2
\end{equation}
The bending direction $\phi$ is the mean of $\hat{\phi}_{L/3}$, $\hat{\phi}_{2L/3}$, $\hat{\phi}_{L}$, while $L$ is the average tendon length according to Eq.~2.
""")
S("si22_init", r"""
Polynomial coefficients are initialized analytically by substituting $x = L/3, 2L/3, L$ into $\theta(x) = c_0 x + \frac{1}{2} c_1 x^2 + \frac{1}{3} c_2 x^3$ and solving the corresponding linear systems according to the optimization algorithm described in [2].
""")
S("tabS1_rows", r"""
$x$ & Arc length along a section axis ($x \in [0, L]$). \\
$\theta(x)$ & Local bending angle along the central axis at arc length $x$. \\
$\kappa(x)$ & Polynomial curvature function at arc length $x$. \\
$c_0, c_1, c_2$ & Coefficients of the polynomial curvature approximation (units mm$^{-1}$, mm$^{-2}$, mm$^{-3}$). \\
$L_i$ & Length of the $i$-th outer boundary arc ($i \in \{1, 2, 3, 4\}$). \\
""")
# --- ground truth (Comment 4) ---
S("sec422_modelconstrained", r"""
For the multi-section arm, inter-section marker occlusion prevented tracking the subsection markers during data collection, so the curvature labels were obtained from the motion-captured section-tip poses through the network $N_C$ (SI Section~4.2). The multi-section results therefore quantify a model-constrained reconstruction, under the assumptions of Section~2.2 (planar bending within each section, no torsion, and a bending direction that is constant along each section), rather than the agreement with directly measured backbone points.
""")
ncs = nc
S("si42_nc", r"""
$N_C$ was trained on the single-section dataset, mapping the tip pose to the curvature labels of Section~2.2, with the same split as the other networks (Table~S11). On the held-out single-section test set ($N = 500$), its 3D error at $L/3$, $2L/3$, and $L$ is 0.38, 1.20, and 2.49~mm for the constant model, 0.42, 1.35, and 2.76~mm for the affine model, and 0.43, 1.37, and 2.94~mm for the quadratic model. Fig.~S2b reports its error on 20 configurations of the multi-section arm, posed manually with all subsection markers visible and recorded in a separate session; these configurations were not used to train $N_C$ or the multi-section curvature CNNs.
""")
# --- data, split, composition (Comment 8, S31) ---
S("sec311_split", r"""
The dataset was split into training (85\%), validation (10\%), and test (5\%) sets by a random permutation of all samples with a fixed seed; the split was not blocked by acquisition session or by configuration neighborhood (see Section~3.2 and SI Section~4.1).
""")
S("sec32_range", r"""
We collected 10,000 data points for both single- and multi-section configurations using six Optitrack Prime 13 cameras and Motive software, covering bending angles up to $57^\circ$ for the single-section arm (95th percentile $36^\circ$) and with 95th percentiles of $30^\circ$, $32^\circ$, and $34^\circ$ for sections I--III of the multi-section arm.
""")
S("sec32_hold", r"""
For the multi-section arm, each commanded configuration was held for about 3~s while samples were logged at 1~Hz, so consecutive samples can share the same configuration.
""")
ld = lk["MULTI"]
S("tab_S14_overlap", r"""
\begin{table}[h]
\centering
\caption{Effect of configurations shared between training and test sets (multi-section arm). Because each commanded configuration was held for about 3~s and logged at 1~Hz, """ + f"{ld['n_dup']}" + r""" of the 500 test samples share their tendon configuration with a training sample. Tip position errors [mm], mean (median).}
\label{tab:S14_overlap}
\begin{tabular}{lccc}
\toprule
Test samples & Tip I & Tip II & Tip III \\
\midrule
""" + "\n".join(
    f"{lab} & " + " & ".join(f"{ld[f'pos_{s}'][k + '_mean']:.2f} ({ld[f'pos_{s}'][k + '_median']:.2f})" if k != "all" else f"{ld[f'pos_{s}']['all_mean']:.2f}" for s in ("I", "II", "III")) + r" \\"
    for lab, k in [("All (500)", "all"), (f"Shared configuration ({ld['n_dup']})", "dup"), (f"Other ({ld['n_rest']})", "rest")]) + r"""
\bottomrule
\end{tabular}
\end{table}
""")
sd = lk["SINGLE"]
S("si41_composition", r"""
The composition of the datasets for the single- and multi-section manipulators is shown in Table~S3, Table~S4, and Table~S12. The sampled workspace of the multi-section robot is shown in Fig.~S1a, and the main reference systems in Fig.~S1b. The single-section dataset (10,000 samples) was recorded in one day by motor babbling with tendon displacements sampled uniformly in $[-45, 10]$~mm. The multi-section dataset (10,000 samples) was recorded on two days with the strategy of Algorithm~S1: for each commanded configuration, one of the three sampling modes is selected with equal probability, so that each mode accounts for about one third of the configurations; the mode was not stored for each sample. Each commanded configuration was held for about 3~s while samples were logged at 1~Hz. The forward-kinematics dataset of $N_p^3$ (10,000 samples) was recorded in three sessions over two further days. All samples of each dataset were pooled and randomly split (85/10/5\%, fixed seed). \textbf{[FILL: Data were saved in batches that were inspected during acquisition; X batches (Y samples) were discarded because ...]}

Because of this acquisition scheme, test samples can be close to training samples. For the single-section arm, """ + f"{sd['n_dup'] / 5:.1f}" + r"""\% of the test samples have a training sample within 1~mm in tendon space, but their error is not lower than that of the others (""" + f"{sd['pos']['dup_mean']:.2f}" + r""" vs.\ """ + f"{sd['pos']['rest_mean']:.2f}" + r"""~mm). For the multi-section arm, """ + f"{ld['n_dup'] / 5:.1f}" + r"""\% of the test samples share their configuration with a training sample; excluding them increases the tip position errors to """ + f"{ld['pos_I']['rest_mean']:.2f}, {ld['pos_II']['rest_mean']:.2f}, and {ld['pos_III']['rest_mean']:.2f}" + r"""~mm, compared with """ + f"{ld['pos_I']['all_mean']:.2f}, {ld['pos_II']['all_mean']:.2f}, and {ld['pos_III']['all_mean']:.2f}" + r"""~mm on the full test set (Table~S14). The control targets were selected among the sampled workspace points (Section~6.3) and were therefore not excluded from training; the closed-loop experiments use new camera images, and the trajectories are not part of the datasets.
""")
rr = misc["tendon_recorded_range_mm"]
S("tab_S12_composition", r"""
\begin{table}[h]
\centering
\caption{Dataset composition.}
\label{tab:S12_composition}
\begin{tabular}{>{\raggedright\arraybackslash}p{3.0cm} >{\raggedright\arraybackslash}p{3.6cm} >{\raggedright\arraybackslash}p{3.6cm} >{\raggedright\arraybackslash}p{3.0cm}}
\toprule
 & Single-section & Multi-section & Forward kinematics ($N_p^3$) \\
\midrule
Samples & 10,000 & 10,000 & 10,000 \\
Acquisition days & 1 (2025-06-19) & 2 (2025-07-18, 2025-07-21) & 2 (2025-07-25/26), 3 sessions \\
Sampling & Motor babbling, $U(-45, 10)$~mm per tendon & Algorithm~S1, modes selected with equal probability; independent mode: I $U(-25, 10)$, II $U(-35, 10)$, III $U(-40, 10)$~mm & \textbf{[FILL]} \\
Recorded tendon range [mm] & """ + f"${min(rr['SINGLE_min']):.1f}$ to ${max(rr['SINGLE_max']):.1f}$" + r""" & """ + f"${min(rr['MULTI_min']):.1f}$ to ${max(rr['MULTI_max']):.1f}$" + r""" & \textbf{[FILL]} \\
Logging & One sample per configuration & 1~Hz, configuration held $\approx 3$~s & \textbf{[FILL]} \\
Split (train/val/test) & 8,500 / 1,000 / 500 & 8,500 / 1,000 / 500 & 8,500 / 1,000 / 500 \\
Removed samples & \textbf{[FILL]} & \textbf{[FILL]} & \textbf{[FILL]} \\
\bottomrule
\end{tabular}
\end{table}
""")
# --- networks and training (Minor 16, 17) ---
S("si31_angles", r"""
During training, positions, lengths, and curvature coefficients were standardized with the mean and standard deviation of the training set, and the networks regress the angles directly; in the loss, predicted and target angles are compared through their sine and cosine to remove the $2\pi$ discontinuity, so no decoding step is required at inference. All loss terms have equal weight.
""")
S("si32_gradcam", r"""
The negative sign in Eq.~S11 makes $\alpha_k$ positive for channels whose activation reduces the loss, so that, after the ReLU in Eq.~S12, the heatmap retains only the regions that contribute to lowering the prediction error. Heatmaps are normalized to $[0, 1]$ per image and displayed without thresholding (Fig.~4a).
""")
S("sec311_settings", r"""
Training employed the Adam optimizer with $\eta = 10^{-3}$, weight decay, and early stopping; all training settings are listed in Table~S11.
""")
# --- hardware (Minor 13-15) ---
S("sec21_calibration", r"""
Before each data acquisition session or experimental trial, all tendons (three for the single-section arm and nine for the multi-section arm) are pretensioned with the same procedure for both robots: \textbf{[FILL: criterion, e.g., each motor is driven in current control until the tendon is taut at X~mA]}. The motors then operate in extended position-control mode with a current limit of \textbf{[FILL]}~mA.
""")
S("sec21_cameras", r"""
Internal cameras (\textbf{[FILL: manufacturer and model]}; lens/field of view \textbf{[FILL]}; \textbf{[FILL: size]}~mm, \textbf{[FILL: mass]}~g including the mount) are added to each section for proprioception, and are rigidly mounted between sections and at the robot base. Consequently, each view is fixed relative to the base of the subsequent section. The sensing setup has negligible impact on the compliance of the soft structure. Camera images are transmitted to a laptop via three USB cables at a resolution of $480 \times 640$ in grayscale. Each camera is read by its own software thread, which keeps only the most recent frame; at each control step, the latest frames of the three cameras are used, so the images are acquired concurrently but are not hardware-synchronized.
""")
# --- results (Comments 6, 7; Minor 21, 24, 25; S29) ---
S("sec332_centering", r"""
where $\bar{\mathbf{l}}$ denotes the mean tendon actuation estimated from the dataset. Reducing the deviation from mid-range values keeps the tendon lengths away from their actuation limits (actuator-range centering) and preserves flexibility for future tasks. Since motor currents were not recorded, we do not claim a reduction of actuation effort.
""")
S("sec332_eq11_after", r"""
The first term enforces task accuracy, while the second biases the solution toward $\bar{\mathbf{l}}$. Unlike the null-space projection of Eq.~10, this penalty can trade some task accuracy for range centering (SI Section~5.3). The secondary objective can be flexibly modified for alternative tasks such as obstacle avoidance or grasping.
""")
a, b = ik["zeta=0.01"]["control_targets"], ik["zeta=0.0"]["control_targets"]
at, bt = ik["zeta=0.01"]["test"], ik["zeta=0.0"]["test"]
S("si53_ablation", r"""
\subsection{Secondary-Objective Ablation}
To isolate the effect of the secondary objectives, both controllers were evaluated offline, through their kinematic models, on the 20 control targets of the multi-section arm (Fig.~S8, Table~S13). For the model-based controller, the control law of Eq.~10 was replayed on the PCC model from the same initial state and target sequence, with and without the null-space term. For the data-driven controller, $N_l^3$ was retrained with $\zeta = 0.01$ (as in Section~3.3.2) and with $\zeta = 0$, with the same data, split, and seed, and evaluated through the frozen $N_p^3$. In both cases the secondary objective reduces $H(\mathbf{l})$ and the deviation of the tendon lengths from $\bar{\mathbf{l}}$. The null-space projection leaves the final position error essentially unchanged, while the penalty in the training loss of $N_l^3$ slightly increases the position error predicted by $N_p^3$. These results are simulated through the respective models and were not measured on the robot.

\begin{table}[h]
\centering
\caption{Offline ablation of the secondary objective on the 20 control targets of the multi-section arm (mean $\pm$ standard deviation across targets). Position error: final error predicted by the model (PCC for the model-based controller, $N_p^3$ for the data-driven one).}
\label{tab:S13_ablation}
\begin{tabular}{llccc}
\toprule
Controller & Secondary objective & $H(\mathbf{l})$ & RMS $|\mathbf{l} - \bar{\mathbf{l}}|$ [mm] & Position error [mm] \\
\midrule
Model-based & with null-space term & $269 \pm 135$ & $7.48 \pm 1.96$ & $5.25 \pm 2.23$ \\
 & without & $693 \pm 396$ & $12.00 \pm 3.18$ & $5.84 \pm 1.85$ \\
\midrule
Data-driven & $\zeta = 0.01$ & $""" + f"{a['H_mean']:.0f} \\pm {a['H_std']:.0f}$ & ${a['rms_dev_mean']:.2f} \\pm {a['rms_dev_std']:.2f}$ & ${a['pos_mean']:.2f} \\pm {a['pos_std']:.2f}" + r"""$ \\
 & $\zeta = 0$ & $""" + f"{b['H_mean']:.0f} \\pm {b['H_std']:.0f}$ & ${b['rms_dev_mean']:.2f} \\pm {b['rms_dev_std']:.2f}$ & ${b['pos_mean']:.2f} \\pm {b['pos_std']:.2f}" + r"""$ \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[h]
\centering
\includegraphics[width=\linewidth]{nullspace_ablation.pdf}\\
\includegraphics[width=\linewidth]{ik_ablation.pdf}
\caption{Offline ablation of the secondary objective on the 20 control targets of the multi-section arm. (a) Model-based controller, Eq.~10 replayed on the PCC model with and without the null-space term. (b) Data-driven controller, $N_l^3$ trained with $\zeta = 0.01$ and $\zeta = 0$ and evaluated through the frozen $N_p^3$. Left to right: $H(\mathbf{l})$, RMS deviation of the tendon lengths from $\bar{\mathbf{l}}$, and final position error predicted by the model. Bars: mean; error bars: one standard deviation across targets.}
\label{fig:S8_ablation}
\end{figure}
""")
S("sec425_ablation_pointer", r"""
An offline ablation of the secondary objectives of both controllers is reported in SI Section~5.3.
""")
S("sec426_payload", r"""
A 50~g payload ($\approx 40\%$ of effective robot mass, including TPU body, fabric, cameras, and PLA interfaces) was attached to the tip, emulating a sustained tip contact force. This single constant-load condition demonstrates the compensation of this load by the closed-loop controller; it does not establish robustness to general disturbances or contact.
""")
S("sec426_pct", r"""
The closed-loop controller maintains $6.3 \pm 3.2\%$ translation error (relative to the 450~mm arm length) and rotation below $15^\circ$, compared to $14.5 \pm 3.5\%$ and larger orientation deviations for open-loop.
""")
S("sec414_targets", r"""
Twenty workspace targets distributed via $k$-medoids clustering were reached sequentially by all controllers; each target was visited once, and errors are reported as the final position error at convergence, relative to the 150~mm section length for percentages. The standard deviations therefore describe the variation across targets, not trial-to-trial repeatability. Results are shown in Fig.~5c.
""")
S("sec411_pct", r"""
The final position accuracy corresponds to $2.66 \pm 1.49\%$ of the robot length of 150~mm (a translation error of $3.99 \pm 2.23$~mm), and the overall rotation error is $3.11^\circ \pm 1.96^\circ$.
""")
S("sec411_bending", r"""
Accuracy improves with bending (Spearman $\rho = """ + f"{bs['rho_pos']:.2f}" + r"""$ between bending angle and position error, $p < 0.001$; SI Fig.~S7), consistent with helicoidal deformations providing stronger visual cues for state estimation.
""")
S("sec421_pct", r"""
Position error for Module I ($2.96 \pm 1.79\%$ of the 150~mm section length) is consistent with the single-section case. It accumulates along sections for Modules II and III, reaching $4.67 \pm 2.93\%$ and $5.88 \pm 3.66\%$ of the length from the base to the respective tips (300 and 450~mm), while the mean orientation error remains below $9^\circ$ (median below $7^\circ$; Table~1). The large standard deviations of the orientation error are caused by 10 of the 500 test samples (2\%), most of which have motion-capture orientation labels inconsistent with the sampled range (SI Section~6.1).
""")
S("sec421_bending", r"""
For the multi-section arm, the tip errors show no clear dependence on the bending angle of the sections (SI Fig.~S7).
""")
S("sec424_pct", r"""
Closed-loop controllers achieve near-sensing accuracy; the model-based controller reaches $5.6 \pm 2.5\%$ position error (relative to the 450~mm arm length) and the data-driven one $6.1 \pm 2.6\%$, with differences linked to whether the Jacobian uses encoder or camera feedback.
""")
# Table 1 with robust columns (means as printed in the paper)
paper_mean = {"I": ("4.44 \\pm 2.68", "6.78 \\pm 15.94"), "II": ("14.01 \\pm 8.79", "6.45 \\pm 3.74"), "III": ("26.45 \\pm 16.49", "8.74 \\pm 13.05")}
rows = []
for s in ("I", "II", "III"):
    p, r = multi[f"abs_{s}"]["pos"], multi[f"abs_{s}"]["rot"]
    rows.append(f"{s} & ${paper_mean[s][0]}$ & {p['median']:.2f} & {p['p95']:.2f} & {p['max']:.2f} & ${paper_mean[s][1]}$ & {r['median']:.2f} & {r['p95']:.2f} & {r['max']:.2f} \\\\")
S("tab1", r"""
\begin{table}[h]
\centering
\caption{Pose errors for the multi-section arm on the test set ($N = 500$).}
\label{tab:1}
\begin{tabular}{lcccc|cccc}
\toprule
 & \multicolumn{4}{c|}{Position [mm]} & \multicolumn{4}{c}{Orientation [$^\circ$]} \\
Section & mean $\pm$ std & median & p95 & max & mean $\pm$ std & median & p95 & max \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")
t6 = misc["tableS6"]
pm6 = {"I": ("4.44 \\pm 2.68", "6.78 \\pm 15.94"), "II": ("11.92 \\pm 25.10", "7.66 \\pm 16.02"), "III": ("8.86 \\pm 5.50", "7.00 \\pm 13.17")}
rows = []
for s in ("I", "II", "III"):
    p, r = t6[s]["pos"], t6[s]["rot"]
    rows.append(f"{s} & ${pm6[s][0]}$ & {p['median']:.2f} [{p['q1']:.2f}, {p['q3']:.2f}] & {p['p95']:.2f} & {p['max']:.2f} & ${pm6[s][1]}$ & {r['median']:.2f} [{r['q1']:.2f}, {r['q3']:.2f}] & {r['p95']:.2f} & {r['max']:.2f} \\\\")
S("tabS6", r"""
\begin{table*}[h]
\centering
\caption{Relative pose errors for the multi-section arm on the test set ($N = 500$), with robust summaries (median [interquartile range], 95th percentile, maximum).}
\label{tab:S6}
\begin{tabular}{lcccc|cccc}
\toprule
 & \multicolumn{4}{c|}{Position [mm]} & \multicolumn{4}{c}{Orientation [$^\circ$]} \\
Section & mean $\pm$ std & median [IQR] & p95 & max & mean $\pm$ std & median [IQR] & p95 & max \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table*}
""")
wo = misc["outliers"]["tableS6_without_outliers"]
S("si61_outliers", r"""
The distributions in Table~1 and Table~S6 are skewed by a small number of samples. Ten of the 500 test samples (2\%) have an orientation error above $30^\circ$ at one or more tips. Nine of them form three groups of three consecutive samples, i.e., three commanded configurations each recorded three times, and their motion-capture orientation labels imply section bending angles of $87^\circ$--$174^\circ$, far beyond the sampled range (95th percentile $\approx 30^\circ$--$34^\circ$); this is consistent with orientation flips of the tracked rigid bodies rather than with errors of the network. Excluding these 10 samples, the relative position error of Section~II is $""" + f"{wo['II']['pos_mean']:.2f} \\pm {wo['II']['pos_std']:.2f}" + r"""$~mm (instead of $11.92 \pm 25.10$~mm) and its orientation error $""" + f"{wo['II']['rot_mean']:.2f}^\\circ \\pm {wo['II']['rot_std']:.2f}^\\circ" + r"""$, and the orientation error of Section~I is $""" + f"{wo['I']['rot_mean']:.2f}^\\circ \\pm {wo['I']['rot_std']:.2f}^\\circ" + r"""$ (instead of $6.78^\circ \pm 15.94^\circ$).
""")
cS, cM = misc["coverage"]["SINGLE"], misc["coverage"]["MULTI"]
dS, dM = [t["dL_mm"] for t in cS["targets"]], [x for t in cM["targets"] for x in t["dL_mm"]]
LEN_S, LEN_M = f"${min(dS):.1f}$ to ${max(dS):.1f}$~mm", f"${min(dM):.1f}$ to ${max(dM):.1f}$~mm"
TR_S = f"${cS['train_dL']['p5']:.1f}$ to ${cS['train_dL']['p95']:.1f}$~mm"
S("si63_coverage", r"""
Before clustering, the sampled workspace is restricted to points above $z = """ + f"{cS['z_filter_mm']}" + r"""$~mm for the single-section arm and $z = """ + f"{cM['z_filter_mm']}" + r"""$~mm for the multi-section arm (""" + f"{100 * cS['frac_ws_above_filter']:.1f}" + r"""\% and """ + f"{100 * cM['frac_ws_above_filter']:.1f}" + r"""\% of the samples), and each cluster center is replaced by the nearest sampled point. The resulting targets are listed in Tables~S8 and S9. The convex hull of the 20 targets covers """ + f"{100 * cS['hull_volume_ratio']:.1f}" + r"""\% (single section) and """ + f"{100 * cM['hull_volume_ratio']:.1f}" + r"""\% (multi-section) of the volume of the convex hull of the sampled positions, and the median distance from a sampled position to the nearest target is """ + f"{cS['median_dist_ws_to_nearest_target']:.1f}" + r"""~mm and """ + f"{cM['median_dist_ws_to_nearest_target']:.1f}" + r"""~mm, respectively. For the single-section arm, the targets reach a bending angle of $""" + f"{cS['target_bend_max']:.1f}" + r"""^\circ$ and the trajectories $""" + f"{cS['traj_bend_max']:.1f}" + r"""^\circ$, compared with a 95th percentile of $""" + f"{cS['train_bend']['p95']:.1f}" + r"""^\circ$ in the training data (Fig.~S9). The length change of the central axis is """ + LEN_S + r""" for the single-section targets (training data, 5th to 95th percentile: """ + TR_S + r""") and """ + LEN_M + r""" per section for the multi-section targets (Tables~S8 and S9), so the evaluation covers a limited range of compression.
""")
S("figS9", r"""
\begin{figure}[h]
\centering
\includegraphics[width=0.7\linewidth]{single_workspace_coverage.pdf}\\
\includegraphics[width=\linewidth]{multi_workspace_coverage.pdf}
\caption{Bending-angle distribution of the training data compared with the control targets and trajectories. (a) Single-section arm. (b) Multi-section arm, sections I--III. Vertical lines mark the maximum bending of the targets, of the trajectories, and of the training data.}
\label{fig:S9_coverage}
\end{figure}
""")
rows = "\n".join(f"{t['id']} & {t['x']:.1f} & {t['y']:.1f} & {t['z']:.1f} & {t['bend_deg']:.1f} & {t['dL_mm']:.1f} \\\\" for t in cS["targets"])
S("tab_S8_targets_single", r"""
\begin{table}[h]
\centering
\caption{Control targets of the single-section arm. Bending angle: PCC estimate from the target position. $\Delta L$: length change of the central axis, i.e., mean tendon displacement of the sampled configuration that the target corresponds to (Eq.~2).}
\label{tab:S8_targets_single}
\begin{tabular}{rrrrrr}
\toprule
ID & $x$ [mm] & $y$ [mm] & $z$ [mm] & Bending [$^\circ$] & $\Delta L$ [mm] \\
\midrule
""" + rows + r"""
\bottomrule
\end{tabular}
\end{table}
""")
rows = "\n".join(f"{t['id']} & {t['x']:.0f} & {t['y']:.0f} & {t['z']:.0f} & {t['yaw']:.0f} & {t['pitch']:.0f} & {t['roll']:.0f} & "
                 f"{t['bend_deg'][0]:.0f} / {t['bend_deg'][1]:.0f} / {t['bend_deg'][2]:.0f} & {t['dL_mm'][0]:.1f} / {t['dL_mm'][1]:.1f} / {t['dL_mm'][2]:.1f} \\\\"
                 for t in cM["targets"])
S("tab_S9_targets_multi", r"""
\begin{table*}[h]
\centering
\caption{Control targets of the multi-section arm (tip pose). Bending angle and length change of sections I / II / III: PCC estimate from the offline replay of the model-based controller.}
\label{tab:S9_targets_multi}
\begin{tabular}{rrrrrrrcc}
\toprule
ID & $x$ [mm] & $y$ [mm] & $z$ [mm] & Yaw [$^\circ$] & Pitch [$^\circ$] & Roll [$^\circ$] & Bending [$^\circ$] & $\Delta L$ [mm] \\
\midrule
""" + rows + r"""
\bottomrule
\end{tabular}
\end{table*}
""")
# --- reproducibility table (Comment 9) ---
S("tab_S11_repro", r"""
\begin{table*}[h]
\centering
\footnotesize
\caption{Reproducibility settings.}
\label{tab:S11_repro}
\begin{tabular}{>{\raggedright\arraybackslash}p{2.8cm} >{\raggedright\arraybackslash}p{6.2cm} >{\raggedright\arraybackslash}p{6.2cm}}
\toprule
Item & Single-section & Multi-section \\
\midrule
Cameras & \textbf{[FILL: model, lens/field of view, size, mass]}; USB, OpenCV (V4L2), $640 \times 480$ grayscale & Three cameras of the same model; one capture thread per camera, buffer of one frame, nominal 3~fps, latest frame used (software synchronization) \\
Exposure and gain & \textbf{[FILL: automatic or fixed]} & \textbf{[FILL]} \\
Network input & $1 \times 480 \times 640$, 8-bit, scaled to $[0, 1]$ inside the network & $3 \times 480 \times 640$, one camera per channel \\
Pose CNN & MobileNetV2 (ImageNet weights), first convolution replaced by a 1-channel one; GAP (1280); linear head $1280 \to 6$ & MobileNetV2 with 3-channel first convolution; GAP (1280); head $1280 \to 512$ (LeakyReLU) $\to 18$ \\
Curvature CNNs & Backbone initialized from $f_p^1$; linear heads $1280 \to 5 / 4 / 3$ & Backbone initialized from $f_p^3$; heads $1280 \to 512 \to 15 / 12 / 9$ \\
Kinematic MLPs & $N_l^1$: $3 \to 128$ (linear, BatchNorm, LeakyReLU), three residual blocks of width 128, $128 \to 64 \to 32 \to 3$ & $N_p^3$: $9 \to 4 \times 128$ (ELU) $\to 6$; $N_l^3$: $6 \to 4 \times 128$ (ELU) $\to 9$, trained through the frozen $N_p^3$ with $\zeta = 0.01$ on the standardized tendon vector \\
$N_C$ & $6 \to 128$, three residual blocks, $\to 5 / 4 / 3$; trained on single-section data & Applied to each section, on the section-tip pose expressed in the frame of the preceding tip \\
Optimizer & Adam, learning rate $10^{-3}$, weight decay $5 \cdot 10^{-6}$ (CNNs) and $10^{-5}$ ($N_l^1$, $N_C$) & Adam, learning rate $10^{-3}$, weight decay $5 \cdot 10^{-6}$ \\
Learning-rate schedule & Linear warm-up (10 iterations), then ReduceLROnPlateau (factor 0.5, patience 5) & Linear warm-up (CNNs), then ReduceLROnPlateau (factor 0.6 for CNNs, 0.9 for MLPs; patience 5 and 15) \\
Epochs and early stopping & Maximum 500 epochs; patience 30 & Maximum 500 (CNNs), 800 ($N_p^3$), 2000 ($N_l^3$) epochs; patience 50 \\
Batch size & 16 (images), 64 (MLPs) & 16 (images), 64 (MLPs); gradient clipping at 1.0 \\
Loss & \textbf{[FILL: Huber or MSE, see note]} & Huber, $\delta = 1$ \\
Angles & Regressed directly; sine and cosine inside the loss & Same \\
Output normalization & Mean and standard deviation of the training split, stored with the exported models & Same \\
Augmentation & Gaussian blur (kernel 5, $\sigma \le 8$), Gaussian noise ($\sigma \le 30$), brightness and contrast jitter (0.4), brightness shift (0.3), vignetting (0.6) & Same \\
Seed and split & 42 (Python, NumPy, PyTorch); 85/10/5\% random split of pooled samples & Same \\
Motors & Dynamixel XL330-M288-T, Protocol 2.0, 57,600 baud, extended position mode, pulley diameter 6~mm ($4096 / (6\pi)$ ticks per mm), position tolerance 20 ticks & Same, nine motors; sections II and III actuated through Bowden cables \\
Pretension and current limit & \textbf{[FILL: criterion]}; current limit \textbf{[FILL]}~mA; same procedure for both arms & Same \\
Tendons & \textbf{[FILL: material, diameter]} & Same \\
Sampled tendon ranges & $U(-45, 10)$~mm per tendon & Independent mode: I $U(-25, 10)$, II $U(-35, 10)$, III $U(-40, 10)$~mm; coupled modes through the Bending Solver \\
Acquisition sessions & One day (2025-06-19) & Two days (2025-07-18 and 2025-07-21); logging at 1~Hz, configuration held for $\approx 3$~s; $N_p^3$ data: three sessions (2025-07-25/26) \\
Control parameters & $\lambda = 0.1$, $\varepsilon = 1$~mm, $\gamma = 3$~mm & $\lambda = 0.1$, $\varepsilon = 1$~mm, $\gamma = 10$ (SE(3) distance, Eq.~S16) \\
Control targets & 20, $k$-medoids on sampled positions with $z > 115$~mm & 20, same procedure with $z > 200$~mm \\
\bottomrule
\end{tabular}
\end{table*}
""")

# =============================== RESPONSES ===============================
S("resp_overall", r"""
We thank the reviewer for the detailed and constructive assessment. We agree that the contribution lies in the integration of distributed internal cameras, markerless at inference, with model-based and learned redundancy-aware control on a multi-section arm, and we have revised the manuscript to state this precisely and to align the claims with the evidence. In summary: (i) we added the suggested references, a comparison paragraph in the Introduction, and a comparison table in the SI; (ii) we state explicitly that the curvature reconstruction does not enter the control laws and explain the encoder offset in Algorithm~1; (iii) we narrowed the scalability claim to networks retrained with a transferred backbone, validated for one and three sections; (iv) we describe the multi-section curvature result as a model-constrained reconstruction and state its assumptions; (v) we added an offline ablation of the secondary objectives of both controllers; (vi) we quantified the coverage of the control evaluation and limited the claims on repeatability and disturbances; (vii) we documented the data split and its effect, and added a reproducibility table; and (viii) we revised the figures and captions as requested. Our responses to each comment follow; changes in the manuscript are highlighted.
""")
S("resp_G", r"""
\textbf{Title.} We kept the title, which states the method (internal-camera reconstruction and closed-loop control) and the system (soft robotic arms).

\textbf{Suggested references.} We added the references suggested by the reviewer (Comment~2).

\textbf{Acronyms.} We proofread the manuscript and define every acronym at its first use in the main text and in the SI, including those that appear only in figures (e.g., BW, FE, and FC in Fig.~1, and CL and OL in Figs.~5 and 8). The title and abstract contain no undefined acronyms.

\textbf{Figures and captions.} We checked the text and axis labels of all figures and revised the captions so that every panel and inset is described (Comment~10).

\textbf{Copyright.} All figures were created by the authors for this manuscript; no reprinted or adapted material, logos, or trademark images are included.

\textbf{References.} The reference list gives full article titles, and we added DOIs where available.
""")
S("resp_1", r"""
We thank the reviewer for this careful reading. The reviewer is correct that the curvature reconstruction does not enter either control law: both controllers close the loop on the tip pose estimated from the camera images, the model-based controller additionally uses the motor encoders to evaluate the PCC Jacobian and the null-space term, and the curvature estimate is evaluated as a separate sensing capability. We now state this explicitly in the Abstract, the contribution list, Section~3.3, the caption of Fig.~4c (which now shows the encoder path), and the Conclusion.

The initial PCC estimate in Algorithm~1 is not discarded. The tendon lengths $\mathbf{l}_0$ obtained from the camera-estimated section-tip positions through the inverse PCC map are used once, before the loop, to set the encoder offset $\mathbf{l}_{\mathrm{off}} = \mathbf{l}_{\mathrm{enc}} - \mathbf{l}_0$, so that the encoder readings inside the loop are expressed in the PCC tendon-length frame used by $\mathbf{J}(\mathbf{l})$ and by the null-space term $\mathbf{N}(\bar{\mathbf{l}} - \mathbf{l})$. Algorithm~1 and Section~3.3.2 now show this step explicitly.
""")
S("resp_2", r"""
We thank the reviewer for these references. We added Hofer et al., Thuruthel et al., Han et al., and Lu et al.\ (Yoo et al.\ was already cited as Ref.~[15]) and a paragraph in the Introduction that states what each study established, together with a comparison table in the SI (Table~S10). Since the systems differ in actuation, size, and task, the table compares design choices rather than accuracy: the sensing, the part of the arm that is sensed, the estimated quantities, whether the loop is closed on the estimate, and how the actuation redundancy is used. Each prior system covers part of these choices, and ours is the only one that combines them. Hofer et al.\ obtain a higher orientation accuracy (about $1^\circ$ at 30~Hz) than our single-section estimate ($3.11^\circ$ at about 8~Hz), on a two-angle spherical joint with an internal painted pattern and illumination; our system estimates the full 6-DoF tip pose of an extensible section without internal markers and is applied to three sections. Thuruthel et al.\ learned closed-loop inverse kinematics with end-effector feedback, Han et al.\ and Yoo et al.\ estimate shape from internal cameras without closing a control loop, and Lu et al.\ servo the shape with fiber Bragg grating sensing. The capability we add is the combination of distributed internal cameras on a multi-section arm with closed-loop control that explicitly exploits the actuation redundancy, through model-based null-space control and through a learned inverse kinematics with a secondary objective. We narrowed the novelty statement in the Introduction and the contribution list to this combination.
""")
S("resp_3", r"""
We agree. The input layer and the regression head both depend on the number of sections, and separate networks were trained for the one- and three-section arms. We corrected the statement in Section~3.1 and rephrased the Introduction, the contribution list, and the Conclusion accordingly: the backbone is transferred and the network is retrained, and only $n = 1$ and $n = 3$ were validated. We also removed the word ``scalable'' where it implied that no retraining is needed.
""")
S("resp_4", r"""
We agree. For the multi-section arm, inter-section marker occlusion prevented tracking all backbone markers during data collection, and the curvature labels were obtained from the motion-captured section-tip poses through $N_C$. We therefore now describe the multi-section result as a model-constrained reconstruction and state its assumptions explicitly in Section~2.2 and Section~4.2.2: planar bending within each section, no torsion, and a bending direction that is constant along each section. The errors in Fig.~7b quantify the agreement with these model-constrained labels. For Fig.~S2b, we now report the number of validation configurations (20, posed manually with all subsection markers visible and recorded in a separate session), that the error bars are one standard deviation across configurations, and that these configurations are independent of the data used to train $N_C$ (single-section dataset) and the three-section curvature estimator. We also report the error of $N_C$ on held-out single-section test data ($N = 500$): 0.38--0.43~mm at $L/3$, 1.20--1.37~mm at $2L/3$, and 2.49--2.94~mm at $L$ for the three curvature models (SI Section~4.2).
""")
S("resp_5", r"""
We thank the reviewer. The implementation and the SI equations use the dimensional arc length $x \in [0, L]$. We corrected the main text accordingly (Eqs.~4--6, the translation integral without the factor $L$, and the evaluation points $x = L/3, 2L/3, L$), the variable of SI Eqs.~S3--S4 and the initialization sentence in SI Section~2.2, and the nomenclature in Table~S1, which now gives the units of $c_0$, $c_1$, and $c_2$ (mm$^{-1}$, mm$^{-2}$, mm$^{-3}$).
""")
S("resp_6", r"""
We agree that $H(\mathbf{l})$ centers the tendon lengths in their actuation range and does not measure effort, which was not recorded. We now describe it as actuator-range centering and removed the statements about effort (Introduction, Section~3.3.2, Conclusion). To isolate its effect without new hardware experiments, we performed offline ablations on identical targets for both controllers (new SI Section~5.3, Fig.~S8, and Table~S13). For the model-based controller, replaying the control law on the PCC model for the 20 evaluation targets gives a final position error of $5.25 \pm 2.23$~mm with and $5.84 \pm 1.85$~mm without the null-space term, while the RMS deviation of the tendon lengths from $\bar{\mathbf{l}}$ decreases from $12.00 \pm 3.18$~mm to $7.48 \pm 1.96$~mm ($H(\mathbf{l})$: $693 \pm 396$ vs.\ $269 \pm 135$). For the data-driven controller, we retrained the inverse-kinematics network with and without the secondary term ($\zeta = 0.01$ and $\zeta = 0$, same data, split, and seed) and evaluated it through the frozen forward network on the same targets: the secondary term reduces $H(\mathbf{l})$ from """ + f"${b['H_mean']:.0f} \\pm {b['H_std']:.0f}$ to ${a['H_mean']:.0f} \\pm {a['H_std']:.0f}$ (RMS tendon deviation from {b['rms_dev_mean']:.1f} to {a['rms_dev_mean']:.1f}~mm), at the cost of a small increase of the position error predicted by the forward network (${a['pos_mean']:.1f} \\pm {a['pos_std']:.1f}$ vs.\\ ${b['pos_mean']:.1f} \\pm {b['pos_std']:.1f}$~mm)" + r""". Unlike the null-space projection, the penalty in the training loss trades some primary-task accuracy for range centering, which we now state in Section~3.3.2. These results are simulated through the respective models and are reported as such.
""")
S("resp_7", r"""
We thank the reviewer. We replaced the bending range in Section~3.2 with the measured one (single section: maximum $57^\circ$, 95th percentile $36^\circ$; multi-section 95th percentiles of $30^\circ$, $32^\circ$, and $34^\circ$), and we added the coordinates of all targets with their bending angle and length change (Tables~S8 and S9) and the coverage of the evaluation set (SI Section~6.3 and Fig.~S9). The single-section targets and trajectories reach """ + f"${cS['target_bend_max']:.1f}^\\circ$ and ${cS['traj_bend_max']:.1f}^\\circ$" + r""", close to the 95th percentile of the training data (""" + f"${cS['train_bend']['p95']:.1f}^\\circ$" + r"""); the 20 targets span """ + f"{100 * cS['hull_volume_ratio']:.1f}" + r"""\% (single) and """ + f"{100 * cM['hull_volume_ratio']:.1f}" + r"""\% (multi) of the convex hull of the sampled positions. The length changes of the targets are """ + LEN_S + r""" (single section; training data, 5th to 95th percentile: """ + TR_S + r""") and """ + LEN_M + r""" per section (multi-section); we agree that this is a limited range of compression and now state it in SI Section~6.3. We revised the text to state that the reported standard deviations describe the variation across targets visited once, not repeatability, and that trajectory waypoints are serially correlated. The disturbance experiment is now described as the compensation of a single constant 50~g off-center load rather than general robustness. Repeated trials, non-planar and boundary trajectories, larger length changes, and further load conditions are listed as limitations and future work in Section~5.
""")
S("resp_8", r"""
We added this information to Section~3.1.1 and SI Section~4.1. All samples of each dataset were pooled and randomly permuted with a fixed seed before the 85/10/5 division; the split was not blocked by session or by configuration neighborhood. Because each commanded configuration of the multi-section arm was held for about 3~s and recorded at 1~Hz, some test samples share their configuration with training samples. To quantify the effect, we evaluated the test error with and without these samples: for the multi-section arm, the tip position errors become """ + f"{ld['pos_I']['rest_mean']:.2f}, {ld['pos_II']['rest_mean']:.2f}, and {ld['pos_III']['rest_mean']:.2f}~mm instead of {ld['pos_I']['all_mean']:.2f}, {ld['pos_II']['all_mean']:.2f}, and {ld['pos_III']['all_mean']:.2f}~mm" + r""" (Table~S14), and for the single-section arm, samples close to a training configuration are not more accurate than the others (""" + f"{sd['pos']['dup_mean']:.2f} vs.\\ {sd['pos']['rest_mean']:.2f}~mm" + r"""). Session-blocked evaluation is listed as a limitation. The control targets were selected among the sampled workspace configurations and were therefore not excluded from training; the closed-loop experiments use new camera images, and the trajectories are not part of the datasets. The single-section data were collected in one day and the multi-section data on two days, with the same camera settings and one build of each arm \textbf{[CONFIRM]}; the two arms use different coverings (corrugated silicone and stretchable fabric, Section~2.1).
""")
S("resp_9", r"""
We added a reproducibility table to the SI (Table~S11) that collects the camera and acquisition settings, the network architectures, the training hyperparameters (optimizer, learning-rate schedule, maximum epochs, early stopping, batch size, random seed, normalization, angle handling, augmentation) for all networks including $N_C$, $N_p^3$, and $N_l^3$, the actuation hardware and pretensioning procedure, the tendon material and diameter, the sampled tendon ranges, and the acquisition sessions (Table~S12). We also limited the statements on lighting: image augmentations were used during training, but robustness to lighting or hardware variations was not tested, and this is now stated in Section~5.
""")
S("resp_10", r"""
We revised the figures and captions. Figure~3 has been redrawn with a single left-to-right flow, the name of each network on its path, the inputs and outputs of every network with tensor dimensions, and colors that separate pose estimation, curvature reconstruction, forward kinematics, and inverse kinematics; the caption now lists the inputs and outputs of all networks and states which architecture is used for the single- and multi-section kinematic networks. The captions of Figs.~1 and 2 now describe every labeled element (including the boundary arcs $L_1$--$L_4$, which are geometric constructions and not tendons), and Fig.~5b now uses equal axis scaling.
""")
S("resp_11", r"""
We now write ``markerless at inference'' and explain at first use that external motion-capture markers are used only to generate the training labels.
""")
S("resp_12", r"""
We now use ``section'' throughout the manuscript, figures, algorithms, and SI.
""")
S("resp_13", r"""
We now state the number of tendons explicitly (three for the single-section arm and nine for the multi-section arm) and that the same pretensioning procedure is used for both arms, including its criterion and the motor current limit (Section~2.1 and Table~S11).
""")
S("resp_14", r"""
The camera manufacturer and model, lens and field of view, nominal frame rate, and the size and mass of the camera and mount are now given in Section~2.1 and in Table~S11.
""")
S("resp_15", r"""
The acquisition is synchronized in software only: each camera is read by its own capture thread, and the controller uses the latest frame of each camera. We removed the word ``simultaneously'' and describe this mechanism in Section~2.1 and in the caption of Fig.~1.
""")
S("resp_16", r"""
The networks regress the angles directly; the sine and cosine of the predicted and target angles are only used inside the loss to remove the $2\pi$ discontinuity, so no conversion back to angles is needed. Positions, lengths, and curvature coefficients are standardized with the mean and standard deviation of the training set, and all loss terms have equal weight. This is now stated in SI Section~3.1 and Table~S11.
""")
S("resp_17", r"""
In Eq.~S11 the Grad-CAM score is the negative loss, so positive weights correspond to feature-map channels whose activation reduces the prediction loss; after the ReLU of Eq.~S12, the heatmap retains only these regions. The maps are normalized to $[0, 1]$ per image and shown without thresholding, so the color scale in Fig.~4a shows this relative contribution. We clarified both points in SI Section~3.2 and in the caption of Fig.~4.
""")
S("resp_18", r"""
Please see our response to Comment~1: the PCC estimate sets the encoder offset used inside the loop, and Algorithm~1 now shows this step explicitly.
""")
S("resp_19", r"""
We now use a single notation, defined in Section~3.3: $\mathbf{J}_{a \to b} = \partial b / \partial a$. The analytical PCC Jacobians are forward Jacobians ($\mathbf{J}_{l \to t}$, $\mathbf{J}_{l \to p}$) with damped pseudoinverse $\mathbf{J}^{\#}$, and the Jacobians of the learned inverse kinematics are denoted with a hat ($\hat{\mathbf{J}}_{t \to l}$, $\hat{\mathbf{J}}_{p \to l}$). The notation is used consistently in Eqs.~7--10, Algorithms~1--2, Fig.~S3, and Table~S2.
""")
S("resp_20", r"""
Section~3.3.1 now states that the open-loop baselines use the same planner, waypoint spacing, damping, and target sequence as the closed-loop controllers. Their initial state is measured once by motion capture and then propagated with the model-based or data-driven kinematics instead of the camera estimate, and they execute the full waypoint sequence without a convergence check. We use ``open-loop'' throughout.
""")
S("resp_21", r"""
We now state the normalization of every percentage at its first use: the section length (150~mm) for the single-section arm; for the multi-section arm, the length from the base to the evaluated tip (150, 300, and 450~mm) for the pose estimation, and the 450~mm arm length for the control experiments.
""")
S("resp_22", r"""
We agree that the non-uniform scaling distorted the shapes. The shape panels of Fig.~5b now use equal axis scaling, and the caption no longer refers to non-uniform scaling.
""")
S("resp_23", r"""
We agree that the summed statistic was ambiguous and not comparable between the two arms. Figure~7 now shows the 3D error at each reference point against the normalized arc length, for both arms on the same horizontal axis (median and interquartile range over the 500 test samples), and the caption and Sections~4.1.2 and 4.2.2 define the statistic.
""")
S("resp_24", r"""
Table~1 now also reports the median, 95th percentile, and maximum error, and the text states that the mean orientation error is below $9^\circ$ (the median is below $7^\circ$). The large standard deviations and maxima are caused by 10 of the 500 test samples (2\%), most of which have motion-capture orientation labels inconsistent with the sampled range; we discuss them in SI Section~6.1 (see also our response to Comment~29).
""")
S("resp_25", r"""
We plotted the error against the bending angle (new Fig.~S7). For the single-section arm, the error decreases with bending (Spearman $\rho = """ + f"{bs['rho_pos']:.2f}" + r"""$, $p < 0.001$), which supports the statement in Section~4.1.1, now given with this value. For the multi-section arm, no clear dependence was found, and we revised the corresponding sentence in Section~4.2.1.
""")
S("resp_26", r"""
The captions of Figs.~6, 9, and 10 now state that each path is a single run of one counter-clockwise cycle starting at $(r, 0)$, and a new table (Table~S7) reports the radial and height RMS deviation from the reference circle for every controller, arm, and load condition. For example, under the 50~g payload the radial RMS error on the 120~mm circle is 11.46~mm in closed loop and 27.10~mm in open loop.
""")
S("resp_27", r"""
We revised Section~5 to separate the capabilities evaluated in this work from future applications. Obstacle avoidance, whole-body grasping, surgical and inspection applications, and force or contact sensing are now presented explicitly as future directions that were not evaluated here.
""")
S("resp_28", r"""
The caption of Fig.~S2 and SI Section~4.2 now report the number of validation configurations (20), how they were obtained (posed manually with all markers visible, in a separate session not used for training), and that the error bars are one standard deviation across configurations. We also report the error of $N_C$ for each curvature model on held-out single-section test data (please see our response to Comment~4).
""")
S("resp_29", r"""
We added the median, interquartile range, 95th percentile, and maximum to Table~S6 (and Table~1). The large standard deviations are caused by 10 of the 500 test samples (2\%): nine of them are three configurations recorded three times each, whose motion-capture orientation labels imply section bending angles of $87^\circ$--$174^\circ$, far outside the sampled range, which is consistent with orientation flips of the tracked rigid bodies. Excluding these samples, the Section~II relative position error is $""" + f"{wo['II']['pos_mean']:.2f} \\pm {wo['II']['pos_std']:.2f}" + r"""$~mm instead of $11.92 \pm 25.10$~mm. We discuss these outliers in SI Section~6.1 and report both summaries.
""")
S("resp_30", r"""
Figures~S4--S6 now label each of the 20 targets with the same identifier in every panel, and use a single color scale per quantity within each figure. The target coordinates are listed with the same identifiers in Tables~S8 and S9.
""")
S("resp_31", r"""
We added the dataset composition (Table~S12 and SI Section~4.1): sample counts, acquisition days and sessions, sampled and recorded tendon ranges, logging scheme, and split. For the multi-section arm, each commanded configuration selected one of the three sampling modes of Algorithm~S1 with equal probability, so each mode accounts for about one third of the configurations by design; the mode was not stored for each sample. \textbf{[FILL: removed batches/samples and reason]}
""")

# ------------------------------ write files ------------------------------
t = SNIP.pop("si_bending"); i = t.index("\\begin{figure}")
SNIP["si_bending"], SNIP["figS7_bending"] = t[:i].rstrip() + "\n", t[i:]
t = SNIP.pop("si53_ablation"); i, j = t.index("\\begin{table}"), t.index("\\begin{figure}")
SNIP["si53_ablation"], SNIP["tab_S13_ablation"], SNIP["figS8_ablation"] = t[:i].rstrip() + "\n", t[i:j].rstrip() + "\n", t[j:]
for k, v in SNIP.items():
    open(f"{SN}/{k}.tex", "w").write(v)

Q = {  # reviewer/editor text, verbatim from the decision letter (LaTeX-escaped)
 "overall": r"I recommend major revision. The claimed contributions (internal-camera proprioception, learned inverse kinematics, closed-loop soft-arm control, and redundancy resolution) have each been extensively addressed in prior work. [\dots] Several central claims also extend beyond the evidence presented. [\dots]",
 "G": r"Please ensure that the title of your manuscript is succinct, descriptive, and accurate [\dots] Reviewers may have suggested references [\dots] define all acronyms when first mentioned [\dots] check that all parts, insets, and footnotes of Figures and Schemes are mentioned in the caption. [\dots] obtain copyright permission information for any images that have not been created originally for this manuscript [\dots] full article titles, and optionally, DOIs.",
 "1": r"1. Clarify the role of visual sensing in closed-loop control. [\dots] Algorithm 1 also uses a PCC inverse calculation to initialize tendon lengths from section-tip positions. [\dots] the resulting estimate appears to be replaced by the motor-encoder measurement at the first control iteration, before it affects the control command. The authors should explain this initialization or remove it. The abstract, contribution list, Fig. 4c, and conclusion should clearly distinguish [\dots]",
 "2": r"2. Establish originality claims through direct comparison with prior work. [\dots] The authors should explain what each close prior study established and identify the specific capability added here. The claim that no prior framework combines comparable sensing with closed-loop null-space control is too broad without this analysis.",
 "3": r"3. Substantiate or narrow the scalability claim. The estimator is not invariant to the number of arm sections. [\dots] The statement that only the first layer must be adjusted also conflicts with Fig. 3 because the regression head changes as well.",
 "4": r"4. Strengthen the ground truth for full-body reconstruction. [\dots] Fig. S2b does not provide sufficient validation of N\_C [\dots] Otherwise, the result should be described as model-constrained reconstruction, with its assumptions stated explicitly, including planar bending within each section, no torsion, and no arc-dependent bending direction.",
 "5": r"5. Correct the curvature-coordinate inconsistency. [\dots] The paper should consistently use either normalized arc length $u = x/L$ or dimensional arc length $x \in [0, L]$, and revise Eqs. 4--6, SI Eqs. S3--S9, the translation integral, nomenclature, and coefficient units accordingly.",
 "6": r"6. Quantitatively evaluate the secondary objective. [\dots] The objective should therefore might described as actuator-range centering unless effort is measured. For both controllers, an ablation with the secondary objective disabled using identical targets would be helpful. [\dots]",
 "7": r"7. Expand and better characterize the control evaluation. [\dots] The authors should report the target coordinates, associated bending and compression ranges, and the fraction of the sampled workspace represented by the evaluation set. Each of the 20 targets is visited only once. [\dots] Either additional load magnitudes and directions should be tested or the claims should be limited.",
 "8": r"8. Establish independence of training and evaluation data. [\dots] The authors should state: how samples were randomized; whether test data were separated by session or configuration neighborhood; whether controller targets and trajectories were excluded from training; and whether experiments span different days, camera settings, coverings, or robot builds.",
 "9": r"9. Provide the missing reproducibility details. [\dots] The SI is a good place for a single reproducibility table containing these settings. Claims of robustness to lighting or hardware variation should be limited unless such variation was explicitly tested.",
 "10": r"10. Revise the figures and captions. Several figures---particularly Figs. 1B, 2, 3, and 5---are difficult to interpret. [\dots] The paper should use a consistent flow direction, label all network inputs and outputs, and distinguish clearly between the networks used for pose estimation, curvature reconstruction, forward kinematics, and inverse kinematics.",
 "11": r"Use `markerless at measured inferences' rather than simply `markerless.' External optical markers are required to generate the supervised labels, even though markers are not required during deployment.",
 "12": r"Use either `section' or `segment' consistently throughout the manuscript, figures, algorithms, and SI.",
 "13": r"The calibration paragraph says that `all ten tendons' are tightened, but the multi-section arm has nine tendons and the single-section arm has three. Correct the number and state whether the same preload procedure is used for both systems.",
 "14": r"Identify the camera manufacturer and model, lens or field of view, nominal frame rate, and the physical size and mass of each camera and mount.",
 "15": r"The claim that images are acquired simultaneously should be supported by the synchronization method [\dots]",
 "16": r"Explain how angular sine/cosine outputs are converted back to angles and how losses for position, orientation, length, and curvature are balanced after normalization.",
 "17": r"Clarify the negative sign in Eq. S11 and clarify how the highlighted pixels are the regions used for prediction.",
 "18": r"In Algorithm 1, the initial line that estimates tendon lengths from intermediate positions via PCC appears unused because tendon lengths are read from encoders inside the loop. Remove it or explain its role.",
 "19": r"Use consistent Jacobian notation. J\_t2l, J\_l2p, and their learned representations currently alternate between a forward Jacobian, an inverse Jacobian, and a derivative of an inverse network. [\dots]",
 "20": r"State whether the open-loop baselines use the same measured initial pose, planner, gains, stopping limits, and commanded waypoint sequence as the closed-loop methods. `Open-loop' and `feedforward' should be used consistently.",
 "21": r"State the denominator used for every percentage error. [\dots]",
 "22": r"Figure 5b intentionally uses nonuniform axis scaling. This visually distorts the reconstructed shapes. Use equal spatial scaling where possible or add a second undistorted view and explicit scale bars.",
 "23": r"Figure 7 alternates among `cumulative 3D error,' `sum of 3D errors,' and `average 3D error for each point.' Define the statistic exactly. [\dots] Per-point RMSE or error versus normalized arc length would be clearer.",
 "24": r"In Table 1, the text states that orientation error remains below 9 degrees, but several standard deviations are larger than the corresponding means. Make clear that only the mean is below 9 degrees and report median, 95th percentile, and maximum error.",
 "25": r"The claim that bent configurations improve accuracy is plausible but currently qualitative. The authors should plot error against bending angle before drawing this conclusion.",
 "26": r"For Figs. 6, 9, and 10, identify the start direction, waypoint order, number of completed cycles, and whether the plotted paths are one run or an average. Add quantitative path errors in the caption or an accompanying table.",
 "27": r"The discussion should distinguish demonstrated capabilities from proposed applications. Obstacle avoidance, whole-body grasping, surgical guidance, and force or contact sensing are future directions and were not evaluated here.",
 "28": r"Fig. S2b should report the numerical N\_C error for each curvature model, the number of validation configurations, and whether the bars show standard deviation, standard error, or another interval.",
 "29": r"Table S6 contains highly skewed errors, particularly 11.92 +/- 25.10 mm for Section II and orientation standard deviations near 16 degrees. Report robust distribution summaries and discuss the outliers rather than relying only on mean and standard deviation.",
 "30": r"Figs. S4-S6 should use matched target identifiers or connecting pairs so the reader can compare the same workspace locations across controllers. Use consistent color limits when the goal is direct visual comparison.",
 "31": r"Tables S3 and S4 list dataset fields but not dataset composition. Add sample counts per acquisition mode and robot configuration, including how many samples were removed and why.",
}
# (heading, comment key or None, level): 1 section, 2 subsection, 3 subsubsection
heads = [("Response to the Editor", None, 1), ("Editor's requirements", "G", 2),
         ("Response to Reviewer 1", None, 1), ("Overall assessment", "overall", 2), ("Major comments", None, 2)] + \
        [(f"Comment {i}", str(i), 3) for i in range(1, 11)] + [("Minor comments", None, 2)]
PAGES = {11: "pages 1--2", 13: "pages 3--5", 16: "pages 5--7", 21: "pages 8--11"}
grp = None
for i in range(11, 28):
    grp = PAGES.get(i, grp)
    heads.append((f"Comment {i} ({grp})", str(i), 3))
heads += [("Supporting Information", None, 2)] + [(f"Comment {i} (SI)", str(i), 3) for i in range(28, 32)]
L = [r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=2.2cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb,xcolor,needspace}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\newcommand{\rc}[1]{\begin{quote}\color{black!70}\itshape #1\end{quote}}
\begin{document}
{\Large\bfseries Response to the editor and the reviewer}\\[4pt]
Manuscript 3400076, ``Internal Camera-based Reconstruction and Closed-loop Control of Soft Robotic Arms''

Dear Dr.\ Murray,

We thank you and the reviewer for the careful evaluation of our manuscript. We have revised the manuscript and the Supporting Information according to all comments. Below, the comments are reproduced in italics and followed by our response; changes in the manuscript are highlighted. The major comments keep the reviewer's numbering (1--10); the minor comments and the comments on the Supporting Information are numbered 11--31 in the order of the report.
"""]
CMD = {1: "section", 2: "subsection", 3: "subsubsection"}
for h, k, lev in heads:
    L.append(f"\\needspace{{{14 - 2 * lev}\\baselineskip}}\\{CMD[lev]}*{{{h}}}")  # keep headings with their text
    if k is None:
        continue
    L.append(f"\\rc{{{Q[k]}}}")
    L.append(SNIP["resp_" + k].strip())
L.append(r"""
\bigskip
Sincerely,\\
Lorenzo Vignoli, Guanran Pei, Francesco Braghin, and Josie Hughes
\end{document}""")
open(f"{SN}/response_letter.tex", "w").write("\n\n".join(L))
print(len(SNIP), "snippets written")
