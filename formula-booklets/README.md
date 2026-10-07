# Formula booklets

Two printable formula booklets. They list every formula of the course notes, with symbols, units
and the conditions under which each one applies.

| File | Covers | Pages |
|---|---|---|
| [`pdf/Formula-Booklet_Quantum-Chemistry.pdf`](pdf/Formula-Booklet_Quantum-Chemistry.pdf) | Chemistry S1-1, handout chapters 1–5: the atom and its particles; light and spectra (Rydberg, Bohr); quantum numbers and orbitals; configurations and the periodic table; periodic properties (Slater, PES, dipole moment, Pauling, Allred–Rochow); standard quantum results for going further (de Broglie, Heisenberg, the Bohr derivation, particle in a box) | 6 |
| [`pdf/Formula-Booklet_Physics.pdf`](pdf/Formula-Booklet_Physics.pdf) | Physics for Engineers: Electricity Part 1 (1.A–3.C, Boxes 1–24) and Thermodynamics Part 1 (1.A–3.C, Boxes 1–18). Part III covers work, heat and heat engines: the first law, ideal-gas processes, Carnot and Stirling cycles | 9 |

## How the booklets are organised

- Each row gives the quantity and where it is in the notes (box, equation, section or page),
  then the formula, then the symbols with their units and when the formula applies. The
  notes' blank boxes are filled in.
- **†** marks a result that is not printed in the notes. It is a direct consequence, a
  standard result used in the exercises, or (in the physics booklet) the material of
  Part III, which goes beyond Thermodynamics Part 1.
- Page 1 lists the constants and conversions. The last page summarises the units of every
  quantity and the letters that mean two different things (p, ρ, n…).

## Corrections to the notes

Both booklets flag the misprints found in the source material:

- **Chemistry, §2.4.3:** in Balmer's formula, n = 3, 4, 5…, not 1, 2, 3.
- **Electricity, eq. (17):** the denominator of Millman's formula should read
  1/R₁ + 1/R₂ + … + 1/Rₙ.
- **Electricity, eqs. (15)–(16):** the left-hand side is u₂, not u₁.
- **Electricity, eq. (24):** P_Th there means E_Th·i⋆.
- **Electricity, Tabs. 3–4:**
  - The five ratios average 50.04 Ω, not the printed 50.17 Ω.
  - The regression gives 49.99 Ω ≈ 50.0 Ω.
  - The uncertainty formula gives 0.08 Ω, not the printed 1.001 Ω.

## Checks

`python3 tools/check_formulas.py` checks the booklets independently. It re-derives every
relation symbolically with sympy and recomputes every constant, number and table value: **145
checks, 0 failures**. Examples include the radial nodes n − ℓ − 1 from the hydrogen wavefunctions,
the Madelung order and period lengths, the group rules for Z = 1–36, the Van der Waals critical
point against the T_c column of Tab. 7, and the Carnot and Stirling energy balances.

## Rebuilding

You need TeX Live (`pdflatex` with `tcolorbox`, `siunitx`, `mathtools`, `mhchem`) and Python 3 with
`sympy`.

```bash
./build.sh                     # both booklets, then the checks
./build.sh physics             # one booklet
python3 tools/check_formulas.py
```

The shared layout is `src/formulabook.sty`. Add a formula with
`\fe[source]{quantity}{formula}{symbols, units, conditions}`, or with `\fe*` for one that is not
in the notes.

---
*Unofficial study material written from the course notes. It is not an official formula sheet;
check with your teachers what is allowed in an exam.*
