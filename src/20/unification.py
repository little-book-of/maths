#!/usr/bin/env python3
# unification.py
#
# 20. The Dream of Unification — Mathematics as Cosmos
#
# Demos:
#   • unity     : Mathematics seeks unity beneath diversity (ℂ ↔ matrices ↔ rotation+scale)
#   • symmetry  : Symmetry & transformation reveal deep links (Burnside’s lemma on a square)
#   • mirrors   : Each branch mirrors the others — determinant as invariant (area, eigen, invertibility)
#   • pursuit   : Unification as pursuit — exponentials solve both y' = a y and x_{n+1} = r x_n
#   • whole     : The whole becomes clearer — eigenvectors in Markov chains & Fibonacci
#
# Pure standard library. ASCII output only.

from __future__ import annotations
import argparse, math
from typing import List, Tuple, Callable

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def matmul2(A: Tuple[Tuple[float,float],Tuple[float,float]],
            v: Tuple[float,float]) -> Tuple[float,float]:
    (a,b),(c,d) = A
    x,y = v
    return (a*x + b*y, c*x + d*y)

def matdet2(A: Tuple[Tuple[float,float],Tuple[float,float]]) -> float:
    (a,b),(c,d) = A
    return a*d - b*c

# ------------------------------------------------------------
# (1) UNITY — ℂ, 2×2 matrices, rotation+scale are the same story
# ------------------------------------------------------------

def complex_to_matrix(z: complex) -> Tuple[Tuple[float,float],Tuple[float,float]]:
    a, b = (z.real, z.imag)
    # matrix of multiplication by (a+ib), acting on (x,y) representing (x+iy)
    return ((a, -b),
            (b,  a))

def polar(z: complex) -> Tuple[float,float]:
    r = abs(z)
    theta = math.atan2(z.imag, z.real)
    return r, theta

def demo_unity():
    hr("Unity beneath diversity — one transformation, three guises")
    z = 1.2*math.cos(0.6) + 1.2j*math.sin(0.6)  # rotate by 0.6 rad, scale 1.2
    A = complex_to_matrix(z)
    v = (2.0, 1.0)  # point (x,y) ↔ x+iy
    # (i) complex multiplication
    w_complex = complex(v[0], v[1]) * complex(z)
    # (ii) matrix action
    w_matrix = matmul2(A, v)
    # (iii) geometric: rotate+scale
    r, theta = polar(z)
    rot = ((math.cos(theta), -math.sin(theta)),
           (math.sin(theta),  math.cos(theta)))
    w_geom = matmul2(rot, (r*v[0], r*v[1]))
    print(f"z = {z:.5f} = scale {r:.3f} then rotate {theta:.3f} rad")
    print(f"Apply to v={v}:")
    print("  ℂ-mult      → ", (w_complex.real, w_complex.imag))
    print("  matrix A v  → ", w_matrix)
    print("  rot∘scale v → ", w_geom)
    print("\nSame map, three languages: algebra (ℂ), linear algebra (A), geometry (rotate+scale).")

# ------------------------------------------------------------
# (2) SYMMETRY — Burnside’s lemma on the square’s vertex colorings
# ------------------------------------------------------------

# D4 group actions on four vertices labelled 0,1,2,3 (clockwise)
def apply_perm(p: Tuple[int,int,int,int], coloring: Tuple[int,int,int,int]) -> Tuple[int,int,int,int]:
    return tuple(coloring[i] for i in p)

def fixed_count(permutation: Tuple[int,int,int,int], colors: int) -> int:
    # number of colorings fixed by a permutation = colors^(# cycles of permutation)
    seen = [False]*4
    cycles = 0
    for i in range(4):
        if not seen[i]:
            j = i
            while not seen[j]:
                seen[j] = True
                j = permutation[j]
            cycles += 1
    return colors**cycles

def demo_symmetry():
    hr("Symmetry & transformation — counting with Burnside (D₄ on a square)")
    # D4 permutations on vertices 0,1,2,3: rotations and reflections
    D4 = {
        "id"  : (0,1,2,3),
        "r90" : (1,2,3,0),
        "r180": (2,3,0,1),
        "r270": (3,0,1,2),
        "fx"  : (1,0,3,2),   # reflect across vertical axis
        "fy"  : (3,2,1,0),   # across horizontal
        "fd1" : (0,3,2,1),   # main diagonal
        "fd2" : (2,1,0,3),   # other diagonal
    }
    k = 3  # number of colors
    total = 0
    print(f"Distinct colorings of 4 vertices with {k} colors, up to square symmetries:")
    for name, p in D4.items():
        fc = fixed_count(p, k)
        total += fc
        print(f"  {name:<5}: fixes {fc} colorings")
    distinct = total // len(D4)
    print(f"\nBurnside: average fixed = {total}/8 → {distinct} distinct orbits (colorings up to symmetry).")
    print("Symmetry turns a messy count into structure: transformations + invariants = clarity.")

# ------------------------------------------------------------
# (3) MIRRORS — determinant as a unifying invariant
# ------------------------------------------------------------

def eigenvalues2(A: Tuple[Tuple[float,float],Tuple[float,float]]) -> Tuple[complex,complex]:
    (a,b),(c,d) = A
    tr = a + d
    disc = tr*tr - 4*(a*d - b*c)
    s = math.sqrt(disc) if disc >= 0 else 1j*math.sqrt(-disc)
    return ((tr + s)/2, (tr - s)/2)

def demo_mirrors():
    hr("One invariant, many meanings — det as geometry, algebra, solvability")
    A = ((2.0, 1.0),
         (0.5, 1.5))
    det = matdet2(A)
    lam1, lam2 = eigenvalues2(A)
    area_scale = abs(det)
    print("Matrix A = [[2, 1],[0.5, 1.5]]")
    print(f"det(A) = {det:.3f}  →  geometric area scale |det| = {area_scale:.3f}")
    print(f"Eigenvalues λ₁,₂ = {lam1:.3f}, {lam2:.3f}  →  λ₁·λ₂ = {lam1*lam2:.3f}")
    print("Invertibility: det ≠ 0 ⇔ unique solution to A x = b for any b.")
    print("Same number binds geometry (area), algebra (spectrum), and analysis (Jacobian).")

# ------------------------------------------------------------
# (4) PURSUIT — exponentials unify differential & difference equations
# ------------------------------------------------------------

def demo_pursuit():
    hr("Exponential unity — the same form solves ODEs and recurrences")
    # ODE: y' = a y  → y(t) = y0 e^{a t}
    a = 0.7; y0 = 3.0
    y1 = y0 * math.exp(a * 5.0)
    print(f"ODE  y' = {a} y,  y(0)={y0}  ⇒  y(5) = y0 e^{a·5} = {y1:.4f}")

    # Recurrence: x_{n+1} = r x_n → x_n = x0 r^n, with r = e^{aΔt}
    Δt = 0.5
    r = math.exp(a*Δt)
    x0 = y0
    n = int(5.0/Δt)
    xn = x0 * (r**n)
    print(f"REC  x_{{n+1}} = r x_n with r=e^({a}·{Δt})={r:.4f}, n={n} ⇒ x_n = {xn:.4f}")
    print("Continuous or discrete, the same exponential law appears — a bridge across branches.")

# ------------------------------------------------------------
# (5) WHOLE — a tiny weave of eigenvectors across domains
# ------------------------------------------------------------

def steady_state_markov(P: Tuple[Tuple[float,float],Tuple[float,float]]) -> Tuple[float,float]:
    # Solve πP = π with π summing to 1 for a 2×2 stochastic matrix
    (p00,p01),(p10,p11) = P
    # π0, π1 with equations: π0 = π0 p00 + π1 p10 ; π0 + π1 = 1
    # Rearranged: π0(1 - p00) - π1 p10 = 0; π0 + π1 = 1
    # Solve:
    A = ((1 - p00, -p10),
         (1,          1))
    b0 = 0.0; b1 = 1.0
    detA = matdet2(A)
    x0 = (b0*A[1][1] - (-p10)*b1) / detA
    x1 = ( (1 - p00)*b1 - b0*A[1][0]) / detA
    return (x0, x1)

def fib(n: int) -> int:
    # Fibonacci via power of Q = [[1,1],[1,0]] (eigen-idea; fast-doubling could be used, but keep it simple)
    def matmul(A,B):
        return ((A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]),
                (A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]))
    def matpow(M, k):
        R = ((1,0),(0,1))
        while k:
            if k & 1: R = matmul(R,M)
            M = matmul(M,M)
            k >>= 1
        return R
    Q = ((1,1),(1,0))
    if n == 0: return 0
    Qn = matpow(Q, n-1)
    return Qn[0][0]  # F_n

def demo_whole():
    hr("The whole is clearer — one idea across different worlds (eigenvectors)")
    # (a) Markov chain (two states): eigenvalue 1 eigenvector = steady state
    P = ((0.8, 0.2),
         (0.3, 0.7))
    π = steady_state_markov(P)
    print("Markov chain P = [[0.8,0.2],[0.3,0.7]]  → steady state (π satisfies πP=π):")
    print(f"  π ≈ {π[0]:.3f}, {π[1]:.3f}  (sum=1)")

    # (b) Fibonacci: powers of a matrix / characteristic polynomial
    n = 12
    print(f"\nFibonacci via matrix powers (same eigen-idea): F_{n} = {fib(n)}")

    # (c) Rotation/scale already seen: eigenvalues as “normal modes” of a linear map
    A = ((2.0, -2.0),
         (1.0,  1.0))
    lam1, lam2 = eigenvalues2(A)
    print(f"\nLinear map A has eigenvalues λ₁,₂ = {lam1:.3f}, {lam2:.3f}  (normal modes of action).")
    print("\nDifferent problems, same backbone (eigen/characteristic). The fabric is one.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="The Dream of Unification — runnable micro-demos.")
    p.add_argument("--demo",
                   choices=["all","unity","symmetry","mirrors","pursuit","whole"],
                   default="all", help="Which demo to run.")
    args = p.parse_args()

    print("The Dream of Unification — Mathematics as Cosmos")
    print("Demos: unity (ℂ↔matrix↔geometry), symmetry (Burnside/D₄), mirrors (determinant),")
    print("       pursuit (exponential law), whole (eigenvectors across domains)")

    if args.demo in ("all","unity"):
        demo_unity()
    if args.demo in ("all","symmetry"):
        demo_symmetry()
    if args.demo in ("all","mirrors"):
        demo_mirrors()
    if args.demo in ("all","pursuit"):
        demo_pursuit()
    if args.demo in ("all","whole"):
        demo_whole()

if __name__ == "__main__":
    main()
