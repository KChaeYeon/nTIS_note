"""
Lead Field Electric Field Magnitude Calculator
-----------------------------------------------
COMSOL lead field CSV → per-electrode |E| and anti-phase channel |E|

Input CSV columns:
    x, y, ec.Ex@idx=1, ec.Ey@idx=1, ec.Ex@idx=2, ec.Ey@idx=2
    (complex phasors: real+imagj)

Anti-phase channel f1: electrode 1 (+I) and electrode 2 (-I)
    E_f1 = E_lead1 - E_lead2
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # 헤드리스 환경(WSL)에서 파일 저장용
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

# ── 설정 ──────────────────────────────────────────────────────────────────────
CSV_PATH = (
    "/mnt/d/00_Project/nTIS/docs/07_Simulation"
    "/20260626_TI_field_CompactXY_X05_Y05_leadField_Ch1_1,2.csv"
)
CURRENT_MA = 1.0  # 인가 전류 (mA) — 스케일링용

# ── CSV 로드 (% 주석 행 스킵) ──────────────────────────────────────────────────
def parse_complex(s: str) -> complex:
    """'a+bi' 또는 'a-bi' 형태 문자열 → Python complex"""
    return complex(s.strip().replace("i", "j"))


def load_lead_field(path: str) -> dict:
    """CSV 로드 → dict of numpy arrays"""
    x_list, y_list = [], []
    ex1_list, ey1_list, ex2_list, ey2_list = [], [], [], []

    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("%"):
                continue
            parts = line.strip().split(",")
            if len(parts) != 6:
                continue
            x_list.append(float(parts[0]))
            y_list.append(float(parts[1]))
            ex1_list.append(parse_complex(parts[2]))
            ey1_list.append(parse_complex(parts[3]))
            ex2_list.append(parse_complex(parts[4]))
            ey2_list.append(parse_complex(parts[5]))

    return {
        "x": np.array(x_list),
        "y": np.array(y_list),
        "Ex1": np.array(ex1_list),
        "Ey1": np.array(ey1_list),
        "Ex2": np.array(ex2_list),
        "Ey2": np.array(ey2_list),
    }


# ── 전기장 크기 계산 ───────────────────────────────────────────────────────────
def compute_magnitudes(data: dict, current_mA: float = 1.0) -> dict:
    scale = current_mA * 1e-3  # mA → A

    # 전극별 lead field 크기 (V/m per A → V/m)
    data["E1"] = np.sqrt(np.abs(data["Ex1"]) ** 2 + np.abs(data["Ey1"]) ** 2) * scale
    data["E2"] = np.sqrt(np.abs(data["Ex2"]) ** 2 + np.abs(data["Ey2"]) ** 2) * scale

    # Anti-phase 채널 f1: E_f1 = E_lead1 - E_lead2
    Ex_f1 = data["Ex1"] - data["Ex2"]
    Ey_f1 = data["Ey1"] - data["Ey2"]
    data["E_f1"] = np.sqrt(np.abs(Ex_f1) ** 2 + np.abs(Ey_f1) ** 2) * scale

    return data


# ── 시각화 ────────────────────────────────────────────────────────────────────
def plot_magnitudes(data: dict, save_path: str | None = None):
    x, y = data["x"], data["y"]
    triang = mtri.Triangulation(x, y)

    fields = {
        "Electrode 1  |E₁|": data["E1"],
        "Electrode 2  |E₂|": data["E2"],
        "f1 Anti-phase  |E_f1|": data["E_f1"],
    }

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (title, values) in zip(axes, fields.items()):
        tcf = ax.tricontourf(triang, values, levels=50, cmap="hot_r")
        fig.colorbar(tcf, ax=ax, label="|E| (V/m)")
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")
        ax.set_aspect("equal")

    fig.suptitle(f"Lead Field Magnitude  (I = {CURRENT_MA} mA)", fontsize=13)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Figure saved: {save_path}")
    else:
        plt.show()


# ── 요약 출력 ─────────────────────────────────────────────────────────────────
def print_summary(data: dict):
    for key, label in [("E1", "Electrode 1"), ("E2", "Electrode 2"), ("E_f1", "f1 Anti-phase")]:
        v = data[key]
        print(f"{label:20s}  max={v.max():.1f}  mean={v.mean():.1f}  median={np.median(v):.1f}  (V/m)")


# ── 메인 ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    data = load_lead_field(CSV_PATH)
    data = compute_magnitudes(data, CURRENT_MA)

    print(f"Nodes loaded: {len(data['x'])}")
    print()
    print_summary(data)

    plot_magnitudes(
        data,
        save_path="/mnt/d/00_Project/nTIS/docs/05_Code/Simulation/lead_field_magnitude.png",
    )
