#!/usr/bin/env python3
# geometry.py
#
# 4. Geometry and the Divine — Measuring Heaven and Earth
#
# Demos:
#   • surveying   : Rope-stretchers, right angles (3–4–5), and land area (shoelace)
#   • proportion  : Similar triangles (gnomon & pyramid-shadow height)
#   • shapes      : Meaning in form — square vs. circle (same perimeter, different area)
#   • order       : From observation to order — fit a circle from noisy boundary points
#   • ritual      : Cardinal alignment by the "equal shadows" method (E–W, then N–S)
#
# Pure standard library. ASCII output only.

from __future__ import annotations
import argparse
import math
import random
from dataclasses import dataclass
from typing import Iterable, List, Tuple

random.seed(404)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def hr(title: str) -> None:
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

Point = Tuple[float, float]

def dist(a: Point, b: Point) -> float:
    return math.hypot(a[0]-b[0], a[1]-b[1])

def shoelace_area(poly: List[Point]) -> float:
    """Polygon area (positive for CCW)."""
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        s += x1*y2 - x2*y1
    return abs(s) / 2.0

# ------------------------------------------------------------
# (1) SURVEYING — rope, right angles, and land area
# ------------------------------------------------------------

def demo_surveying():
    hr("Surveying — rope-stretchers, right angles, land as number")

    print("Rope with 12 equal knots → 3–4–5 triangle makes a right angle:")
    print("""
        knots: *---*---*   (3)
               |       \\
               |        \\
               *---*---*---*---*   (5)
               (4)
    """.rstrip())

    # Verify 3-4-5 is right via Pythagoras
    a, b, c = 3.0, 4.0, 5.0
    lhs = a*a + b*b
    rhs = c*c
    print(f"Check: 3^2 + 4^2 = {lhs:.1f}, 5^2 = {rhs:.1f}  → right angle ✓")

    # A farmer’s irregular field (surveyed points walking the boundary)
    field = [(0,0), (8,0), (9,2), (7,5), (3,6), (1,3)]
    A = shoelace_area(field)
    perim = sum(dist(field[i], field[(i+1)%len(field)]) for i in range(len(field)))
    print("\nIrregular plot vertices:", field)
    print(f"Perimeter ≈ {perim:.2f} units")
    print(f"Area by shoelace ≈ {A:.2f} square units")

    print("\nMeaning: with a rope and stakes we tame the landscape;")
    print("         lines, angles, and areas turn place into plan.")

# ------------------------------------------------------------
# (2) PROPORTION — similar triangles (gnomon & pyramid)
# ------------------------------------------------------------

def gnomon_height(stick_h: float, stick_shadow: float, pyramid_shadow: float) -> float:
    # Similar triangles: stick_h / stick_shadow = pyramid_h / pyramid_shadow
    return stick_h * (pyramid_shadow / stick_shadow)

def demo_proportion():
    hr("Proportion — heaven and earth in similar triangles")

    stick_h = 1.8      # meters (gnomon height)
    stick_shadow = 2.4 # meters (measured)
    pyramid_shadow = 128.0 # meters (measured at the same moment)
    H = gnomon_height(stick_h, stick_shadow, pyramid_shadow)

    print(f"Gnomon: stick {stick_h} m casts {stick_shadow} m shadow.")
    print(f"Monument shadow: {pyramid_shadow} m at the same time.")
    print(f"Estimated monument height ≈ {H:.2f} m")

    print("""
          sun
           ☼
            \\   /|
             \\ / |  height = H
              *  |    
                 |      (similar triangles)
          -----shadow-------
            s    S
    """.rstrip())

    print("Idea: the sky sets the ratio; proportion unites the near and the far.")

# ------------------------------------------------------------
# (3) SHAPES — square vs circle, same perimeter, different area
# ------------------------------------------------------------

def demo_shapes():
    hr("Shapes — stability, eternity, and efficiency")

    P = 40.0  # same perimeter for both shapes
    # Square: side = P/4, area = s^2
    s = P/4.0
    area_square = s*s
    # Circle: circumference = P = 2πr ⇒ r = P/(2π); area = πr^2
    r = P/(2*math.pi)
    area_circle = math.pi*r*r

    print(f"Perimeter fixed at {P:.1f} units.")
    print(f"Square: side={s:.2f}, area≈{area_square:.2f}")
    print(f"Circle: radius={r:.2f}, area≈{area_circle:.2f}")
    eff = area_circle/area_square
    print(f"Area(circle)/Area(square) ≈ {eff:.3f}")

    print("""
    Square → stability (axes, corners, grids)
    +--------+
    |        |
    |        |
    +--------+

    Circle → eternity (no beginning, no end)
        *****
      **     **
     *         *
      **     **
        *****
    """.rstrip())

    print("Lesson: with the same boundary, the circle encloses the most area —")
    print("        a whisper of optimality that made the circle a symbol of the infinite.")

# ------------------------------------------------------------
# (4) ORDER — fit a circle from noisy points (observation → law)
# ------------------------------------------------------------

def fit_circle_kasa(points: Iterable[Point]) -> Tuple[Point, float]:
    """
    Kåsa least-squares fit to x^2 + y^2 + A x + B y + C = 0.
    Returns (center, radius).
    """
    xs, ys = zip(*points)
    Sx  = sum(xs);  Sy  = sum(ys)
    Sxx = sum(x*x for x in xs)
    Syy = sum(y*y for y in ys)
    Sxy = sum(x*y for x, y in points)
    Sxz = sum((x*x + y*y)*x for x, y in points)
    Syz = sum((x*x + y*y)*y for x, y in points)
    n   = float(len(list(points)))  # careful: points was consumed above if not list
    # Recompute as list to avoid iterator exhaustion:
    pts = list(points) if not isinstance(points, list) else points
    if not isinstance(points, list):
        xs, ys = zip(*pts)
        Sx  = sum(xs);  Sy  = sum(ys)
        Sxx = sum(x*x for x in xs)
        Syy = sum(y*y for y in ys)
        Sxy = sum(x*y for x, y in pts)
        Sxz = sum((x*x + y*y)*x for x, y in pts)
        Syz = sum((x*x + y*y)*y for x, y in pts)
        n   = float(len(pts))

    # Solve the normal equations for A,B,C
    # | Sxx  Sxy  Sx | |A| = | -Sxz |
    # | Sxy  Syy  Sy | |B|   | -Syz |
    # | Sx   Sy   n  | |C|   | -(Sxx+Syy) |
    M = [
        [Sxx, Sxy, Sx],
        [Sxy, Syy, Sy],
        [Sx,  Sy,  n ]
    ]
    b = [-Sxz, -Syz, -(Sxx + Syy)]

    # Solve 3x3 linear system (Cramer's rule or small Gaussian elimination)
    def det3(M):
        return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
              - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
              + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
    D = det3(M)
    if abs(D) < 1e-12:
        raise ValueError("Degenerate point configuration for circle fit.")
    # Replace columns with b to get determinants
    def replace_col(M, col, vec):
        N = [row[:] for row in M]
        for i in range(3):
            N[i][col] = vec[i]
        return N
    A = det3(replace_col(M, 0, b))/D
    B = det3(replace_col(M, 1, b))/D
    C = det3(replace_col(M, 2, b))/D

    cx, cy = -A/2.0, -B/2.0
    r = math.sqrt(max(cx*cx + cy*cy - C, 0.0))
    return (cx, cy), r

def demo_order():
    hr("Observation → Order — a circle behind noisy stones")

    # True circle
    true_center = (12.0, 7.0)
    true_r = 5.0

    # Surveyed boundary stones (noisy)
    pts: List[Point] = []
    for k in range(18):
        theta = 2*math.pi*k/18
        x = true_center[0] + true_r*math.cos(theta) + random.gauss(0, 0.15)
        y = true_center[1] + true_r*math.sin(theta) + random.gauss(0, 0.15)
        pts.append((x, y))

    est_center, est_r = fit_circle_kasa(pts)

    print("Measured points (first five):", [tuple(round(v,2) for v in p) for p in pts[:5]], "...")
    print(f"Estimated center ≈ ({est_center[0]:.2f}, {est_center[1]:.2f})  (true {true_center})")
    print(f"Estimated radius ≈ {est_r:.2f}                         (true {true_r})")
    print("\nSense: geometry takes scattered observations and reveals a hidden form.")

# ------------------------------------------------------------
# (5) RITUAL — equal-shadows method for East–West, then North–South
# ------------------------------------------------------------

def equal_shadows_steps(stick_h: float, sun_alt: float, sun_decl: float) -> List[str]:
    """
    We don't simulate astronomy precisely; we show the geometric ritual steps.
    sun_alt/decl are placeholders to keep the interface suggestive.
    """
    steps = [
        "1) Plant a vertical stick (gnomon) on level ground.",
        "2) Draw a circle on the ground centered at the stick's base.",
        "3) Mark the point where the tip of the morning shadow crosses the circle.",
        "4) In the afternoon, mark where the tip crosses the circle again.",
        "5) Connect the two circle marks → an East–West line (equal-shadow principle).",
        "6) Draw a perpendicular through the stick's base → North–South line.",
        "7) Align building axes to these lines; lay out the sacred rectangle/square."
    ]
    return steps

def demo_ritual():
    hr("Ritual of Alignment — science and spirit in one act")

    steps = equal_shadows_steps(stick_h=2.0, sun_alt=40.0, sun_decl=10.0)
    for s in steps:
        print(s)

    print("""
           morning shadow •             • afternoon shadow
                          \\             /
                           \\           /
                            \\         /
                             \\       /
                               (•)  ← gnomon base
                   ⟲ drawn circle —— circle boundary
                    E———————————————W   (equal-shadow chord)
                               |
                               |  ⟂
                               |
                               N
    """.rstrip())

    print("Meaning: measurement and meaning meet—orientation binds the work of hands")
    print("         to the rhythm of sky and season.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Geometry and the Divine — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all", "surveying", "proportion", "shapes", "order", "ritual"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Geometry and the Divine — Measuring Heaven and Earth")
    print("Demos: surveying (3–4–5 & area), proportion (gnomon), shapes (square vs circle),")
    print("       order (fit circle), ritual (equal shadows → E–W, then N–S)")

    if args.demo in ("all", "surveying"):
        demo_surveying()
    if args.demo in ("all", "proportion"):
        demo_proportion()
    if args.demo in ("all", "shapes"):
        demo_shapes()
    if args.demo in ("all", "order"):
        demo_order()
    if args.demo in ("all", "ritual"):
        demo_ritual()

if __name__ == "__main__":
    main()
