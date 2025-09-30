#!/usr/bin/env python3
# descartes.py
#
# 11. Descartes’ Grid — Merging Shape and Symbol
#
# Demos:
#   • plane   : The coordinate plane joins geometry with algebra (axes, distance)
#   • curves  : Points↔equations — parabola y=x^2 and circle x^2+y^2=r^2 (ASCII plot)
#   • solve   : Visual problems solved symbolically (line through two points; intersection)
#   • motion  : Geometry describes motion & change (parametric paths)
#   • abstract: Mathematics both spatial & abstract (linear transforms: rotate/scale/translate)
#
# Pure standard library. ASCII rendering only.

from __future__ import annotations
import argparse
import math
from typing import Iterable, List, Tuple, Callable, Optional

Point = Tuple[float, float]

# ------------------------------------------------------------
# ASCII plotting helpers
# ------------------------------------------------------------

def plot_points_ascii(points: Iterable[Point],
                      x_range=(-10, 10), y_range=(-10, 10),
                      width=61, height=25,
                      axes=True, mark='•') -> str:
    """
    Render a scatter of points into an ASCII grid with optional axes.
    (0,0) is centered; y increases upwards.
    """
    xmin, xmax = x_range
    ymin, ymax = y_range
    W, H = width, height
    grid = [[' ' for _ in range(W)] for _ in range(H)]

    def to_grid(p: Point) -> Optional[Tuple[int,int]]:
        x, y = p
        if x < xmin or x > xmax or y < ymin or y > ymax:
            return None
        gx = int(round((x - xmin) / (xmax - xmin) * (W - 1)))
        gy = int(round((ymax - y) / (ymax - ymin) * (H - 1)))  # invert y
        return gx, gy

    # axes
    if axes:
        # y=0 horizontal
        if ymin <= 0 <= ymax:
            gy0 = int(round((ymax - 0) / (ymax - ymin) * (H - 1)))
            for x in range(W):
                grid[gy0][x] = '─'
        # x=0 vertical
        if xmin <= 0 <= xmax:
            gx0 = int(round((0 - xmin) / (xmax - xmin) * (W - 1)))
            for y in range(H):
                grid[y][gx0] = '│'
        # origin
        if xmin <= 0 <= xmax and ymin <= 0 <= ymax:
            grid[int(round((ymax - 0) / (ymax - ymin) * (H - 1)))][int(round((0 - xmin) / (xmax - xmin) * (W - 1)))] = '┼'

    # plot points
    for p in points:
        coord = to_grid(p)
        if coord:
            gx, gy = coord
            grid[gy][gx] = mark

    # add border
    top_bottom = '┌' + '─'*(W) + '┐'
    body = ['│' + ''.join(row) + '│' for row in grid]
    return '\n'.join([top_bottom] + body + ['└' + '─'*(W) + '┘'])

def sample_curve(f: Callable[[float], float], x_from: float, x_to: float, n: int) -> List[Point]:
    xs = [x_from + (x_to - x_from)*i/(n-1) for i in range(n)]
    return [(x, f(x)) for x in xs]

def sample_implicit(F: Callable[[float,float], float], x_range, y_range, step=0.1, tol=0.05) -> List[Point]:
    """
    Sample an implicit curve F(x,y)=0 by scanning a grid and recording near-zero points.
    """
    xmin, xmax = x_range; ymin, ymax = y_range
    xs = [xmin + i*step for i in range(int((xmax-xmin)/step)+1)]
    ys = [ymin + j*step for j in range(int((ymax-ymin)/step)+1)]
    pts: List[Point] = []
    for y in ys:
        for x in xs:
            if abs(F(x,y)) <= tol:
                pts.append((x,y))
    return pts

# ------------------------------------------------------------
# (1) PLANE — axes, coordinates, distance
# ------------------------------------------------------------

def distance(p: Point, q: Point) -> float:
    return math.hypot(p[0]-q[0], p[1]-q[1])

def demo_plane():
    print("\n=== Cartesian Plane — joining shape with symbol ===")
    A = (-4, 2)
    B = (5, -3)
    C = (0, 6)
    pts = [A, B, C, (0,0)]
    labels = {"A":A, "B":B, "C":C, "O":(0,0)}
    art = plot_points_ascii(pts, x_range=(-10,10), y_range=(-7,7), width=61, height=21, axes=True, mark='•')
    print(art)
    for name, p in labels.items():
        print(f"{name} = {p}")
    print(f"Distance AB = √((x_B−x_A)^2+(y_B−y_A)^2) = {distance(A,B):.3f}")
    print("A point ↔ a pair of numbers. Geometry becomes data; algebra speaks the picture.")

# ------------------------------------------------------------
# (2) CURVES — parabola & circle as equations
# ------------------------------------------------------------

def demo_curves():
    print("\n=== Points become equations; curves become pictures ===")
    # Parabola y = x^2 (clamped range)
    parabola = sample_curve(lambda x: 0.1*(x**2), -10, 10, 200)
    art1 = plot_points_ascii(parabola, x_range=(-10,10), y_range=(-2,10), width=61, height=21, axes=True, mark='·')
    print("Parabola  y = 0.1 x^2")
    print(art1)

    # Circle x^2 + y^2 = r^2
    r = 5.0
    circle = sample_implicit(lambda x,y: x*x + y*y - r*r, (-6,6), (-6,6), step=0.1, tol=0.05)
    art2 = plot_points_ascii(circle, x_range=(-6,6), y_range=(-6,6), width=61, height=21, axes=True, mark='·')
    print(f"Circle   x^2 + y^2 = {r*r:.0f}")
    print(art2)
    print("Now the eye reads the symbol, and the symbol draws what the eye can see.")

# ------------------------------------------------------------
# (3) SOLVE — visual questions solved symbolically
# ------------------------------------------------------------

def line_through(P: Point, Q: Point) -> Tuple[float,float]:
    """
    Return slope m and intercept b for the line y = m x + b through P, Q (assuming non-vertical).
    """
    (x1,y1),(x2,y2) = P,Q
    if x1 == x2:
        raise ValueError("Vertical line: use x = const form.")
    m = (y2-y1)/(x2-x1)
    b = y1 - m*x1
    return m,b

def intersect_line_circle(m: float, b: float, r: float) -> List[Point]:
    """
    Solve intersection of y = m x + b with x^2 + y^2 = r^2.
    Substitute → x^2 + (mx+b)^2 = r^2 → (1+m^2)x^2 + 2mb x + (b^2 - r^2) = 0
    """
    A = 1 + m*m
    B = 2*m*b
    C = b*b - r*r
    disc = B*B - 4*A*C
    if disc < 0:
        return []
    sqrtD = math.sqrt(disc)
    x1 = (-B + sqrtD)/(2*A)
    x2 = (-B - sqrtD)/(2*A)
    return [(x1, m*x1 + b)] + ([(x2, m*x2 + b)] if abs(x2-x1) > 1e-9 else [])

def demo_solve():
    print("\n=== Solve by symbol what began as a picture ===")
    P = (-3, 1)
    Q = (4, 4)
    m, b = line_through(P, Q)
    print(f"Line through P{P} and Q{Q}: y = {m:.3f} x + {b:.3f}")

    r = 5
    pts = intersect_line_circle(m,b,r)
    if pts:
        print(f"Intersection with circle x^2 + y^2 = {r*r}:")
        for i, (x,y) in enumerate(pts, 1):
            print(f"  Point {i}: ({x:.3f}, {y:.3f})")
        art = plot_points_ascii(pts + [P,Q], x_range=(-6,6), y_range=(-6,6), width=61, height=21, axes=True, mark='•')
        print(art)
    else:
        print("No real intersection.")
    print("Sight gives the question; symbol gives the steps. The two now speak together.")

# ------------------------------------------------------------
# (4) MOTION — parametric paths on the plane
# ------------------------------------------------------------

def parametric_points(xf: Callable[[float], float], yf: Callable[[float], float],
                      t0: float, t1: float, n: int) -> List[Point]:
    ts = [t0 + (t1-t0)*i/(n-1) for i in range(n)]
    return [(xf(t), yf(t)) for t in ts]

def demo_motion():
    print("\n=== Geometry describes motion and change (parametric) ===")
    # Circle motion
    circle = parametric_points(lambda t: 4*math.cos(t), lambda t: 4*math.sin(t), 0, 2*math.pi, 400)
    art1 = plot_points_ascii(circle, x_range=(-5,5), y_range=(-5,5), width=61, height=21, axes=True, mark='·')
    print("Uniform circular motion: x=4 cos t, y=4 sin t")
    print(art1)

    # Lissajous figure: different frequencies (motion as shape)
    lis = parametric_points(lambda t: 5*math.sin(3*t), lambda t: 5*math.sin(2*t), 0, 2*math.pi, 1000)
    art2 = plot_points_ascii(lis, x_range=(-6,6), y_range=(-6,6), width=61, height=21, axes=True, mark='·')
    print("Lissajous (x=5 sin 3t, y=5 sin 2t): motion draws algebra into picture")
    print(art2)

# ------------------------------------------------------------
# (5) ABSTRACT — linear transformations acting on shapes
# ------------------------------------------------------------

def apply_affine(pts: Iterable[Point],
                 A: Tuple[Tuple[float,float], Tuple[float,float]],
                 t: Point=(0.0,0.0)) -> List[Point]:
    """
    Apply x ↦ A x + t to a list of points.
    A = ((a11,a12),(a21,a22)), t = (tx,ty)
    """
    a11,a12 = A[0]; a21,a22 = A[1]
    tx, ty = t
    out: List[Point] = []
    for x,y in pts:
        out.append((a11*x + a12*y + tx, a21*x + a22*y + ty))
    return out

def regular_polygon(n: int, r: float=3.0, phase: float=0.0) -> List[Point]:
    return [(r*math.cos(phase+2*math.pi*k/n), r*math.sin(phase+2*math.pi*k/n)) for k in range(n)] + [(r*math.cos(phase), r*math.sin(phase))]

def demo_abstract():
    print("\n=== Spatial & abstract — matrices as machines on shapes ===")
    square = [(-2,-2), (2,-2), (2,2), (-2,2), (-2,-2)]
    print("Original square (side 4) and its transforms:")
    art0 = plot_points_ascii(square, x_range=(-6,6), y_range=(-6,6), width=61, height=21, axes=True, mark='•')
    print(art0)

    # Scale X by 2 (stretch), Y by 0.5 (squash) → rectangle
    S = ((2.0,0.0),(0.0,0.5))
    rect = apply_affine(square, S)
    print("Scale (x2 in x, ÷2 in y):")
    print(plot_points_ascii(rect, x_range=(-6,6), y_range=(-6,6), width=61, height=21, axes=True, mark='•'))

    # Rotate by 30°
    th = math.radians(30)
    R = ((math.cos(th), -math.sin(th)), (math.sin(th), math.cos(th)))
    rot = apply_affine(square, R)
    print("Rotate by 30°:")
    print(plot_points_ascii(rot, x_range=(-6,6), y_range=(-6,6), width=61, height=21, axes=True, mark='•'))

    # Shear in x (x' = x + 0.6 y)
    Sh = ((1.0, 0.6),(0.0,1.0))
    shear = apply_affine(square, Sh)
    print("Shear (x' = x + 0.6 y):")
    print(plot_points_ascii(shear, x_range=(-6,6), y_range=(-6,6), width=61, height=21, axes=True, mark='•'))

    print("Algebra (matrices) *acts on* geometry (points).")
    print("The same symbols that solve equations also move shapes.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Descartes’ Grid — runnable micro-demos.")
    parser.add_argument("--demo",
                        choices=["all", "plane", "curves", "solve", "motion", "abstract"],
                        default="all",
                        help="Which demo to run.")
    args = parser.parse_args()

    print("Descartes’ Grid — Merging Shape and Symbol")
    print("Demos: plane (axes & distance), curves (parabola/circle), solve (line & intersection),")
    print("       motion (parametric), abstract (linear transforms)")

    if args.demo in ("all", "plane"):
        demo_plane()
    if args.demo in ("all", "curves"):
        demo_curves()
    if args.demo in ("all", "solve"):
        demo_solve()
    if args.demo in ("all", "motion"):
        demo_motion()
    if args.demo in ("all", "abstract"):
        demo_abstract()

if __name__ == "__main__":
    main()
