"""
TIS 2D Phantom — Vector Field (amplitude + direction) 기반 MDI 분석

핵심 수정:
  이전: A₁(r) = scalar amplitude만 사용 → E_min = |A₁ - A₂| (평행 가정)
  이번: E⃗₁(r) = (Ex₁, Ey₁) 벡터 사용  → E_min = |E⃗₁ - E⃗₂| (정확)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# ─────────────────────────────────────────────────
# 1. 팬텀 설정
# ─────────────────────────────────────────────────
L   = 10.0
N   = 300
eps = 0.4

x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)

# ─────────────────────────────────────────────────
# 2. 전기장 벡터 계산 — (Ex, Ey) 모두 반환
#
#   E⃗(r) = I · [ (r - r+)/|r - r+|²  −  (r - r-)/|r - r-|² ]
#
#   반환: Ex, Ey (각 성분), A (크기), theta (방향 [degree])
# ─────────────────────────────────────────────────
def field_vector(X, Y, pos_elec, neg_elec, current=1.0, eps=0.4):
    xp, yp = pos_elec
    xn, yn = neg_elec

    rp = np.sqrt((X - xp)**2 + (Y - yp)**2) + eps
    rn = np.sqrt((X - xn)**2 + (Y - yn)**2) + eps

    Ex = current * ((X - xp)/rp**2 - (X - xn)/rn**2)
    Ey = current * ((Y - yp)/rp**2 - (Y - yn)/rn**2)

    A     = np.sqrt(Ex**2 + Ey**2)                 # 크기 [V/m]
    theta = np.degrees(np.arctan2(Ey, Ex))          # 방향 [degree]

    return Ex, Ey, A, theta

# ─────────────────────────────────────────────────
# 3. 전극 배치
# ─────────────────────────────────────────────────
ch1_pos = (0.0, L*0.3);  ch1_neg = (0.0, L*0.7)   # Ch1: 왼쪽
ch2_pos = (L,   L*0.3);  ch2_neg = (L,   L*0.7)   # Ch2: 오른쪽

I1, I2 = 1.0, 1.0

Ex1, Ey1, A1, theta1 = field_vector(X, Y, ch1_pos, ch1_neg, I1, eps)
Ex2, Ey2, A2, theta2 = field_vector(X, Y, ch2_pos, ch2_neg, I2, eps)

# ─────────────────────────────────────────────────
# 4. 벡터 기반 Envelope — 핵심 수정 부분
#
#   E_max(r) = |E⃗₁(r) + E⃗₂(r)|   보강 간섭 (두 벡터 합)
#   E_min(r) = |E⃗₁(r) - E⃗₂(r)|   소상 간섭 (두 벡터 차)
# ─────────────────────────────────────────────────
E_max_vec = np.sqrt((Ex1 + Ex2)**2 + (Ey1 + Ey2)**2)   # |E⃗₁ + E⃗₂|
E_min_vec = np.sqrt((Ex1 - Ex2)**2 + (Ey1 - Ey2)**2)   # |E⃗₁ - E⃗₂|
E_AM_vec  = E_max_vec - E_min_vec

# 비교: 이전 스칼라 공식 (평행 가정)
E_max_scl = A1 + A2
E_min_scl = np.abs(A1 - A2)

# 두 채널 사이 각도 [degree]
delta_theta = theta1 - theta2   # 방향 차이
delta_theta = (delta_theta + 180) % 360 - 180   # [-180, 180] 정규화

# ─────────────────────────────────────────────────
# 5. MDI (벡터 기반)
# ─────────────────────────────────────────────────
TINY = 1e-10
MDI_vec = E_AM_vec  / (E_max_vec + TINY)
MDI_scl = (E_max_scl - E_min_scl) / (E_max_scl + TINY)   # 이전 방식

# E_min 오차: 스칼라가 벡터 대비 얼마나 다른가
err_Emin = E_min_vec - E_min_scl   # 양수 = 스칼라가 과소추정

# ─────────────────────────────────────────────────
# 6. Zone 분류 (벡터 기반 E_min 사용)
# ─────────────────────────────────────────────────
E_th = np.percentile(E_max_vec, 55)

zone = np.zeros_like(MDI_vec, dtype=int)
zone[E_max_vec >= E_th]                              = 1   # AM zone
zone[(E_max_vec >= E_th) & (E_min_vec >= E_th)]     = 2   # Inhibition

# ─────────────────────────────────────────────────
# 7. 시각화
# ─────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 13))
gs  = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

CBAR_KW   = dict(fraction=0.046, pad=0.04)
ELEC_KW   = dict(s=120, zorder=6, edgecolors='k', lw=1.0)
QUIVER_KW = dict(scale=80, width=0.003, alpha=0.6, pivot='middle')

def draw_electrodes(ax):
    ax.scatter(*ch1_pos, color='red',  marker='^', **ELEC_KW)
    ax.scatter(*ch1_neg, color='blue', marker='v', **ELEC_KW)
    ax.scatter(*ch2_pos, color='red',  marker='^', **ELEC_KW)
    ax.scatter(*ch2_neg, color='blue', marker='v', **ELEC_KW)
    ax.set_xlim(0, L); ax.set_ylim(0, L)
    ax.set_xlabel('x [cm]'); ax.set_ylabel('y [cm]')
    ax.set_aspect('equal')

# 화살표 서브샘플링
step = 20
Xq, Yq = X[::step, ::step], Y[::step, ::step]

# ── (1) Ch1 전기장 벡터 ──
ax1 = fig.add_subplot(gs[0, 0])
cf1 = ax1.contourf(X, Y, A1, levels=40, cmap='Blues', alpha=0.7)
plt.colorbar(cf1, ax=ax1, **CBAR_KW, label='A1 [a.u.]')
ax1.quiver(Xq, Yq,
           Ex1[::step,::step]/A1[::step,::step],
           Ey1[::step,::step]/A1[::step,::step],
           color='navy', **QUIVER_KW)
ax1.set_title('Ch1 E-field vector\nA1(r)=amplitude, theta1(r)=direction', fontsize=10)
draw_electrodes(ax1)

# ── (2) Ch2 전기장 벡터 ──
ax2 = fig.add_subplot(gs[0, 1])
cf2 = ax2.contourf(X, Y, A2, levels=40, cmap='Oranges', alpha=0.7)
plt.colorbar(cf2, ax=ax2, **CBAR_KW, label='A2 [a.u.]')
ax2.quiver(Xq, Yq,
           Ex2[::step,::step]/A2[::step,::step],
           Ey2[::step,::step]/A2[::step,::step],
           color='saddlebrown', **QUIVER_KW)
ax2.set_title('Ch2 E-field vector\nA2(r)=amplitude, theta2(r)=direction', fontsize=10)
draw_electrodes(ax2)

# ── (3) 두 채널 방향 차이 Δθ ──
ax3 = fig.add_subplot(gs[0, 2])
cf3 = ax3.contourf(X, Y, np.abs(delta_theta), levels=40,
                   cmap='RdYlGn_r', vmin=0, vmax=180)
plt.colorbar(cf3, ax=ax3, **CBAR_KW, label='|Delta theta| [deg]')
ax3.set_title('|Delta_theta(r)| = |theta1 - theta2|\n'
              '0=parallel  90=perpendicular  180=anti-parallel', fontsize=10)
draw_electrodes(ax3)

# ── (4) E_min 비교: 벡터 vs 스칼라 ──
ax4 = fig.add_subplot(gs[1, 0])
cf4 = ax4.contourf(X, Y, E_min_vec, levels=40, cmap='Reds')
plt.colorbar(cf4, ax=ax4, **CBAR_KW, label='E_min [a.u.]')
ax4.set_title('E_min VECTOR = |E1 - E2|\n(correct)', fontsize=10)
draw_electrodes(ax4)

ax5 = fig.add_subplot(gs[1, 1])
cf5 = ax5.contourf(X, Y, E_min_scl, levels=40, cmap='Reds')
plt.colorbar(cf5, ax=ax5, **CBAR_KW, label='E_min [a.u.]')
ax5.set_title('E_min SCALAR = |A1 - A2|\n(parallel assumption)', fontsize=10)
draw_electrodes(ax5)

ax6 = fig.add_subplot(gs[1, 2])
vmax_err = np.percentile(np.abs(err_Emin), 98)
cf6 = ax6.contourf(X, Y, err_Emin, levels=40, cmap='RdBu_r',
                   vmin=-vmax_err, vmax=vmax_err)
plt.colorbar(cf6, ax=ax6, **CBAR_KW, label='error [a.u.]')
ax6.set_title('E_min error = VECTOR - SCALAR\n(+red: scalar underestimates)', fontsize=10)
draw_electrodes(ax6)

# ── (5) MDI 비교 ──
ax7 = fig.add_subplot(gs[2, 0])
cf7 = ax7.contourf(X, Y, MDI_vec, levels=np.linspace(0,1,51),
                   cmap='RdYlBu', vmin=0, vmax=1)
plt.colorbar(cf7, ax=ax7, **CBAR_KW, label='MDI')
ax7.set_title('MDI VECTOR = E_AM_vec / E_max_vec', fontsize=10)
draw_electrodes(ax7)

ax8 = fig.add_subplot(gs[2, 1])
cf8 = ax8.contourf(X, Y, MDI_scl, levels=np.linspace(0,1,51),
                   cmap='RdYlBu', vmin=0, vmax=1)
plt.colorbar(cf8, ax=ax8, **CBAR_KW, label='MDI')
ax8.set_title('MDI SCALAR = (A1+A2 - |A1-A2|) / (A1+A2)', fontsize=10)
draw_electrodes(ax8)

# ── (6) Zone map (벡터 기반) ──
ax9 = fig.add_subplot(gs[2, 2])
zone_colors = ['lightgray', 'steelblue', 'salmon']
ax9.contourf(X, Y, zone, levels=[-0.5, 0.5, 1.5, 2.5], colors=zone_colors)
handles = [mpatches.Patch(color=c, label=l) for c, l in zip(
    zone_colors,
    ['Sub-threshold', 'AM zone (blinks)', 'Inhibition (always on)'])]
ax9.legend(handles=handles, loc='lower center', fontsize=8, framealpha=0.9)
ax9.set_title(f'Zone map (vector E_min, E_th={E_th:.3f})', fontsize=10)
draw_electrodes(ax9)

fig.suptitle('TIS 2D Phantom — Vector vs Scalar Field Comparison\n'
             'E⃗(r) = (Ex, Ey) = A(r)*[cos(theta), sin(theta)]',
             fontsize=13, fontweight='bold')

out = '/mnt/d/00_Project/nTIS/docs/05_Exp/Simulation/tis_mdi_vector.png'
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f"saved: {out}")
plt.close()

# ─────────────────────────────────────────────────
# 8. 수치 확인 — 중앙선 y=L/2
# ─────────────────────────────────────────────────
mid = N // 2
print("\n── 중앙선 (y=L/2) 수치 비교 ──")
print(f"{'x':>5} {'A1':>7} {'theta1':>8} {'A2':>7} {'theta2':>8} "
      f"{'Dtheta':>8} {'Emin_vec':>10} {'Emin_scl':>10} {'diff':>7}")
print("─" * 80)
for cx in [0, 2.5, 5.0, 7.5, 10.0]:
    ix  = np.argmin(np.abs(x - cx))
    a1_ = A1[mid, ix];     t1_ = theta1[mid, ix]
    a2_ = A2[mid, ix];     t2_ = theta2[mid, ix]
    dt_ = delta_theta[mid, ix]
    ev_ = E_min_vec[mid, ix]
    es_ = E_min_scl[mid, ix]
    print(f"{cx:>5.1f} {a1_:>7.3f} {t1_:>8.1f} {a2_:>7.3f} {t2_:>8.1f} "
          f"{dt_:>8.1f} {ev_:>10.4f} {es_:>10.4f} {ev_-es_:>7.4f}")
