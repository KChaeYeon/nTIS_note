"""
TIS AM Field Analysis — Grossman 2017
======================================
f1 (1 kHz,  1 mA): electrodes 1, 2  anti-phase
f2 (1.04 kHz, 1 mA): electrodes 3, 4  anti-phase

Outputs 3 panels:
  [1] AM_x  — x-direction AM depth
  [2] AM_y  — y-direction AM depth
  [3] AM_max — max over all projection directions (Grossman 2017)

Center point (0, 0) is marked with a cross and values annotated.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

# ── 경로 설정 ─────────────────────────────────────────────────────────────────
SIM_DIR = "/mnt/d/00_Project/nTIS/docs/07_Simulation"
CSV_F1  = f"{SIM_DIR}/20260626_TI_field_CompactXY_X05_Y05_leadField_Ch1_1,2.csv"
CSV_F2  = f"{SIM_DIR}/20260626_TI_field_CompactXY_X05_Y05_leadField_Ch2_3,4.csv"
SAVE    = "/mnt/d/00_Project/nTIS/docs/05_Code/Simulation/tis_am_analysis.png"

CURRENT_MA = 1.0   # 인가 전류 [mA] — 양 채널 동일
N_ANGLES   = 360   # AM_max 스캔 각도 수

# ── CSV 로더 ──────────────────────────────────────────────────────────────────
def load_lead_field(path: str) -> dict:
    """
    Returns dict with keys: x, y, Ex1, Ey1, Ex2, Ey2 (complex arrays).
    idx=1 → 첫 번째 전극, idx=2 → 두 번째 전극 (COMSOL parametric)
    """
    xs, ys = [], []
    ex1, ey1, ex2, ey2 = [], [], [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("%"):
                continue
            p = line.strip().split(",")
            if len(p) != 6:
                continue
            xs.append(float(p[0]))
            ys.append(float(p[1]))
            ex1.append(complex(p[2].strip().replace("i", "j")))
            ey1.append(complex(p[3].strip().replace("i", "j")))
            ex2.append(complex(p[4].strip().replace("i", "j")))
            ey2.append(complex(p[5].strip().replace("i", "j")))
    return {
        "x": np.array(xs), "y": np.array(ys),
        "Ex1": np.array(ex1), "Ey1": np.array(ey1),
        "Ex2": np.array(ex2), "Ey2": np.array(ey2),
    }


# ── Anti-phase 채널 전기장 계산 ────────────────────────────────────────────────
def channel_field(data: dict, current_mA: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Anti-phase: E_ch = E_lead1 - E_lead2
    Real part만 사용 (Im << Re, ~1.5%)
    반환: (Ex_ch, Ey_ch) — 실수 배열 [V/m]
    """
    scale = current_mA * 1e-3
    Ex = np.real(data["Ex1"] - data["Ex2"]) * scale
    Ey = np.real(data["Ey1"] - data["Ey2"]) * scale
    return Ex, Ey


# ── AM 계산 ───────────────────────────────────────────────────────────────────
def compute_am(Ex1, Ey1, Ex2, Ey2, n_angles: int = 360) -> tuple:
    """
    각 노드에서:
      AM_x   = 2·min(|Ex1|, |Ex2|)
      AM_y   = 2·min(|Ey1|, |Ey2|)
      AM_max = max_θ { 2·min(|E1·n̂(θ)|, |E2·n̂(θ)|) }  [Grossman 2017]
    """
    AM_x = 2 * np.minimum(np.abs(Ex1), np.abs(Ex2))
    AM_y = 2 * np.minimum(np.abs(Ey1), np.abs(Ey2))

    # 벡터화 스캔: (n_angles, n_nodes)
    theta   = np.linspace(0, np.pi, n_angles, endpoint=False)
    cos_t   = np.cos(theta)[:, None]   # (n_angles, 1)
    sin_t   = np.sin(theta)[:, None]

    p1 = np.abs(Ex1[None, :] * cos_t + Ey1[None, :] * sin_t)  # (n_angles, N)
    p2 = np.abs(Ex2[None, :] * cos_t + Ey2[None, :] * sin_t)

    AM_max = 2 * np.max(np.minimum(p1, p2), axis=0)            # (N,)

    return AM_x, AM_y, AM_max


# ── 중심점 찾기 ───────────────────────────────────────────────────────────────
def find_center(x: np.ndarray, y: np.ndarray) -> int:
    return int(np.argmin(x**2 + y**2))


# ── 시각화 ────────────────────────────────────────────────────────────────────
def plot_results(x, y, AM_x, AM_y, AM_max, center_idx: int, save_path: str):
    triang = mtri.Triangulation(x, y)
    cx, cy = x[center_idx], y[center_idx]

    panels = [
        ("AM$_x$  (x-direction)", AM_x),
        ("AM$_y$  (y-direction)", AM_y),
        ("AM$_{max}$  (Grossman 2017)",  AM_max),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    for ax, (title, values) in zip(axes, panels):
        tcf = ax.tricontourf(triang, values, levels=50, cmap="inferno")
        cb  = fig.colorbar(tcf, ax=ax, shrink=0.85)
        cb.set_label("|E| (V/m)", fontsize=9)

        # 중심점 마커
        ax.plot(cx, cy, marker="*", color="cyan", markersize=12,
                markeredgecolor="white", markeredgewidth=0.8, zorder=10)
        ax.annotate(
            f"({cx:.2f}, {cy:.2f}) mm\n{values[center_idx]:.2f} V/m",
            xy=(cx, cy), xytext=(cx + 0.8, cy + 0.8),
            fontsize=7.5, color="cyan",
            arrowprops=dict(arrowstyle="->", color="cyan", lw=0.8),
            bbox=dict(boxstyle="round,pad=0.2", fc="black", alpha=0.6),
            zorder=11,
        )

        ax.set_title(title, fontsize=11)
        ax.set_xlabel("x (mm)", fontsize=9)
        ax.set_ylabel("y (mm)", fontsize=9)
        ax.set_aspect("equal")

    fig.suptitle(
        f"TIS AM Field   f1=1 kHz / f2=1.04 kHz / I={CURRENT_MA} mA (anti-phase)",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"Figure saved: {save_path}")


# ── 메인 ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 데이터 로드
    d1 = load_lead_field(CSV_F1)
    d2 = load_lead_field(CSV_F2)
    print(f"f1 nodes: {len(d1['x'])}  |  f2 nodes: {len(d2['x'])}")

    # 채널 전기장
    Ex1, Ey1 = channel_field(d1, CURRENT_MA)
    Ex2, Ey2 = channel_field(d2, CURRENT_MA)

    # AM 계산
    AM_x, AM_y, AM_max = compute_am(Ex1, Ey1, Ex2, Ey2, N_ANGLES)

    # 중심점
    ci = find_center(d1["x"], d1["y"])
    cx, cy = d1["x"][ci], d1["y"][ci]

    # 요약 출력
    print(f"\nCenter point: ({cx:.3f}, {cy:.3f}) mm")
    print(f"  |E_f1|     = {np.sqrt(Ex1[ci]**2 + Ey1[ci]**2):.3f} V/m")
    print(f"  |E_f2|     = {np.sqrt(Ex2[ci]**2 + Ey2[ci]**2):.3f} V/m")
    print(f"  AM_x       = {AM_x[ci]:.3f} V/m")
    print(f"  AM_y       = {AM_y[ci]:.3f} V/m")
    print(f"  AM_max     = {AM_max[ci]:.3f} V/m")

    print("\nGlobal stats [V/m]:")
    for name, arr in [("AM_x", AM_x), ("AM_y", AM_y), ("AM_max", AM_max)]:
        print(f"  {name:8s}  max={arr.max():.2f}  mean={arr.mean():.2f}  median={np.median(arr):.2f}")

    plot_results(d1["x"], d1["y"], AM_x, AM_y, AM_max, ci, SAVE)
