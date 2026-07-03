"""
TIS 2D Phantom — MDI (Modulation Depth Index) 분석
참조: Grossman et al., Cell 2017

전기장 표현:
  E⃗_k(r) = (Ex_k(r), Ey_k(r))  — 벡터 (크기 + 방향)
  A_k(r)  = |E⃗_k(r)|           — 진폭 (크기만)
  θ_k(r)  = atan2(Ey_k, Ex_k)   — 방향 [degree]

Envelope (벡터 기반):
  E_max(r) = |E⃗₁(r) + E⃗₂(r)|  — 보강 간섭 최댓값
  E_min(r) = |E⃗₁(r) - E⃗₂(r)|  — 소상 간섭 최솟값
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# ─────────────────────────────────────────────────
# 1. 팬텀 설정
# ─────────────────────────────────────────────────
L   = 10.0   # 사각형 한 변 길이 [cm]
N   = 400    # 그리드 해상도
eps = 0.4    # 전극 정규화 반경 [cm] (점전극 특이점 방지)

x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)

# ─────────────────────────────────────────────────
# 2. 전기장 벡터 계산
#
#   2D 선원(line source) 모델:
#   E⃗(r) = I · [ (r-r+)/|r-r+|²  −  (r-r-)/|r-r-|² ]
#
#   반환: Ex, Ey (성분), A (크기), theta (방향 [deg])
# ─────────────────────────────────────────────────
def field_vector(X, Y, pos_elec, neg_elec, current=1.0, eps=0.4):
    """
    전극쌍이 만드는 전기장 벡터 계산.

    Parameters
    ----------
    pos_elec, neg_elec : tuple (x, y)  — 양극, 음극 좌표 [cm]
    current            : float         — 전류 진폭 [a.u.]
    eps                : float         — 전극 반경 정규화 [cm]

    Returns
    -------
    Ex    : x방향 전기장 성분
    Ey    : y방향 전기장 성분
    A     : 진폭 = sqrt(Ex²+Ey²)     [V/m a.u.]
    theta : 방향 = atan2(Ey, Ex)     [degree]
    """
    xp, yp = pos_elec
    xn, yn = neg_elec

    rp = np.sqrt((X - xp)**2 + (Y - yp)**2) + eps
    rn = np.sqrt((X - xn)**2 + (Y - yn)**2) + eps

    Ex    = current * ((X - xp)/rp**2 - (X - xn)/rn**2)
    Ey    = current * ((Y - yp)/rp**2 - (Y - yn)/rn**2)
    A     = np.sqrt(Ex**2 + Ey**2)
    theta = np.degrees(np.arctan2(Ey, Ex))

    return Ex, Ey, A, theta

# ─────────────────────────────────────────────────
# 3. 전극 배치 및 벡터 필드 계산
#    Ch1: 왼쪽 (x=0),  Ch2: 오른쪽 (x=L)
# ─────────────────────────────────────────────────
ch1_pos = (0.0, L*0.3);  ch1_neg = (0.0, L*0.7)
ch2_pos = (L,   L*0.3);  ch2_neg = (L,   L*0.7)

I1, I2 = 1.0, 1.0

Ex1, Ey1, A1, theta1 = field_vector(X, Y, ch1_pos, ch1_neg, I1, eps)
Ex2, Ey2, A2, theta2 = field_vector(X, Y, ch2_pos, ch2_neg, I2, eps)

# ─────────────────────────────────────────────────
# 4. Envelope 계산 — 벡터 기반
#
#   E_max(r) = |E⃗₁ + E⃗₂| = sqrt((Ex1+Ex2)² + (Ey1+Ey2)²)
#   E_min(r) = |E⃗₁ - E⃗₂| = sqrt((Ex1-Ex2)² + (Ey1-Ey2)²)
#
#   ※ 스칼라 공식 |A1-A2|은 두 벡터가 평행(Δθ=0)일 때만 성립
# ─────────────────────────────────────────────────
E_max = np.sqrt((Ex1 + Ex2)**2 + (Ey1 + Ey2)**2)   # 보강 간섭
E_min = np.sqrt((Ex1 - Ex2)**2 + (Ey1 - Ey2)**2)   # 소상 간섭
E_AM  = E_max - E_min                                # AM 변조 깊이

# 두 채널 방향 차이 [degree], [-180, 180] 정규화
delta_theta = (theta1 - theta2 + 180) % 360 - 180

# ─────────────────────────────────────────────────
# 5. MDI (Modulation Depth Index)
#
#   MDI(r) = E_AM(r) / E_max(r)
#           = (E_max - E_min) / E_max
#           = 1 - E_min/E_max
#
#   범위: [0, 1]
#     0 → 항상 켜짐 (inhibition zone)
#     1 → 완전 깜빡임 (AM zone)
# ─────────────────────────────────────────────────
TINY = 1e-10

MDI    = E_AM  / (E_max + TINY)
MDI_v2 = 1 - E_min / (E_max + TINY)

assert np.allclose(MDI, MDI_v2, atol=1e-5), "MDI 등가 표현 불일치"

# ─────────────────────────────────────────────────
# 6. Zone 분류
#
#   Sub-threshold : E_max < E_th
#   AM zone       : E_min < E_th  AND  E_max >= E_th
#   Inhibition    : E_min >= E_th (AND E_max >= E_th)
# ─────────────────────────────────────────────────
E_th = np.percentile(E_max, 55)

zone = np.zeros_like(MDI, dtype=int)
zone[E_max >= E_th]                              = 1   # AM zone
zone[(E_max >= E_th) & (E_min >= E_th)]         = 2   # Inhibition

# ─────────────────────────────────────────────────
# 7. 시각화
# ─────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 11))
gs  = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

CBAR_KW   = dict(fraction=0.046, pad=0.04)
ELEC_KW   = dict(s=120, zorder=6, edgecolors='k', lw=1.0)
QUIVER_KW = dict(scale=80, width=0.003, alpha=0.55, pivot='middle')

def draw_electrodes(ax):
    ax.scatter(*ch1_pos, color='red',  marker='^', **ELEC_KW)
    ax.scatter(*ch1_neg, color='blue', marker='v', **ELEC_KW)
    ax.scatter(*ch2_pos, color='red',  marker='^', **ELEC_KW)
    ax.scatter(*ch2_neg, color='blue', marker='v', **ELEC_KW)
    ax.set_xlim(0, L); ax.set_ylim(0, L)
    ax.set_xlabel('x [cm]'); ax.set_ylabel('y [cm]')
    ax.set_aspect('equal')

step = 20   # quiver 서브샘플링
Xq   = X[::step, ::step]
Yq   = Y[::step, ::step]

# ── (1) Ch1 전기장 벡터 ──
ax1 = fig.add_subplot(gs[0, 0])
cf1 = ax1.contourf(X, Y, A1, levels=40, cmap='Blues', alpha=0.75)
plt.colorbar(cf1, ax=ax1, **CBAR_KW, label='A1 [a.u.]')
ax1.quiver(Xq, Yq,
           Ex1[::step,::step]/(A1[::step,::step]+TINY),
           Ey1[::step,::step]/(A1[::step,::step]+TINY),
           color='navy', **QUIVER_KW)
ax1.set_title('E-field vector Ch1\ncolor=A1(r), arrow=direction theta1(r)', fontsize=10)
draw_electrodes(ax1)

# ── (2) Ch2 전기장 벡터 ──
ax2 = fig.add_subplot(gs[0, 1])
cf2 = ax2.contourf(X, Y, A2, levels=40, cmap='Oranges', alpha=0.75)
plt.colorbar(cf2, ax=ax2, **CBAR_KW, label='A2 [a.u.]')
ax2.quiver(Xq, Yq,
           Ex2[::step,::step]/(A2[::step,::step]+TINY),
           Ey2[::step,::step]/(A2[::step,::step]+TINY),
           color='saddlebrown', **QUIVER_KW)
ax2.set_title('E-field vector Ch2\ncolor=A2(r), arrow=direction theta2(r)', fontsize=10)
draw_electrodes(ax2)

# ── (3) E_min 맵 + E_th 등고선 ──
ax3 = fig.add_subplot(gs[0, 2])
cf3 = ax3.contourf(X, Y, E_min, levels=40, cmap='Reds')
plt.colorbar(cf3, ax=ax3, **CBAR_KW, label='E_min [a.u.]')
cs3 = ax3.contour(X, Y, E_min, levels=[E_th], colors='black', linewidths=2)
ax3.clabel(cs3, fmt=f'E_th={E_th:.2f}', fontsize=8)
ax3.set_title('E_min(r) = |E1 - E2|  (vector)\nblack line = E_th boundary', fontsize=10)
draw_electrodes(ax3)

# ── (4) MDI 맵 ──
ax4 = fig.add_subplot(gs[1, 0])
cf4 = ax4.contourf(X, Y, MDI, levels=np.linspace(0, 1, 51),
                   cmap='RdYlBu', vmin=0, vmax=1)
plt.colorbar(cf4, ax=ax4, **CBAR_KW, label='MDI [0~1]')
ax4.set_title('MDI(r) = E_AM / E_max = 1 - E_min/E_max\n0=inhibition  1=full AM', fontsize=10)
draw_electrodes(ax4)

# ── (5) Zone 맵 ──
ax5 = fig.add_subplot(gs[1, 1])
zone_colors = ['lightgray', 'steelblue', 'salmon']
ax5.contourf(X, Y, zone, levels=[-0.5, 0.5, 1.5, 2.5], colors=zone_colors)
handles = [mpatches.Patch(color=c, label=l) for c, l in zip(
    zone_colors,
    ['Sub-threshold', 'AM zone (blinks)', 'Inhibition (always on)'])]
ax5.legend(handles=handles, loc='lower center', fontsize=8, framealpha=0.9)
ax5.set_title(f'Zone map  (E_th = {E_th:.3f})\n'
              'E_min < E_th: AM  |  E_min >= E_th: Inhibition', fontsize=10)
draw_electrodes(ax5)

# ── (6) 중앙선 단면 (y = L/2) ──
ax6 = fig.add_subplot(gs[1, 2])
mid = N // 2
lw  = 2.0

ax6.plot(x, A1[mid, :],    color='steelblue',   lw=lw, label='A1(x) = |E1|')
ax6.plot(x, A2[mid, :],    color='darkorange',   lw=lw, label='A2(x) = |E2|')
ax6.plot(x, E_min[mid, :], color='crimson',      lw=lw, ls='--', label='E_min = |E1-E2|')
ax6.plot(x, E_max[mid, :], color='purple',       lw=lw, ls=':',  label='E_max = |E1+E2|')
ax6.fill_between(x, E_min[mid,:], E_max[mid,:],
                 alpha=0.12, color='green', label='AM swing')
ax6.axhline(E_th, color='black', ls='-.', lw=1.5, label=f'E_th={E_th:.2f}')

inhib_1d = E_min[mid, :] >= E_th
ax6.fill_between(x, 0, E_max[mid,:],
                 where=inhib_1d, alpha=0.18, color='red', label='Inhibition')

ax6.set_xlabel('x [cm]'); ax6.set_ylabel('[a.u.]')
ax6.set_title('Center line (y=L/2) cross-section', fontsize=10)
ax6.legend(fontsize=7.5, loc='upper center')

fig.suptitle(
    'TIS 2D Phantom — Vector Field MDI Analysis\n'
    'E_max = |E1+E2|,  E_min = |E1-E2|,  MDI = 1 - E_min/E_max',
    fontsize=13, fontweight='bold')

out = '/mnt/d/00_Project/nTIS/docs/05_Exp/Simulation/tis_mdi_analysis.png'
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f"saved: {out}")
plt.close()

# ─────────────────────────────────────────────────
# 8. 수치 확인 — 중앙선 y=L/2
# ─────────────────────────────────────────────────
mid = N // 2
print(f"\n{'x':>5} {'A1':>7} {'th1':>7} {'A2':>7} {'th2':>7} "
      f"{'Dth':>7} {'E_min':>8} {'E_max':>8} {'MDI':>7} {'Zone':>12}")
print("─" * 85)
zone_lbl = ['Sub-th', 'AM zone', 'Inhibit.']
for cx in [0, 2.5, 5.0, 7.5, 10.0]:
    ix = np.argmin(np.abs(x - cx))
    print(f"{cx:>5.1f} {A1[mid,ix]:>7.3f} {theta1[mid,ix]:>7.1f} "
          f"{A2[mid,ix]:>7.3f} {theta2[mid,ix]:>7.1f} "
          f"{delta_theta[mid,ix]:>7.1f} {E_min[mid,ix]:>8.4f} "
          f"{E_max[mid,ix]:>8.4f} {MDI[mid,ix]:>7.3f} "
          f"{zone_lbl[zone[mid,ix]]:>12}")

print(f"\nE_th = {E_th:.4f}")
print("MDI == 1 - E_min/E_max: OK")
