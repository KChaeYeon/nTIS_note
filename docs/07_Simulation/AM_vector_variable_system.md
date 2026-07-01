# AM_vector COMSOL 변수 체계

> **출처**: `2D_2phase_max.txt` — COMSOL Variables로 등록하여 사용  
> **목적**: 2채널 TIS의 진정한 AM_max를 신경 방향 최적화 기반으로 계산

---

## 배경: ec.normE 와 AM_vector의 차이

| | ec.normE | AM_vector |
|--|---------|-----------|
| 의미 | 전기장 크기 (방향 무관) | 신경 방향 최적화된 AM 깊이 |
| 단위 | V/m | V/m |
| 값 범위 | 항상 양수 | 항상 ≤ ec.normE |
| 용도 | Lead Field 크기 확인 | 실제 자극 효과 예측 |

---

## 변수 정의 전체 목록

```
sol1_amp  withsol('sol1',ec.normE)
sol2_amp  withsol('sol2',ec.normE)
E1_amp    max(sol1_amp,sol2_amp)
E2_amp    min(sol1_amp,sol2_amp)
E1_x      if((sol1_amp>sol2_amp),withsol('sol1',ec.Ex),withsol('sol2',ec.Ex))
E2_x      if((sol1_amp<=sol2_amp),withsol('sol1',ec.Ex),withsol('sol2',ec.Ex))
E1_y      if((sol1_amp>sol2_amp),withsol('sol1',ec.Ey),withsol('sol2',ec.Ey))
E2_y      if((sol1_amp<=sol2_amp),withsol('sol1',ec.Ey),withsol('sol2',ec.Ey))
Ex_m      if((ang<pi/2),E1_x-E2_x,E1_x+E2_x)
Ey_m      if((ang<pi/2),E1_y-E2_y,E1_y+E2_y)
Ex_p      if((ang<pi/2),E1_x+E2_x,E1_x-E2_x)
Ey_p      if((ang<pi/2),E1_y+E2_y,E1_y-E2_y)
cosB      ((withsol('sol1',ec.Ex)*withsol('sol2',ec.Ex))+(withsol('sol1',ec.Ey)*withsol('sol2',ec.Ey)))/(E1_amp*E2_amp)
ang       acos(cosB)
sinB      sin(acos(cosA))
cosA      if((ang<pi/2),cosB,((E1_x)*(-E2_x)+(E1_y)*(-E2_y))/(E1_amp*E2_amp))
tot_cross term_cross/sqrt((Ex_m)^2+(Ey_m)^2)
term_cross 2*E1_amp*E2_amp*sinB
cosBB     if((ang<pi/2),(-(E2_amp)^2+(E1_x*E2_x)+(E1_y*E2_y))/(E2_amp*sqrt((Ex_m)^2+(Ey_m)^2)),(-(E2_amp)^2+(E1_x*-E2_x)+(E1_y*-E2_y))/(E2_amp*sqrt((Ex_m)^2+(Ey_m)^2)))
sinBB     sin(acos(cosBB))
AM_vector if((E2_amp<E1_amp*cosA),2*E2_amp,2*E2_amp*sinBB)
```

---

## 단계별 물리적 의미

### Step 1 — 진폭 재정렬

```
E1_amp = max(|E_CH1|, |E_CH2|)   ← 항상 더 큰 채널
E2_amp = min(|E_CH1|, |E_CH2|)   ← 항상 더 작은 채널
```

AM_max 계산에서 두 채널의 크기를 정렬하여 기하학적 처리를 단순화한다.

### Step 2 — 두 전기장 사이 각도

```
cosB = (E1·E2) / (|E1|·|E2|)   ← 내적으로 각도 코사인 계산
ang  = acos(cosB)               ← 두 전기장 벡터 사이 각도 [0, π]
cosA = |cosB|                   ← 항상 양수 (예각/둔각 구분 제거)
```

### Step 3 — 최소/최대 간섭 벡터

```
               ang < 90°        ang ≥ 90°
Em (소멸) =   E1 - E2          E1 + E2
Ep (보강) =   E1 + E2          E1 - E2
```

두 벡터 각도에 따라 보강/소멸 간섭 방향이 바뀌므로 조건 분기.

### Step 4 — AM_vector 최종 계산

$$\text{AM\_vector}(r) = \begin{cases} 2A_2 & \text{if } A_2 < A_1 |\cos\theta| \\ 2A_2 \sin\beta\beta & \text{otherwise} \end{cases}$$

**Case 1** ($A_2 < A_1|\cos\theta|$): E1의 E2방향 projection이 E2보다 크다.  
→ 최적 신경 방향 = E2 방향, AM_max = $2A_2$

**Case 2** ($A_2 \geq A_1|\cos\theta|$): 균형 최적화 필요.  
→ sinBB = E2와 Em(소멸벡터) 사이 각도의 sin, AM_max = $2A_2 \cdot \sin\beta\beta$

---

## 검증

| 조건 | AM_vector | 기댓값 |
|------|-----------|--------|
| $E_1 \parallel E_2$ (θ=0°) | $2 \cdot \min(A_1, A_2)$ | Grossman 2017 공식 ✅ |
| $E_1 \perp E_2$ (θ=90°) | $\dfrac{2A_1 A_2}{\sqrt{A_1^2+A_2^2}}$ | 기하학적 계산 ✅ |

---

## COMSOL 등록 방법

```
Component 1 → Definitions → Variables 우클릭 → Variables
→ 위 변수 목록을 순서대로 입력 (Name / Expression / Unit / Description)
→ Study 1, 2 Compute 완료 후 Results에서 AM_vector 사용 가능
```

Results에서 확인:
```
2D Plot Group → Surface → Expression: AM_vector
```

---

## Export 및 Python 연동

COMSOL Export 시 포함할 컬럼:

| Expression | Python 컬럼명 |
|-----------|--------------|
| `x` | x |
| `y` | y |
| `withsol('sol1',ec.Ex)` | ch1_Ex |
| `withsol('sol1',ec.Ey)` | ch1_Ey |
| `withsol('sol2',ec.Ex)` | ch2_Ex |
| `withsol('sol2',ec.Ey)` | ch2_Ey |
| `withsol('sol1',ec.normE)` | ch1_normE |
| `withsol('sol2',ec.normE)` | ch2_normE |
| `AM_vector` | am_max |
| `Ex_m` | Ex_m |
| `Ey_m` | Ey_m |
| `sqrt((Ex_m)^2+(Ey_m)^2)` | E_min |

→ `dual_overlay_map.py` 에서 바로 로드 가능

---

## 관련 파일

- `2D_2phase_max.txt` — COMSOL Variables 원본
- `dual_overlay_map.py` — Python 시각화 코드
- `tis_mdi_analysis.py` — MDI 분석 코드
- `COMSOL_simulation_guide.md` — 전체 시뮬레이션 절차
