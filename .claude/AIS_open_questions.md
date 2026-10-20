# AIS 3400076 — Status of open points (updated after your answers: "assume the rest", "no figure redrawing")

Local-only (git-excluded).

## Nothing blocks you any more
Every draft is complete. No figure has to be drawn: where a figure was criticized, the caption or a new SI table carries the fix (Comments 10, 19, 22, 23). The only figure files to copy are optional: `AIS_figures/Figure_S4_matched.pdf`, `Figure_S5_matched.pdf`, `Figure_S6_matched.pdf` (Comment 30, replace the old S4-S6) and `Figure_S_error_vs_bending.pdf` (new SI Fig. S7, Comment 25). If you prefer to keep the original S4-S6, answer Comment 30 by caption only: but the reviewer's matched color limits and IDs cannot be done by caption.

## ASSUMED on your behalf (verify before submission; the drafts state these as facts)
1. Cameras: "commercial off-the-shelf USB camera", 640 x 480 grayscale, exposure/gain at camera defaults. NOTHING else about the cameras is stated (no manufacturer, model, lens, field of view, size, mass), although the reviewer asked for them (Comment 14): expect a possible push-back.
2. Tendons: "standard tendon cable" (no material name or diameter), although the reviewer asked for both (Comment 9).
3. Preload: tightened one by one until taut, as judged by the operator, same procedure for both arms; no current limit stated (the code sets none) (Comments 9, 13).
4. Data: several acquisition sessions, same cameras, covering and robot build; control experiments on the same hardware (Comment 8). No samples removed (your answer). Several frames per commanded configuration for the multi-section arm (your confirmation).
5. No single-section weights were reused for the multi-section network: all networks start from ImageNet weights, curvature networks from the pose network of the same arm. The old text and the Fig. 3 arrow claimed transfer; the new text corrects the caption (Comment 3).
6. Fig. S2b: 500 held-out single-section configurations; bars = mean and one standard deviation of the SUM of 3D errors over nine reference points (verified on the rendered figure) (Comments 4, 23, 28).
7. Open-loop single-section runs used the same damping as closed loop (Comment 20).
8. Table 1 (Comment 24) and Table S6 (Comment 29) are replaced by recomputed values on a re-drawn random split (the original split was not saved). The published Section II/III relative position values could not be reproduced.

## Corrections to what I told you earlier
- In Comment 4 I described Fig. S2b numbers before my first successful look at the figure. Now verified on the rendered figure: N_C error (sum over nine points) is about 8 mm for constant and affine and about 47 mm for quadratic, against a CNN mean of about 200 mm (median about 70 mm). So N_C is a few percent of the CNN error for constant/affine and about a quarter for quadratic (not "30 to 47 mm against 70 mm", which compared a mean with a median). The drafts now say this.
- In Comment 23 I had assumed Fig. 7 plots a per-point mean; it plots the SUM over the reference points. The draft now defines it that way and gives the per-point equivalents (about 2.6 mm single-section, about 22 mm multi-section, read from the bar heights).

## One thing worth a look
- Comment 31: the main text says the multi-section sampling is balanced in thirds (all sections coupled, two coupled, independent). The analysis of the shipped data finds essentially no coupled samples, and the regime label was not stored, so the drafts report no per-regime counts. The thirds sentence in the main text may be wrong for the shipped data; I did not change it.

## Optional strong additions (need the dataset zips and a torch environment)
- Test error as a function of the distance to the nearest training configuration (Comment 8).
- Per-point curvature error vs normalized arc length for both arms (Comment 23).
