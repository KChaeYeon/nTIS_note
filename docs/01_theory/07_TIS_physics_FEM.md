# TIS 전기장 계산 원리 — FEM 물리와 Peak Ratio 완전 이해

> 작성: 2026-06-16 | 대상: TIS FEM 논문 리뷰 준비 — Kim 2023 방법론 완전 이해
>
> 관련 파일: [TIS 원리 기초](04_tis_complete_guide.md) | [경골신경 TIS](05_tibial_nerve_TIS.md)

---

## 목차

1. [Part 1. Maxwell → Quasi-Static → Laplace 방정식](#part-1-maxwell--quasi-static--laplace-방정식)
2. [Part 2. TI 전기장 수식의 물리적 의미](#part-2-ti-전기장-수식의-물리적-의미)
3. [Part 3. Peak Ratio (PR) 지표 완전 해부](#part-3-peak-ratio-pr-지표-완전-해부)
4. [Part 4. PR 지표의 구조적 한계](#part-4-pr-지표의-구조적-한계)
5. [Part 5. 우리 연구에 주는 함의](#part-5-우리-연구에-주는-함의)

---

## Part 1. Maxwell → Quasi-Static → Laplace 방정식

### 1-1. 출발점: Maxwell 방정식

생체조직에 전류를 흘릴 때 전기장이 어떻게 분포하는지를 기술하는 완전한 방정식:

$$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t} \quad \text{(Faraday 법칙)}$$

$$\nabla \times \mathbf{H} = \mathbf{J} + \frac{\partial \mathbf{D}}{\partial t} \quad \text{(Ampere 법칙)}$$

$$\nabla \cdot \mathbf{D} = \rho, \quad \nabla \cdot \mathbf{B} = 0$$

이것을 그대로 풀면 계산이 매우 복잡하다. Kim 2023은 **Ohmic Quasi-Static 근사**를 적용한다.

---

### 1-2. Quasi-Static 근사 — 왜 성립하는가

근사 조건: **변위 전류 $\partial \mathbf{D}/\partial t$를 무시할 수 있는가?**

조건 성립 여부: $\sigma \gg \omega\varepsilon$

발목 피부 기준으로 수치 검증 (carrier 2 kHz):

| 물리량 | 값 |
|--------|---|
| 전도도 $\sigma$ | 0.17 S/m |
| 비유전율 $\varepsilon_r$ | ~1,000 (피부, kHz 범위) |
| 각주파수 $\omega = 2\pi \times 2000$ | 12,566 rad/s |
| 변위 전류 $\omega\varepsilon_0\varepsilon_r$ | $\approx 1.1\times10^{-4}$ S/m |

$$\frac{\sigma}{\omega\varepsilon} = \frac{0.17}{1.1\times10^{-4}} \approx 1{,}545 \gg 1 \quad \checkmark$$

**전도 전류가 변위 전류보다 1,545배 크다 → 변위 전류 완전히 무시 정당.**

추가 조건: 자기 유도 효과 무시 ($\partial \mathbf{B}/\partial t \approx 0$)  
→ 전극 간 거리가 파장보다 훨씬 짧음 (2 kHz 파장 = 150 m >> 발목 크기 수 cm) ✅

---

### 1-3. 단순화 결과 → Generalized Laplace 방정식

두 근사 적용 후 Maxwell 방정식이 극적으로 단순해진다:

$$\nabla \times \mathbf{E} \approx 0 \implies \mathbf{E} = -\nabla V$$

$$\mathbf{J} = \sigma\mathbf{E} = -\sigma\nabla V \quad \text{(Ohm의 법칙)}$$

전류 연속 조건 $\nabla \cdot \mathbf{J} = 0$ 적용:

$$\boxed{\nabla \cdot (\sigma \nabla V) = 0}$$

이것이 **Generalized Laplace 방정식**이며, FEM(유한요소법)이 실제로 푸는 방정식이다.

```
발목 횡단면 (FEM 모델):

     ┌──────────────────────────────────┐
     │         피부  σ=0.17 S/m         │
     │   ┌──────────────────────────┐   │
     │   │    지방  σ=0.057 S/m     │   │
     │   │   ┌──────────────────┐   │   │
     │   │   │  근육  σ=0.355   │   │   │
     │   │   │   ┌────┐         │   │   │
     │   │   │   │ 뼈 │         │   │   │
     │   │   │   └────┘         │   │   │
     │   │   │  ★ 경골신경      │   │   │
     │   │   │    σ=0.265 S/m   │   │   │
     │   │   └──────────────────┘   │   │
     │   └──────────────────────────┘   │
     └──────────────────────────────────┘

[+]전극                              [-]전극
  │                                    │
  └────────── 전류 J 흐름 ─────────────┘

FEM: 각 메쉬 요소에서 V 계산 → E = -grad(V)
```

---

### 1-4. 경계 조건

| 위치 | 조건 | 물리적 의미 |
|------|------|------------|
| 전극 표면 | $-\sigma\nabla V \cdot \hat{n} = J_0$ | 주입 전류 밀도 지정 |
| 피부 외벽 | $\mathbf{J} \cdot \hat{n} = 0$ | 전류가 피부 밖으로 나가지 않음 |
| 조직 계면 | $V$, $\mathbf{J}\cdot\hat{n}$ 연속 | 계면에서 전류 보존 |

**핵심**: 각 TIS 채널을 **독립적으로** 풀어서 공간 분포를 계산:

- 채널 1만 켰을 때 → $\mathbf{E}_1(\mathbf{r})$ (공간 전기장 분포)
- 채널 2만 켰을 때 → $\mathbf{E}_2(\mathbf{r})$ (공간 전기장 분포)

---

## Part 2. TI 전기장 수식의 물리적 의미

### 2-1. 두 채널의 시간 영역 중첩

$$\mathbf{E}_\text{total}(\mathbf{r}, t) = \mathbf{E}_1(\mathbf{r}) \cos(2\pi f_1 t) + \mathbf{E}_2(\mathbf{r}) \cos(2\pi f_2 t)$$

여기서 $f_2 = f_1 + \Delta f$, $\Delta f \ll f_1$.

$\mathbf{E}_1(\mathbf{r})$, $\mathbf{E}_2(\mathbf{r})$는 FEM으로 계산한 **정적 공간 분포**이며, 시간 의존성은 코사인 곱으로 들어온다.

---

### 2-2. Envelope 유도

한 공간점 $\mathbf{r}$에서, $\mathbf{E}_1 \parallel \mathbf{E}_2$ 단순화:

$$E(t) = E_1 \cos(\omega_1 t) + E_2 \cos((\omega_1 + \Delta\omega) t)$$

복소 Phasor 표현:

$$E(t) = \text{Re}\!\left[e^{j\omega_1 t} \underbrace{\left(E_1 + E_2 e^{j\Delta\omega t}\right)}_{\text{천천히 변하는 포락선 } A(t)}\right]$$

**Envelope amplitude** ($\Delta f$ 주파수로 진동):

$$A(t) = \left|E_1 + E_2 e^{j\Delta\omega t}\right| = \sqrt{E_1^2 + E_2^2 + 2E_1 E_2 \cos(\Delta\omega t)}$$

최대·최소:

$$A_\text{max} = E_1 + E_2 \quad (\cos = +1, \text{ 완전 보강})$$

$$A_\text{min} = |E_1 - E_2| \quad (\cos = -1, \text{ 최대 상쇄})$$

**Envelope 진동 폭 = TI 전기장:**

$$\boxed{E_\text{TI}(\mathbf{r}) = \Big|\,|\mathbf{E}_1(\mathbf{r}) + \mathbf{E}_2(\mathbf{r})| - |\mathbf{E}_1(\mathbf{r}) - \mathbf{E}_2(\mathbf{r})|\,\Big|}$$

---

### 2-3. 세 가지 케이스로 이해

**케이스 1: $E_1 = E_2 = E$ (완전 변조)**

$$E_\text{TI} = |(E+E) - |E-E|| = |2E - 0| = 2E \quad \leftarrow \text{최대 TI 효과}$$

```
Envelope:
2E ─────╮      ╭──────╮      ╭────
        │╲    ╱│      │╲    ╱│
        │  ╲╱  │      │  ╲╱  │
 0 ─────╯      ╰──────╯      ╰────
     ←── 1/Δf = 50ms (Δf=20Hz) ──→

Δf=20Hz로 0에서 2E까지 완전히 진동
```

**케이스 2: $E_1 \gg E_2$ (Undermodulation)**

$$E_\text{TI} = |(E_1+E_2) - (E_1-E_2)| = 2E_2 \quad \leftarrow \text{약한 채널이 TI 크기 결정!}$$

```
Envelope:
E1+E2 ──╮      ╭──────╮      ╭────
         │╲    ╱│      │╲    ╱│
         │  ╲╱  │      │  ╲╱  │
E1-E2 ───╯      ╰──────╯      ╰────

진동 폭 = (E1+E2) - (E1-E2) = 2E2  → 작음
```

**케이스 3: $\mathbf{E}_1 \perp \mathbf{E}_2$ (직교)**

$$|\mathbf{E}_1 + \mathbf{E}_2| = \sqrt{E_1^2+E_2^2} = |\mathbf{E}_1 - \mathbf{E}_2|$$

$$\therefore E_\text{TI} = 0 \quad \leftarrow \text{TI 효과 없음!}$$

---

### 2-4. 왜 심부(교차점)에서만 TI 효과가 최대인가

```
        전극A(+)                 전극A(-)
          │                         │
    ──────●─────────────────────────●──────  피부
          │                         │
          │   E1 강함               │
          │   E2 약함               │
          │                         │
          │      ★ 교차점(경골신경)  │
          │     E1 ≈ E2             │
          │   → E_TI 최대!          │
          │                         │
    ──────●─────────────────────────●──────
          │                         │
        전극B(+)                 전극B(-)

위치별 E_TI 크기:
  전극A 근방: E1 강, E2 약  → E_TI = 2×E2  (작음)
  전극B 근방: E2 강, E1 약  → E_TI = 2×E1  (작음)
  ★ 교차점:  E1 ≈ E2        → E_TI = 2E    (최대!)
```

**이것이 TIS 심부 선택적 자극 원리의 핵심:**  
표적 위치에서만 $E_1 \approx E_2$ 조건이 성립하도록 전극을 배치 → $E_\text{TI}$ 최대화.

---

## Part 3. Peak Ratio (PR) 지표 완전 해부

### 3-1. 정의

$$\text{PR} = \frac{\bar{E}_\text{TI,nerve}}{\bar{E}_\text{TI,total}} = \frac{\dfrac{1}{A_\text{nerve}}\displaystyle\iint_{\text{nerve}} E_\text{TI}(\mathbf{r})\, dA}{\dfrac{1}{A_\text{total}}\displaystyle\iint_{\text{total}} E_\text{TI}(\mathbf{r})\, dA}$$

- **분자**: 경골신경 횡단면 내 $E_\text{TI}$ 평균
- **분모**: 전체 발목 횡단면 내 $E_\text{TI}$ 평균

---

### 3-2. PR 값의 물리적 해석

```
발목 횡단면 E_TI 분포 (최적 전극 배치):

E_TI
높음│                  ╭──╮
    │                 ╱    ╲
    │           ╭─╮  ╱      ╲
    │          ╱   ╲╱        ╲
낮음│─────────╱               ╲──────────
    └─────────────────────────────────── 위치
                    ★
               경골신경 위치

PR = ★ 위치 평균 / 전체 평균
   = 4.206 → 경골신경에 전체 평균의 4.2배 집중
```

| PR 값 | 물리적 의미 |
|-------|-----------|
| **0.039** (최악 배치) | 경골신경에 전체 평균의 4%만 도달 — 거의 무자극 |
| **1.0** | 전기장이 발목 전체에 균등 분포 — 특이성 없음 |
| **3.396** (병렬 최적) | 경골신경에 전체 평균의 3.4배 집중 |
| **4.206** (강도 최적) | 경골신경에 전체 평균의 4.2배 집중 |

**PR 이론적 최대값:**

$$\text{PR}_\text{max} \approx \frac{A_\text{total}}{A_\text{nerve}} \approx \frac{1{,}000\,\text{mm}^2}{5\,\text{mm}^2} = 200$$

실제는 전기장이 주변으로 퍼지므로 훨씬 낮게 나온다.

---

### 3-3. Kim 2023 최적화 3단계의 물리적 의미

```
Level 1: 전극 위상학(topology) 최적화
  ─────────────────────────────────────────
  최악 배치: 전극이 경골신경에서 먼 쪽
             E1, E2 교차점이 경골신경과 일치 안 함
             PR = 0.039

  병렬 최적: E1·E2 교차점이 경골신경 위치에 정확히 일치
             PR = 3.396  (87배 향상!)

  → 전극 배치가 결과의 90%를 결정

Level 2: Parallel → Cross 전환
  ─────────────────────────────────────────
  같은 4개 전극, 연결 방향만 교차
  E1·E2의 방향 alignment 개선
  PR = 3.788  (+12%)

Level 3: 전류 비율 I1:I2 최적화
  ─────────────────────────────────────────
  목표: 경골신경 위치에서 E1 ≈ E2 달성
        → 케이스 1 조건 → E_TI = 2E (최대화)

  총 2 mA, 0.1 mA 단위로 I1:I2 조절
  PR = 4.206  (+11%)
```

---

## Part 4. PR 지표의 구조적 한계

### 한계 1: 평균값 — 공간 분포 정보 소실

```
두 경우 모두 PR = 4 (평균 동일):

경우 A (뾰족):  ─────────▄█▄─────────  국소 집중
경우 B (넓음):  ───────▄▄███▄▄───────  분산

신경 발화: 어느 한 점이 역치 초과하면 발화 →
           경우 A가 더 효율적일 수 있지만 PR은 구별 못함
```

### 한계 2: 절대 역치 없음

```
역치선: ─ ─ ─ ─ ─ ─ ─ ─ ─ (예: 10 V/m)

상황 A: PR=4, 역치 초과 ✅
              ╭──╮
E_TI         ╱    ╲
역치─ ─ ─ ─ ╱─ ─ ─╲─ ─ ─ ─
            │        │

상황 B: PR=4, 역치 미달 ❌
역치─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
       ╭──╮
E_TI  ╱    ╲  (전체적으로 낮은 절대값)
```

→ PR이 같아도 실제 전류가 너무 작으면 신경 발화 없음

### 한계 3: 전기장 방향 무시

경골신경은 발목에서 **세로 방향**(종아리 → 발 방향, $\hat{z}$)으로 주행.  
실제 신경 발화를 유발하는 성분:

$$E_{\text{효과적}} = \mathbf{E}_\text{TI}(\mathbf{r}) \cdot \hat{z}$$

PR은 $|\mathbf{E}_\text{TI}|$ (크기)만 사용 → 경골신경 방향과의 **정렬 효율 무시**.

### 한계 4: Budde 2023과의 충돌

$E_\text{TI}$ 수식은 Grossman 2017의 **envelope extraction 가정**에 기반:

> "뉴런이 진폭 변조 envelope을 추출하여 $\Delta f$ 주파수로 발화한다"

Budde 2023 반론:

> "뉴런은 envelope을 추출하지 않는다. 막은 RC integrator로 작동하며,  
> 발화 결정 요인은 **peak-to-peak amplitude**이다."

Budde 관점에서 더 적절한 자극 지표:

$$E_\text{peak}(\mathbf{r}) = |\mathbf{E}_1(\mathbf{r}) + \mathbf{E}_2(\mathbf{r})|_\text{max} = E_1(\mathbf{r}) + E_2(\mathbf{r})$$

→ 최적 전극 배치는 두 관점 모두 비슷하나, **메커니즘 해석**이 다르다.

---

## Part 5. 우리 연구에 주는 함의

### 5-1. Rat FEM에서 PR 외 추가 지표 도입

| 지표 | 수식 | 장점 |
|------|------|------|
| PR (Kim 2023) | $\bar{E}_\text{nerve} / \bar{E}_\text{total}$ | 집중도 비교 |
| **역치 초과 면적 비율** | $A_\text{nerve}\{E_\text{TI}>E_\text{th}\} / A_\text{nerve}$ | 절대 역치 반영 |
| **E_peak** | $E_1+E_2$ (Budde 관점) | 메커니즘 논쟁 대응 |

### 5-2. Level 3 (전류 비율) 최적화의 실험적 의미

Rat 발목에서 $I_1:I_2$를 조절 → 경골신경 위치에서 $E_1 \approx E_2$ 달성  
→ 케이스 1: $E_\text{TI} = 2E$ (완전 변조)  
→ Cystometry ICI 최대화 가설 → **in vivo로 검증 가능**

### 5-3. Budde 논쟁 in vivo 검증 설계

실험 조건: 총 전류 $I_1+I_2$ 고정, $\Delta f$만 변경

```
그룹 A: Δf = 20 Hz (PTNS 표준)
그룹 B: Δf = 100 Hz
그룹 C: Δf = 0 Hz (Sham — carrier만, envelope 없음)
그룹 D: PTNS (비교)

ICI 결과:
  Δf 의존성 있음 → Envelope extraction 지지 (Grossman)
  Δf 무관, 총 진폭만 중요 → RC integrator 지지 (Budde)
```

이 결과 자체가 **논문의 추가 기여**가 된다.

---

*Last updated: 2026-06-16 — TIS FEM 물리 + PR 지표 + 실험 설계 함의*
