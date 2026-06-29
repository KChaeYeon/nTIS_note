# STEP 7: 전극 위치에 따른 AM 전기장 맵 변화

> 작성일: 2026-06-29 | 기반: Grossman et al., Cell 2017; COMSOL 시뮬레이션 (송솔웅)

## 학습 목표

1. 표준 4전극 TIS 설정에서 중심점 전기장 방향(E₁∥E₂)을 유도할 수 있다
2. X축 수렴 시 AM zone이 좁고 밝은 수직 컬럼으로 집속되는 이유를 설명할 수 있다
3. Y축 수렴 시 AM이 약해지는 이유를 쌍극자 모멘트 공식으로 설명할 수 있다
4. COMSOL 시뮬레이션 결과 맵을 물리적으로 해석할 수 있다

---

## 1. COMSOL 시뮬레이션 설정

### 모델 구성

```
원형 단면 팬텀 (균일 σ):
  - 4전극 TIS (Ch1: 좌측 수직 쌍극자, Ch2: 우측 수직 쌍극자)
  - Ch1: 1,000 Hz, Ch2: 1,040 Hz  →  Δf = 40 Hz envelope
  - 지배방정식: ∇·(σ∇φ) = 0  (준정적 근사, λ = 50 km >> 팬텀)
  - AM_max 계산: E_AM_max = max_{n̂} 2·min(|E⃗₁·n̂|, |E⃗₂·n̂|)
```

### 시뮬레이션 시리즈

| 폴더 | 프레임 | 변화 방향 | 물리적 의미 |
|------|--------|-----------|------------|
| `Figures/Horizontal/` | 1→17 | X축 이동 | 전극 수평 이동에 따른 AM zone 위치 변화 |
| `Figures/Vertical/` | 1→34 | Y축 이동 | 전극 수직 이동에 따른 AM zone 위치·세기 변화 |
| `Figures/1to5.png` | — | 실제 해부학 | Rat 경골 단면 + tibial nerve 위치 |

---

## 2. 기초 물리 — 3가지 핵심 개념

### 2-1. 쌍극자 전기장

전극 쌍(+, -)이 만드는 원거리 전기장:

$$E_\text{far} \propto \frac{p}{r^3} = \frac{I \cdot d}{r^3}$$

- $p = I \times d$: 쌍극자 모멘트 [A·m]
- $I$: 채널 전류 (1 mA 고정)
- $d$: 쌍극자 내부 전극 간격
- $r$: 관심 지점까지의 거리

### 2-2. AM_max 조건

$$E_\text{AM\_max} = \max_{\hat{n}} \ 2 \cdot \min(|\vec{E}_1 \cdot \hat{n}|, |\vec{E}_2 \cdot \hat{n}|)$$

| E₁, E₂ 관계 | AM 효율 |
|------------|--------|
| E₁ ∥ E₂ (평행) | 최대: $2 \cdot \min(\|E_1\|, \|E_2\|)$ |
| E₁ ⊥ E₂ (수직) | ≈ 0 |

### 2-3. 표준 4전극 중심점에서 전기장 방향

```
    +● Ch1(1kHz)    +● Ch2(1.04kHz)
     |    ←L→         |
    -● Ch1           -● Ch2
         ↑
      중심점 (0,0)

중심점에서:  E⃗₁ = (0, -kₑqd/L³)  →  -y 방향
            E⃗₂ = (0, -kₑqd/L³)  →  -y 방향
            ∴ E⃗₁ ∥ E⃗₂  →  AM 효율 최대
```

*(Grossman et al., Cell 2017, Supplementary)*

---

## 3. X축 수렴 — 집속(Focusing) 효과

**변화**: 채널 간 수평 거리 $L$ 감소

### 전기장 증가 메커니즘

$$E_\text{center} \propto \frac{1}{L^3}$$

| L | 전기장 비율 |
|---|----------|
| 20 mm | 기준 (×1) |
| 10 mm | ×8 (2³) |
| 5 mm  | ×64 (4³) |

### 수직 컬럼 형성 이유

중심선(y축) 위 임의 점 $(0, y)$에서:

$$E_{1x} = +\frac{3k_e qd \cdot yL}{(L^2+y^2)^{5/2}}, \quad E_{2x} = -\frac{3k_e qd \cdot yL}{(L^2+y^2)^{5/2}}$$

$$E_{1y} = E_{2y} = \frac{k_e qd \cdot (2y^2 - L^2)}{(L^2+y^2)^{5/2}}$$

→ x 성분: **상쇄** (AM 기여 없음)  
→ y 성분: **평행 보강** → AM 활성 영역이 수직 띠 형태

### COMSOL 시뮬레이션 결과 (Horizontal 시리즈)

> 프레임 진행에 따라 AM zone 위치 이동 + 집속 관찰

**해석**:
- 대칭 배치(Horizontal/1): AM zone 중앙 수직 타원 형태
- 한쪽 채널 수평 이동: AM zone이 전극 중간 지점을 따라 이동
- 두 채널 수평 근접: AM zone 좁아지고 밝아짐 (집속 효과)

---

## 4. Y축 수렴 — 소멸(Defocusing) 효과

**변화**: 각 채널 내부 전극 간격 $d$ 감소

### 쌍극자 모멘트 감소

$$p = I \times d \quad (I = 1 \text{ mA 고정})$$

| d | p | 원거리 E |
|---|---|---------|
| 20 mm | 20 (기준) | 기준 |
| 10 mm | 10 | 1/2 |
| 5 mm  |  5 | 1/4 |
| → 0   | → 0 | → 0 |

### AM 약화 과정

$$d = 20 \text{ mm}: \quad E_1=E_2=10 \Rightarrow AM = 2\times\min(10,10) = 20$$
$$d = 10 \text{ mm}: \quad E_1=E_2=5  \Rightarrow AM = 2\times\min(5,5)  = 10$$
$$d \to 0: \quad E_1,E_2 \to 0 \Rightarrow AM \to 0$$

### 주의: 근전극 효과

전극 바로 옆 근거리에서는 전류 밀도 집중으로 전기장이 강해지지만,  
**AM은 E₁과 E₂가 동시에 겹치는 지점에서만 발생** →  
전극 직근방에는 Ch2의 E₂가 없으므로 AM 발생 불가.

### COMSOL 시뮬레이션 결과 (Vertical 시리즈)

> 프레임 진행에 따라 AM zone 위치 이동 + 점진적 약화

**해석**:
- 초기(Vertical/1): AM zone 중앙, 대칭
- 중간(Vertical/17): AM zone 상방 이동, 크기 감소, 밝기 감소
- 끝(Vertical/34): AM zone 상단 경계, 매우 작고 어두움

---

## 5. 비교 요약

| | X축 수렴 (L↓) | Y축 수렴 (d↓) |
|--|--------------|--------------|
| **변하는 것** | 채널 간 거리 L | 쌍극자 내부 간격 d |
| **전기장 방향** | E₁∥E₂ 유지 ✓ | E₁∥E₂ 유지 ✓ |
| **전기장 세기** | ∝ 1/L³ → 급증 ↑↑ | ∝ I·d → 감소 ↓↓ |
| **AM_max** | 증가, 집속 | 감소, 소멸 |
| **맵 모양** | 좁고 밝은 수직 컬럼 | 전반적으로 어두운 넓은 영역 |
| **물리적 본질** | 두 파원의 중첩 강화 | 파원 자체 세기 감소 |

> **핵심**: 두 경우 모두 E₁∥E₂는 유지되므로 AM 방향성은 동일.  
> 차이는 오직 **세기의 방향**: 집속(↑) vs 소멸(↓).

---

## 6. 관련 논문

- **Grossman N et al.** (2017). *Noninvasive deep brain stimulation via temporally interfering electric fields.* Cell, 169(6), 1029–1041. — AM_max 공식, FEM 파이프라인
- **Rampersad S et al.** (2019). *Prospects for transcranial temporal interference stimulation in humans.* Brain Stimulation. — FEM 검증
- **Kim et al.** (2023). *Optimization Framework for TIS in Tibial Nerves.* — 경골신경 TIS 최적화, PR 최적화

---

## 7. 다음 단계

- [ ] COMSOL dual overlay map 구현 (AM zone + Inhibition zone 동시 시각화)
- [ ] E_th 결정 방법 선택: 교수님 실측값 (Rheobase=25V, Chronaxie=30μs) vs HH 모델
- [ ] 전극 간격 파라미터 스위프 (L, d 체계적 변화)
