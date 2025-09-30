#!/usr/bin/env python3
# pebbles.py
#
# 1. Pebbles and Shadows — The First Count
#
# Key Ideas expressed as runnable mini-demos:
#   • Counting arose from need — memory made visible.
#   • Pebbles and marks acted as early symbols.
#   • Representation was a leap: one object could stand for another (bijection).
#   • The first mathematics was about care (inventory, loss), not curiosity.
#   • Abstraction began when humans stepped beyond what they saw (count anything).
#
# No external dependencies. Pure standard library. ASCII visuals.

from __future__ import annotations
import argparse
import itertools
import random
from collections import Counter, deque
from dataclasses import dataclass, field

random.seed(91)

# ---------------------------
# Utilities
# ---------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def render_tally(n: int, group: int = 5) -> str:
    """
    Render n as grouped tally marks (||||/ ||||/ ...)
    Every 'group' items, cross with '/' to make auditing easier at a glance.
    """
    if n <= 0:
        return "∅"
    out = []
    for i in range(1, n+1):
        if i % group == 0:
            out.append("/")  # cross the fifth
        else:
            out.append("|")
        if i % group == 0:
            out.append(" ")  # spacer between groups
    return "".join(out).rstrip()

def unary(n: int) -> str:
    return "│"*n if n > 0 else "∅"

def decimal(n: int) -> str:
    return str(n)

def symbol_cost(s: str) -> int:
    # crude: count visible glyphs (spaces ignored)
    return sum(1 for ch in s if ch != " ")

# ---------------------------
# (1) Pebbles at the Gate: one-to-one matching
# ---------------------------

@dataclass
class PebbleGate:
    """A shepherd places one pebble per sheep as they exit; removes one as they return."""
    name: str = "Shepherd"
    out_pebbles: int = 0
    log: list[str] = field(default_factory=list)

    def sheep_out(self, sheep_id: str) -> None:
        self.out_pebbles += 1
        self.log.append(f"→ Sheep {sheep_id} OUT  | pebbles={self.out_pebbles}")

    def sheep_in(self, sheep_id: str) -> None:
        if self.out_pebbles == 0:
            self.log.append(f"⚠ Sheep {sheep_id} IN but pebbles=0 (recording error)")
        else:
            self.out_pebbles -= 1
            self.log.append(f"← Sheep {sheep_id} IN   | pebbles={self.out_pebbles}")

    def summary(self) -> str:
        if self.out_pebbles == 0:
            return "All sheep accounted for. No pebbles left."
        return f"{self.out_pebbles} pebble(s) remain: missing {self.out_pebbles} sheep."

def demo_gate():
    hr("Pebbles at the Gate — one thing stands for another")
    # Initialize a small flock
    flock = [f"S{i}" for i in range(1, 11)]  # 10 sheep
    gate = PebbleGate()

    # Morning: all go out
    for s in flock:
        gate.sheep_out(s)
    # Day: a few wander independently; one gets lost (S7 never returns)
    returning_order = deque(flock)
    returning_order.remove("S7")  # lost
    random.shuffle(flock)
    random.shuffle(returning_order)

    # Evening: the rest come back in jumbled order
    for s in returned := list(returning_order):
        gate.sheep_in(s)

    # Print log and summary
    for line in gate.log:
        print(line)
    print("--")
    print(gate.summary())
    print("\nInterpretation: the mismatch is visible as leftover pebble(s) — care made visible.")

# ---------------------------
# (2) Tally marks: days and grouping
# ---------------------------

def demo_tally():
    hr("Tally Marks — memory externalized into matter")
    days = 23
    print(f"Days passed: {days}")
    print("Ungrouped (unary):")
    print(unary(days))
    print("\nGrouped tallies (groups of 5):")
    print(render_tally(days, group=5))
    print("\nWhy group? Quick visual audit: each '/' marks five. Count by 5s, then add remainder.")

# ---------------------------
# (3) From gesture to symbol: unary → positional
# ---------------------------

def demo_symbols():
    hr("From Gesture to Symbol — unary vs positional")
    samples = [1, 4, 5, 9, 12, 23, 37, 58]
    print(f"{'n':>4}  {'unary':<20} {'cost':>4}   {'decimal':<8} {'cost':>4}")
    print("-"*50)
    for n in samples:
        u = unary(n)
        d = decimal(n)
        print(f"{n:>4}  {u:<20} {symbol_cost(u):>4}   {d:<8} {symbol_cost(d):>4}")
    print("\nObservation: positional notation compresses memory as quantities grow.")

# ---------------------------
# (4) The first ledger: tokens and reconciliation
# ---------------------------

@dataclass
class PebbleLedger:
    """Token inventory for goods; reconcile tokens with observed events."""
    tokens: Counter[str] = field(default_factory=Counter)
    audit: list[str] = field(default_factory=list)

    def deposit(self, kind: str, qty: int = 1) -> None:
        self.tokens[kind] += qty
        self.audit.append(f"+ {qty} {kind} (tokens now {self.tokens[kind]})")

    def withdraw(self, kind: str, qty: int = 1) -> None:
        self.tokens[kind] -= qty
        self.audit.append(f"- {qty} {kind} (tokens now {self.tokens[kind]})")

    def reconcile(self, observed: dict[str, int]) -> list[str]:
        """Compare token counts to observed world; report differences."""
        report = []
        kinds = set(observed) | set(self.tokens)
        for k in sorted(kinds):
            world = observed.get(k, 0)
            record = self.tokens.get(k, 0)
            if world != record:
                report.append(f"✧ MISMATCH {k}: tokens={record}, world={world}  (Δ={world-record:+})")
        if not report:
            report.append("Ledger matches world.")
        return report

def demo_ledger():
    hr("Pebble Ledger — care before curiosity")
    ledger = PebbleLedger()
    # Morning deposits (stocking)
    ledger.deposit("jar", 7)
    ledger.deposit("loaf", 12)
    ledger.deposit("oil", 3)
    # Day events
    ledger.withdraw("loaf", 2)   # eaten
    ledger.withdraw("oil", 1)    # used
    ledger.deposit("jar", 1)     # found an extra jar

    # Observe world at dusk (actual counts on shelves)
    observed_world = {"jar": 7, "loaf": 10, "oil": 2}

    print("Event log:")
    for line in ledger.audit:
        print(" ", line)
    print("\nReconciliation:")
    for line in ledger.reconcile(observed_world):
        print(" ", line)
    print("\nMeaning: a symbol system lets us *notice* when care requires action.")

# ---------------------------
# (5) Abstraction: counting anything
# ---------------------------

def demo_abstract():
    hr("Abstraction — the same count, different things")
    baskets = {
        "sheep": ["S1", "S2", "S3", "S4"],
        "jars": ["J101", "J102"],
        "days": list(range(1, 11)),
        "names": ["Ana", "Bao", "Chi", "Diep", "Eli"]
    }
    # Strip identity, keep cardinality — a minimal abstraction of "how many"
    cardinalities = {k: len(set(v)) for k, v in baskets.items()}

    for k, v in baskets.items():
        print(f"{k:<6}: items={v}")
    print("--")
    for k, c in cardinalities.items():
        print(f"count({k}) = {c}")

    total = sum(cardinalities.values())
    print(f"\nTotal across categories = {total}")
    print("Insight: counting forgets *what* things are and remembers *how many*.")

# ---------------------------
# CLI
# ---------------------------

def main():
    parser = argparse.ArgumentParser(description="Pebbles and Shadows — runnable micro-demos of first counting.")
    parser.add_argument("--demo",
                        choices=["all", "gate", "tally", "symbols", "ledger", "abstract"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Pebbles and Shadows — The First Count")
    print("Demos: gate (bijection), tally (grouped marks), symbols (unary→positional), ledger (care), abstract (forget identity)")

    if args.demo in ("all", "gate"):
        demo_gate()
    if args.demo in ("all", "tally"):
        demo_tally()
    if args.demo in ("all", "symbols"):
        demo_symbols()
    if args.demo in ("all", "ledger"):
        demo_ledger()
    if args.demo in ("all", "abstract"):
        demo_abstract()

if __name__ == "__main__":
    main()
