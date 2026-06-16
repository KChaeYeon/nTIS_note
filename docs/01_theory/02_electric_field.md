# 전기장 모델 & FEM 방법론

> TIS 시뮬레이션의 수학적 토대: Maxwell → Quasi-Static → FEM → 선형중첩 → TI 포락선

---

## 1. Maxwell 방정식 → Quasi-Static 단순화

생물학적 조직 내 준정적(quasi-static) 조건에서:

$$\nabla \cdot (\sigma \nabla V) = 0$$

여기서 $\sigma$는 전도도 텐서(S/m), $V$는 전위(V).

전기장: $\mathbf{E} = -\nabla V$

**왜 Quasi-Static인가?**

TI 자극 주파수는 수 kHz 수준. 이 범위에서 피부 기준:

| 항 | 값 | 비고 |
|----|-----|------|
| 전도 전류 $\sigma$ | 0.170 S/m | 주된 전류 |
| 변위 전류 $\omega\varepsilon$ | 0.00011 | 1,545배 작음 |

→ 변위 전류 무시 가능 → $\nabla \cdot (\sigma \nabla V) = 0$ 만 풀면 됨.

---

## 2. 선형 중첩 (Linear Superposition) — FEM 효율화의 핵심

### 기준 전극과 단독 해석

24개 전극이 있는 경우 모든 조합을 각각 FEM으로 계산하면 수백 회가 필요하다.

**해결책**: 기준 전극(Reference Electrode, $V = 0$ V 고정)을 정하고, 각 전극에서 **단독으로** FEM을 24회만 실행한다.

$$\mathbf{E}_{A\text{-Ref}},\quad \mathbf{E}_{B\text{-Ref}},\quad \ldots \quad (24\text{회})$$

임의의 A→B 경로 전기장은 뺄셈으로 복원:

$$\mathbf{E}_{A\to B} = \mathbf{E}_{A\text{-Ref}} - \mathbf{E}_{B\text{-Ref}}$$

**왜 성립하는가?** FEM은 선형 시스템($[K]\{V\} = \{f\}$)이므로, 동일한 경계 조건(기준전극 $V=0$)을 공유한 두 해를 빼면 기준점의 기여가 정확히 소거된다.

> **결론**: 24회 FEM → $\binom{24}{4} = 10{,}626$가지 이상의 4전극 조합 모두 계산 가능

---

## 3. TI 포락선 수식 도출

### 두 채널의 독립 전기장

- 채널 1 (경로 A→B, 반송파 $f_1$): $\mathbf{E}_1 = \mathbf{E}_{A\text{-Ref}} - \mathbf{E}_{B\text{-Ref}}$
- 채널 2 (경로 C→D, 반송파 $f_2$): $\mathbf{E}_2 = \mathbf{E}_{C\text{-Ref}} - \mathbf{E}_{D\text{-Ref}}$

### 합성 전기장과 포락선

두 고주파 전기장의 시간 합성:

$$|\mathbf{E}_\text{total}(t)| = |\mathbf{E}_1 \cos(2\pi f_1 t) + \mathbf{E}_2 \cos(2\pi f_2 t)|$$

포락선의 최대·최솟값:

$$E_{\max} = |\mathbf{E}_1 + \mathbf{E}_2|, \qquad E_{\min} = \bigl||\mathbf{E}_1| - |\mathbf{E}_2|\bigr|$$

**TI 자극 포락선** (저주파 성분의 진폭):

$$\boxed{E_{\text{TI}}(\mathbf{r}) = E_{\max} - E_{\min} = \bigl||\mathbf{E}_1 + \mathbf{E}_2| - |\mathbf{E}_1 - \mathbf{E}_2|\bigr|}$$

| 조건 | 결과 |
|------|------|
| $\mathbf{E}_1 = \mathbf{E}_2$ | $E_\text{TI} = 2|\mathbf{E}_1|$ (최대 변조) |
| $\mathbf{E}_1 \gg \mathbf{E}_2$ | $E_\text{TI} \approx 2|\mathbf{E}_2|$ (작음) |
| $\mathbf{E}_1 \perp \mathbf{E}_2$ | $E_\text{TI} = 0$ (자극 없음) |

---

## 4. FEM 구성 요소

### 지배방정식

$$\nabla \cdot (\sigma \nabla V) = 0$$

FEM은 이를 이산화하여 대형 선형 시스템 $[K]\{V\} = \{f\}$로 변환·풀이한다.

### 경계조건

| 경계 | 조건 | 유형 |
|------|------|------|
| 능동 전극 | $V = 1\,\text{V}$ | Dirichlet |
| 기준 전극 | $V = 0\,\text{V}$ | Dirichlet |
| 모델 외부 경계 | 법선 전류 = 0 ($\mathbf{J}\cdot\hat{n}=0$) | Neumann |

### 전류 정규화

FEM 해는 1 V 인가 시의 전위 분포를 준다. 실제 주입 전류 1 mA로 정규화:

$$\mathbf{E}_\text{normalized} = \frac{\mathbf{E}_{1\,\text{V}}}{I_\text{computed}} \times 1\,\text{mA}$$

---

## 5. 전기장 중첩 (Superposition)

TI stimulation에서 두 주파수 성분의 전기장은 선형 중첩:

$$\mathbf{E}_\text{total}(\mathbf{r}, t) = \mathbf{E}_1(\mathbf{r})\cos(2\pi f_1 t) + \mathbf{E}_2(\mathbf{r})\cos(2\pi f_2 t + \phi_0)$$

최대 envelope은 $\mathbf{E}_1 \parallel \mathbf{E}_2$ 조건에서 달성된다.

---

## 6. Peak Ratio (PR) — 집중도 지표 개요

$$\text{PR} = \frac{E_\text{target}}{E_\text{total}}$$

| 항목 | 정의 |
|------|------|
| $E_\text{target}$ | 목표 신경 영역 내 체적 평균 TI 전기장 (V/m) |
| $E_\text{total}$ | 전체 모델 내 체적 평균 TI 전기장 (V/m) |

PR이 클수록 표적 신경에 에너지가 집중된 것.

> 모식도·최적화 단계·PR 한계: [TIS 물리 & FEM 심층](07_TIS_physics_FEM.md)

---

## 7. 수치 해석 소프트웨어

| 소프트웨어 | 특징 | 주 사용처 |
|-----------|------|---------|
| **Sim4Life** | TIS 특화, Ohmic QS 솔버 내장, ViZOO 가상 모델 연계 | 연구용 상업 S/W |
| **COMSOL** | 범용 FEM, Electric Currents 모듈, 팀 보유 | 전극 최적화·Rat 모델 |
| SimNIBS | 뇌 TIS 특화 오픈소스 | tES/TMS 연구 |

---

*Last updated: 2026-06-16*
