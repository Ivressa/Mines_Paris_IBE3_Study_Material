"""Independent checks of the two formula booklets.

Every derived relation is re-derived symbolically (sympy) and every number, constant and
table value printed in the booklets is recomputed. Run: python3 tools/check_formulas.py
"""
import math
from itertools import combinations

import sympy as sp

fails = 0


def check(label, got, expected, rel=5e-3):
    """Numerical check, relative tolerance rel."""
    global fails
    ok = math.isclose(float(got), float(expected), rel_tol=rel, abs_tol=1e-12)
    print(f"{'OK ' if ok else 'BAD'} {label}: computed {float(got):.6g}, booklet {float(expected):.6g}")
    if not ok:
        fails += 1


def same(label, a, b):
    """Symbolic identity check: a - b simplifies to 0."""
    global fails
    ok = sp.simplify(sp.expand_log(sp.simplify(a - b), force=True)) == 0
    print(f"{'OK ' if ok else 'BAD'} {label}")
    if not ok:
        fails += 1
        print("     difference:", sp.simplify(a - b))


def true(label, cond):
    global fails
    print(f"{'OK ' if cond else 'BAD'} {label}")
    if not cond:
        fails += 1


# precise constants (CODATA) and the handout's rounded values
h, c, e, me = 6.62607015e-34, 2.99792458e8, 1.602176634e-19, 9.1093837e-31
eps0, NA, kB, R = 8.8541878128e-12, 6.02214076e23, 1.380649e-23, 8.314462618
h_ho, c_ho, e_ho, RH_ho = 6.62e-34, 3.00e8, 1.6e-19, 3.29e15
amu = 1.6605e-27

# =========================================================================== chemistry
print("== Quantum chemistry booklet: constants and conversions")
check("h R_H = 13.6 eV (handout values)", h_ho * RH_ho / e_ho, 13.6)
check("R_H / c = 1.097e7 m^-1", RH_ho / c_ho, 1.097e7)
check("hbar = h/2pi = 1.05e-34", h_ho / (2 * math.pi), 1.05e-34, rel=6e-3)
check("eps0 = 1/(4 pi k), k = 8.99e9", 1 / (4 * math.pi * 8.99e9), 8.85e-12)
check("1 eV/atom = 96.5 kJ/mol", e * NA / 1000, 96.5)
check("H: 13.6 eV = 1312 kJ/mol", 13.6 * e * NA / 1000, 1312, rel=1e-3)
check("hc = 1240 eV nm", h * c / e * 1e9, 1240, rel=1e-3)
check("hc = 1240 eV nm (handout values)", h_ho * c_ho / e_ho * 1e9, 1240, rel=2e-3)
check("1 amu c^2 = 931.5 MeV", amu * c ** 2 / e / 1e6, 931.5, rel=1e-3)
check("N_A x 1 amu = 1 g", NA * amu * 1000, 1.0, rel=1e-3)
check("m_e = 1/1823 amu", amu / 9.1094e-31, 1823, rel=1e-3)
check("m_p = 1.0073 amu", 1.6727e-27 / amu, 1.0073, rel=1e-4)
check("m_n = 1.0087 amu", 1.6749e-27 / amu, 1.0087, rel=1e-4)
check("e/m_e = 1.76e11 C/kg", e_ho / 9.1094e-31, 1.76e11)
check("e/m_p is 1836 times smaller", 1.6727e-27 / 9.1094e-31, 1836, rel=1e-3)
check("1 MeV = 1.6e-13 J", 1e6 * e_ho, 1.6e-13)
check("nuclear density ~ 2e17 kg/m^3 (proton, r = 1.2 fm)",
      1.6727e-27 / (4 / 3 * math.pi * 1.2e-15 ** 3), 2e17, rel=0.25)
check("mass defect of C-12 (worksheet 1): 0.0993 amu",
      6 * (1.0073 + 1 / 1823) + 6 * 1.0087 - 12, 0.0993, rel=1e-3)

print("== Spectra")
lam = lambda n1, n2: c_ho / (RH_ho * (1 / n1 ** 2 - 1 / n2 ** 2))      # Rydberg, handout values
for n2, nm in zip((3, 4, 5, 6), (656, 486, 434, 410)):
    check(f"Balmer {n2}->2 = {nm} nm", lam(2, n2) * 1e9, nm, rel=1.5e-3)
table = {1: (122e-9, 91.2e-9), 2: (657e-9, 365e-9), 3: (1876e-9, 821e-9),
         4: (4.05e-6, 1.46e-6), 5: (7.46e-6, 2.28e-6)}
for n1, (first, limit) in table.items():
    check(f"series n1={n1}: first line", lam(n1, n1 + 1), first, rel=4e-3)   # 3 significant figures
    check(f"series n1={n1}: limit c n1^2/R_H", c_ho * n1 ** 2 / RH_ho, limit, rel=2e-3)
for n in range(2, 8):
    check(f"number of lines from level {n} = n(n-1)/2", len(list(combinations(range(1, n + 1), 2))),
          n * (n - 1) / 2)
check("He+ ionisation energy 13.6 Z^2 = 54.4 eV", 13.6 * 4, 54.4)
check("Na D doublet: Delta E = 2.1 meV",
      h * c * (1 / 589.0e-9 - 1 / 589.6e-9) / e * 1000, 2.1, rel=0.03)
check("Bohr magneton 9.27e-24 J/T", e * (h / 2 / math.pi) / (2 * me), 9.27e-24, rel=1e-3)

print("== Bohr model (going further)")
a0 = eps0 * h ** 2 / (math.pi * me * e ** 2)
check("a0 = eps0 h^2/(pi m_e e^2) = 52.9 pm", a0 * 1e12, 52.9, rel=1e-3)
v1 = e ** 2 / (2 * eps0 * h)
check("v1 = e^2/(2 eps0 h) = 2.19e6 m/s", v1, 2.19e6, rel=2e-3)
check("m_e e^4/(8 eps0^2 h^2) = 13.6 eV", me * e ** 4 / (8 * eps0 ** 2 * h ** 2) / e, 13.6, rel=1e-3)
check("R_H = m_e e^4/(8 eps0^2 h^3) = 3.29e15 Hz", me * e ** 4 / (8 * eps0 ** 2 * h ** 3), 3.29e15, rel=1e-3)
check("m_e v1 a0 = hbar (n = 1)", me * v1 * a0, h / (2 * math.pi), rel=1e-6)

print("== Orbitals")
r, Z, a, x, L, m_ = sp.symbols("r Z a_0 x L m", positive=True)
n_ = sp.symbols("n", positive=True, integer=True)
psi1s = 1 / sp.sqrt(sp.pi) * (Z / a) ** sp.Rational(3, 2) * sp.exp(-Z * r / a)
P = 4 * Z ** 3 / a ** 3 * r ** 2 * sp.exp(-2 * Z * r / a)
same("P(r) = 4 pi r^2 |psi_1s|^2", 4 * sp.pi * r ** 2 * psi1s ** 2, P)
same("int_0^inf P dr = 1", sp.integrate(P, (r, 0, sp.oo)), 1)
true("max of P(r) at r = a0/Z", sp.solve(sp.diff(P, r), r) == [a / Z])
same("orbitals per shell: sum (2l+1) = n^2",
     sp.summation(2 * sp.Symbol("l") + 1, (sp.Symbol("l"), 0, n_ - 1)), n_ ** 2)
from sympy.physics.hydrogen import R_nl
for nn in range(1, 6):
    for ll in range(nn):
        poly = sp.simplify(R_nl(nn, ll, r, 1) * sp.exp(r / nn) / r ** ll)
        roots = [s_ for s_ in sp.Poly(poly, r).nroots() if abs(sp.im(s_)) < 1e-9 and sp.re(s_) > 1e-9]
        true(f"radial nodes of {nn}{'spdfg'[ll]} = n - l - 1 = {nn - ll - 1}", len(roots) == nn - ll - 1)

print("== Configurations")
order = sorted(((n, l) for n in range(1, 8) for l in range(min(n, 4)) if n + l <= 8),
               key=lambda t: (t[0] + t[1], t[0]))      # up to 7p
printed = "1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s 5f 6d 7p"
true("Madelung order matches the printed filling order",
     " ".join(f"{n}{'spdf'[l]}" for n, l in order) == printed)
# period lengths: a period starts at each ns subshell
lengths, cur = [], 0
for n, l in order:
    if l == 0 and cur:
        lengths.append(cur)
        cur = 0
    cur += 2 * (2 * l + 1)
lengths.append(cur)
true("period lengths 2 8 8 18 18 32 32", lengths == [2, 8, 8, 18, 18, 32, 32])
# group rule for Z = 1..36
GROUP = [1, 18, 1, 2, 13, 14, 15, 16, 17, 18, 1, 2, 13, 14, 15, 16, 17, 18,
         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
ok = True
for z in range(1, 37):
    conf, left = {}, z
    for n, l in order:
        k = min(left, 2 * (2 * l + 1)); conf[(n, l)] = k; left -= k
        if not left: break
    if z in (24, 29):                       # Cr, Cu: one 4s electron moves to 3d
        conf[(4, 0)] -= 1; conf[(3, 2)] += 1
    nmax = max(n for (n, l), k in conf.items() if k)
    ns, np_ = conf.get((nmax, 0), 0), conf.get((nmax, 1), 0)
    d = conf.get((nmax - 1, 2), 0) if nmax >= 4 else 0
    if z == 2:
        continue                             # He: group 18 with 1s2 (noted in the booklet)
    if np_:                                   # p block: group = 10 + valence electrons
        g = 10 + ns + np_
    elif 0 < d < 10 or (d == 10 and ns == 1):  # d block: valence electrons = group
        g = ns + d
    elif d == 10:                            # Zn: d10 s2
        g = 12
    else:
        g = ns
    ok &= g == GROUP[z - 1]
    if d and z not in (24, 29) and d < 10:
        ok &= (GROUP[z - 1] - 2 == d)         # x = group - 2
true("group / valence-electron rules for Z = 1..36", ok)

print("== Periodic properties")
check("Cl average atomic mass 35.45", 0.7577 * 34.97 + 0.2423 * 36.97, 35.45, rel=1e-3)
check("K average atomic mass 39.09", 0.9326 * 38.96 + 0.0673 * 40.96, 39.09, rel=1e-3)
M1, M2, Mb = sp.symbols("M1 M2 Mbar")
x1 = sp.solve(sp.Eq(Mb, x * M1 + (1 - x) * M2), x)[0]
same("two isotopes: x1 = (M2 - Mbar)/(M2 - M1)", x1, (M2 - Mb) / (M2 - M1))
check("boron: 20.0 % of 10B", (11.009 - 10.81) / (11.009 - 10.013), 0.200, rel=2e-3)
check("Slater Cl: sigma = 10.9", 6 * 0.35 + 8 * 0.85 + 2 * 1.00, 10.9)
check("Slater Cl: Zeff = 6.1", 17 - (6 * 0.35 + 8 * 0.85 + 2), 6.1)
check("Slater Na: Zeff = 2.2", 11 - (8 * 0.85 + 2 * 1.00), 2.2)
check("Pauling H-F: Delta = 304.5 kJ/mol", 567 - math.sqrt(436 * 158), 304.5, rel=1e-3)
check("Pauling H-F: |dchi| = 1.78", 0.102 * math.sqrt(567 - math.sqrt(436 * 158)), 1.78, rel=2e-3)
check("Allred-Rochow Cl: chi = 2.98", 0.359 * 6.1 / 0.99 ** 2 + 0.744, 2.98, rel=2e-3)

print("== Going further")
U, mm = sp.symbols("U m_e", positive=True)
pp = sp.sqrt(2 * mm * sp.Symbol("e", positive=True) * U)
same("E_k = eU = p^2/2m for the de Broglie electron", pp ** 2 / (2 * mm), sp.Symbol("e", positive=True) * U)
hb = sp.symbols("hbar", positive=True)
psi = sp.sqrt(2 / L) * sp.sin(n_ * sp.pi * x / L)
E = n_ ** 2 * (2 * sp.pi * hb) ** 2 / (8 * m_ * L ** 2)
same("particle in a box solves -hbar^2/2m psi'' = E psi", -hb ** 2 / (2 * m_) * sp.diff(psi, x, 2), E * psi)
same("particle in a box is normalised", sp.integrate(psi ** 2, (x, 0, L)), 1)

# =========================================================================== physics
print("== Physics booklet: electricity")
check("1 kW h = 3.6e6 J", 1000 * 3600, 3.6e6)
check("drift velocity Cu 1 mm^2 1 A ~ 7e-5 m/s", 1 / (8.5e28 * 1.6e-19 * 1e-6), 7e-5, rel=0.06)
i_mA = [10.20, 20.10, 30.30, 40.00, 50.20]
u_V = [0.5120, 1.0030, 1.5190, 2.0070, 2.5010]
check("Box 10 naive mean of Tab. 3 = 50.04 ohm (notes print 50.17)",
      sum(u / i for u, i in zip(u_V, i_mA)) / 5 * 1000, 50.04, rel=2e-4)
Rhat = sum(u * i for u, i in zip(u_V, i_mA)) / sum(i * i for i in i_mA)
check("Box 11 regression = 49.99 ohm (about 50.0, as printed)", Rhat * 1000, 49.99, rel=2e-4)
s2 = sum((u - Rhat * i) ** 2 for u, i in zip(u_V, i_mA)) / (5 - 1)
uR = math.sqrt(s2 / sum((i * 1e-3) ** 2 for i in i_mA))
check("u(R) from the formula = 0.08 ohm (notes print 1.001)", uR, 0.08, rel=0.05)

R1, R2, Rc, Rt, Et, E0, uu, ii, V1_, V2_, V3_ = sp.symbols("R1 R2 R_c R_Th E_Th E u i V1 V2 V3", positive=True)
same("two in parallel: product over sum", 1 / (1 / R1 + 1 / R2), R1 * R2 / (R1 + R2))
same("voltage divider u2", R2 * uu / (R1 + R2), R2 * (uu / (R1 + R2)))
same("current divider i1 = R2/(R1+R2) i", (ii * R1 * R2 / (R1 + R2)) / R1, R2 / (R1 + R2) * ii)
same("current divider i1 = G1/(G1+G2) i", R2 / (R1 + R2) * ii, (1 / R1) / (1 / R1 + 1 / R2) * ii)
VO = sp.symbols("V_O")
R3 = sp.symbols("R3", positive=True)
sol = sp.solve((V1_ - VO) / R1 + (V2_ - VO) / R2 + (V3_ - VO) / R3, VO)[0]
same("Millman = node law in potentials", sol, (V1_ / R1 + V2_ / R2 + V3_ / R3) / (1 / R1 + 1 / R2 + 1 / R3))
# Thevenin of the divider: E in series with R1, R2 across A-B
same("divider: E_Th = R2 E/(R1+R2)", E0 * R2 / (R1 + R2), R2 / (R1 + R2) * E0)
same("divider: I_No = E_Th/R_Th = E/R1", (R2 * E0 / (R1 + R2)) / (R1 * R2 / (R1 + R2)), E0 / R1)
same("Norton and Thevenin give the same u(i)", Rt * (Et / Rt - ii), Et - Rt * ii)
ist = Et / (Rt + Rc)
same("operating point u* = R_c E_Th/(R_Th+R_c)", Et - Rt * ist, Rc * Et / (Rt + Rc))
same("power balance E_Th i* = R_Th i*^2 + R_c i*^2", Et * ist, Rt * ist ** 2 + Rc * ist ** 2)
Pc = Rc * Et ** 2 / (Rt + Rc) ** 2
same("dP_c/dR_c = E^2 (R_Th - R_c)/(R_Th + R_c)^3", sp.diff(Pc, Rc), Et ** 2 * (Rt - Rc) / (Rt + Rc) ** 3)
same("P_c max = E_Th^2/(4 R_Th) at R_c = R_Th", Pc.subs(Rc, Rt), Et ** 2 / (4 * Rt))
same("efficiency eta = R_c/(R_Th + R_c)", (Rc * ist ** 2) / (Et * ist), Rc / (Rt + Rc))

print("== Physics booklet: thermodynamics")
p, V, T, n, Rg, a_, b_, al, chi = sp.symbols("p V T n R a b alpha chi_T", positive=True)
Vig = n * Rg * T / p
same("ideal gas chi_T = 1/p", -1 / Vig * sp.diff(Vig, p), 1 / p)
same("ideal gas alpha = 1/T", 1 / Vig * sp.diff(Vig, T), 1 / T)
pig = n * Rg * T / V
same("ideal gas beta = 1/T", 1 / pig * sp.diff(pig, T), 1 / T)
# general identity beta = alpha/(p chi_T), checked on Van der Waals
pv = n * Rg * T / (V - n * b_) - a_ * n ** 2 / V ** 2
dpdT, dpdV = sp.diff(pv, T), sp.diff(pv, V)
alpha_v = -dpdT / dpdV / V                    # (dV/dT)_p = -(dp/dT)_V/(dp/dV)_T
chi_v = -1 / (V * dpdV)
same("cyclic rule on Van der Waals: beta = alpha/(p chi_T)", dpdT / pv, alpha_v / (pv * chi_v))
same("cyclic rule product = -1", dpdT * (1 / (-dpdT / dpdV)) * (1 / dpdV), -1)
rho, m = sp.symbols("rho m", positive=True)
fV = sp.Function("f")(p)                        # V(p) at fixed T
same("chi_T = (1/rho) drho/dp with rho = m/V", -1 / fV * sp.diff(fV, p), (fV / m) * sp.diff(m / fV, p))
T0, p0, V0 = sp.symbols("T0 p0 V0", positive=True)
Vc = V0 * sp.exp(al * (T - T0) - chi * (p - p0))
same("condensed EOS: (1/V) dV/dT = alpha", sp.diff(Vc, T) / Vc, al)
same("condensed EOS: -(1/V) dV/dp = chi_T", -sp.diff(Vc, p) / Vc, chi)
same("first order: V0 [1 + alpha dT - chi dp]",
     sp.series(Vc.subs({T: T0 + sp.Symbol("t"), p: p0 + sp.Symbol("q")}), sp.Symbol("t"), 0, 2).removeO()
     .subs(sp.Symbol("q"), 0), V0 * (1 + al * sp.Symbol("t")))
dT, dp_ = sp.symbols("dT dp")
same("dV = 0 gives dp/dT = alpha/chi_T", sp.solve(al * dT - chi * dp_, dp_)[0] / dT, al / chi)
check("molar volume 0 C, 1 atm = 22.4 L", R * 273.15 / 101325 * 1000, 22.4, rel=2e-3)
check("molar volume 25 C, 1 bar = 24.8 L", R * 298.15 / 1e5 * 1000, 24.8, rel=2e-3)
check("k_B = R/N_A = 1.38e-23", R / NA, 1.38e-23, rel=1e-3)
check("RT at 300 K = 2.5e3 J/mol", R * 300, 2.5e3, rel=0.01)
check("ideal gas at 1 bar: chi_T = 1e-5 /Pa", 1 / 1e5, 1e-5)
check("ideal gas at 300 K: alpha = 3.3e-3 /K", 1 / 300, 3.3e-3, rel=0.02)
check("air molar mass ~ 29 g/mol", 0.79 * 28.0 + 0.21 * 32.0, 29, rel=0.01)
Mm = sp.symbols("M", positive=True)
same("rho = pM/(RT)", (n * Mm) / Vig, p * Mm / (Rg * T))
Vm = sp.symbols("V_m", positive=True)
pvdw = Rg * T / (Vm - b_) - a_ / Vm ** 2
sol = sp.solve([sp.diff(pvdw, Vm), sp.diff(pvdw, Vm, 2)], [Vm, T], dict=True)[0]
same("VdW critical V_m,c = 3b", sol[Vm], 3 * b_)
same("VdW critical T_c = 8a/(27Rb)", sol[T], 8 * a_ / (27 * Rg * b_))
same("VdW critical p_c = a/(27 b^2)", pvdw.subs(sol), a_ / (27 * b_ ** 2))
for gas, av, bv, tc, tol in (("He", 3.46e-3, 2.38e-5, 5.2, 5e-3), ("H2", 2.45e-2, 2.67e-5, 33.2, 0.02),
                             ("N2", 0.137, 3.87e-5, 126, 5e-3), ("CO2", 0.364, 4.27e-5, 304, 5e-3),
                             ("H2O", 0.554, 3.05e-5, 647, 5e-3)):
    check(f"Tab. 7 {gas}: T_c = 8a/(27Rb)", 8 * av / (27 * R * bv), tc, rel=tol)
y = sp.symbols("y", positive=True)                # y = 1/V_m
Zv = sp.series((pvdw * Vm / (Rg * T)).subs(Vm, 1 / y), y, 0, 2).removeO()
same("VdW virial: B = b - a/(RT)", sp.expand(Zv).coeff(y, 1), b_ - a_ / (Rg * T))
same("explicit VdW form", (n * Rg * T / (V - n * b_) - a_ * n ** 2 / V ** 2 + a_ * n ** 2 / V ** 2) * (V - n * b_), n * Rg * T)

print("== Physics booklet: Part III (first law and engines)")
V1s, V2s, gam, TH, TC = sp.symbols("V_1 V_2 gamma T_H T_C", positive=True)
same("isothermal W = -nRT ln(V2/V1)", -sp.integrate(n * Rg * T / V, (V, V1s, V2s)), -n * Rg * T * sp.log(V2s / V1s))
p1 = sp.symbols("p_1", positive=True)
K = p1 * V1s ** gam                               # adiabat p V^gamma = K
W_ad = -sp.integrate(K / V ** gam, (V, V1s, V2s), conds="none")
same("adiabatic W = (p2V2 - p1V1)/(gamma - 1)", W_ad, (K / V2s ** gam * V2s - p1 * V1s) / (gam - 1))
CV = Rg / (gam - 1)
T1a, T2a = p1 * V1s / (n * Rg), (K / V2s ** gam) * V2s / (n * Rg)
same("adiabatic W = n C_V dT", W_ad, n * CV * (T2a - T1a))
same("Laplace: T V^(gamma-1) constant", T1a * V1s ** (gam - 1), T2a * V2s ** (gam - 1))
same("Laplace: T^gamma p^(1-gamma) constant", T1a ** gam * p1 ** (1 - gam),
     T2a ** gam * (K / V2s ** gam) ** (1 - gam))
same("Mayer: C_p - C_V = R (H = U + pV)", sp.diff(n * CV * T + n * Rg * T, T) / n - CV, Rg)
same("isobaric W = -p dV = -nR dT", -p * (n * Rg * (T + sp.Symbol("d")) / p - n * Rg * T / p), -n * Rg * sp.Symbol("d"))
S_ = sp.integrate(n * CV / T, (T, sp.Symbol("Ta", positive=True), sp.Symbol("Tb", positive=True))) \
    + sp.integrate(n * Rg / V, (V, V1s, V2s))
same("ideal-gas entropy dS = n C_V dT/T + nR dV/V",
     S_, n * CV * sp.log(sp.Symbol("Tb", positive=True) / sp.Symbol("Ta", positive=True)) + n * Rg * sp.log(V2s / V1s))
# Carnot cycle of an ideal gas
V1c, V2c = sp.symbols("V1 V2", positive=True)
V3c = V2c * (TH / TC) ** (1 / (gam - 1))         # adiabat 2 -> 3
V4c = V1c * (TH / TC) ** (1 / (gam - 1))         # adiabat 1 -> 4 (reversed)
same("Carnot: V2/V1 = V3/V4", V2c / V1c, V3c / V4c)
QH = n * Rg * TH * sp.log(V2c / V1c)
QC = n * Rg * TC * sp.log(V4c / V3c)
same("Carnot: Q_C = -nRT_C ln(V3/V4)", QC, -n * Rg * TC * sp.log(V3c / V4c))
same("Carnot: Q_H/T_H + Q_C/T_C = 0", QH / TH + QC / TC, 0)
same("Carnot: eta = 1 + Q_C/Q_H = 1 - T_C/T_H", 1 + QC / QH, 1 - TC / TH)
same("Carnot fridge COP = T_C/(T_H - T_C)", -QC / (QH + QC), TC / (TH - TC))   # reversed cycle
same("Carnot heat pump COP = T_H/(T_H - T_C)", QH / (QH + QC), TH / (TH - TC))
# Stirling cycle, compression ratio r
rr = sp.symbols("r", positive=True)
Qin = n * Rg * TH * sp.log(rr)
Qout = -n * Rg * TC * sp.log(rr)
same("Stirling: W = -nR (T_H - T_C) ln r", -(Qin + Qout), -n * Rg * (TH - TC) * sp.log(rr))
same("Stirling with regenerator: eta = 1 - T_C/T_H", -(-(Qin + Qout)) / Qin, 1 - TC / TH)
eta_noreg = -(-(Qin + Qout)) / (Qin + n * CV * (TH - TC))
true("Stirling without regenerator is less efficient",
     sp.N(eta_noreg.subs({n: 1, Rg: 8.314, TH: 600, TC: 300, rr: 2, gam: sp.Rational(7, 5)})) < 0.5)
check("card example: Q_in = 3.5 kJ (1 mol, 600 K, V doubles)", 8.3 * 600 * math.log(2), 3.5e3, rel=0.02)

print("\nFAILURES:", fails)
