#!/usr/bin/env python3
# clockwork.py
#
# 9. The Clockwork Universe — Nature as Equation
#
# Demos:
#   • lawful    : Free fall (Galileo) — one law for many masses
#   • equations : Mass–spring (Hooke + Newton) — motion & conserved energy
#   • unity     : Observation + calculation — estimate g from noisy drop data
#   • predict   : Projectile range — analytic prediction vs time-step simulation
#   • cosmos    : Pendulum scaling — T ∝ √(L/g); number makes the world intelligible
#
# Pure standard library (ASCII output).

from __future__ import annotations
import argparse
import math
import random
from typing import List, Tuple

random.seed(9)

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

# ------------------------------------------------------------
# (1) Nature is lawful — free fall, same g for all masses
# ------------------------------------------------------------

def demo_lawful():
    hr("Lawful, not arbitrary — free fall under constant g")
    g = 9.81  # m/s^2
    h0 = 20.0 # meters
    dt = 0.05
    # Two stones of different mass share the same position-time law (ignoring air)
    masses = [0.1, 3.0]  # kg
    t, y = 0.0, h0
    print("t (s)   y_0.1kg (m)   y_3kg (m)")
    print("--------------------------------")
    while y >= 0:
        y = h0 - 0.5*g*t*t
        print(f"{t:5.2f}   {y:12.6f}   {y:10.6f}")
        t += dt
    T = math.sqrt(2*h0/g)
    print(f"\nTime to impact (theory): T = √(2h/g) ≈ {T:.3f} s  (independent of mass)")
    print("Idea: one equation governs many things — law replaces lore.")

# ------------------------------------------------------------
# (2) Equations describe motion, balance, change — mass–spring
# ------------------------------------------------------------

def simulate_spring(m=1.0, k=4.0, x0=1.0, v0=0.0, dt=0.05, steps=80) -> List[Tuple[float,float,float,float]]:
    """
    x'' = -(k/m)x  (no damping). Semi-implicit (symplectic) Euler for better energy behavior.
    Returns rows of (t, x, v, E).
    """
    t, x, v = 0.0, x0, v0
    out = []
    for _ in range(steps):
        a = -(k/m)*x
        v = v + dt*a
        x = x + dt*v
        E = 0.5*m*v*v + 0.5*k*x*x
        out.append((t, x, v, E))
        t += dt
    return out

def demo_equations():
    hr("Equations of motion — Hooke + Newton (mass–spring oscillator)")
    rows = simulate_spring()
    print(" t    x(t)       v(t)       Energy")
    print("-------------------------------------")
    for i, (t,x,v,E) in enumerate(rows):
        if i % 8 == 0:
            print(f"{t:4.2f}  {x:9.5f}  {v:9.5f}  {E:9.5f}")
    E0 = rows[0][3]
    Emin = min(r[3] for r in rows)
    Emax = max(r[3] for r in rows)
    print(f"\nEnergy nearly constant (no damping): E∈[{Emin:.5f}, {Emax:.5f}] around {E0:.5f}")
    print("Message: differential equations are the grammar of change; invariants (energy) reveal structure.")

# ------------------------------------------------------------
# (3) Observation + calculation — estimate g from data
# ------------------------------------------------------------

def demo_unity():
    hr("Observation ∧ Calculation — estimating g from noisy drop data")
    # Drop from rest: y(t) = h0 - (1/2) g t^2  ⇒  h0 - y = (1/2) g t^2.
    h0 = 12.0
    g_true = 9.81
    # Simulate measurements of t and y with small noise
    ts = [0.20, 0.35, 0.50, 0.65, 0.80, 0.95]
    ys = [h0 - 0.5*g_true*t*t + random.gauss(0, 0.02) for t in ts]  # ±2 cm noise
    # Linear fit of (h0 - y) vs t^2: slope ≈ (1/2) g
    X = [t*t for t in ts]
    Z = [h0 - y for y in ys]
    # Least squares for simple line through origin: slope = (ΣXZ)/(ΣX^2)
    num = sum(x*z for x,z in zip(X,Z))
    den = sum(x*x for x in X)
    slope = num/den
    g_est = 2*slope
    print("t (s)   y_measured (m)")
    for t,y in zip(ts,ys):
        print(f"{t:4.2f}   {y:10.4f}")
    print(f"\nEstimated g ≈ {g_est:.3f} m/s²   (true {g_true})")
    err = abs(g_est - g_true)/g_true*100
    print(f"Relative error ≈ {err:.2f}%")
    print("Unity: careful observation + equation turns data into law.")

# ------------------------------------------------------------
# (4) Predicting, not just witnessing — projectile range
# ------------------------------------------------------------

def simulate_projectile(speed: float, angle_deg: float, g: float = 9.81, dt: float = 0.005) -> Tuple[float,float]:
    vx = speed*math.cos(math.radians(angle_deg))
    vy = speed*math.sin(math.radians(angle_deg))
    x, y, t = 0.0, 0.0, 0.0
    while True:
        # update
        vy -= g*dt
        x  += vx*dt
        y  += vy*dt
        t  += dt
        if y <= 0 and t > 0.0:
            break
    return x, t

def demo_predict():
    hr("Predicting replaces merely witnessing — projectile motion")
    v0 = 30.0     # m/s
    theta = 40.0  # degrees
    g = 9.81
    # Theory (no air): Range R = v0^2 sin(2θ) / g; time T = 2 v0 sinθ / g
    R_theory = (v0*v0*math.sin(math.radians(2*theta)))/g
    T_theory = (2*v0*math.sin(math.radians(theta)))/g
    R_sim, T_sim = simulate_projectile(v0, theta, g=g)
    print(f"Initial speed {v0} m/s, angle {theta}°")
    print(f"Range — theory: {R_theory:.3f} m   |   simulation: {R_sim:.3f} m")
    print(f"Time  — theory: {T_theory:.3f} s   |   simulation: {T_sim:.3f} s")
    print("Lesson: an equation foretells an outcome; measurement checks it.")

# ------------------------------------------------------------
# (5) The cosmos intelligible through number — pendulum scaling
# ------------------------------------------------------------

def small_angle_period(L: float, g: float = 9.81) -> float:
    # Small-angle approximation: T ≈ 2π √(L/g)
    return 2*math.pi*math.sqrt(L/g)

def simulate_pendulum_period(L: float, theta0_deg: float = 5.0, g: float = 9.81, dt: float = 0.001) -> float:
    """
    Simple pendulum θ'' + (g/L) sinθ = 0, integrated by symplectic Euler.
    Measure time between two successive zero-crossings of θ with negative slope.
    """
    theta = math.radians(theta0_deg)
    omega = 0.0
    t = 0.0
    last_cross = None
    periods: List[float] = []
    # warm-up few seconds
    for _ in range(60000):
        omega += - (g/L) * math.sin(theta) * dt
        theta += omega * dt
        t += dt
        # detect zero-crossing from + to -
        if theta == 0.0:
            continue
        # Check sign change around zero
        # We'll record when theta changes sign and omega<0 (passing downward)
        # Use a simple linear interpolation for crossing time.
        if (theta > 0 and omega < 0) or (theta < 0 and omega < 0 and abs(theta) < 1e-3):
            # Not robust; we'll detect when θ switches sign in practice
            pass
    # Better: run and track sign of theta
    theta = math.radians(theta0_deg)
    omega = 0.0
    t = 0.0
    prev_theta = theta
    for _ in range(600000):  # up to 600 s at dt=0.001
        omega += - (g/L) * math.sin(theta) * dt
        theta_next = theta + omega * dt
        t_next = t + dt
        # zero crossing (from + to -)
        if prev_theta > 0 and theta_next <= 0 and omega < 0:
            if last_cross is None:
                last_cross = t_next
            else:
                periods.append(t_next - last_cross)
                last_cross = t_next
                if len(periods) >= 2:
                    break
        prev_theta = theta_next
        theta = theta_next
        t = t_next
    return sum(periods)/len(periods) if periods else float("nan")

def demo_cosmos():
    hr("Cosmos intelligible through number — pendulum law T ∝ √(L/g)")
    g = 9.81
    lengths = [0.25, 0.5, 1.0, 2.0]  # meters
    print(" L (m)   T_theory(s)   T_sim(s)    T/√L (theory) ")
    print("--------------------------------------------------")
    for L in lengths:
        T_th = small_angle_period(L, g)
        T_sm = simulate_pendulum_period(L, theta0_deg=5.0, g=g, dt=0.001)
        print(f"{L:5.2f}    {T_th:10.4f}   {T_sm:8.4f}     {T_th/math.sqrt(L):8.4f}")
    const = 2*math.pi/math.sqrt(g)
    print(f"\nInvariants: T/√L ≈ 2π/√g ≈ {const:.4f}  (independent of length L)")
    print("Reading: proportion and invariants make the world legible.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="The Clockwork Universe — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all", "lawful", "equations", "unity", "predict", "cosmos"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("The Clockwork Universe — Nature as Equation")
    print("Demos: lawful (free fall), equations (spring), unity (fit g), predict (projectile), cosmos (pendulum)")

    if args.demo in ("all", "lawful"):
        demo_lawful()
    if args.demo in ("all", "equations"):
        demo_equations()
    if args.demo in ("all", "unity"):
        demo_unity()
    if args.demo in ("all", "predict"):
        demo_predict()
    if args.demo in ("all", "cosmos"):
        demo_cosmos()

if __name__ == "__main__":
    main()
