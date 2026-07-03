# -*- coding: utf-8 -*-
"""
nTIS Dual Overlay Map 시각화
Ch1(빨강) + Ch2(파랑) + AM_max(보라) + Inhibition Zone(주황)

실행 전 확인:
  1. FILEPATH - txt 파일 경로
  2. E_TH     - Inhibition zone 판별 역치 [V/m]
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════
# 설정값 — 여기만 수정
# ═══════════════════════════════════════════════════════════════════
FILEPATH = r"D:\00_Project\nTIS\docs\07_Simulation\20260626_TI_field_Base_X50_Y50.txt"
SAVEPATH = r"D:\00_Project\nTIS\docs\07_Simulation\dual_overlay_map.png"

E_TH     = None    # [V/m] None이면 자동 설정 (E_min 중앙값 사용) → 나중에 숫자로 교체
GRID_RES = 300     # 보간 해상도 (300×300)

# ═══════════════════════════════════════════════════════════════════
# 1. 파일 읽기
# ═══════════════════════════════════════════════════════════════════
COL_NAMES = ['x', 'y',
             'ch1_Ex', 'ch1_Ey',
             'ch2_Ex', 'ch2_Ey',
             'ch1_normE', 'ch2_normE',
             'am_max', 'Ex_m', 'Ey_m', 'E_min']

# ── 파일 형식 진단 ────────────────────────────────────────────────
print("=== 파일 원본 첫 5줄 ===")
with open(FILEPATH, 'r', encoding='utf-8', errors='replace') as f:
    for i, line in enumerate(f):
        print(repr(line))
        if i >= 4:
            break
print("========================\n")

print("파일 읽는 중... (수 분 소요될 수 있음)")

# 탭 구분으로 먼저 시도
df = pd.read_csv(FILEPATH, sep='\t', comment='%',
                 header=None, names=COL_NAMES, skipinitialspace=True)

# 탭 실패 시 공백 구분으로 재시도
if df[COL_NAMES[2]].isna().all():
    print("[재시도] 탭 구분 실패 → 공백 구분으로 재시도")
    df = pd.read_csv(FILEPATH, sep=r'\s+', comment='%',
                     header=None, names=COL_NAMES,
                     engine='python', skipinitialspace=True)

print(f"읽기 완료: {len(df):,} rows")
print(df.head())
print(df.describe())


# ═══════════════════════════════════════════════════════════════════
# 3. 정규 격자 보간
# ═══════════════════════════════════════════════════════════════════
x      = df['x'].values
y      = df['y'].values
points = np.column_stack([x, y])

xi = np.linspace(x.min(), x.max(), GRID_RES)
yi = np.linspace(y.min(), y.max(), GRID_RES)
Xi, Yi = np.meshgrid(xi, yi)

def interp(col):
    return griddata(points, df[col].values, (Xi, Yi), method='linear')

print("격자 보간 중...")
ch1_grid  = interp('ch1_normE')
ch2_grid  = interp('ch2_normE')
am_grid   = interp('am_max')
emin_grid = interp('E_min')
print("보간 완료.")

# ═══════════════════════════════════════════════════════════════════
# E_min 분포 확인 → E_TH 자동 설정
# ═══════════════════════════════════════════════════════════════════
emin_valid = emin_grid[~np.isnan(emin_grid)]
print("\n=== E_min 분포 [V/m] ===")
print(f"  최솟값  : {emin_valid.min():.2f}")
print(f"  25%     : {np.percentile(emin_valid, 25):.2f}")
print(f"  중앙값  : {np.median(emin_valid):.2f}")
print(f"  75%     : {np.percentile(emin_valid, 75):.2f}")
print(f"  최댓값  : {emin_valid.max():.2f}")
print("========================")

E_TH = float(np.percentile(emin_valid, 70))
print(f"→ E_TH 자동 설정: {E_TH:.2f} V/m (E_min 상위 25% 기준)")


# ═══════════════════════════════════════════════════════════════════
# 4. RGBA 레이어 생성 (세기 → 투명도)
# ═══════════════════════════════════════════════════════════════════
def make_rgba(data, color_rgb, pct=99):
    """강할수록 불투명. 상위 pct% 기준 정규화."""
    vmax  = np.nanpercentile(data, pct)
    alpha = np.clip(data / vmax, 0, 1)
    rgba  = np.zeros((*data.shape, 4))
    rgba[..., :3] = color_rgb
    rgba[..., 3]  = alpha
    return rgba

ch1_rgba = make_rgba(ch1_grid, [1.0, 0.0, 0.0])   # 빨강
ch2_rgba = make_rgba(ch2_grid, [0.0, 0.0, 1.0])   # 파랑
am_rgba  = make_rgba(am_grid,  [0.5, 0.0, 0.5])   # 보라

# ═══════════════════════════════════════════════════════════════════
# 5. 시각화
# ═══════════════════════════════════════════════════════════════════
extent = [x.min(), x.max(), y.min(), y.max()]

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor('black')

# Layer 1: Ch1 전기장 (빨강)
ax.imshow(ch1_rgba, origin='lower', extent=extent, aspect='equal',
          interpolation='bilinear')

# Layer 2: Ch2 전기장 (파랑)
ax.imshow(ch2_rgba, origin='lower', extent=extent, aspect='equal',
          interpolation='bilinear')

# Layer 3: AM_max 진폭 (보라)
ax.imshow(am_rgba,  origin='lower', extent=extent, aspect='equal',
          interpolation='bilinear')

# Layer 4: Inhibition Zone (주황 채우기 + 흰 경계선)
emin_max = np.nanmax(emin_grid)
if emin_max > E_TH:
    ax.contourf(Xi, Yi, emin_grid,
                levels=[E_TH, emin_max],
                colors=['#FF8C00'], alpha=0.45, zorder=4)
    ax.contour(Xi, Yi, emin_grid,
               levels=[E_TH],
               colors=['white'], linewidths=1.5, zorder=5)
else:
    print(f"[주의] E_min 최대값({emin_max:.1f} V/m) < E_TH({E_TH} V/m)")
    print("       Inhibition zone이 없거나 E_TH 값을 낮춰야 합니다.")

# 범례
legend_elements = [
    Patch(facecolor='red',     alpha=0.7, label='Ch1 E-field'),
    Patch(facecolor='blue',    alpha=0.7, label='Ch2 E-field'),
    Patch(facecolor='purple',  alpha=0.7, label='AM_max'),
    Patch(facecolor='#FF8C00', alpha=0.6,
          label=f'Inhibition Zone (E_min > {E_TH} V/m)'),
    Line2D([0], [0], color='white', lw=1.5, label='Inhibition boundary'),
]
ax.legend(handles=legend_elements, loc='upper right',
          framealpha=0.8, fontsize=9,
          facecolor='#222222', labelcolor='white')

ax.set_xlabel('x [m]', fontsize=11)
ax.set_ylabel('y [m]', fontsize=11)
ax.set_title('nTIS Dual Overlay Map', fontsize=13, fontweight='bold')
plt.tight_layout()

#plt.savefig(SAVEPATH, dpi=150, bbox_inches='tight')
plt.show()
print(f"저장 완료: {SAVEPATH}")
