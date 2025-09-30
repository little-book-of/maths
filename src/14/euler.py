#!/usr/bin/env python3
# euler.py
#
# 14. Euler’s Vision — The Web of Relations
#
# Demos:
#   • unify     : e^{iθ} = cos θ + i sin θ — geometry ↔ analysis, one circle seen two ways
#   • notation  : Enduring notations (e, i, π, f(x), Σ, Π) and Euler's identity
#   • invariant : Euler characteristic V − E + F = 2 for convex polyhedra (topology ↔ geometry)
#   • bridges   : Königsberg bridges — Eulerian path criterion from vertex degrees (relations > objects)
#   • basel     : Basel problem & Euler product — symmetry/simplicity emerging from infinite structure
#
# Pure standard library. ASCII output only.

from __future__ import annotations
import argparse
import cmath
import math
from typing import Dict, Iterable, List, Tuple

# ------------------------------------------------------------
# helpers
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))

# ------------------------------------------------------------
# 1) unify — e^{iθ} = cos θ + i sin θ
# ------------------------------------------------------------

def demo_unify():
    hr("Unifying Worlds — e^{iθ} draws the unit circle (geometry ⇄ analysis)")
    thetas = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2, 2*math.pi/3, 5*math.pi/6, math.pi]
    print(" θ (rad)   Re(e^{iθ})   Im(e^{iθ})    cos θ        sin θ")
    print("----------------------------------------------------------")
    for θ in thetas:
        z = cmath.exp(1j*θ)
        print(f"{θ:7.4f}   {z.real:10.6f}  {z.imag:10.6f}   {math.cos(θ):10.6f} {math.sin(θ):10.6f}")
    print("\nOne formula, two readings: a spinning complex number and a point on a circle.")
    print("Analysis supplies the symbol; geometry supplies the picture — same object, two languages.")

# ------------------------------------------------------------
# 2) notation — Euler's enduring symbols
# ------------------------------------------------------------

def demo_notation():
    hr("Notation that Lives — e, i, π, f(x), Σ, Π")
    # Euler's identity (numeric check)
    val = cmath.exp(1j*math.pi) + 1
    print("e^{iπ} + 1 =", f"{val.real:.12f}+{val.imag:.12f}i  (≈ 0)")
    print("\nMini-glossary:")
    rows = [
        ("e^x",        "growth by proportionality; compounding as calculus' native base"),
        ("i",          "√(-1): turns lines into rotations; enables e^{iθ}"),
        ("π",          "circle's constant; appears across analysis, number theory, probability"),
        ("f(x)",       "function: relation from x to y; modern math’s basic actor"),
        ("Σ",          "sum over many parts; discrete accumulation"),
        ("∏",          "product over many factors; multiplicative structure (e.g., Euler product)"),
    ]
    for sym, note in rows:
        print(f"  {sym:<6} — {note}")
    print("\nEuler didn’t just solve problems; he gave us a *language* that still does the solving.")

# ------------------------------------------------------------
# 3) invariant — Euler characteristic V − E + F = 2
# ------------------------------------------------------------

def euler_characteristic(V: int, E: int, F: int) -> int:
    return V - E + F

def demo_invariant():
    hr("Relations over Objects — Euler Characteristic (topology in a number)")
    solids = {
        "Tetrahedron": (4, 6, 4),
        "Cube":        (8,12, 6),
        "Octahedron":  (6,12, 8),
        "Icosahedron": (12,30,20),
        "Dodecahedron":(20,30,12)
    }
    print("Solid         V   E   F   V−E+F")
    print("--------------------------------")
    for name, (V,E,F) in solids.items():
        χ = euler_characteristic(V,E,F)
        print(f"{name:<12} {V:>3} {E:>3} {F:>3}   {χ}")
    print("\nDifferent shapes, same relation χ=2 (sphere-like):")
    print("not the *material* but the *connectivity* is what the number sees.")

# ------------------------------------------------------------
# 4) bridges — Eulerian path criterion
# ------------------------------------------------------------

Graph = Dict[str, List[str]]

def degree_parities(G: Graph) -> Dict[str, int]:
    return {v: len(G[v]) for v in G}

def eulerian_status(G: Graph) -> str:
    odd = [v for v,d in degree_parities(G).items() if d % 2 == 1]
    if len(odd) == 0:
        return "Eulerian circuit exists (start=end)."
    if len(odd) == 2:
        return "Eulerian trail exists (start≠end)."
    return "No Eulerian trail (more than two odd-degree vertices)."

def demo_bridges():
    hr("Königsberg Bridges — structure decides possibility")
    # Classic abstraction: landmasses A,B,C,D; edges = bridges
    G: Graph = {
        "A": ["B","B","C","D"],
        "B": ["A","A","C","D"],
        "C": ["A","B","D"],
        "D": ["A","B","C"]
    }
    print("Vertices and degrees:")
    deg = degree_parities(G)
    for v in sorted(deg):
        print(f"  {v}: degree {deg[v]}")
    print("\nConclusion:", eulerian_status(G))
    print("\nModify the city: add a bridge C-D.")
    G["C"].append("D"); G["D"].append("C")
    deg2 = degree_parities(G)
    for v in sorted(deg2):
        print(f"  {v}: degree {deg2[v]}")
    print("New conclusion:", eulerian_status(G))
    print("\nEuler’s move: replace bricks with a *relation* (graph).")
    print("Possibility depends on parity — a simple, global property.")

# ------------------------------------------------------------
# 5) basel — ζ(2)=π²/6 and Euler product (partial)
# ------------------------------------------------------------

def zeta2_partial(N: int) -> float:
    return sum(1.0/(n*n) for n in range(1, N+1))

def euler_product_partial(primes: Iterable[int]) -> float:
    prod = 1.0
    for p in primes:
        prod *= 1.0 / (1.0 - 1.0/(p*p))
    return prod

def demo_basel():
    hr("Simplicity in Complexity — Basel sum and Euler product")
    target = (math.pi**2)/6.0
    Ns = [10, 50, 100, 500, 2000]
    print("Partial sums S_N = Σ 1/n² → π²/6")
    for N in Ns:
        s = zeta2_partial(N)
        err = abs(s - target)
        print(f"  N={N:<5}  S_N={s:.10f}   |err|={err:.3e}")
    print(f"Target π²/6 ≈ {target:.10f}\n")

    primes = [2,3,5,7,11,13,17,19]
    prod = euler_product_partial(primes)
    errp = abs(prod - target)
    print("Euler product (partial)  ∏ 1/(1 - p^{-2}) over small primes:")
    print(f"  P={{2,3,5,7,11,13,17,19}} → {prod:.10f}   |err|={errp:.3e}")
    print("Arithmetic (primes) meets analysis (ζ): one fabric, many threads.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Euler’s Vision — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all","unify","notation","invariant","bridges","basel"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Euler’s Vision — The Web of Relations")
    print("Demos: unify (e^{iθ} circle), notation (e,i,π,f,Σ,Π), invariant (V−E+F),")
    print("       bridges (Eulerian paths), basel (ζ(2)=π²/6 & Euler product)")

    if args.demo in ("all","unify"):
        demo_unify()
    if args.demo in ("all","notation"):
        demo_notation()
    if args.demo in ("all","invariant"):
        demo_invariant()
    if args.demo in ("all","bridges"):
        demo_bridges()
    if args.demo in ("all","basel"):
        demo_basel()

if __name__ == "__main__":
    main()
