#!/usr/bin/env python3
# noneuclidean.py
#
# 19. Non-Euclidean Spaces — Parallel Worlds of Geometry
#
# Demos:
#   • axiom     : Change one axiom → new geometries (parallel postulate variants)
#   • logic     : Logical consistency via concrete models (sphere, Poincaré disk)
#   • product   : Geometry as definition, not destiny (axioms shape worlds)
#   • curvature : Compare triangles across curvatures (sum <,=,> 180°)
#   • relativity: Curved geometry anticipates relativity (geodesics bend light)
#
# Pure standard library, ASCII output.

from __future__ import annotations
import argparse, math

# ------------------------------------------------------------
# (1) Change one axiom → new worlds
# ------------------------------------------------------------

def demo_axiom():
    print("\n=== Parallel Postulate Variants — One Change, Three Worlds ===")
    table = [
        ("Euclidean",    "Exactly one line through a point not on a given line is parallel."),
        ("Hyperbolic",   "At least two distinct lines through the point are parallel."),
        ("Elliptic",     "No line through the point is parallel (all lines meet)."),
    ]
    for name, postulate in table:
        print(f"\n{name} geometry:")
        print(f"  {postulate}")
    print("\nParallelism, once assumed, becomes optional — and each choice builds a consistent cosmos.")
    print("Mathematics learns: laws can vary; truth can branch.")

# ------------------------------------------------------------
# (2) Consistency via concrete models (spherical / hyperbolic)
# ------------------------------------------------------------

def demo_logic():
    print("\n=== Consistency by Model — Geometry as Logical System ===")
    print("• **Spherical model**: points on a sphere, lines = great circles.")
    print("   All lines (great circles) meet ⇒ no parallels ⇒ elliptic geometry.")
    print("• **Poincaré disk model**: points inside unit circle, lines = arcs orthogonal to boundary.")
    print("   Infinitely many parallels through a point ⇒ hyperbolic geometry.")
    print("\nEach satisfies Euclid’s first 4 postulates, differs on the 5th.")
    print("Thus non-Euclidean systems are *logically consistent* — real by model, not by intuition.")

# ------------------------------------------------------------
# (3) Geometry as product of definition, not destiny
# ------------------------------------------------------------

def demo_product():
    print("\n=== Geometry is Definition, not Destiny ===")
    axioms = [
        "1. Two points determine a line.",
        "2. Lines extend indefinitely.",
        "3. Circles exist with any center and radius.",
        "4. All right angles are equal.",
        "5. Parallel postulate — choose your own adventure.",
    ]
    for ax in axioms:
        print(" ", ax)
    print("\nKeep 1–4, alter 5 → new consistent geometries.")
    print("Geometry becomes *synthetic*: a structure born of thought, not dictated by nature.")
    print("Euclid described one world; reason can describe many.")

# ------------------------------------------------------------
# (4) Compare curvatures — triangle angle sums
# ------------------------------------------------------------

def triangle_sums(K: float, a: float) -> float:
    """
    Given constant curvature K and triangle side length a (same on all sides, small),
    return approximate sum of angles (radians) via spherical / hyperbolic excess formula.
    For small a, excess ≈ K * Area; Area ≈ (√3/4) a²
    Flat (K=0): sum = π.
    """
    area = (math.sqrt(3)/4) * a*a
    return math.pi + K * area

def demo_curvature():
    print("\n=== Triangle Angle Sum across Curvatures ===")
    print("Equilateral triangle with side a=1 (small), curvature K = +1, 0, -1:")
    a = 1.0
    cases = [("Spherical (K=+1)", 1.0),
             ("Euclidean (K=0)",  0.0),
             ("Hyperbolic (K=-1)",-1.0)]
    for name, K in cases:
        sumang = triangle_sums(K, a)
        deg = math.degrees(sumang)
        print(f"  {name:<20}: angle sum ≈ {sumang:.4f} rad = {deg:.2f}°")
    print("\nPositive curvature ⇒ excess (>180°), Negative ⇒ deficit (<180°).")
    print("Flatness is a special case, not a necessity.")

# ------------------------------------------------------------
# (5) From geometry to relativity
# ------------------------------------------------------------

def demo_relativity():
    print("\n=== From Geometry to Relativity ===")
    print("Riemann’s insight: curvature need not live on surfaces — it can live in spacetime.")
    print("Einstein took geometry from map to cosmos:")
    print("  • Mass bends spacetime (positive curvature).")
    print("  • Light follows geodesics, curving near stars.")
    print("  • Gravity = geometry, not force.")
    print("\nNon-Euclidean geometry made it thinkable that:")
    print("  ‘Straight lines’ (geodesics) can meet again,")
    print("  and the universe itself can possess shape.")
    print("What began as logic became a theory of reality.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Non-Euclidean Spaces — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all","axiom","logic","product","curvature","relativity"],
                        default="all", help="Which demo to run.")
    args = parser.parse_args()

    print("Non-Euclidean Spaces — Parallel Worlds of Geometry")
    print("Demos: axiom (change postulate), logic (models), product (axioms),")
    print("       curvature (triangle sums), relativity (spacetime curvature)")

    if args.demo in ("all","axiom"):     demo_axiom()
    if args.demo in ("all","logic"):     demo_logic()
    if args.demo in ("all","product"):   demo_product()
    if args.demo in ("all","curvature"): demo_curvature()
    if args.demo in ("all","relativity"):demo_relativity()

if __name__ == "__main__":
    main()
