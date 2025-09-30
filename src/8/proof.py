#!/usr/bin/env python3
# proof.py
#
# 8. The Logic of Proof — From Belief to Knowledge
#
# Demos:
#   • independence : Proof makes knowledge independent of authority (counterexample logic)
#   • geometry     : Greek geometry as logical structure (two-column proof style)
#   • axioms       : From axioms to certainty (Peano arithmetic mini-system)
#   • necessity    : Show that truth must follow (contradiction & syllogism)
#   • republic     : A republic of reason (multiple proofs for same truth)
#
# Pure standard library. ASCII text only.

from __future__ import annotations
import argparse
from typing import List, Callable

# ------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))

def show_lines(lines: List[str]) -> None:
    for line in lines:
        print(line)

# ------------------------------------------------------------
# (1) Independence — counterexample vs authority
# ------------------------------------------------------------

def is_even(n: int) -> bool:
    return n % 2 == 0

def demo_independence():
    hr("Proof ≠ Authority — Logic over Voice")
    claim = "All prime numbers are odd."
    print(f"Claim: {claim}")
    print("Authority might assert it. But proof demands verification.\n")

    # Check first few primes
    primes = [2, 3, 5, 7, 11, 13]
    counter = [p for p in primes if is_even(p)]
    print("Testing small primes:", primes)
    if counter:
        print(f"Counterexample found: {counter[0]} is even.")
        print("Thus the claim is false — one counterexample refutes universal assertion.")
    print("\nLesson: proof needs no oracle; logic alone compels assent.")

# ------------------------------------------------------------
# (2) Geometry — two-column proof (Euclid I.5 example simplified)
# ------------------------------------------------------------

def demo_geometry():
    hr("Greek Geometry — The Shape of Logical Reasoning")
    theorem = "Base angles of an isosceles triangle are equal."
    print("Theorem:", theorem)
    print("\nTwo-column proof (outline):")
    left = [
        "1. Triangle ABC with AB = AC",
        "2. Extend AB, AC beyond B,C; mark equal segments BD = CE",
        "3. Join DE",
        "4. Triangles ABD and ACE share side AD = AE",
        "5. AB = AC, BD = CE, AD = AE (SSS)"
    ]
    right = [
        "Given",
        "Construction",
        "Construction",
        "Common side",
        "By SSS, △ABD ≅ △ACE"
    ]
    for l, r in zip(left, right):
        print(f"{l:<45} | {r}")
    print("6. Therefore ∠ABC = ∠ACB (CPCTC)")
    print("\nIdea: statements justified by prior truths — a chain of reason, not decree.")

# ------------------------------------------------------------
# (3) Axioms — building certainty from primitives
# ------------------------------------------------------------

def peano_axioms() -> List[str]:
    return [
        "A1. 0 is a natural number.",
        "A2. Every number has a successor.",
        "A3. 0 is not the successor of any number.",
        "A4. Distinct numbers have distinct successors.",
        "A5. (Induction) If 0 has P and P(n)→P(n+1), then all n have P."
    ]

def prove_add_zero_identity(n: int) -> List[str]:
    lines = [
        f"Prove: n + 0 = n for all n (by induction)",
        "Base case: 0 + 0 = 0 (A1)",
        "Inductive step:",
        "  Assume n + 0 = n.",
        "  Then S(n) + 0 = S(n + 0) = S(n).",
        "Hence holds for all n."
    ]
    return lines

def demo_axioms():
    hr("From Axioms — The Ideal of Certainty")
    print("Peano Arithmetic (axioms for natural numbers):")
    show_lines(peano_axioms())
    print()
    show_lines(prove_add_zero_identity(5))
    print("\nMeaning: certainty flows from first principles — axioms, not authority.")

# ------------------------------------------------------------
# (4) Necessity — showing truth must follow (contradiction / syllogism)
# ------------------------------------------------------------

def prove_contradiction() -> List[str]:
    return [
        "Goal: √2 is irrational.",
        "Assume √2 = a/b in lowest terms.",
        "Then 2 = a²/b² ⇒ a² = 2b².",
        "So a² even ⇒ a even ⇒ a=2k.",
        "Substitute: (2k)²=2b² ⇒ 4k²=2b² ⇒ b²=2k² ⇒ b even.",
        "But if a,b even, fraction not lowest ⇒ contradiction.",
        "Therefore √2 ∉ ℚ."
    ]

def syllogism_example() -> List[str]:
    return [
        "All humans are mortal.",
        "Socrates is a human.",
        "Therefore Socrates is mortal."
    ]

def demo_necessity():
    hr("Necessity — Truth That Must Follow")
    print("A) Proof by contradiction:")
    show_lines(prove_contradiction())
    print("\nB) Syllogistic reasoning:")
    show_lines(syllogism_example())
    print("\nIn both, denial collapses logic itself — truth becomes unavoidable.")

# ------------------------------------------------------------
# (5) Republic — many proofs, shared law
# ------------------------------------------------------------

def algebraic_proof_of_pythagoras(a: int, b: int) -> List[str]:
    c = math.hypot(a, b)
    return [
        f"Given right triangle with legs {a}, {b}, hypotenuse {c:.1f}:",
        f"a² + b² = {a*a} + {b*b} = {a*a + b*b}",
        f"c² = {c:.1f}² = {c*c:.1f}",
        "Thus a² + b² = c² ✓"
    ]

def geometric_reasoning_summary() -> List[str]:
    return [
        "Squares on sides: areas of small squares together equal big square.",
        "Each decomposition rearranges exactly — geometry mirrors algebra."
    ]

def demo_republic():
    hr("A Republic of Reason — Many Roads, One Truth")
    show_lines(algebraic_proof_of_pythagoras(3,4))
    print()
    show_lines(geometric_reasoning_summary())
    print("\nTakeaway: In the republic of proof, any citizen may show the law —")
    print("           authority rests not in who speaks, but in what follows.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="The Logic of Proof — runnable micro-demos.")
    parser.add_argument(
        "--demo",
        choices=["all", "independence", "geometry", "axioms", "necessity", "republic"],
        default="all",
        help="Which demo to run."
    )
    args = parser.parse_args()

    print("The Logic of Proof — From Belief to Knowledge")
    print("Demos: independence (logic vs authority), geometry (two-column), axioms (Peano),")
    print("       necessity (contradiction/syllogism), republic (many proofs, one law)")

    if args.demo in ("all", "independence"):
        demo_independence()
    if args.demo in ("all", "geometry"):
        demo_geometry()
    if args.demo in ("all", "axioms"):
        demo_axioms()
    if args.demo in ("all", "necessity"):
        demo_necessity()
    if args.demo in ("all", "republic"):
        demo_republic()

if __name__ == "__main__":
    main()
