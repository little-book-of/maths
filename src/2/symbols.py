#!/usr/bin/env python3
# symbols.py
#
# 2. Symbols of the Invisible — Writing Number
#
# Key Ideas as runnable demos:
#   • Writing preserves thought beyond memory (record vs. ephemeral state).
#   • Early systems: tallies, cuneiform-like sexagesimal, Egyptian additive numerals.
#   • Writing supports trade/law via persistent ledgers.
#   • Symbols make number independent of what is counted (same quantity, many scripts/bases).
#   • Written numerals gain new power (checksums / reliable identifiers).
#
# Pure standard library. ASCII renderers.

from __future__ import annotations
import argparse
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def save_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ------------------------------------------------------------
# (1) Record vs. Memory — Writing makes thought persistent
# ------------------------------------------------------------

class EphemeralCounter:
    def __init__(self) -> None:
        self.count = 0
    def tick(self, n: int = 1) -> None:
        self.count += n

TABLET_PATH = "tablet.txt"

def demo_record():
    hr("Record vs. Memory — a written 'tablet' outlives the counter")
    # Memory-only counter
    mem = EphemeralCounter()
    for _ in range(7): mem.tick()
    print(f"Ephemeral counter (in RAM): {mem.count}")

    # Now “write number”: persist to a 'clay tablet' (file)
    number = mem.count
    tablet = {"mark": number, "note": "Jars of grain counted at dusk"}
    save_text(TABLET_PATH, json.dumps(tablet, ensure_ascii=False, indent=2))
    print(f"Written to tablet: {TABLET_PATH}")

    # Simulate loss of memory (new process / object)
    mem2 = EphemeralCounter()
    print(f"New counter starts blank: {mem2.count}")

    # Read the tablet back
    restored = json.loads(load_text(TABLET_PATH))
    print("Tablet read:", restored)
    print("Meaning: the sign keeps the thought even when the thinker changes.")

# ------------------------------------------------------------
# (2) Early Numeral Systems — Tallies, Cuneiform, Egyptian
# ------------------------------------------------------------

def render_tallies(n: int, group: int = 5) -> str:
    if n <= 0: return "∅"
    out = []
    for i in range(1, n+1):
        out.append("/" if i % group == 0 else "|")
        if i % group == 0: out.append(" ")
    return "".join(out).rstrip()

# Sumerian/Babylonian sexagesimal (base 60) used two basic cuneiform digit shapes (1..9 and 10..50).
# We’ll approximate with ASCII symbols: ◇ for units, △ for tens.
# A sexagesimal number is a list of base-60 digits.
def to_sexagesimal(n: int) -> List[int]:
    if n == 0: return [0]
    digits = []
    while n > 0:
        digits.append(n % 60)
        n //= 60
    return list(reversed(digits))

def render_cuneiform_digit(d: int) -> str:
    if d == 0: return "·"
    tens, ones = divmod(d, 10)
    return "△"*tens + "◇"*ones

def render_cuneiform(n: int) -> str:
    digits = to_sexagesimal(n)
    return "  :  ".join(render_cuneiform_digit(d) for d in digits)

# Egyptian additive numerals (Old Kingdom style) had separate glyphs for 1, 10, 100, 1_000, ...
# We’ll approximate: 1=𓏺, 10=𓎆, 100=𓍢, 1_000=𓆼, 10_000=𓂭, 100_000=𓆐, 1_000_000=𓁨 (ASCII fallbacks if console lacks glyphs).
EGYPTIAN_MAP: List[Tuple[int, str]] = [
    (1_000_000, "𓁨"), (100_000, "𓆐"), (10_000, "𓂭"),
    (1_000, "𓆼"), (100, "𓍢"), (10, "𓎆"), (1, "𓏺")
]
EGYPTIAN_FALLBACK: List[Tuple[int, str]] = [
    (1_000_000, "M~"), (100_000, "R~"), (10_000, "F~"),
    (1_000, "L~"), (100, "C~"), (10, "X~"), (1, "I")
]

def render_egyptian(n: int, fallback: bool = False) -> str:
    glyphs = EGYPTIAN_FALLBACK if fallback else EGYPTIAN_MAP
    out = []
    for value, mark in glyphs:
        k, n = divmod(n, value)
        out.append(mark * k)
    s = "".join(out)
    return s if s else "∅"

def demo_numerals():
    hr("Early Numeral Systems — tallies, cuneiform-style base-60, Egyptian additive")
    samples = [0, 4, 5, 12, 23, 60, 73, 202, 1337, 2024]

    print(f"{'n':>6}  {'tallies':<20}  {'sexagesimal (cuneiform-ish)':<30}  {'Egyptian':<20}")
    print("-"*90)
    for n in samples:
        tall = render_tallies(n)
        sex  = render_cuneiform(n)
        egy  = render_egyptian(n, fallback=True)
        print(f"{n:>6}  {tall:<20}  {sex:<30}  {egy:<20}")

    print("\nNotes:")
    print("  • Tallies show counting as repeated mark; groups help quick reading.")
    print("  • Sexagesimal groups by 60; each 'place' is base-60 (echoes modern time: 60s, 60m).")
    print("  • Egyptian is additive: repeat symbols by value. Shape carries meaning beyond count.")

# ------------------------------------------------------------
# (3) Trade & Law — a tiny written ledger
# ------------------------------------------------------------

@dataclass
class Entry:
    account: str
    delta: int          # positive for credit/add, negative for debit/remove
    memo: str = ""

@dataclass
class Ledger:
    entries: List[Entry] = field(default_factory=list)

    def post(self, account: str, delta: int, memo: str = "") -> None:
        self.entries.append(Entry(account, delta, memo))

    def balance(self) -> Dict[str, int]:
        bal: Dict[str, int] = {}
        for e in self.entries:
            bal[e.account] = bal.get(e.account, 0) + e.delta
        return bal

    def render(self) -> str:
        lines = ["ACCOUNT        Δ        MEMO", "-----------------------------"]
        for e in self.entries:
            lines.append(f"{e.account:<12} {e.delta:>4}     {e.memo}")
        lines.append("-----------------------------")
        bal = self.balance()
        for k in sorted(bal):
            lines.append(f"{k:<12} = {bal[k]}")
        return "\n".join(lines)

def demo_trade():
    hr("Trade & Law — recording transactions enables verification")
    L = Ledger()
    # Morning stock
    L.post("grain_jars", +12, "Stocked")
    L.post("oil_jugs",  +4,  "Stocked")
    # Midday trades
    L.post("grain_jars", -3,  "Sold to caravan #17")
    L.post("oil_jugs",  -1,  "Temple offering")
    L.post("grain_jars", +2,  "Purchased from farmer A")
    # Evening audit
    print(L.render())
    print("\nMeaning: writing stabilizes agreements across time—trade and rule rely on records.")

# ------------------------------------------------------------
# (4) Independence of Symbols — same number, many scripts/bases
# ------------------------------------------------------------

ROMAN_DIGITS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
]

def to_roman(n: int) -> str:
    if not (0 < n < 4000): return "(out of range)"
    s = []
    for val, sym in ROMAN_DIGITS:
        k, n = divmod(n, val)
        s.append(sym * k)
    return "".join(s)

def to_base(n: int, b: int) -> str:
    assert 2 <= b <= 36
    if n == 0: return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = []
    m = n
    while m > 0:
        m, r = divmod(m, b)
        out.append(digits[r])
    return "".join(reversed(out))

def demo_independence():
    hr("Independence of Symbols — the sign is not the thing")
    n = 2025
    representations = {
        "decimal": str(n),
        "binary": to_base(n, 2),
        "sexagesimal (place values)": ":".join(map(lambda d: f"{d:02d}", to_sexagesimal(n))),
        "roman": to_roman(n),
        "egyptian (fallback)": render_egyptian(n, fallback=True),
        "cuneiform-ish": render_cuneiform(n),
    }
    for name, rep in representations.items():
        print(f"{name:<24} → {rep}")
    print("\nObservation: the *quantity* is invariant; the *script* is conventional.")
    print("Writing frees number from the objects it counts.")

# ------------------------------------------------------------
# (5) Power of Writing — checksums (Luhn) for reliable identifiers
# ------------------------------------------------------------

def luhn_checksum(digits: str) -> int:
    """Compute Luhn checksum digit for a numeric string (without the check digit)."""
    s = 0
    flip = True
    for ch in reversed(digits):
        d = ord(ch) - 48
        if flip:
            d *= 2
            if d > 9: d -= 9
        s += d
        flip = not flip
    return (10 - (s % 10)) % 10

def luhn_verify(number: str) -> bool:
    body, check = number[:-1], number[-1]
    return luhn_checksum(body) == (ord(check) - 48)

def demo_power():
    hr("Power of Writing — from numerals to reliable reference")
    base_id = "57204193"         # suppose: merchant account id
    check = luhn_checksum(base_id)
    full = base_id + str(check)
    print(f"Assigned ID with Luhn check: {full}")

    # Copying error demo (transposed digits)
    typo = "57240193" + str(check)  # swapped 20 → 02 in the body
    ok = luhn_verify(full)
    bad = luhn_verify(typo)
    print(f"Verify {full}: {ok}")
    print(f"Verify {typo}: {bad}")
    print("\nMeaning: once numbers are written, we can *compute on the sign itself*")
    print("to detect/correct human error—new powers born of writing.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Symbols of the Invisible — writing number as runnable demos.")
    parser.add_argument("--demo",
                        choices=["all", "record", "numerals", "trade", "independence", "power"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Symbols of the Invisible — Writing Number")
    print("Demos: record (persistence), numerals (early scripts), trade (ledger), independence (many scripts), power (checksums)")

    if args.demo in ("all", "record"):
        demo_record()
    if args.demo in ("all", "numerals"):
        demo_numerals()
    if args.demo in ("all", "trade"):
        demo_trade()
    if args.demo in ("all", "independence"):
        demo_independence()
    if args.demo in ("all", "power"):
        demo_power()

if __name__ == "__main__":
    main()
