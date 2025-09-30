#!/usr/bin/env python3
# curvature.py
#
# 16. The Geometry of Curvature — Space Bends Thought
#
# Demos:
#   • curved    : Curved spaces extend geometry beyond the plane (spherical triangles)
#   • gauss     : Gauss & Riemann — curvature via geodesic circles (Theorema Egregium vibe)
#   • measure   : Curvature measures departure from flatness (spherical excess ~ area)
#   • intrinsic : Geometry from within — metric, distances, holonomy = area
#   • relativity: Geodesic deviation (neighboring geodesics focus) — seeds of relativity
#
# Pure standard library, ASCII output.

from __future__ import annotations
import argparse, math
from typing import Tuple, List

# -------------------------------
# Utilities: sphere of radius R=1
# -------------------------------

R = 1.0  # unit sphere; Gaussian curvature K = 1/R^2 = 1

def d2r(d: float) -> float: return d*math.pi/180.0
def r2d(r: float) -> float: return r*180.0/math.pi

def sph_to_vec(lat_deg: float, lon_deg: float) -> Tuple[float,float,float]:
    φ = d2r(lat_deg)     # latitude
    λ = d2r(lon_deg)     # longitude
    x = math.cos(φ)*math.cos(λ)
    y = math.cos(φ)*math.sin(λ)
    z = math.sin(φ)
    return (x,y,z)

def clamp(x: float, a: float=-1.0, b: float=1.0) -> float:
    return max(a, min(b, x))

def gc_dist(p: Tuple[float,float,float], q: Tuple[float,float,float]) -> float:
    # central angle between unit vectors
    dot = p[0]*q[0] + p[1]*q[1] + p[2]*q[2]
    return math.acos(clamp(dot))

def spherical_triangle_angles(A_ll, B_ll, C_ll) -> Tuple[float,float,float,float,float,float]:
    # Inputs: (lat,lon) degrees. Returns: sides a,b,c and angles A,B,C in radians.
    A = sph_to_vec(*A_ll); B = sph_to_vec(*B_ll); C = sph_to_vec(*C_ll)
    a = gc_dist(B,C)  # side a opposite vertex A
    b = gc_dist(A,C)
    c = gc_dist(A,B)
    # Spherical law of cosines for angles
    def angle_at(cos_a, cos_b, cos_c, sin_b, sin_c):
        # cos A = (cos a - cos b cos c) / (sin b sin c)
        num = cos_a - cos_b*cos_c
        den = sin_b*sin_c
        return math.acos(clamp(num/den))
    Aang = angle_at(math.cos(a), math.cos(b), math.cos(c), math.sin(b), math.sin(c))
    Bang = angle_at(math.cos(b), math.cos(c), math.cos(a), math.sin(c), math.sin(a))
    Cang = angle_at(math.cos(c), math.cos(a), math.cos(b), math.sin(a), math.sin(b))
    return a,b,c,Aang,Bang,Cang

def spherical_excess(A: float, B: float, C: float) -> float:
    # Girard: E = A + B + C − π = Area/R^2 (for unit sphere, Area = E)
    return A + B + C - math.pi

# Geodesic circle of geodesic radius ρ centered at North Pole has circumference C = 2π sin ρ.
def geodesic_circle_circumference(rho: float) -> float:
    return 2*math.pi*math.sin(rho)

# Metric on unit sphere: ds^2 = dθ^2 + (sin θ)^2 dφ^2  (θ = colatitude)
def small_geodesic_circle_plane_circumference(rho: float) -> float:
    return 2*math.pi*rho  # flat comparison

# -------------------------------
# (1) Curved spaces — spherical triangle angle sum
# -------------------------------

def demo_curved():
    print("\n=== Curved Space: spherical triangle with three right angles ===")
    # Vertices: A = (0°N,   0°E),  B = (0°N, 90°E),  C = (90°N, any) → each angle is 90°
    A_ll = (0.0, 0.0)
    B_ll = (0.0, 90.0)
    C_ll = (90.0, 0.0)
    a,b,c,Aang,Bang,Cang = spherical_triangle_angles(A_ll,B_ll,C_ll)
    Sdeg = r2d(Aang)+r2d(Bang)+r2d(Cang)
    E = spherical_excess(Aang,Bang,Cang)
    print(f"Angles: A≈{r2d(Aang):.1f}°, B≈{r2d(Bang):.1f}°, C≈{r2d(Cang):.1f}°  ⇒  sum ≈ {Sdeg:.1f}°")
    print(f"Spherical excess E = sum − 180° ≈ {Sdeg-180:.1f}°  (Area on unit sphere = E in radians)")
    print("Flat geometry demands 180°. Here we see 270°: space itself is curved.")

# -------------------------------
# (2) Gauss & Riemann — geodesic circles “measure” curvature intrinsically
# -------------------------------

def demo_gauss():
    print("\n=== Geodesic Circles Detect Curvature (intrinsically) ===")
    print("For small geodesic radius ρ on a unit sphere:")
    print("  C_sphere(ρ) = 2π sin ρ  vs  C_plane(ρ) = 2π ρ")
    print("Ratio C_sphere / C_plane ≈ 1 − ρ²/6 + …  (coefficient involves Gaussian curvature K)")
    for rho in [0.1, 0.2, 0.4, 0.8]:
        Csp = geodesic_circle_circumference(rho)
        Cpl = small_geodesic_circle_plane_circumference(rho)
        print(f"ρ={rho:>3.1f} : C_sphere={Csp:8.5f} , C_plane={Cpl:8.5f} , ratio={Csp/Cpl: .6f}")
    print("\nNo rulers outside the surface needed: circumference alone betrays curvature.")
    print("This is the spirit of Gauss’s Theorema Egregium and Riemann’s intrinsic program.")

# -------------------------------
# (3) Curvature as departure — excess scales with area (≈ K·Area)
# -------------------------------

def demo_measure():
    print("\n=== Curvature = Departure from Flatness (excess ~ area) ===")
    # Use a family of spherical triangles shrinking toward the pole:
    # A=(90-α, 0), B=(90-α, β), C=(90°, any) ⇒ small cap; excess ≈ area ≈ K·area (K=1)
    for (alpha_deg, beta_deg) in [(30,60), (20,40), (10,20), (5,10), (2,4)]:
        A_ll = (90-alpha_deg, 0.0)
        B_ll = (90-alpha_deg, beta_deg)
        C_ll = (90.0, 0.0)
        a,b,c,Aang,Bang,Cang = spherical_triangle_angles(A_ll,B_ll,C_ll)
        E = spherical_excess(Aang,Bang,Cang)             # radians
        area = E * R*R                                   # unit sphere: area=E
        print(f"α={alpha_deg:>2}°, β={beta_deg:>2}°  →  excess={E:.6f} rad , area≈{area:.6f}")
    print("\nAs triangles shrink, excess ≈ area (since K=1).")
    print("Flat space would give excess=0 no matter the area.")

# -------------------------------
# (4) Intrinsic geometry — distances & holonomy (no embedding)
# -------------------------------

def great_circle_distance_deg(A_ll, B_ll) -> float:
    A = sph_to_vec(*A_ll); B = sph_to_vec(*B_ll)
    return r2d(gc_dist(A,B))

def demo_intrinsic():
    print("\n=== Intrinsic Geometry — distances & holonomy from within ===")
    A_ll = (0.0, 0.0)
    B_ll = (0.0, 90.0)
    C_ll = (90.0, 0.0)
    # Distances (geodesic/“straightest” on the sphere):
    dAB = great_circle_distance_deg(A_ll,B_ll)
    dBC = great_circle_distance_deg(B_ll,C_ll)
    dCA = great_circle_distance_deg(C_ll,A_ll)
    print(f"Geodesic distances: AB={dAB:.1f}°, BC={dBC:.1f}°, CA={dCA:.1f}° (all along great circles)")

    # Holonomy: if you parallel-transport a tangent vector around the triangle,
    # it rotates by exactly the spherical excess (Gauss–Bonnet on the unit sphere).
    _,_,_,Aang,Bang,Cang = spherical_triangle_angles(A_ll,B_ll,C_ll)
    E = spherical_excess(Aang,Bang,Cang)   # radians
    print(f"Parallel transport around triangle rotates a vector by E ≈ {r2d(E):.1f}°.")
    print("This rotation is *intrinsic*; it depends only on the surface’s geometry, not the ambient space.")

# -------------------------------
# (5) Toward relativity — geodesic deviation (focusing on a sphere)
# -------------------------------

def demo_relativity():
    print("\n=== Geodesic Deviation — neighboring “straight lines” converge on a sphere ===")
    # Two meridians separated by Δλ start at the equator and head north; separation shrinks like s(θ)=R·Δλ·cos(latitude)=R·Δλ·sin(colatitude).
    Δλ = d2r(10.0)  # 10° longitude separation
    print("Latitude   separation along parallel (arc length)")
    for lat in [0, 15, 30, 45, 60, 75, 89]:
        φ = d2r(lat)
        s = math.cos(φ) * Δλ * R   # arc length along circle of latitude = R cosφ * Δλ
        print(f"{lat:>3}°       s≈{s:.6f} (radians)")
    print("\nIn flat space, parallel straight lines stay at constant distance.")
    print("Here they *focus* and meet at the pole — a manifestation of positive curvature.")
    print("In General Relativity, mass/energy curves spacetime and geodesics of free fall focus likewise.")
    print("The conceptual groundwork (intrinsic curvature, geodesics, deviation) comes from Gauss/Riemann.")

# -------------------------------
# CLI
# -------------------------------

def main():
    p = argparse.ArgumentParser(description="The Geometry of Curvature — runnable micro-demos.")
    p.add_argument("--demo",
                   choices=["all","curved","gauss","measure","intrinsic","relativity"],
                   default="all", help="Which demo to run.")
    args = p.parse_args()

    print("The Geometry of Curvature — Space Bends Thought")
    print("Demos: curved (spherical triangles), gauss (geodesic circles), measure (excess~area),")
    print("       intrinsic (distances & holonomy), relativity (geodesic deviation)")

    if args.demo in ("all","curved"):     demo_curved()
    if args.demo in ("all","gauss"):      demo_gauss()
    if args.demo in ("all","measure"):    demo_measure()
    if args.demo in ("all","intrinsic"):  demo_intrinsic()
    if args.demo in ("all","relativity"): demo_relativity()

if __name__ == "__main__":
    main()
