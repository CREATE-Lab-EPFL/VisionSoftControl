# AIS 3400076 — Comment 3: "Substantiate or narrow the scalability claim" (draft for the user)

Local-only file (git-excluded). Rules: short manuscript edits, keep existing wording/notation, reply = one plain continuous block with NO numbers (no section/table/result numbers, no numeric counts), no bold.

## Code facts (verified in `SINGLE/SINGLE_helyx_training.ipynb` and `MULTI/MULTI_helyx_training.ipynb`)
- SINGLE `NetCameraBW`: ImageNet-pretrained MobileNetV2, first conv REPLACED by a 1-channel conv, head `Linear(1280, 6)`. MULTI `NetCameraBW3x`: ImageNet-pretrained `mobilenet.features` used as is (its native 3-channel first conv takes the three stacked grayscale images, i.e. NOT modified), head `Linear(1280,512)-LeakyReLU-Linear(512,18)`.
  So the head differs in size AND structure, and the first layer is modified only for the single-section arm. The reviewer is right, and the manuscript's "the first 2D kernel is modified" is only true for the single-section arm.
- Curvature networks: heads 5/4/3 outputs (single) and 15/12/9 (multi) for quadratic/affine/constant models, each created from the corresponding pose network of the same arm (`load_state_dict(..., strict=False)`).
- ASSUMED (user: assume the rest): no single-section weights were reused for the multi-section network (the notebooks load none); all networks start from ImageNet weights and each curvature network starts from the pose network of the same arm. Verify before submission; if wrong, drop edits E5 to E7.

## Manuscript edits (search by Find text)

### E1. Section 3.1 (Vision Based Proprioception, CNN architecture paragraph)

Find:
```latex
To process the image batches, the first 2D kernel is modified and preceded by a normalization layer. This is the only non-pre-trained component of the feature extractor, making the sensing design scalable, as adapting to a different number of sections requires adjusting only the first layer (Fig.~\ref{fig:Figure_3}\textbf{a}).
```
Replace:
```latex
To process the image batches, the first 2D kernel is adapted to the number of input channels and preceded by a normalization layer. Only this layer and the regression head depend on the number of sections, so the pretrained backbone is reused and extending the design to a different number of sections requires adapting both and retraining the network (Fig.~\ref{fig:Figure_3}\textbf{a}); we validate one and three sections.
```

### E2. Introduction, "Research problem and hypothesis" paragraph

Find:
```latex
that scales with the number of segments.
```
Replace:
```latex
that extends to different numbers of sections.
```

### E3. Contribution list, item 1 (two small replacements)

Find:
```latex
A distributed and scalable vision-based sensing strategy
```
Replace:
```latex
A distributed and modular vision-based sensing strategy
```

Find:
```latex
It scales to arms with different numbers of sections through modular hardware design and a lightweight CNN architecture.
```
Replace:
```latex
It extends to arms with different numbers of sections through modular hardware design and a lightweight CNN architecture whose input and output layers are retrained for each arm.
```

### E4. Conclusion (two small replacements)

Find:
```latex
This work proposes a scalable framework for vision-based proprioception
```
Replace:
```latex
This work proposes a modular framework for vision-based proprioception
```

Find:
```latex
scales along the arm length without affecting its behavior
```
Replace:
```latex
extends along the arm length without affecting its behavior
```

Fig. 3 caption: handled in E6 (and the network table of `AIS_comment10_final.md`).

### E5. Section 3.1.1 Network Training (main text)
Find:
```latex
We used transfer learning within the same robot and across the two manipulators: $f_C^1$ networks were initialized with the $f_p^1$ backbone, and $f_p^3$ was initialized from $f_p^1$.
```
Replace:
```latex
All networks start from ImageNet-pretrained MobileNetV2 weights, and the curvature networks of each arm were initialized from the pose network of the same arm.
```

### E6. Fig. 3 caption (no redraw; the arrow in the figure is explained in the caption)
Find:
```latex
Transfer learning is applied between pose and curvature networks and to adapt the single-section to the multi-section network.
```
Replace:
```latex
Transfer learning is applied between the pose and the curvature networks of the same arm; the networks of the two arms are initialized independently from ImageNet-pretrained weights, and the left transfer-learning arrow indicates the reuse of this pretrained backbone for the one-image and the three-image inputs, not of trained single-section weights. The input convolution and the regression head depend on the number of sections and are retrained for each arm.
```

### E7. SI, CNN Architecture and Training Parameters
Find:
```latex
For network initialization across the multi-section arm, $f_p^3$ was initialized from $f_p^1$ by modifying the first convolutional layer, and the resulting backbone was subsequently used to initialize the curvature estimators $f_C^3$.
```
Replace:
```latex
For the multi-section arm, $f_p^3$ starts from ImageNet-pretrained weights, with a three-channel input convolution for the three stacked images, and the resulting backbone was subsequently used to initialize the curvature estimators $f_C^3$.
```

## Letter block (replaces the Comment 3 block in `response_letter.tex`)

```latex
\begin{point}[Substantiate or narrow the scalability claim]\label{c:3}
The estimator is not invariant to the number of arm sections. Images from $n_{\text{cameras}}$ are stacked as $n_{\text{input}}$ channels, so the first convolutional layer changes with $n$. The output head must also change---from 6 to 18 pose variables and from one to three sets of curvature parameters. Separate networks are trained for the one- and three-section arms.

Transfer learning may reduce retraining effort, but the present method is not plug-and-play across arbitrary arm lengths and is not validated on an unseen section count. The statement that only the first layer must be adjusted also conflicts with Fig.~3 because the regression head changes as well.
\end{point}
\begin{reply}
We thank the reviewer for this comment and agree that the scalability claim was overstated. The estimator depends on the number of sections: the number of stacked input channels determines the input layer, and the regression head changes with the number of sections, so separate networks are trained for the single-section and multi-section arms, and the design was validated only on these two arms. We have therefore removed the statement that only the first layer must be adjusted. The manuscript now states that the pretrained backbone is reused while the input layer and the regression head are adapted and the network is retrained for each arm, and that only the single-section and multi-section arms were validated. The words scalable and scales have been replaced by modular and extends in the introduction, the contribution list and the conclusion. We also corrected the description of transfer learning: the networks of the two arms are initialized independently from ImageNet-pretrained weights, and the curvature networks from the pose network of the same arm.
\end{reply}
```
