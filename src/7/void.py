#!/usr/bin/env python3
# void.py
#
# 7. Zero and Infinity — Taming the Void
#
# Demos:
#   • placeholder : Zero turns emptiness into something countable (positional power)
#   • limits      : Approach vs reach — sin(x)/x near 0; (1+1/n)^n toward e; divide-by-zero trap
#   • paradox     : Infinity’s surprises — Hilbert’s Hotel; Galileo’s bijection (N ↔ squares/evens)
#   • series      : Infinite processes — geometric (converges) vs harmonic (diverges)
#   • frame       : The frame of math — zero identities/annihilator; extended real line & limits
#
# Pure standard library, ASCII output.

from __future__ import annotations
import argparse
import math
from typing import List, Tuple

# ---------------------------------------
# Helpers
# ---------------------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def expand_decimal(n: int) -> str:
    s = str(n)
    terms = []
    for i, ch in enumerate(s):
        d = int(ch)
        p = len(s) - i - 1
        terms.append(f"{d}×10^{p}")
    return " + ".join(terms)

# Roman (no zero symbol), to contrast length/clarity vs positional with zeros
ROMAN_DIGITS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
]
def to_roman(n: int) -> str:
    if not (0 < n < 4000): return "(out of range)"
    out = []
    for val, sym in ROMAN_DIGITS:
        k, n = divmod(n, val)
        out.append(sym * k)
    return "".join(out)

# ---------------------------------------
# (1) Zero as placeholder — positional power
# ---------------------------------------

def demo_placeholder():
    hr("Zero as Placeholder — the power of position")

    a, b = 205, 25
    print(f"{a} in expanded form: {expand_decimal(a)}")
    print(f"{b} in expanded form: {expand_decimal(b)}")
    print("Observation: the 0 in 205 keeps the tens place empty yet *counted*.\n")

    nums = [9, 90, 900, 9000]
    print("Same digit, different place ⇒ different value:")
    for n in nums:
        print(f"  {n:<5}  → {expand_decimal(n)}")

    n = 2025
    print("\nWith and without a zero-symbol (contrast to Roman):")
    print(f"  Decimal: {n}")
    print(f"  Roman  : {to_roman(n)}   (no symbol for zero)")
    print("Takeaway: zero turns absence into structure — enabling compact, scalable notation.")

# ---------------------------------------
# (2) Limits — approach vs divide-by-zero; e from compounding
# ---------------------------------------

def demo_limits():
    hr("Approach, Not Reach — limits around 0 and ∞")

    print("A) sin(x)/x near x=0 (the value at 0 is *defined by* a limit):")
    xs = [1, 0.5, 0.1, 0.01, 0.001]
    for x in xs:
        print(f"  x={x:>7} → sin(x)/x ≈ {math.sin(x)/x:.10f}")
    print("Limit tends to 1 as x→0, even though direct substitution would be 0/0 (undefined).")

    print("\nB) Divide-by-zero trap (undefined, not ∞):")
    try:
        y = 1/0
    except Exception as e:
        print("  1/0 raises:", type(e).__name__, "-", e)

    print("\nC) Reaching e by method, not leap: (1+1/n)^n as n grows")
    ns = [1, 2, 5, 10, 50, 100, 1000, 10000]
    for n in ns:
        approx = (1 + 1/n)**n
        print(f"  n={n:<5} → {(approx):.12f}")
    print(f"  math.e = {math.e:.12f}")
    print("Meaning: certainty comes from controlled approach — the algorithm of limits.")

# ---------------------------------------
# (3) Infinity’s surprises — Hilbert & Galileo
# ---------------------------------------

def demo_paradox():
    hr("Infinity’s Surprises — Hilbert’s Hotel & Galileo’s Bijections")

    print("Hilbert’s Hotel: countably infinite rooms 1,2,3,... all occupied.")
    print("  Move every guest from n → n+1. Room 1 becomes free.")
    print("  Mapping (first 10):")
    for n in range(1, 11):
        print(f"    guest in room {n:>2}  →  room {n+1:>2}")

    print("\nWhole numbers vs even numbers — same cardinality:")
    print("  n ↦ 2n  (bijection N → Evens)")
    for n in range(1, 8):
        print(f"    {n} ↦ {2*n}")

    print("\nGalileo’s paradox — squares are “as many” as naturals:")
    print("  n ↦ n²  (bijection N → Squares)")
    for n in range(1, 8):
        print(f"    {n} ↦ {n*n}")
    print("Counter-intuition: a proper *subset* of an infinite set can match it one-to-one.")

# ---------------------------------------
# (4) Infinite series — converge vs diverge
# ---------------------------------------

def partial_sums(seq: List[float]) -> List[float]:
    out = []
    s = 0.0
    for a in seq:
        s += a
        out.append(s)
    return out

def demo_series():
    hr("Infinite Processes — some sums settle, some drift forever")

    # Geometric series 1/2 + 1/4 + 1/8 + ... → 1
    g = [0.5*(0.5**k) for k in range(0, 20)]
    G = partial_sums(g)
    print("Geometric (ratio 1/2): first 10 partial sums")
    for i, s in enumerate(G[:10], 1):
        print(f"  S_{i:<2} = {s:.10f}")
    print("Limit exists (→1). Finite rule captures an infinite process.\n")

    # Harmonic series 1 + 1/2 + 1/3 + ... diverges (grows without bound)
    h = [1.0/(k+1) for k in range(2000)]
    H = partial_sums(h)
    print("Harmonic: S_10, S_100, S_1000, S_2000")
    idx = [10, 100, 1000, 2000]
    for i in idx:
        print(f"  S_{i:<4} ≈ {H[i-1]:.6f}")
    print("No finite limit — it keeps creeping upward. Infinity can arrive by *accumulation*.")

# ---------------------------------------
# (5) The frame — zero & ±∞ shaping math
# ---------------------------------------

def solve_zero_product(a: int, b: int) -> Tuple[int, int]:
    # Solve (x-a)(x-b)=0 via zero-product property
    return (a, b)

def demo_frame():
    hr("The Frame: between absence (0) and boundlessness (±∞)")

    print("Zero as identity & annihilator:")
    print("  Additive identity: n + 0 = n")
    print("  Multiplicative annihilator: n × 0 = 0")
    print("  Zero-product property: if uv=0 then u=0 or v=0")

    print("\nExample: (x−3)(x+2)=0 ⇒ x=3 or x=−2")
    roots = solve_zero_product(3, -2)
    print("  roots:", roots)

    print("\nExtended real line in practice (floating point):")
    big = 1e308
    print(f"  big = {big}, big*10 →", big*10)   # overflows to inf in IEEE-754
    print("  math.inf behaves as +∞ in comparisons:", math.inf > big)

    print("\nLimits frame change into structure:")
    ns = [10, 100, 1000, 10000, 100000]
    print("  a_n = (n+1)/n → 1")
    for n in ns:
        print(f"    n={n:<6} → {(n+1)/n:.12f}")
    print("  b_n = n/(n+1) → 1")
    for n in ns:
        print(f"    n={n:<6} → {n/(n+1):.12f}")

    print("\nSense: zero anchors the line; infinity extends it.")
    print("Together they let us reason at the edges — where calculus, measure,")
    print("and modern physics learned to speak precisely about the void and the vast.")

# ---------------------------------------
# CLI
# ---------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Zero and Infinity — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all", "placeholder", "limits", "paradox", "series", "frame"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Zero and Infinity — Taming the Void")
    print("Demos: placeholder (positional zero), limits (approach vs division),")
    print("       paradox (Hilbert/Galileo), series (converge vs diverge), frame (identities & ±∞)")

    if args.demo in ("all", "placeholder"):
        demo_placeholder()
    if args.demo in ("all", "limits"):
        demo_limits()
    if args.demo in ("all", "paradox"):
        demo_paradox()
    if args.demo in ("all", "series"):
        demo_series()
    if args.demo in ("all", "frame"):
        demo_frame()

if __name__ == "__main__":
    main()
