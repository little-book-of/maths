#!/usr/bin/env python3
# certainty.py
#
# 10. The Logic of Certainty — Proof as Power
#
# Demos:
#   • belief  : Proof transforms belief into knowledge (Pythagoras demonstration)
#   • build   : Certainty is built, not assumed (induction on n(n+1)/2)
#   • gold    : Mathematics as gold standard of truth (logical equivalence table)
#   • inspire : Mathematical method inspiring science (law validation via data fit)
#   • spirit  : The pursuit of proof — automated checking (truth tables, brute verification)
#
# Pure standard library. ASCII output only.

from __future__ import annotations
import argparse
import math
import random
from typing import List, Tuple

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

# ------------------------------------------------------------
# (1) Belief → Knowledge — Pythagorean proof (area rearrangement)
# ------------------------------------------------------------

def pythagoras_area(a:int,b:int) -> Tuple[float,float,float]:
    c = math.hypot(a,b)
    return a*a, b*b, c*c

def demo_belief():
    hr("From Belief to Knowledge — Pythagoras by area")
    a, b = 3, 4
    A1, A2, A3 = pythagoras_area(a,b)
    print(f"For right triangle with legs {a},{b}:")
    print(f"  small squares: {a}²={A1}, {b}²={A2}")
    print(f"  big square: c²={(math.isqrt(int(A1+A2)))**2 if A1+A2==25 else A1+A2}")
    print(f"Check: {A1}+{A2}={A1+A2} = {A3}")
    print("Equality shown, not asserted — belief replaced by demonstration.")

# ------------------------------------------------------------
# (2) Build Certainty — Induction proof n(n+1)/2
# ------------------------------------------------------------

def demo_build():
    hr("Certainty is built — Induction on sum of first n integers")
    steps = [
        "Statement: 1 + 2 + ... + n = n(n+1)/2",
        "Base: n=1 → 1 = 1·2/2 ✓",
        "Assume true for n=k: 1+...+k = k(k+1)/2",
        "Add next term: 1+...+k+(k+1) = k(k+1)/2 + (k+1)",
        "Simplify RHS: (k+1)(k/2+1) = (k+1)(k+2)/2",
        "Replace k+1→n: holds for n=k+1 → proven ∀n∈ℕ"
    ]
    for s in steps:
        print(s)
    print("\nCertainty is *constructed* by steps — each rests on the last.")

# ------------------------------------------------------------
# (3) Gold Standard — logic table: equivalence of ¬(A∨B) and ¬A∧¬B
# ------------------------------------------------------------

def truth_table_equiv():
    rows=[]
    for A in [False,True]:
        for B in [False,True]:
            lhs = not(A or B)
            rhs = (not A) and (not B)
            rows.append((A,B,lhs,rhs))
    return rows

def demo_gold():
    hr("Mathematics as Gold Standard of Truth — Logical Equivalence")
    rows = truth_table_equiv()
    print("A     B    ¬(A∨B)   ¬A∧¬B")
    print("--------------------------")
    for A,B,lhs,rhs in rows:
        print(f"{A!s:<5}{B!s:<5}{lhs!s:<8}{rhs!s}")
    if all(lhs==rhs for _,_,lhs,rhs in rows):
        print("\nAll rows match → identities hold universally, not by opinion.")
    print("Logic’s precision sets the benchmark for every truth claim.")

# ------------------------------------------------------------
# (4) Inspire Rational Inquiry — fit data to a law (Galileo parabola)
# ------------------------------------------------------------

def fit_parabola(ts:List[float], ys:List[float]) -> Tuple[float,float]:
    # Model y = a t^2; slope = Σ(t^2*y)/Σ(t^4)
    X2=[t*t for t in ts]
    num=sum(x*y for x,y in zip(X2,ys))
    den=sum(x*x for x in X2)
    a=num/den
    return a,0.0

def demo_inspire():
    hr("Method Inspires Science — verifying y ∝ t² (Galilean fall)")
    g_true=9.81; h0=0
    ts=[0.2,0.3,0.4,0.5,0.6]
    ys=[0.5*g_true*t*t + random.gauss(0,0.01) for t in ts]
    a,_=fit_parabola(ts,ys)
    g_est=2*a
    print("t(s)   y(m)")
    for t,y in zip(ts,ys):
        print(f"{t:4.2f}  {y:6.3f}")
    print(f"\nFit yields y≈{a:.3f}·t²  ⇒ g≈{g_est:.2f}")
    print("Empirical law tested by method — reasoning applied to nature.")

# ------------------------------------------------------------
# (5) Spirit of Reason — exhaustive verification / truth search
# ------------------------------------------------------------

def verify_distributive_law(limit:int=3) -> bool:
    for a in range(limit):
        for b in range(limit):
            for c in range(limit):
                lhs=a*(b+c)
                rhs=a*b+a*c
                if lhs!=rhs:
                    print("Counterexample:",a,b,c)
                    return False
    return True

def demo_spirit():
    hr("Spirit of Reason — Let every claim be shown")
    print("Check distributive law a(b+c)=ab+ac for a,b,c∈{0,1,2}")
    ok=verify_distributive_law()
    if ok:
        print("All combinations verified ✓  (mechanical proof by exhaustion)")
    print("Lesson: the ideal of mathematics — no step rests on trust alone.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser=argparse.ArgumentParser(description="The Logic of Certainty — runnable micro-demos.")
    parser.add_argument("--demo",
        choices=["all","belief","build","gold","inspire","spirit"],
        default="all",help="Which demo to run.")
    args=parser.parse_args()

    print("The Logic of Certainty — Proof as Power")
    print("Demos: belief (proof→knowledge), build (induction), gold (logic table),")
    print("       inspire (method in science), spirit (verification)")

    if args.demo in ("all","belief"): demo_belief()
    if args.demo in ("all","build"): demo_build()
    if args.demo in ("all","gold"): demo_gold()
    if args.demo in ("all","inspire"): demo_inspire()
    if args.demo in ("all","spirit"): demo_spirit()

if __name__=="__main__":
    main()
