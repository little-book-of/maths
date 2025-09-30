#!/usr/bin/env python3
# algorithmic_mind.py
#
# 6. The Algorithmic Mind — Rules, Steps, and Certainty
#
# Demos:
#   • structure : Algorithms as structured procedures (Euclid's GCD)
#   • systematic: Reasoning can be systematic (binary search)
#   • skill     : Stepwise logic turns skill into knowledge (long division)
#   • ancient   : Early algorithms — Babylonian square root (Heron’s method)
#   • method    : Method → computation (recipe to code: factorial)
#
# Pure standard library. ASCII output only.

from __future__ import annotations
import argparse
import math
from typing import List, Tuple

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))

def show_steps(steps: List[str]) -> None:
    for s in steps:
        print(s)

# ------------------------------------------------------------
# (1) STRUCTURE — Euclid’s algorithm for GCD
# ------------------------------------------------------------

def gcd_steps(a: int, b: int) -> Tuple[int, List[str]]:
    steps = [f"Find gcd({a}, {b})"]
    while b != 0:
        q, r = divmod(a, b)
        steps.append(f"{a} = {b}·{q} + {r}")
        a, b = b, r
    steps.append(f"gcd = {a}")
    return a, steps

def demo_structure():
    hr("Structured Procedure — Euclid’s Algorithm (GCD)")
    a, b = 252, 198
    g, steps = gcd_steps(a, b)
    show_steps(steps)
    print(f"\nResult: gcd({a},{b}) = {g}")
    print("Idea: a finite list of steps, each justified, leading with certainty to a result.")

# ------------------------------------------------------------
# (2) SYSTEMATIC — Binary search on sorted list
# ------------------------------------------------------------

def binary_search_trace(arr: List[int], target: int) -> Tuple[int, List[str]]:
    lo, hi = 0, len(arr) - 1
    trace = []
    while lo <= hi:
        mid = (lo + hi) // 2
        trace.append(f"Check middle index {mid}, value {arr[mid]}")
        if arr[mid] == target:
            trace.append(f"Found {target} at index {mid}")
            return mid, trace
        elif arr[mid] < target:
            trace.append(f"{arr[mid]} < {target} → search right half")
            lo = mid + 1
        else:
            trace.append(f"{arr[mid]} > {target} → search left half")
            hi = mid - 1
    trace.append(f"{target} not found")
    return -1, trace

def demo_systematic():
    hr("Systematic Reasoning — Binary Search")
    arr = list(range(2, 41, 2))
    target = 26
    idx, trace = binary_search_trace(arr, target)
    print("Array:", arr)
    print(f"Target: {target}\n")
    show_steps(trace)
    print("\nBinary search halves the uncertainty each step — thought as procedure.")

# ------------------------------------------------------------
# (3) SKILL — Long division as algorithm (23 ÷ 7)
# ------------------------------------------------------------

def long_division(dividend: int, divisor: int, digits: int = 5) -> Tuple[str, List[str]]:
    steps = [f"Divide {dividend} by {divisor} step by step:"]
    quotient = dividend // divisor
    remainder = dividend % divisor
    steps.append(f"{divisor} × {quotient} = {divisor*quotient}, remainder {remainder}")
    decimals = []
    for _ in range(digits):
        remainder *= 10
        q = remainder // divisor
        remainder = remainder % divisor
        decimals.append(str(q))
        steps.append(f"Bring down 0 → {remainder//10 if remainder>=10 else remainder}, quotient digit {q}, new remainder {remainder}")
        if remainder == 0:
            break
    result = f"{quotient}." + "".join(decimals)
    steps.append(f"Approximate result: {result}")
    return result, steps

def demo_skill():
    hr("Stepwise Logic — Long Division Algorithm")
    dividend, divisor = 23, 7
    result, steps = long_division(dividend, divisor)
    show_steps(steps)
    print(f"\nCheck: {dividend}/{divisor} ≈ {float(result):.5f}")
    print("Meaning: a craft (division) encoded as repeatable knowledge — step by step.")

# ------------------------------------------------------------
# (4) ANCIENT — Babylonian / Heron’s algorithm for sqrt
# ------------------------------------------------------------

def heron_sqrt_trace(n: float, guess: float = 1.0, tol: float = 1e-6) -> Tuple[float, List[str]]:
    x = guess
    steps = [f"Approximate √{n} (start x₀={x})"]
    k = 0
    while True:
        k += 1
        x_next = 0.5 * (x + n / x)
        steps.append(f"x{k} = 0.5 * ({x:.6f} + {n}/{x:.6f}) = {x_next:.6f}")
        if abs(x_next - x) < tol:
            x = x_next
            break
        x = x_next
    steps.append(f"Converged: √{n} ≈ {x:.6f}")
    return x, steps

def demo_ancient():
    hr("Ancient Algorithm — Babylonian (Heron’s) Square Root")
    n = 10
    approx, steps = heron_sqrt_trace(n, guess=3.0)
    show_steps(steps)
    print(f"\nCheck: math.sqrt({n}) = {math.sqrt(n):.6f}")
    print("Insight: iteration embodies refinement — each step halves the error.")

# ------------------------------------------------------------
# (5) METHOD — from recipe to computation (factorial)
# ------------------------------------------------------------

def factorial_iter(n: int) -> Tuple[int, List[str]]:
    steps = [f"Compute {n}! iteratively:"]
    acc = 1
    for k in range(1, n+1):
        acc *= k
        steps.append(f"step {k}: ×{k} → {acc}")
    return acc, steps

def factorial_recursive(n: int, depth=0) -> Tuple[int, List[str]]:
    pad = "  " * depth
    if n == 0 or n == 1:
        return 1, [f"{pad}return 1"]
    sub, ssteps = factorial_recursive(n-1, depth+1)
    val = n * sub
    steps = [f"{pad}compute {n}! = {n} × ({n-1})!"] + ssteps + [f"{pad}return {val}"]
    return val, steps

def demo_method():
    hr("Method to Machine — Factorial as Algorithm")
    n = 5
    val, steps = factorial_iter(n)
    show_steps(steps)
    print(f"Result: {n}! = {val}")

    print("\nRecursive form (shows self-reference):")
    val2, steps2 = factorial_recursive(n)
    show_steps(steps2)
    print(f"Check: {n}! = {val2}")
    print("\nLesson: when knowledge is explicit in steps, it can be delegated — to apprentice or automaton.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="The Algorithmic Mind — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all", "structure", "systematic", "skill", "ancient", "method"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("The Algorithmic Mind — Rules, Steps, and Certainty")
    print("Demos: structure (Euclid GCD), systematic (binary search), skill (long division),")
    print("       ancient (Heron sqrt), method (factorial iteration/recursion)")

    if args.demo in ("all", "structure"):
        demo_structure()
    if args.demo in ("all", "systematic"):
        demo_systematic()
    if args.demo in ("all", "skill"):
        demo_skill()
    if args.demo in ("all", "ancient"):
        demo_ancient()
    if args.demo in ("all", "method"):
        demo_method()

if __name__ == "__main__":
    main()
