#!/usr/bin/env python3
# arithmetic.py
#
# 3. The Birth of Arithmetic — Adding the World
#
# Demos mapping to the Key Ideas:
#   • trade     : Arithmetic from everyday problems (buy/sell, measure, plan)
#   • patterns  : Repetition reveals pattern (skip-counting, residues, tables)
#   • structure : Operations show structure in change (laws like distributivity)
#   • combine   : Numbers can be combined, not just counted (sums, ratios)
#   • future    : Reasoning ahead (compound growth, inventory projection)
#
# Pure standard library. ASCII output. No external deps.

from __future__ import annotations
import argparse
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def money(amount: int, symbol: str = "$") -> str:
    return f"{symbol}{amount/100:.2f}"

# ------------------------------------------------------------
# (1) TRADE — everyday arithmetic (receipt, change-making, measure)
# ------------------------------------------------------------

@dataclass
class Line:
    item: str
    qty: int
    unit_price_cents: int

    def subtotal(self) -> int:
        return self.qty * self.unit_price_cents

@dataclass
class Receipt:
    lines: List[Line] = field(default_factory=list)
    tax_rate: float = 0.05  # 5%

    def total_before_tax(self) -> int:
        return sum(L.subtotal() for L in self.lines)

    def tax(self) -> int:
        return round(self.total_before_tax() * self.tax_rate)

    def total(self) -> int:
        return self.total_before_tax() + self.tax()

    def render(self) -> str:
        out = ["ITEM                 QTY    UNIT     SUBTOTAL",
               "------------------------------------------------"]
        for L in self.lines:
            out.append(f"{L.item:<20} {L.qty:>3}  {money(L.unit_price_cents):>8}  {money(L.subtotal()):>10}")
        out.append("------------------------------------------------")
        out.append(f"{'Subtotal':<28} {money(self.total_before_tax()):>10}")
        out.append(f"{'Tax':<28} {money(self.tax()):>10}")
        out.append(f"{'Total':<28} {money(self.total()):>10}")
        return "\n".join(out)

COINS = [100, 50, 25, 10, 5, 1]  # cents (greedy optimal in US-style system)

def make_change(change_cents: int, coins: List[int] = COINS) -> Dict[int, int]:
    result: Dict[int, int] = {}
    remaining = change_cents
    for c in coins:
        k, remaining = divmod(remaining, c)
        if k:
            result[c] = k
    return result

def demo_trade():
    hr("Trade — arithmetic in buying and selling")
    r = Receipt(lines=[
        Line("wheat (kg)", 7, 145),   # $1.45/kg
        Line("stone (m²)", 3, 2500),  # $25.00/m²
        Line("jar (ea)",   4, 375),   # $3.75 each
    ], tax_rate=0.05)

    print(r.render())

    # Customer pays with bills/coins; compute change
    paid = 10000  # $100.00
    change = paid - r.total()
    print(f"\nPaid: {money(paid)}   Change due: {money(change)}")

    combo = make_change(change)
    print("Give back as:")
    for c in COINS:
        if c in combo:
            print(f"  {combo[c]} × {money(c)}")

    # Measure quickie: convert meters to feet for a stone slab
    meters = 2.5
    feet = meters * 3.28084
    print(f"\nMeasure: {meters} meters ≈ {feet:.2f} feet")

# ------------------------------------------------------------
# (2) PATTERNS — repetition reveals structure
# ------------------------------------------------------------

def skip_count(start: int, step: int, n: int) -> List[int]:
    return [start + i*step for i in range(n)]

def residues_mod(n: int, mod: int) -> List[int]:
    return [ (i*n) % mod for i in range(mod) ]  # first full cycle

def mult_row(n: int, upto: int = 10) -> List[int]:
    return [n*k for k in range(1, upto+1)]

def demo_patterns():
    hr("Patterns — repetition uncovers regularity")

    # Skip counting: repeated addition
    seq = skip_count(start=0, step=7, n=12)
    print("Skip-count by 7:", seq)
    print("Observation: the pattern is linear — each term adds the same step.")

    # Multiplication rows: repeated addition compressed
    n = 7
    row = mult_row(n, 12)
    print(f"\nMultiplication row for {n}:")
    print("  ", row)
    print("Same information as skip-counting, but summarized as n×k.")

    # Residues modulo 7: cycles in repetition
    r = residues_mod(3, 7)
    print("\nResidues of multiples of 3 modulo 7 (full cycle):")
    print("  ", r)
    print("Pattern: repetition 'wraps' — arithmetic uncovers cycles and periodicity.")

# ------------------------------------------------------------
# (3) STRUCTURE — laws of operation (comm, assoc, dist) & area model
# ------------------------------------------------------------

def check_properties(a: int, b: int, c: int) -> List[str]:
    props = []
    if a + b == b + a:
        props.append("addition commutative: a+b=b+a")
    if (a + b) + c == a + (b + c):
        props.append("addition associative: (a+b)+c=a+(b+c)")
    if a * b == b * a:
        props.append("multiplication commutative: ab=ba")
    if (a * b) * c == a * (b * c):
        props.append("multiplication associative: (ab)c=a(bc)")
    if a*(b + c) == a*b + a*c:
        props.append("distributive: a(b+c)=ab+ac")
    return props

def area_block(w: int, h: int, ch: str = "■") -> List[str]:
    # Tiny ASCII rectangle (clamped to keep it readable)
    w = max(1, min(w, 20))
    h = max(1, min(h, 6))
    return ["".join(ch for _ in range(w)) for _ in range(h)]

def area_model(a: int, b: int, c: int) -> str:
    # Visualize a(b+c)=ab+ac with blocks
    left = area_block(a, b + c, ch="■")
    right_top = area_block(a, b, ch="■")
    right_bot = area_block(a, c, ch="□")
    # Stitch right side vertically
    right = right_top + right_bot
    # Label strings
    L = ["LEFT:  a × (b + c)"] + left
    R = ["RIGHT: a×b + a×c (■=ab, □=ac)"] + right
    # Align columns
    width = max(len(row) for row in L[1:] + R[1:])
    L = [L[0]] + [row.ljust(width) for row in L[1:]]
    R = [R[0]] + [row.ljust(width) for row in R[1:]]
    lines = [l + "   |   " + r for l, r in zip(L, R)]
    return "\n".join(lines)

def demo_structure():
    hr("Structure — the grammar of quantity (laws of operation)")
    a, b, c = 3, 2, 4
    props = check_properties(a, b, c)
    print(f"For a={a}, b={b}, c={c}:")
    for p in props:
        print("  ✓", p)

    print("\nDistributive law via an area model:")
    print(area_model(a, b, c))
    print("Meaning: multiplication distributes over addition — change has structure.")

# ------------------------------------------------------------
# (4) COMBINE — beyond counting (sums, averages, weighted mixes)
# ------------------------------------------------------------

def average(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")

def weighted_average(pairs: List[Tuple[float, float]]) -> float:
    # pairs = [(value, weight), ...]
    wsum = sum(w for _, w in pairs)
    return sum(v*w for v, w in pairs) / wsum if wsum else float("nan")

def demo_combine():
    hr("Combine — numbers join in many ways")
    harvest_weights = [2.1, 1.9, 2.4, 2.0, 2.2]  # kg per crate
    print("Sum (total harvest):", sum(harvest_weights), "kg")
    print("Average crate weight:", round(average(harvest_weights), 3), "kg")

    # Mixing grain from two fields with different moisture content
    fieldA = (12.5, 30)  # 12.5% moisture, 30 sacks
    fieldB = (9.5,  20)  # 9.5% moisture,  20 sacks
    mix = weighted_average([fieldA, fieldB])
    print(f"\nWeighted average moisture of mix: {mix:.2f}%")
    print("Idea: 'combine' is richer than 'count' — ratios and balances matter.")

# ------------------------------------------------------------
# (5) FUTURE — arithmetic as prediction (linear vs compound)
# ------------------------------------------------------------

def years_to_target(principal: float, rate: float, target: float) -> int:
    """
    Compound annually: P -> P*(1+r)^t. Return minimal integer t with P*(1+r)^t >= target.
    rate given as 0.05 for 5%
    """
    if principal <= 0 or rate <= 0:
        return 0 if principal >= target else float("inf")
    t = 0
    value = principal
    while value < target:
        value *= (1 + rate)
        t += 1
        if t > 1000: break
    return t

def project_inventory(start: int, weekly_add: int, weeks: int, weekly_sales: int) -> List[int]:
    """
    Linear forecast: stock_{t+1} = stock_t + weekly_add - weekly_sales.
    """
    s = start
    series = [s]
    for _ in range(weeks):
        s = s + weekly_add - weekly_sales
        series.append(s)
    return series

def demo_future():
    hr("Future — arithmetic as a tool to see ahead")

    # Compound growth: saving grain or money
    P = 1000.0   # starting units
    r = 0.06     # 6% per period
    T = 2000.0   # target
    t = years_to_target(P, r, T)
    print(f"Compound growth: starting {P}, rate {r*100:.1f}%, target {T} ⇒ ~{t} periods")

    # Linear inventory planning
    stock_path = project_inventory(start=120, weekly_add=35, weeks=10, weekly_sales=42)
    print("\nProjected inventory over 10 weeks (start=120, +35/week, sell 42/week):")
    print(stock_path)
    when_short = next((i for i, s in enumerate(stock_path) if s < 0), None)
    if when_short is not None:
        print(f"Warning: stockout around week {when_short}. Adjust plan.")
    else:
        print("Plan covers demand — no stockout in horizon.")

    print("\nTakeaway: the same rules that total a receipt let us plan harvests and inventories.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="The Birth of Arithmetic — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all", "trade", "patterns", "structure", "combine", "future"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("The Birth of Arithmetic — Adding the World")
    print("Demos: trade (receipt/change), patterns (repetition), structure (laws), combine (sums/ratios), future (forecast)")

    if args.demo in ("all", "trade"):
        demo_trade()
    if args.demo in ("all", "patterns"):
        demo_patterns()
    if args.demo in ("all", "structure"):
        demo_structure()
    if args.demo in ("all", "combine"):
        demo_combine()
    if args.demo in ("all", "future"):
        demo_future()

if __name__ == "__main__":
    main()
