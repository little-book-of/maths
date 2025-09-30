#!/usr/bin/env python3
# newton.py
#
# 12. Newton’s Laws — The Universe as Formula
#
# Demos:
#   • laws      : Nature follows consistent mathematical laws (F=ma; free fall, mass-independence)
#   • calculus  : Newton’s calculus models change (integrate F→a→v→x on a spring-mass(-damper))
#   • unity     : Same rules for earth and sky (inverse-square gravity → orbit with conserved L,E)
#   • predict   : Equations as tools for prediction (projectile: analytic vs time-step simulation)
#   • precision : Mathematics quantifies nature (estimate gravitational μ from orbital measurements)
#
# Pure standard library. ASCII output.

from __future__ import annotations
import argparse
import math
import random
from typing import List, Tuple

random.seed(12)

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

# ------------------------------------------------------------
# (1) LAWS — F = m a; free fall is mass-independent
# ------------------------------------------------------------

def demo_laws():
    hr("Nature follows law — F = m a and mass-independent free fall (no air)")
    # Same force, different mass → different acceleration
    F = 12.0  # N
    for m in [1.0, 3.0, 6.0]:
        a = F/m
        print(f"Force {F:>4.1f} N on mass {m:.1f} kg → a = {a:.3f} m/s²")

    # Same gravitational field g acts equally on all masses (equivalence in Newtonian model)
    g = 9.81
    h0 = 30.0
    dt = 0.05
    t = 0.0
    print("\nFree fall y = h0 − ½ g t² (ignoring air). Two different masses share the same y(t).")
    print("t (s)   height (m)")
    while True:
        y = h0 - 0.5*g*t*t
        if y < 0: break
        if int(t*20) % 5 == 0:
            print(f"{t:4.2f}   {y:9.4f}")
        t += dt
    T = (2*h0/g) ** 0.5
    print(f"Impact time T ≈ √(2h/g) = {T:.3f} s  (independent of mass)")

# ------------------------------------------------------------
# (2) CALCULUS — integrate F→a→v→x (spring-mass-damper)
# ------------------------------------------------------------

def simulate_smd(m=1.0, k=9.0, c=0.6, x0=1.2, v0=0.0, dt=0.01, steps=1200):
    """
    Spring-mass-damper: m x'' + c x' + k x = 0.
    Symplectic-ish (Euler-Cromer) integration to keep energy behavior reasonable.
    Returns list of (t, x, v, E).
    """
    t, x, v = 0.0, x0, v0
    out = []
    for _ in range(steps):
        a = -(c/m)*v - (k/m)*x
        v += a*dt
        x += v*dt
        E = 0.5*m*v*v + 0.5*k*x*x
        out.append((t, x, v, E))
        t += dt
    return out

def demo_calculus():
    hr("Calculus in motion — integrating F→a→v→x for a spring-mass-damper")
    rows = simulate_smd()
    print(" t     x(t)       v(t)       Energy")
    print("--------------------------------------")
    for i, (t,x,v,E) in enumerate(rows[0:400:40]):
        print(f"{t:5.2f}  {x:9.5f}  {v:9.5f}  {E:9.5f}")
    E0 = rows[0][3]; Emin = min(r[3] for r in rows); Emax = max(r[3] for r in rows)
    print(f"\nEnergy decays with damping (c>0): E ∈ [{Emin:.5f}, {Emax:.5f}], start {E0:.5f}")
    print("Newton’s program: specify force → compute acceleration → integrate to predict motion.")

# ------------------------------------------------------------
# (3) UNITY — same law for earth & sky: inverse-square orbit
# ------------------------------------------------------------

def simulate_orbit(mu=1.0, r0=(1.0, 0.0), v0=(0.0, 1.0), dt=0.002, steps=30000):
    """
    Keplerian motion under central gravity: r'' = -μ r / |r|^3.
    Semi-implicit (leapfrog/Euler-Cromer) integrator; returns (positions, energies, momenta).
    """
    rx, ry = r0
    vx, vy = v0
    xs: List[Tuple[float,float]] = []
    Es: List[float] = []
    Ls: List[float] = []
    for _ in range(steps):
        r = (rx*rx + ry*ry) ** 0.5
        ax, ay = -mu*rx/r**3, -mu*ry/r**3
        # half step velocity, full step position, finish velocity (leapfrog-ish)
        vxh, vyh = vx + 0.5*dt*ax, vy + 0.5*dt*ay
        rx += dt*vxh; ry += dt*vyh
        r = (rx*rx + ry*ry) ** 0.5
        ax2, ay2 = -mu*rx/r**3, -mu*ry/r**3
        vx = vxh + 0.5*dt*ax2; vy = vyh + 0.5*dt*ay2
        # store invariants
        E = 0.5*(vx*vx + vy*vy) - mu/r
        L = rx*vy - ry*vx
        xs.append((rx, ry)); Es.append(E); Ls.append(L)
    return xs, Es, Ls

def demo_unity():
    hr("One sky, one earth — the same inverse-square law shapes both")
    # Choose μ=1, near-circular v = √(μ/r)
    mu = 1.0; r0 = (1.0, 0.0); v0 = (0.0, 1.0)
    pts, Es, Ls = simulate_orbit(mu, r0, v0)
    Espan = (min(Es), max(Es)); Lspan = (min(Ls), max(Ls))
    print("Simulated a closed orbit under r'' = −μ r/|r|^3 (no drag).")
    print(f"Energy nearly constant:  [{Espan[0]:+.6f}, {Espan[1]:+.6f}]")
    print(f"Angular momentum steady: [{Lspan[0]:+.6f}, {Lspan[1]:+.6f}]")
    # Print a handful of sample positions
    print("Sample positions (first 6):")
    for (x,y) in pts[::len(pts)//6][:6]:
        print(f"  ({x:+.4f}, {y:+.4f})")
    print("Message: the law that drops an apple also guides the moon — same equation, new scale.")

# ------------------------------------------------------------
# (4) PREDICTION — projectile: analytic vs simulation
# ------------------------------------------------------------

def simulate_projectile(v0: float, theta_deg: float, g: float = 9.81, dt: float = 0.001):
    vx = v0*math.cos(math.radians(theta_deg))
    vy = v0*math.sin(math.radians(theta_deg))
    x, y, t = 0.0, 0.0, 0.0
    while True:
        vy -= g*dt
        x  += vx*dt
        y  += vy*dt
        t  += dt
        if y <= 0 and t > 0: break
    return x, t

def demo_predict():
    hr("Equations predict — projectile range/time: theory vs simulation")
    g = 9.81; v0 = 35.0; theta = 37.0
    R_theory = (v0*v0*math.sin(math.radians(2*theta)))/g
    T_theory = (2*v0*math.sin(math.radians(theta)))/g
    R_sim, T_sim = simulate_projectile(v0, theta, g=g, dt=0.0008)
    print(f"v0={v0} m/s, θ={theta}°")
    print(f"Range: theory {R_theory:.3f} m | sim {R_sim:.3f} m")
    print(f"Time : theory {T_theory:.3f} s | sim {T_sim:.3f} s")
    dR = abs(R_sim-R_theory)/R_theory*100
    dT = abs(T_sim-T_theory)/T_theory*100
    print(f"Relative error: ΔR≈{dR:.3f}%, ΔT≈{dT:.3f}%")
    print("Prediction first, measurement second — the Newtonian habit of mind.")

# ------------------------------------------------------------
# (5) PRECISION — estimate μ from orbital data (Kepler 3)
# ------------------------------------------------------------

def estimate_mu_from_orbit(sample_pts: List[Tuple[float,float]], T: float) -> float:
    """
    Estimate gravitational parameter μ from (assumed near-elliptic) orbit samples and period T,
    using Kepler's 3rd law with semi-major axis a estimated from sample radii.
    """
    rs = [(x*x + y*y) ** 0.5 for (x,y) in sample_pts]
    rmin, rmax = min(rs), max(rs)
    a = 0.5*(rmin + rmax)  # crude a ≈ (r_p + r_a)/2
    mu_est = 4*math.pi**2 * a**3 / (T*T)
    return mu_est

def measure_period(pts: List[Tuple[float,float]], dt: float) -> float:
    """
    Rough period from successive crossings near +x axis with y ~ 0 and vy>0.
    """
    # Compute coarse velocity sign via finite diff
    crosses = []
    for i in range(1, len(pts)):
        x0,y0 = pts[i-1]; x1,y1 = pts[i]
        if y0 < 0 <= y1 and x1 > 0:  # crossing upward near +x
            crosses.append(i*dt)
            if len(crosses) == 2:
                return crosses[1] - crosses[0]
    return float('nan')

def demo_precision():
    hr("Precision by mathematics — recovering μ from orbital measurements")
    mu_true = 1.0
    # Create a slightly elliptical orbit by under/over circular speed.
    r0 = (1.0, 0.0); v0 = (0.0, 0.9)  # <1 → ellipse
    dt = 0.0015
    pts, Es, Ls = simulate_orbit(mu_true, r0, v0, dt=dt, steps=120000)
    T = measure_period(pts, dt)
    mu_est = estimate_mu_from_orbit(pts[::100], T)  # thin the sample
    rel_err = abs(mu_est - mu_true)/mu_true*100
    print(f"Measured period T ≈ {T:.4f} (arb. units)")
    print(f"Estimated μ from Kepler-3 ≈ {mu_est:.5f}   |   true μ = {mu_true:.5f}")
    print(f"Relative error ≈ {rel_err:.3f}%")
    print("Math turns raw points into constants — precision by law, not by lore.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Newton’s Laws — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all", "laws", "calculus", "unity", "predict", "precision"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Newton’s Laws — The Universe as Formula")
    print("Demos: laws (F=ma, free fall), calculus (integrate motion), unity (inverse-square orbit),")
    print("       predict (projectile), precision (estimate μ)")

    if args.demo in ("all", "laws"):
        demo_laws()
    if args.demo in ("all", "calculus"):
        demo_calculus()
    if args.demo in ("all", "unity"):
        demo_unity()
    if args.demo in ("all", "predict"):
        demo_predict()
    if args.demo in ("all", "precision"):
        demo_precision()

if __name__ == "__main__":
    main()
