#!/usr/bin/env python3
# probability.py
#
# 17. Probability and Uncertainty — Measuring the Unknown
#
# Demos:
#   • structure   : Probability gives structure to randomness (two-dice space, exact vs empirical)
#   • expectation : Expectation links chance with calculation (linearity; game value)
#   • repeated    : Repeated events reveal stable patterns (running means; CLT-ish histogram)
#   • statistics  : Statistics grows from uncertainty (estimate p, Wilson CI; unbiased variance)
#   • decision    : Decision-making as a science of odds (EV vs utility; Kelly fraction)
#
# Pure standard library. ASCII output only.

from __future__ import annotations
import argparse, math, random, statistics
from collections import Counter
from typing import Iterable, List, Tuple

random.seed(1717)

# ------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def ascii_hist(data: Iterable[float], bins: int = 20, width: int = 48) -> str:
    data = list(data)
    if not data: return "(no data)"
    lo, hi = min(data), max(data)
    if lo == hi: hi = lo + 1e-9
    step = (hi - lo) / bins
    counts = [0]*bins
    for x in data:
        k = min(int((x - lo) / step), bins-1)
        counts[k] += 1
    m = max(counts) or 1
    lines = []
    for i, c in enumerate(counts):
        bar = "█" * max(1, int(width * c / m)) if c else ""
        a = lo + i*step
        b = a + step
        lines.append(f"{a:8.3f}–{b:8.3f} | {bar} {c}")
    return "\n".join(lines)

# ------------------------------------------------------------
# (1) STRUCTURE — randomness with structure (two dice)
# ------------------------------------------------------------

def demo_structure():
    hr("Randomness with Structure — two fair dice: exact vs empirical")
    # Sample space & exact distribution for sum S = d1 + d2
    outcomes = [(i,j) for i in range(1,7) for j in range(1,7)]
    sums = [i+j for i,j in outcomes]
    exact = Counter(sums)
    total = 36
    print("Exact probabilities for S = d1 + d2:")
    for s in range(2,13):
        p = exact[s] / total
        print(f"  P(S={s:>2}) = {p:.3f}")
    # Empirical check
    N = 50_000
    emp = Counter(sum((random.randint(1,6), random.randint(1,6))) for _ in range(N))
    print("\nEmpirical frequencies (N=50,000):")
    for s in range(2,13):
        p = emp[s]/N
        print(f"  P̂(S={s:>2}) = {p:.3f}   (err {p - exact[s]/36:+.3f})")
    print("\nMessage: even games of chance carry *structure* — symmetry shapes probability.")

# ------------------------------------------------------------
# (2) EXPECTATION — chance meets calculation
# ------------------------------------------------------------

def demo_expectation():
    hr("Expectation — linking chance to calculation")
    # Expected value of a fair die and of a simple game
    die_ev = sum(k for k in range(1,7))/6
    print(f"E[die] = (1+…+6)/6 = {die_ev:.3f}")

    # Game: roll one fair die. If 6 → +$10; if 1 → −$6; else +$1.
    # EV = 1/6*10 + 1/6*(-6) + 4/6*1
    game_ev = (1/6)*10 + (1/6)*(-6) + (4/6)*1
    print(f"Game payoff EV = {game_ev:.3f} dollars per play")

    # Linearity of expectation, no independence needed:
    # E[aX+bY] = aE[X] + bE[Y]
    print("\nLinearity of expectation (no independence required):")
    print("Let X,Y be two die rolls. E[2X − 3Y] = 2E[X] − 3E[Y] = 2*3.5 − 3*3.5 = −3.5")

    # Waiting time (geometric): flips until first heads (p=0.4)
    p = 0.4
    geo_ev = 1/p
    print(f"Geometric waiting time E[T] for p={p:.1f} → {geo_ev:.2f} flips on average")

    # Empirical confirmation
    trials = 20000
    total_flips = 0
    for _ in range(trials):
        flips = 0
        while True:
            flips += 1
            if random.random() < p:
                break
        total_flips += flips
    print(f"Simulated mean over {trials} trials ≈ {total_flips/trials:.2f}")

# ------------------------------------------------------------
# (3) REPEATED — stability through repetition (LLN & CLT-ish)
# ------------------------------------------------------------

def running_means(p: float, n: int) -> List[float]:
    means = []
    heads = 0
    for k in range(1, n+1):
        if random.random() < p:
            heads += 1
        means.append(heads/k)
    return means

def demo_repeated():
    hr("Repeated Trials — Law of Large Numbers & bell-ish sums")
    # LLN: coin with p=0.6
    p = 0.6
    means = running_means(p, 10_000)
    print(f"Final running mean after 10,000 flips (true p={p}): {means[-1]:.4f}")
    print("First 10 running means:", [f"{m:.2f}" for m in means[:10]])
    print("Last 10 running means :", [f"{m:.4f}" for m in means[-10:]])
    print("\nCentral tendency emerges: randomness shows a stable *average*.")

    # CLT-ish: sum of 12 Uniform(0,1) ≈ Normal (Irwin–Hall)
    sums = [sum(random.random() for _ in range(12)) for _ in range(25_000)]
    print("\nHistogram of sums of 12 uniforms (≈ bell curve):")
    print(ascii_hist(sums, bins=24, width=40))

# ------------------------------------------------------------
# (4) STATISTICS — inference from uncertainty
# ------------------------------------------------------------

def wilson_ci(successes: int, n: int, z: float = 1.96) -> Tuple[float,float,float]:
    # Wilson score interval for binomial proportion p with confidence ~95% at z=1.96
    if n == 0: return (float("nan"), float("nan"), float("nan"))
    phat = successes / n
    denom = 1 + z*z/n
    center = (phat + (z*z)/(2*n)) / denom
    half = (z / denom) * math.sqrt(phat*(1-phat)/n + z*z/(4*n*n))
    return phat, max(0.0, center - half), min(1.0, center + half)

def demo_statistics():
    hr("Statistics from Uncertainty — estimate, variability, confidence")
    # Unknown coin bias; observe data:
    n = 400
    p_true = 0.57
    k = sum(1 for _ in range(n) if random.random() < p_true)
    phat, lo, hi = wilson_ci(k, n)
    print(f"Observed k={k} heads out of n={n} flips")
    print(f"Estimate p̂ = {phat:.4f};  Wilson 95% CI ≈ [{lo:.4f}, {hi:.4f}]  (true p={p_true})")

    # Unbiased variance of a sample
    xs = [random.gauss(10, 2.5) for _ in range(200)]
    s2 = statistics.variance(xs)         # sample variance with Bessel's correction
    mu = statistics.mean(xs)
    print(f"\nSample mean ≈ {mu:.3f}, unbiased variance s² ≈ {s2:.3f}")
    print("Inference = turning data + probability into measured belief (intervals, estimates).")

# ------------------------------------------------------------
# (5) DECISION — odds, EV, utility, Kelly
# ------------------------------------------------------------

def kelly_fraction(p: float, b: float) -> float:
    """
    Kelly optimal fraction for a favorable bet:
      Win with prob p, lose with prob q=1-p; win returns b:1 (stake f grows to 1+bf or 1-f).
      f* = (bp - q)/b, clipped to [0,1].
    """
    q = 1 - p
    f = (b*p - q) / b
    return max(0.0, min(1.0, f))

def simulate_kelly(p: float, b: float, n: int = 200, f: float | None = None) -> Tuple[float,float]:
    bankroll = 1.0
    f_star = kelly_fraction(p, b) if f is None else f
    path = []
    for _ in range(n):
        stake = f_star * bankroll
        win = (random.random() < p)
        bankroll = bankroll + (b*stake if win else -stake)
        path.append(bankroll)
    return bankroll, f_star

def demo_decision():
    hr("Decisions by the Numbers — EV, risk, and the Kelly rule")
    # Two choices with same EV but different risk
    print("Choice A: +$3 with prob 0.5 else −$1  → EV = 0.5*3 + 0.5*(−1) = $1")
    print("Choice B: +$10 with prob 0.1 else $0  → EV = 1 as well")
    print("Risk differs: A is steadier; B is spikier. Utility may prefer A.\n")

    # Kelly sizing for favorable 2:1 bet (b=2) with p=0.6
    p, b = 0.6, 2.0
    f_star = kelly_fraction(p, b)
    print(f"Kelly fraction for p={p}, b={b} → f* = {(f_star*100):.1f}% of bankroll per play")

    # Simulate growth over repeated plays
    terminal, _ = simulate_kelly(p, b, n=200)
    print(f"Simulated bankroll after 200 plays (starting $1) ≈ ${terminal:.2f}")
    print("Lesson: decisions become quantitative — odds, expectations, and growth all computed.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Probability & Uncertainty — runnable micro-demos.")
    ap.add_argument("--demo",
        choices=["all","structure","expectation","repeated","statistics","decision"],
        default="all", help="Which demo to run.")
    args = ap.parse_args()

    print("Probability and Uncertainty — Measuring the Unknown")
    print("Demos: structure (dice law), expectation (EV & linearity), repeated (LLN/CLT),")
    print("       statistics (estimation & CIs), decision (EV/utility/Kelly)")

    if args.demo in ("all","structure"):   demo_structure()
    if args.demo in ("all","expectation"): demo_expectation()
    if args.demo in ("all","repeated"):    demo_repeated()
    if args.demo in ("all","statistics"):  demo_statistics()
    if args.demo in ("all","decision"):    demo_decision()

if __name__ == "__main__":
    main()
