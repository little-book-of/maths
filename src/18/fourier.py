#!/usr/bin/env python3
# fourier.py
#
# 18. Fourier and the Song of the World — Waves, Heat, and Harmony
#
# Demos:
#   • waves : Complex signals as sums of sinusoids (DFT/IDFT, reconstruction)
#   • link  : Time–frequency link (short-time DFT → ASCII spectrogram)
#   • unify : Heat equation on a string/rod — same eigenmodes as sound (Fourier series)
#   • blocks: Waves as universal building blocks (low-pass filter, keep K coefficients)
#   • modern: 2D DFT on a tiny “image” → sparse frequency keeps the essence
#
# Pure standard library. ASCII output only.

from __future__ import annotations
import argparse, cmath, math, random
from typing import List, Tuple

random.seed(1818)

# ------------------------------------------------------------
# Utilities: DFT / IDFT (naive O(N^2) — fine for small N)
# ------------------------------------------------------------

def dft(x: List[complex]) -> List[complex]:
    N = len(x); X = []
    for k in range(N):
        s = 0j
        for n, xn in enumerate(x):
            s += xn * cmath.exp(-2j*math.pi*k*n/N)
        X.append(s)
    return X

def idft(X: List[complex]) -> List[complex]:
    N = len(X); x = []
    for n in range(N):
        s = 0j
        for k, Xk in enumerate(X):
            s += Xk * cmath.exp(2j*math.pi*k*n/N)
        x.append(s/N)
    return x

def ascii_plot(seq: List[float], width=64, height=15, lo=None, hi=None) -> str:
    if not seq: return "(empty)"
    lo = min(seq) if lo is None else lo
    hi = max(seq) if hi is None else hi
    if hi == lo: hi = lo + 1e-9
    H = height; W = min(width, len(seq))
    idxs = [int(round((x - lo) / (hi - lo) * (H-1))) for x in seq[:W]]
    lines = []
    for r in reversed(range(H)):
        row = ''.join('█' if idxs[c] == r else ('·' if abs(idxs[c]-r)==1 else ' ') for c in range(W))
        lines.append(row)
    axis = '-'*W
    return '\n'.join(lines + [axis])

def top_k_mask(X: List[complex], k: int) -> List[complex]:
    mags = sorted(((abs(v), i) for i, v in enumerate(X)), reverse=True)
    keep = set(i for _, i in mags[:k])
    return [X[i] if i in keep else 0j for i in range(len(X))]

# ------------------------------------------------------------
# (1) WAVES — any (nice) signal as a sum of sinusoids
# ------------------------------------------------------------

def make_signal(N=128) -> List[float]:
    t = [n/N for n in range(N)]
    # Sum of three tones + a small chirp
    sig = [1.2*math.sin(2*math.pi*5*ti) +
           0.8*math.sin(2*math.pi*12*ti + 0.7) +
           0.5*math.sin(2*math.pi*21*ti) +
           0.3*math.sin(2*math.pi*(6 + 4*ti)*ti)   # gentle chirp
           for ti in t]
    # light noise
    sig = [s + 0.05*(2*random.random()-1) for s in sig]
    return sig

def demo_waves():
    print("\n=== Complex signal → sum of waves (DFT) ===")
    x = make_signal(N=128)
    print("Time-domain (first 64 samples):")
    print(ascii_plot(x[:64], width=64, height=12))
    X = dft([complex(v, 0.0) for v in x])
    mags = [abs(v) for v in X]
    # Only show first half (real signal symmetry)
    half = mags[:len(mags)//2]
    print("\nFrequency magnitudes |k| (bins 0 … N/2):")
    print(ascii_plot(half, width=min(64,len(half)), height=12, lo=0, hi=max(half)*1.01))
    # Reconstruct from top K frequencies
    for K in (6, 12, 24):
        Xk = top_k_mask(X, K)
        xr = [v.real for v in idft(Xk)]
        err = math.sqrt(sum((a-b)**2 for a,b in zip(x, xr))/len(x))
        print(f"\nReconstruction with top K={K} Fourier bins (RMS error ≈ {err:.3f}):")
        print(ascii_plot(xr[:64], width=64, height=10))

    print("\nMoral: the messy curve is a chord of pure waves — arithmetic under the noise.")

# ------------------------------------------------------------
# (2) LINK — time, space, frequency (tiny STFT spectrogram)
# ------------------------------------------------------------

def window(seq: List[float], w: int, hop: int) -> List[List[float]]:
    out=[]; i=0
    while i+w <= len(seq):
        out.append(seq[i:i+w])
        i += hop
    return out

def demo_link():
    print("\n=== Time ↔ Frequency (Short-Time Fourier Transform) ===")
    x = make_signal(N=256)
    W, HOP = 64, 16
    frames = window(x, W, HOP)
    # Compute dominant frequency bin per frame
    rows = []
    for fr in frames:
        X = dft([complex(v,0) for v in fr])
        mags = [abs(c) for c in X[:W//2]]
        k = max(range(len(mags)), key=lambda i: mags[i])
        rows.append(k)
    # Render as ASCII spectrogram (rows = time frames, cols = freq bins coarse-bucketed)
    F = W//2
    B = 32
    bucket = lambda k: min(B-1, int(k/(F)*B))
    grid = [[' ']*B for _ in range(len(rows))]
    for t,k in enumerate(rows):
        grid[t][bucket(k)] = '█'
    print("Time → (rows),  Frequency → (columns)\n")
    for r in grid:
        print(''.join(r))
    print("\nWe see the changing pitch content over time — one signal, two views that agree.")

# ------------------------------------------------------------
# (3) UNIFY — heat equation via Fourier series (same modes as sound)
# ------------------------------------------------------------

def heat_series(x: float, t: float, N: int = 50, alpha: float = 1.0) -> float:
    """
    Solve u_t = α u_xx on x∈(0,1), u(0,t)=u(1,t)=0, with initial u(x,0)=f(x)=x(1-x)
    Fourier sine series: u(x,t)= Σ b_n sin(nπx) e^{-α (nπ)^2 t}
    """
    # b_n coefficients for f(x)=x(1-x)
    s = 0.0
    for n in range(1, N+1):
        # Integral 0..1 x(1-x) sin(nπx) dx = (2/(n^3 π^3))*(1 - (-1)^n)
        b = (2.0 / (n**3 * math.pi**3)) * (1 - (-1)**n)
        s += b * math.sin(n*math.pi*x) * math.exp(-alpha * (n*math.pi)**2 * t)
    return s * (8.0)  # scaling to match the analytic integral factor

def sample_heat(times=(0.0, 0.01, 0.05, 0.2), Nx=64) -> List[Tuple[float, List[float]]]:
    xs = [i/(Nx-1) for i in range(Nx)]
    out = []
    for t in times:
        out.append((t, [heat_series(x, t) for x in xs]))
    return out

def demo_unify():
    print("\n=== Heat flows in modes (the same sine waves as strings & sound) ===")
    data = sample_heat()
    for (t, uxt) in data:
        print(f"\nT = {t:.3f}")
        print(ascii_plot(uxt, width=64, height=10))
    print("\nThe same sines that make musical tones also solve heat flow — one basis, many worlds.")

# ------------------------------------------------------------
# (4) BLOCKS — filtering & sparse reconstruction (keep K largest)
# ------------------------------------------------------------

def lowpass_reconstruct(x: List[float], K: int) -> Tuple[List[float], float]:
    X = dft([complex(v,0) for v in x])
    Xk = top_k_mask(X, K)
    xr = [v.real for v in idft(Xk)]
    err = math.sqrt(sum((a-b)**2 for a,b in zip(x, xr))/len(x))
    return xr, err

def demo_blocks():
    print("\n=== Waves as building blocks — filter & compress by keeping top K ===")
    x = make_signal(N=128)
    print("Original (time):")
    print(ascii_plot(x[:64], width=64, height=10))
    for K in (4, 8, 16, 32):
        xr, err = lowpass_reconstruct(x, K)
        print(f"\nKeep K={K} Fourier bins (RMS error ≈ {err:.3f}):")
        print(ascii_plot(xr[:64], width=64, height=10))
    print("\nFew coefficients capture the essence — compression via harmonic bricks.")

# ------------------------------------------------------------
# (5) MODERN — 2D DFT toy “image” compression
# ------------------------------------------------------------

def dft2(img: List[List[float]]) -> List[List[complex]]:
    H, W = len(img), len(img[0])
    # transform rows, then cols
    rows = [[complex(v,0) for v in row] for row in img]
    rowsX = [dft(r) for r in rows]
    colsX = []
    for c in range(W):
        col = [rowsX[r][c] for r in range(H)]
        colX = dft(col)
        for r in range(H):
            if c == 0: colsX.append([0]*W)
            colsX[r][c] = colX[r]
    return colsX

def idft2(X: List[List[complex]]) -> List[List[float]]:
    H, W = len(X), len(X[0])
    # inverse cols, then rows
    cols = []
    for c in range(W):
        col = [X[r][c] for r in range(H)]
        colx = idft(col)
        for r in range(H):
            if c == 0: cols.append([0j]*W)
            cols[r][c] = colx[r]
    rows = [idft(row) for row in cols]
    return [[row[c].real for c in range(W)] for row in rows]

def ascii_image(img: List[List[float]]) -> str:
    shades = " .:-=+*#%@"
    flat = [v for row in img for v in row]
    lo, hi = min(flat), max(flat)
    if hi == lo: hi = lo + 1e-9
    def mapv(v): return shades[int((len(shades)-1) * (v - lo)/(hi-lo))]
    return "\n".join("".join(mapv(v) for v in row) for row in img)

def make_checkerboard(H=16, W=16, block=4) -> List[List[float]]:
    return [[1.0 if ((r//block + c//block) % 2 == 0) else 0.0 for c in range(W)] for r in range(H)]

def keep_topK_2d(X: List[List[complex]], K: int) -> List[List[complex]]:
    H, W = len(X), len(X[0])
    flat = [ (abs(X[r][c]), r, c) for r in range(H) for c in range(W) ]
    flat.sort(reverse=True)
    keep = set((r,c) for _,r,c in flat[:K])
    return [[X[r][c] if (r,c) in keep else 0j for c in range(W)] for r in range(H)]

def demo_modern():
    print("\n=== 2D Fourier for images — sparse frequencies keep the gist ===")
    img = make_checkerboard(16,16,block=4)
    print("Original 16×16 pattern:")
    print(ascii_image(img))
    X = dft2(img)
    for K in (8, 16, 32, 64):
        Xk = keep_topK_2d(X, K)
        rec = idft2(Xk)
        print(f"\nReconstruction with K={K} largest 2D Fourier coefficients:")
        print(ascii_image(rec))
    print("\nModern signal & image science (compression, denoise, filtering) rides on this idea.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Fourier — Waves, Heat, and Harmony (runnable micro-demos).")
    ap.add_argument("--demo",
        choices=["all","waves","link","unify","blocks","modern"],
        default="all", help="Which demo to run.")
    args = ap.parse_args()

    print("Fourier and the Song of the World — Waves, Heat, and Harmony")
    print("Demos: waves (DFT & reconstruction), link (time–frequency), unify (heat modes),")
    print("       blocks (filter & compression), modern (2D DFT image toy)")

    if args.demo in ("all","waves"):  demo_waves()
    if args.demo in ("all","link"):   demo_link()
    if args.demo in ("all","unify"):  demo_unify()
    if args.demo in ("all","blocks"): demo_blocks()
    if args.demo in ("all","modern"): demo_modern()

if __name__ == "__main__":
    main()
