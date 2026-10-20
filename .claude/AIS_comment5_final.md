# AIS 3400076 — Comment 5: "Correct the curvature-coordinate inconsistency" (draft)

Local-only (git-excluded). Rules: short edits, keep notation, reply = one plain block, no numbers, no bold.

Decision: use DIMENSIONAL arc length `s in [0, L]` everywhere (matches the SI and the code: `SINGLE_reconstruction_utility.py` integrates `c0*s + c1*s^2/2 + c2*s^3/3` in mm, labels are `[S, c0, c1, c2, phi]` with S = L in mm, and the N_C errors in the testing notebook are in mm^-1, mm^-2, mm^-3). Keep the symbol `s` (no refactor to `x`).

## Edits

### E1. Main text, PPC paragraph (Eq. 4 stays as written; only the definition of s changes)
Find:
```latex
as a polynomial in the normalized arc length $s \in [0, 1]$,
```
Replace:
```latex
as a polynomial in the arc length $s \in [0, L]$ (so that $c_0$, $c_1$, $c_2$ have units of $\text{mm}^{-1}$, $\text{mm}^{-2}$, $\text{mm}^{-3}$),
```

### E2. Main text, translation integral (remove the explicit factor L in the three integrals)
Find:
```latex
        c_\phi \int_0^s L s_{\theta(v)}dv &
        s_\phi \int_0^s L s_{\theta(v)}dv &
        \int_0^s L c_{\theta(v)}dv
```
Replace:
```latex
        c_\phi \int_0^s s_{\theta(v)}dv &
        s_\phi \int_0^s s_{\theta(v)}dv &
        \int_0^s c_{\theta(v)}dv
```

### E3. Main text, reference points of the markers
Find:
```latex
at $s = \frac{1}{3}, \frac{2}{3}, 1$ (details in the Supporting Information)
```
Replace:
```latex
at $s = \frac{L}{3}, \frac{2L}{3}, L$ (details in the Supporting Information)
```

### E4. Main text, least-squares fit
Find:
```latex
\sum_{s=\frac{1}{3}, \frac{2}{3}, 1}
```
Replace:
```latex
\sum_{s=\frac{L}{3}, \frac{2L}{3}, L}
```

### E5. SI, initialization of the coefficients
Find:
```latex
$s = \tfrac{1}{3}, \tfrac{2}{3}, 1$
```
Replace:
```latex
$s = \tfrac{L}{3}, \tfrac{2L}{3}, L$
```
(The SI closed-form solutions already use L/3, 2L/3, L and c0 = theta/L, so nothing else changes there.)

### E6. `notation.tex` (used by the main text and the SI)
Find: `$s$ & Normalized arc length along a section axis ($s \in [0, 1]$). \\`
Replace: `$s$ & Arc length along a section axis ($s \in [0, L]$). \\`

Find: `$\theta(s)$ & Local bending angle along the central axis at normalized arc length $s$. \\`
Replace: `$\theta(s)$ & Local bending angle along the central axis at arc length $s$. \\`

Find: `$c(s)$ & Polynomial curvature function at normalized arc length $s$. \\`
Replace: `$c(s)$ & Polynomial curvature function at arc length $s$. \\`

Find: `$c_0, c_1, c_2$ & Coefficients of the polynomial curvature approximation. \\`
Replace: `$c_0, c_1, c_2$ & Coefficients of the polynomial curvature approximation (units $\text{mm}^{-1}$, $\text{mm}^{-2}$, $\text{mm}^{-3}$). \\`

(If a row's exact text differs in Overleaf, search for "normalized arc length".)

## Letter block

```latex
\begin{point}[Correct the curvature-coordinate inconsistency]\label{c:5}
The main manuscript defines $s$ as normalized arc length and writes $\theta(s)=c_0 s+\frac{1}{2}c_1 s^2+\frac{1}{3}c_2 s^3$ in Eq.~4. Under this definition, initialization should not introduce factors of section length $L$. In contrast, SI Eqs.~S5--S9 evaluate the polynomial at $L/3$, $2L/3$, and $L$, and use $c_0=\theta/L$ for constant curvature. This treats the independent variable as dimensional arc length.

These formulations have different coefficient units and cannot both be correct. The paper should consistently use either normalized arc length $u=x/L$ or dimensional arc length $x\in[0,L]$, and revise Eqs.~4--6, SI Eqs.~S3--S9, the translation integral, nomenclature, and coefficient units accordingly.
\end{point}
\begin{reply}
We thank the reviewer for pointing out this inconsistency. The implementation uses dimensional arc length throughout, as in the Supporting Information, so we made the main text consistent with it: the arc length is now defined from zero to the section length, the coefficients carry units of inverse length, inverse length squared and inverse length cubed, the explicit factor of the section length has been removed from the translation integral, the fitting points are now one third, two thirds and the full section length, and the nomenclature states the definition and the units. The initialization in the Supporting Information already used these points and now refers to the same definition.
\end{reply}
```
