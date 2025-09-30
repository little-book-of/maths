#!/usr/bin/env python3
# leibniz.py
#
# 13. Leibniz and the Infinite — The Art of the Differential
#
# Demos:
#   • infinitesimal : Change as sum of infinitesimal parts (numerical derivative & integral)
#   • notation      : Leibniz notation shaping calculus (dy/dx, ∫f dx, Δx→0)
#   • infinity      : Infinity as tool, not mystery (infinite series approximations)
#   • logic         : Logic as computation (symbolic evaluation of truth table)
#   • reasoning     : Dream of mechanical reasoning (enumerate all truths of a small system)
#
# Pure standard library, ASCII output.

from __future__ import annotations
import argparse, math
from typing import Callable, List, Tuple

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def hr(title: str):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

# ------------------------------------------------------------
# (1) Infinitesimal — derivative & integral by small steps
# ------------------------------------------------------------

def derivative(f: Callable[[float], float], x: float, dx: float = 1e-5) -> float:
    return (f(x + dx) - f(x - dx)) / (2 * dx)

def integral(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> float:
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h

def demo_infinitesimal():
    hr("Calculus as Infinitesimal Change — Derivative & Integral from Tiny Steps")
    f = lambda x: x ** 2
    x0 = 3.0
    df = derivative(f, x0)
    area = integral(f, 0, 3)
    print(f"Function f(x)=x²")
    print(f"At x={x0}, derivative df/dx ≈ {df:.4f}  (true 2x=6)")
    print(f"Area ∫₀³ x² dx ≈ {area:.4f}  (true 9)")
    print("Motion, growth, accumulation — all reduced to sums of infinitesimal steps.")

# ------------------------------------------------------------
# (2) Notation — dy/dx, ∫f dx, Δx→0
# ------------------------------------------------------------

def demo_notation():
    hr("Leibniz’s Notation — The Language of Change")
    print("dy/dx  →  the ratio of infinitesimal changes, derivative")
    print("∫f(x) dx  →  the sum of infinitesimal contributions, integral")
    print("Δx → 0  →  finite steps shrink toward the infinitesimal")
    print()
    print("Example:")
    print("Let y = x². Then dy/dx = 2x. At x=3 → dy/dx=6.")
    print("Geometric meaning: slope of tangent; physical meaning: instantaneous velocity.")
    print("Leibniz’s symbols endure — compact, general, and endlessly generative.")

# ------------------------------------------------------------
# (3) Infinity as Tool — infinite series approximations
# ------------------------------------------------------------

def exp_series(x: float, n: int = 10) -> float:
    s = 0.0
    for k in range(n):
        s += x**k / math.factorial(k)
    return s

def demo_infinity():
    hr("Infinity as Tool — Series Approximation of eˣ")
    x = 1.0
    true = math.e ** x
    for n in [1,2,3,5,7,10]:
        approx = exp_series(x, n)
        err = abs(approx - true)
        print(f"n={n:2d}  Σ₀ⁿ x^k/k! = {approx:.6f}   error={err:.2e}")
    print("Endless process, finite precision — infinity harnessed to compute the real.")

# ------------------------------------------------------------
# (4) Logic as Computation — symbolic truth evaluation
# ------------------------------------------------------------

def truth_table():
    rows = []
    for A in [False, True]:
        for B in [False, True]:
            f = (A and not B) or (not A and B)  # XOR
            rows.append((A, B, f))
    return rows

def demo_logic():
    hr("Logic as Calculation — Evaluate Truth Table (XOR)")
    rows = truth_table()
    print("A     B     (A ∧ ¬B) ∨ (¬A ∧ B)")
    print("--------------------------------")
    for A, B, f in rows:
        print(f"{A!s:<5} {B!s:<5} {f!s}")
    print("Boolean symbols manipulated like numbers — reasoning made mechanical.")

# ------------------------------------------------------------
# (5) Mechanical Reasoning — enumerate all truths
# ------------------------------------------------------------

def demo_reasoning():
    hr("Mechanical Reasoning — Enumerating a Mini Logic Space")
    # Suppose variables P,Q,R. Enumerate all 8 states; evaluate formula: (P→Q) ∧ (Q→R) → (P→R)
    print("Formula: (P→Q) ∧ (Q→R) → (P→R)   (transitivity of implication)")
    print("P Q R | Formula")
    print("----------------")
    def implies(a,b): return (not a) or b
    tautology=True
    for P in [False,True]:
        for Q in [False,True]:
            for R in [False,True]:
                val = implies(implies(P,Q) and implies(Q,R), implies(P,R))
                print(f"{int(P)} {int(Q)} {int(R)} | {int(val)}")
                if not val: tautology=False
    print("\nResult:", "Tautology (always true)" if tautology else "Not tautology")
    print("Each case verified — thought unfolded by symbol, not intuition alone.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Leibniz and the Infinite — runnable micro-demos.")
    parser.add_argument("--demo",
        choices=["all","infinitesimal","notation","infinity","logic","reasoning"],
        default="all", help="Which demo to run.")
    args = parser.parse_args()

    print("Leibniz and the Infinite — The Art of the Differential")
    print("Demos: infinitesimal (dx, integral), notation (dy/dx, ∫), infinity (series),")
    print("       logic (truth table), reasoning (mechanical proof)")

    if args.demo in ("all","infinitesimal"): demo_infinitesimal()
    if args.demo in ("all","notation"): demo_notation()
    if args.demo in ("all","infinity"): demo_infinity()
    if args.demo in ("all","logic"): demo_logic()
    if args.demo in ("all","reasoning"): demo_reasoning()

if __name__ == "__main__":
    main()
