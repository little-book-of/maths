#!/usr/bin/env python3
# algebra.py
#
# 5. Algebra as Language — The Grammar of the Unknown
#
# Demos:
#   • nameable   : Treat the unknown as something nameable; step-by-step solving ax+b=c
#   • generalize : From examples to a rule (sum of odd numbers; nth pattern)
#   • reasoning  : Trial-and-error vs algebraic reasoning (sum/product puzzle; elimination)
#   • connect    : Algebra ↔ geometry (area model, completing the square, quadratic formula sketch)
#   • relation   : Equations as universal language of relation (solution sets; invariance)
#
# Pure standard library. ASCII output.

from __future__ import annotations
import argparse
import math
from fractions import Fraction
from typing import List, Tuple, Optional

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def show_steps(steps: List[str]) -> None:
    for s in steps:
        print(s)

# ------------------------------------------------------------
# (1) NAMEABLE — solving ax + b = c as readable algebra
# ------------------------------------------------------------

def solve_linear(a: Fraction, b: Fraction, c: Fraction) -> Fraction:
    if a == 0:
        raise ValueError("a=0: not a linear equation in x.")
    return (c - b) / a

def demo_nameable():
    hr("Name the Unknown — turn language into equation")
    # “Twice a number plus five equals nineteen.”
    # Let x be "the number". Then 2x + 5 = 19.
    a, b, c = Fraction(2), Fraction(5), Fraction(19)
    steps = [
        "Let x be the unknown number.",
        "2x + 5 = 19",
        "Subtract 5 from both sides:",
        "2x = 14",
        "Divide both sides by 2:",
        "x = 7"
    ]
    show_steps(steps)
    x = solve_linear(a, b, c)
    print(f"\nChecked solution: x = {x}  →  2·7+5 = 19 ✓")
    print("Idea: naming the unknown makes the invisible thinkable.")

# ------------------------------------------------------------
# (2) GENERALIZE — find the rule behind many cases
# ------------------------------------------------------------

def sum_first_n_odds(n: int) -> int:
    return sum(2*k+1 for k in range(n))

def demo_generalize():
    hr("Generalize a Pattern — the sum of the first n odd numbers")
    print("n   sum of first n odds      claim")
    print("--  -----------------------  ---------")
    for n in range(1, 8):
        s = sum_first_n_odds(n)
        print(f"{n:<2}  {s:<23}  {n}^2 = {n*n}")
    print("\nPattern: 1 + 3 + 5 + … + (2n−1) = n²")
    print("Reason (algebra): (k+1)² − k² = 2k+1, the next odd number.")
    print("So adding the next odd grows a perfect square → the rule holds for every n.")

# ------------------------------------------------------------
# (3) REASONING vs TRIAL — two routes to the unknown
# ------------------------------------------------------------

def factor_quadratic_sum_prod(S: int, P: int) -> Optional[Tuple[int, int]]:
    # Return integers (u,v) with u+v=S and uv=P if they exist.
    for u in range(-abs(P)-abs(S)-1, abs(P)+abs(S)+2):
        v = S - u
        if u*v == P:
            return (u, v)
    return None

def algebraic_sum_prod(S: int, P: int) -> Tuple[float, float]:
    # Roots of t^2 - S t + P = 0
    D = S*S - 4*P
    if D < 0:
        return (float('nan'), float('nan'))
    r1 = (S + math.sqrt(D)) / 2
    r2 = (S - math.sqrt(D)) / 2
    return (r1, r2)

def eliminate_2x2(a1,b1,c1,a2,b2,c2) -> Tuple[Fraction, Fraction]:
    """
    Solve:
        a1 x + b1 y = c1
        a2 x + b2 y = c2
    by elimination with exact Fractions.
    """
    A1,A2,B1,B2,C1,C2 = map(Fraction, (a1,a2,b1,b2,c1,c2))
    D  = A1*B2 - A2*B1
    if D == 0:
        raise ValueError("No unique solution (parallel or dependent).")
    Dx = C1*B2 - C2*B1
    Dy = A1*C2 - A2*C1
    return (Dx/D, Dy/D)

def demo_reasoning():
    hr("Reasoning Beats Trial — two numbers with given sum and product")

    S, P = 13, 40  # “Find two numbers whose sum is 13 and product is 40.”
    print(f"Problem: u+v={S}, uv={P}")

    # Trial-and-error search
    t = factor_quadratic_sum_prod(S, P)
    print("\nTrial search result:", t)

    # Algebraic reasoning
    r1, r2 = algebraic_sum_prod(S, P)
    print("Algebraic solution (roots of t^2 - 13t + 40):", (r1, r2))
    print("We solved all such problems at once: S and P can vary; the method stays.")

    # A “prices” system solved by elimination
    print("\nElimination example:")
    print("  2x + 3y = 13")
    print("  1x − 1y = 1")
    x, y = eliminate_2x2(2,1,3,-1,13,1)  # (a1,a2,b1,b2,c1,c2) arranged to map to equations above
    # Careful: I arranged parameters as (a1,a2,b1,b2,c1,c2) but function expects (a1,b1,c1,a2,b2,c2).
    # Fix: call correctly:
    x, y = eliminate_2x2(2,3,13,1,-1,1)
    print(f"Solution: x={x}, y={y}  →  2·{x}+3·{y}={2*x+3*y},  {x}−{y}={x-y}")

    print("\nMoral: algebra turns specific puzzles into reusable procedures.")

# ------------------------------------------------------------
# (4) CONNECT — algebra, geometry, and logic meet
# ------------------------------------------------------------

def area_model(a: int, b: int) -> List[str]:
    """
    Visualize (x+a)(x+b) = x^2 + (a+b)x + ab as areas of rectangles stitched together.
    Uses x as a dimension label; we draw the pattern conceptually.
    """
    lines = [
        "Area model for (x+a)(x+b):",
        "┌───────────┬───────┐",
        "│   x·x     │  a·x  │  width x+a",
        "├───────────┼───────┤",
        "│   b·x     │  a·b  │",
        "└───────────┴───────┘",
        "height x+b",
        "",
        "Sum of parts → x·x  + a·x + b·x + a·b = x² + (a+b)x + ab"
    ]
    return lines

def complete_square(p: Fraction, q: Fraction) -> Tuple[str, Fraction, Fraction]:
    """
    Given x^2 + p x + q, return textual completion and its (h,k) with:
        x^2 + p x + q = (x + h)^2 + k,  where h = p/2, k = q - (p/2)^2
    """
    h = p / 2
    k = q - (p * p) / 4
    text = f"x^2 + {p}x + {q} = (x + {h})^2 + {k}"
    return (text, h, k)

def quadratic_formula(a: Fraction, b: Fraction, c: Fraction) -> Tuple[complex, complex]:
    # General solution for ax^2 + bx + c = 0
    a, b, c = Fraction(a), Fraction(b), Fraction(c)
    if a == 0:
        raise ValueError("Not quadratic.")
    D = b*b - 4*a*c
    # Produce exact radicals when D is a perfect square; else show complex/root form (float fallback for sqrt).
    if D >= 0:
        s = int(math.isqrt(D.numerator))
        t = D.denominator
        if s*s == D.numerator and int(math.isqrt(t))**2 == t:
            # Perfect square rational discriminant
            sqrtD = Fraction(s, int(math.isqrt(t)))
            r1 = (-b + sqrtD) / (2*a)
            r2 = (-b - sqrtD) / (2*a)
            return (complex(r1), complex(r2))
    # Fallback float
    sqrtD = complex(float(D))**0.5
    r1 = (-float(b) + sqrtD) / (2*float(a))
    r2 = (-float(b) - sqrtD) / (2*float(a))
    return (complex(r1), complex(r2))

def demo_connect():
    hr("Connecting Worlds — area, squares, and a universal recipe")

    # (x+a)(x+b) expansion (area model)
    for line in area_model(a=3, b=2):
        print(line)

    # Completing the square
    print("\nCompleting the square:")
    txt, h, k = complete_square(Fraction(6), Fraction(5))  # x^2 + 6x + 5
    print(" ", txt)
    print("Interpretation: shift x → (x+3); the leftover constant adjusts the area.")

    # Quadratic formula (derived by completing the square, universally applicable)
    print("\nQuadratic formula example for 2x^2 + 3x - 2 = 0:")
    r1, r2 = quadratic_formula(2, 3, -2)
    print(f"  roots: x = {r1} , {r2}")
    # Quick check
    def f(x): return 2*x*x + 3*x - 2
    for r in (r1, r2):
        val = f(r).real if abs(f(r)) < 1e-9 else f(r)
        print("  check f(root) ≈", val)

# ------------------------------------------------------------
# (5) RELATION — equations as a universal language
# ------------------------------------------------------------

def solve_line(a: Fraction, b: Fraction, c: Fraction, xs: List[int]) -> List[Tuple[int, Fraction]]:
    # Given ax + by = c, solve for y across sample x’s.
    a,b,c = map(Fraction, (a,b,c))
    out = []
    for x in xs:
        y = (c - a*Fraction(x)) / b
        out.append((x, y))
    return out

def invariant_transform(eq: Tuple[Fraction, Fraction, Fraction], k: Fraction) -> Tuple[Fraction, Fraction, Fraction]:
    # Multiply both sides of ax+by=c by k — same relation, different presentation.
    a,b,c = eq
    return (a*k, b*k, c*k)

def demo_relation():
    hr("Equations as Relations — many voices, one meaning")

    print("Line L: 2x - y = 3  (every pair (x,y) satisfying this belongs to L)")
    pairs = solve_line(2, -1, 3, xs=list(range(-2, 5)))
    for x, y in pairs:
        print(f"  ({x:>2}, {y})  →  2·{x} - {y} = 3 ✓")

    print("\nSame relation, different form (multiply by 5): 10x - 5y = 15")
    a,b,c = invariant_transform((Fraction(2), Fraction(-1), Fraction(3)), Fraction(5))
    pairs2 = solve_line(a, b, c, xs=[0,1,2])
    for x, y in pairs2:
        print(f"  ({x}, {y}) still lies on the same line.")

    print("\nTwo lines, one point of meeting (solve simultaneously):")
    # 2x - y = 3  and  x + y = 5
    x, y = eliminate_2x2(2, -1, 3, 1, 1, 5)
    print(f"  Intersection: (x,y)=({x},{y})  →  2x−y={2*x - y}=3,  x+y={x+y}=5")
    print("\nMoral: equations name relationships; the symbols are local, the structure is universal.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Algebra as Language — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all", "nameable", "generalize", "reasoning", "connect", "relation"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Algebra as Language — The Grammar of the Unknown")
    print("Demos: nameable (unknowns), generalize (rules), reasoning (trial vs method),")
    print("       connect (area & squares), relation (equations as sets of pairs)")

    if args.demo in ("all", "nameable"):
        demo_nameable()
    if args.demo in ("all", "generalize"):
        demo_generalize()
    if args.demo in ("all", "reasoning"):
        demo_reasoning()
    if args.demo in ("all", "connect"):
        demo_connect()
    if args.demo in ("all", "relation"):
        demo_relation()

if __name__ == "__main__":
    main()
