# AIS 3400076 — Minor comments 11 to 15 (Pages 1-5) (draft; red/[..] items need the user)

Local-only (git-excluded). Rules: short edits, reply = one plain block, no numbers, no bold, no quoted manuscript text.
Letter headings: "Minor comments --- Pages 1--2" holds 11 and 12; "Pages 3--5" holds 13 to 15.

---
## Comment 11: "markerless"

### Edit (contribution list, item 1; wording from the Comment 1 package)
Find:
```latex
It provides dense, markerless feedback for two outputs:
```
Replace:
```latex
It provides dense feedback, markerless at inference (external optical markers are used only to generate the supervised labels), for two outputs:
```
(If you already applied the Comment 1 text for this item, apply this to the new text. The Comment 2 lead-in "which requires no markers at inference" is already consistent; add "optical" there if you want it identical.)

### Letter
```latex
\begin{point}[``Markerless'']\label{c:11}
Use 'markerless at measured inferences' rather than simply 'markerless.' External optical markers are required to generate the supervised labels, even though markers are not required during deployment.
\end{point}
\begin{reply}
We thank the reviewer for this precise remark. The term now reads markerless at inference in the contribution list, and the manuscript states that external optical markers are used only to generate the supervised labels and are not required during deployment.
\end{reply}
```

---
## Comment 12: "section" vs "segment"

Decision: use "section" everywhere (title, abstract, figures and results already use "section", "Section I/II/III").

### Edit list (Overleaf search for "segment", case-insensitive; replace each hit with "section" except where noted)
main2.tex (line numbers of the version I read; search by text):
- Fig. 1 caption: "three independent segments" -> "three independent sections".
- Intro research-problem sentence: already rewritten in Comment 3 ("extends to different numbers of sections").
- Section 2.1: "corresponds to the first segment of the multi-section arm. The multi-section robot comprises three independent ..." -> section(s) in both places.
- PCC paragraph: "each segment bends in any direction" -> "each section bends ...".
- PPC paragraph: "of a segment as a polynomial" -> "of a section as a polynomial".
- Marker paragraph: "placed along each segment" -> "placed along each section".
- Conventions paragraph: "Curvature parameters $C_j$ for segment $j$" -> "for section $j$"; "for the multi-segment case" (twice) -> "multi-section"; "segment curvature parameters" -> "section curvature parameters".
- Fig. 5 caption: "single-segment arm" -> "single-section arm". Fig. 8 caption: "multi-segment arm" -> "multi-section arm".
- Subsection titles: "Single-Segment Reconstruction and Control" -> "Single-Section ..."; "Multi-Segment Reconstruction and Control" -> "Multi-Section ...".
- Multi-section results: "single-segment case" -> "single-section case"; "between segments" -> "between sections".
- Conclusion: "each segment" is already changed in the Comment 1 package (A6).
Optional consistency fix: replace "Module I/II/III" by "Section I/II/III" in the multi-section static pose results and in the SI relative-error text ("Module II contributes ...").
supporting_information.tex: replace "segment" by "section" in: PCC derivation ("each arc included in a segment", "the cylinder soft segment"), Fig. S1 caption ("multi-segment robot"), "different segments", "single- and multi-segment" (dataset composition), "multi-segment manipulator", "across segments" (twice), "source segment"/"target segment", "preceding segment".
notation.tex: DO NOT replace in the $L_i$ row; change it to: `$L_i$ & Arc length of the $i$-th outer boundary arc ($i \in \{1,2,3,4\}$). \\`
Check by eye in the figures (raster images, not searchable): Fig. 3 and Fig. 8 labels, Fig. S1.

### Letter
```latex
\begin{point}[``Section'' vs.\ ``segment'']\label{c:12}
Use either 'section' or 'segment' consistently throughout the manuscript, figures, algorithms, and SI.
\end{point}
\begin{reply}
We thank the reviewer. The manuscript, the figures, the algorithms and the Supporting Information now use section consistently for the parts of the arm, and the word segment is no longer used for them; in the geometric derivation the boundary arcs are now called arcs.
\end{reply}
```

---
## Comment 13: calibration paragraph

Facts: the submitted text says "tightening all tendons" (no "ten" appears in the manuscript or SI; the reviewer's "all ten tendons" does not match, so the reply states the correct counts without disputing it). In the code, the calibration is interactive and identical for both arms (`calibrate_motors()` in the single- and multi-section controllers and the acquisition scripts: each motor is stepped by keyboard commands, with accelerating steps, and confirmed with a key). The motors run in Dynamixel extended position-control mode (mode 4); no current limit is written anywhere in the repo, so the sentence "through current control ... with a predefined current limit" is NOT supported by the code. CONFIRMED by the user: the manuscript wording on current control and a predefined current limit is not supported by the code, so the replacement below drops it; add a current limit only if the hardware really enforces one.

### Edit
Find:
```latex
Before each data acquisition session or experimental trial, the robots are calibrated by tightening all tendons through current control of the actuation motors. The motors then operate in position-control mode with a predefined current limit.
```
Replace (fill or correct the bracketed items):
```latex
Before each data acquisition session or experimental trial, the same preload procedure is applied to both robots: the three tendons of the single-section arm and the nine tendons of the multi-section arm are tightened one at a time through keyboard-commanded motor steps until each is taut, as judged by the operator, and the encoder readings at this configuration define the zero of the tendon lengths. The motors then operate in extended position-control mode.
```

### Letter
```latex
\begin{point}[Tendon count and preload procedure]\label{c:13}
The calibration paragraph says that 'all ten tendons' are tightened, but the multi-section arm has nine tendons and the single-section arm has three. Correct the number and state whether the same preload procedure is used for both systems.
\end{point}
\begin{reply}
We thank the reviewer. The paragraph now states the number of tendons of each arm, three for the single-section arm and nine for the multi-section arm, and specifies that the same preload procedure is used for both: each tendon is tightened in turn until it is taut, the resulting encoder readings define the zero, and the motors then operate in position-control mode.
\end{reply}
```

---
## Comment 14: camera specification

Facts (code): images 640 x 480, converted to grayscale; capture requested at a low frame rate with a one-frame buffer; no exposure/gain setting anywhere in the repo (camera defaults). Manufacturer, model, lens, field of view, size and mass are NOT in the repo: USER INPUT.

### Edit (Section 2.1, sentence that mentions the USB cables and resolution; add after it)
```latex
 The cameras are commercial off-the-shelf USB cameras delivering $480\times640$ grayscale images, with exposure and gain left at the camera defaults.
```
(The user gave only "commercial USB camera": manufacturer, model, lens, field of view, size and mass are NOT stated, and the reviewer asked for them. The reply below says only what is stated.)

### Letter
```latex
\begin{point}[Camera specifications]\label{c:14}
Identify the camera manufacturer and model, lens or field of view, nominal frame rate, and the physical size and mass of each camera and mount.
\end{point}
\begin{reply}
We thank the reviewer. The cameras are commercial off-the-shelf USB cameras, and the experimental setup and the reproducibility table in the Supporting Information now state the image format, the capture method and the exposure behavior, which was left at the camera defaults. The networks are trained on images from these cameras, so the reported results refer to this hardware, which we now say explicitly.
\end{reply}
```

---
## Comment 15: simultaneous acquisition

Facts (code): `ThreadedCameraSystem` runs one free-running thread per camera (read, store latest frame, sleep), with no shared trigger; the controller takes a snapshot of the latest frame of each camera; hence the three images are not captured simultaneously (they can differ by up to about one read period). During data collection the arm dwells at each commanded configuration before frames are taken, so for quasi-static operation the asynchrony is immaterial, but it must be stated.

### Edit 1: Fig. 1 caption
Find:
```latex
Images from the three cameras are acquired simultaneously and fed to CNNs,
```
Replace:
```latex
Images from the three cameras are captured by software without hardware triggering and fed to CNNs,
```

### Edit 2: Section 2.1, after the sentence on the three USB cables
```latex
 The cameras are read by independent software threads without a common trigger, so the three images are captured within one frame period of each other rather than simultaneously; this is immaterial for the quasi-static operation considered here.
```

### Letter
```latex
\begin{point}[Simultaneous image acquisition]\label{c:15}
The claim that images are acquired simultaneously should be supported by the synchronization metho as this type software capture is not necessarily simultaneous hardware triggering.
\end{point}
\begin{reply}
We thank the reviewer and agree. The cameras are read by independent software threads without hardware triggering, so the images are not captured simultaneously but within one frame period of each other. We removed the claim of simultaneous acquisition from the figure caption and describe the capture method in the experimental setup; the asynchrony is immaterial for the quasi-static operation considered here, since the arm is stationary during capture.
\end{reply}
```
