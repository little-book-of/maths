#!/usr/bin/env python3
# gauss.py
#
# 15. Gauss and the Hidden Order — The Birth of Number Theory
#
# Demos:
#   • structure  : Numbers possess structure, not just value (Z/nZ ring; units & inverses)
#   • residues   : Hidden laws among primes & residues (quadratic residues; Euler's criterion)
#   • rigor      : Rigor with mystery (Fermat’s little theorem; Carmichael 561)
#   • repetition : Modular arithmetic as a lens on cycles (orders; decimal repetends)
#   • science    : Arithmetic as a theoretical science (extended gcd, inverses, CRT)
#
# Pure standard library. ASCII output.

from __future__ import annotations
import argparse
from math import gcd

# --------------------------------------------
# Helpers
# --------------------------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def sieve(n: int):
    if n < 2: return []
    a = [True]*(n+1)
    a[0]=a[1]=False
    p=2
    while p*p <= n:
        if a[p]:
            step = p
            start = p*p
            a[start:n+1:step]=[False]*(((n-start)//step)+1)
        p += 1
    return [i for i,t in enumerate(a) if t]

def extgcd(a: int, b: int):
    """Return (g,x,y) such that ax+by=g=gcd(a,b)."""
    if b==0: return (abs(a), 1 if a>0 else -1, 0)
    g,x1,y1 = extgcd(b, a%b)
    return (g, y1, x1 - (a//b)*y1)

def modinv(a: int, m: int):
    g,x,y = extgcd(a, m)
    if g != 1:
        raise ValueError(f"No inverse for {a} mod {m}")
    return x % m

def powmod(a: int, e: int, m: int) -> int:
    res = 1 % m
    a %= m
    while e>0:
        if e & 1: res = (res*a) % m
        a = (a*a) % m
        e >>= 1
    return res

# --------------------------------------------
# (1) STRUCTURE — Z/nZ: units and inverses
# --------------------------------------------

def units_mod(n: int):
    return [a for a in range(1, n) if gcd(a, n) == 1]

def inverses_table(n: int):
    pairs = []
    for a in units_mod(n):
        inv = modinv(a, n)
        if a <= inv:  # avoid duplicates (a,inv) & (inv,a)
            pairs.append((a, inv))
    return pairs

def demo_structure():
    hr("Numbers have structure — the ring Z/nZ (example n=12)")
    n = 12
    U = units_mod(n)
    print(f"Units modulo {n} (invertible classes): {U}")
    print(f"Count φ({n}) = {len(U)} (Euler’s totient)")
    print("\nMultiplicative inverses mod 12:")
    for a,b in inverses_table(n):
        print(f"  {a:>2} × {b:<2} ≡ 1 (mod {n})")
    print("\nObservation: not every element has an inverse (e.g., 2,3,4,6 share factors with 12).")
    print("Structure (gcd, units, inverses) matters as much as *value*.")

# --------------------------------------------
# (2) RESIDUES — quadratic residues; Euler’s criterion
# --------------------------------------------

def quadratic_residues_mod_p(p: int):
    return sorted({ (a*a) % p for a in range(p) })

def legendre_via_euler(a: int, p: int) -> int:
    """Legendre symbol (a|p) via Euler's criterion: a^{(p-1)/2} ≡ ±1 (mod p), 0 if p|a."""
    a %= p
    if a == 0: return 0
    t = powmod(a, (p-1)//2, p)
    if t == 1: return 1
    if t == p-1: return -1
    # Shouldn't happen for prime p; treat as -1 conservatively.
    return -1

def demo_residues():
    hr("Primes & residues — quadratic residues and Euler’s criterion")
    p = 29
    QR = quadratic_residues_mod_p(p)
    print(f"Quadratic residues mod p={p} ({len(QR)} of them):")
    print(QR)
    tests = [2, 3, 5, 6, 7, 10, 11, 14]
    print("\nLegendre symbol via Euler's criterion (a|p):")
    for a in tests:
        s = legendre_via_euler(a, p)
        tag = "residue" if s==1 else ("non-residue" if s==-1 else "≡0")
        print(f"  ({a}|{p}) = {s:+2d}  → {tag}")
    print("\nFacts unveiled:")
    print("  • Exactly (p−1)/2 numbers are quadratic residues (excluding 0).")
    print("  • Euler’s criterion: a^((p−1)/2) ≡ (a|p) (mod p).")
    print("Gauss systematized these patterns (ultimately leading to Quadratic Reciprocity).")

# --------------------------------------------
# (3) RIGOR — Fermat’s little theorem & the mystery of 561
# --------------------------------------------

def is_probable_prime_fermat(n: int, bases=(2,3,5,7)):
    if n < 2: return False
    for b in bases:
        if b % n == 0: continue
        if powmod(b, n-1, n) != 1:
            return False
    return True

def demo_rigor():
    hr("Rigor with mystery — Fermat’s little theorem, and a warning (561)")
    primes = [p for p in sieve(50) if p > 2]
    print("Fermat’s little theorem: a^{p−1} ≡ 1 (mod p) for prime p and gcd(a,p)=1.\n")
    print("Check for p ≤ 50 and base a=2:")
    for p in primes:
        ok = powmod(2, p-1, p) == 1
        print(f"  2^{p-1} ≡ 1 (mod {p}) → {ok}")
    print("\nBut composites can *masquerade* as primes for many bases:")
    n = 561  # Carmichael number
    outcomes = {b: powmod(b, n-1, n) for b in [2,3,5,7,10]}
    print(f"n = {n} (Carmichael): a^(n−1) mod n for small bases →")
    for b,v in outcomes.items():
        print(f"  a={b:<2} → {v}")
    print("All equal 1 — Fermat passes, yet n is composite!")
    print("Gauss’s rigor led beyond tests to *theorems* explaining such phenomena.")

# --------------------------------------------
# (4) REPETITION — orders & cycles; decimal repetends
# --------------------------------------------

def multiplicative_order(a: int, m: int) -> int:
    if gcd(a, m) != 1:
        return 0
    k = 1
    t = a % m
    while t != 1:
        t = (t * a) % m
        k += 1
        if k > m+1: return 0
    return k

def demo_repetition():
    hr("Repetition seen through modulus — cycles, orders, and decimal patterns")
    m = 7
    print(f"Multiplicative orders modulo {m}:")
    for a in range(1, m):
        if gcd(a, m)==1:
            k = multiplicative_order(a, m)
            print(f"  ord_{m}({a}) = {k}")
    print("\nDecimal repetend length of 1/7 equals ord_7(10):")
    rep_len = multiplicative_order(10, 7)
    print(f"  ord_7(10) = {rep_len}  →  1/7 = 0.{''.join(str((10**i//7)%10) for i in range(rep_len))}… (period {rep_len})")
    print("\nModular arithmetic turns repetition into structure (orders, cycles, periods).")

# --------------------------------------------
# (5) SCIENCE — Chinese Remainder Theorem (CRT)
# --------------------------------------------

def crt(congruences):
    """
    Solve x ≡ a_i (mod m_i) for pairwise coprime m_i.
    Returns (x0, M) with x ≡ x0 (mod M).
    """
    M = 1
    for _, m in congruences:
        M *= m
    x = 0
    for a, m in congruences:
        Mi = M // m
        inv = modinv(Mi % m, m)
        x = (x + a * Mi * inv) % M
    return x, M

def demo_science():
    hr("Arithmetic matures into theory — the Chinese Remainder Theorem")
    # A classic puzzle flavored set:
    # Find x such that:
    #   x ≡ 2 (mod 3)
    #   x ≡ 3 (mod 5)
    #   x ≡ 2 (mod 7)
    congr = [(2,3), (3,5), (2,7)]
    x0, M = crt(congr)
    print("System:")
    for a,m in congr:
        print(f"  x ≡ {a} (mod {m})")
    print(f"\nSolution: x ≡ {x0} (mod {M})")
    checks = [x0 % m for _,m in congr]
    print(f"Checks: {[f'{x0} mod {m} = {x0 % m}' for _,m in congr]}")
    print("\nMeaning: from puzzles to principles — Gauss’ program made arithmetic a *science*.")

# --------------------------------------------
# CLI
# --------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Gauss and the Hidden Order — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all","structure","residues","rigor","repetition","science"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Gauss and the Hidden Order — The Birth of Number Theory")
    print("Demos: structure (Z/nZ units), residues (quadratic/Euler), rigor (FLT & 561),")
    print("       repetition (orders/repetends), science (CRT)")
    if args.demo in ("all","structure"):
        demo_structure()
    if args.demo in ("all","residues"):
        demo_residues()
    if args.demo in ("all","rigor"):
        demo_rigor()
    if args.demo in ("all","repetition"):
        demo_repetition()
    if args.demo in ("all","science"):
        demo_science()

if __name__ == "__main__":
    main()
