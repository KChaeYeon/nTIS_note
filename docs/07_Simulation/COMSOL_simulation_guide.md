# COMSOL TIS 시뮬레이션 사용법

> **환경**: COMSOL Multiphysics 6.3 · AC/DC Module · 2D → 3D 순차 진행  
> **목적**: 2-채널 Temporal Interference Stimulation (TIS) 전기장 시뮬레이션

---

## 목차

1. [새 모델 만들기](#1-새-모델-만들기)
1.5. [Material 물성값 참고표](#material-물성값-참고표)
2. [Geometry 생성](#2-geometry-생성)
3. [Materials 설정](#3-materials-설정)
4. [경계조건 (Physics) 설정](#4-경계조건-physics-설정)
5. [Mesh 설정](#5-mesh-설정)
6. [Study 설정 및 실행](#6-study-설정-및-실행)
7. [결과 후처리](#7-결과-후처리)
8. [TIS AM Envelope 계산](#8-tis-am-envelope-계산)

---

## 배경: 왜 Stationary Study를 쓰는가

TIS에서 사용하는 주파수(1 kHz, 1.04 kHz)는 생체조직 내에서 **quasi-static** 조건을 만족한다.

$$\lambda = \frac{v}{f} \gg L_{\text{model}}$$

- 1 kHz에서 조직 내 전자기파 파장 >> 모델 크기(수 cm)
- → 공간적 전기장 분포는 **주파수에 무관**
- → 채널 1, 채널 2를 각각 **Stationary Study**로 따로 풀고, 후처리에서 합산 가능

---

## 1. 새 모델 만들기

### 1-1. Model Wizard 시작

```
File → New → Model Wizard
```

### 1-2. 공간 차원 선택

```
Space Dimension: 2D → Next
```

### 1-3. Physics 추가

```
AC/DC → Electric Currents (ec) → Add
```

### 1-4. Study 유형 선택

```
General Studies → Stationary → Done
```

완료 후 Model Builder 트리:

```
Model 1 (comp1)
├── Geometry 1          ← 형상 정의
├── Materials           ← 물성값
├── Electric Currents (ec)
│   ├── Current Conservation 1
│   ├── Electric Insulation 1
│   └── Initial Values 1
├── Mesh 1
└── Study 1
    └── Stationary
```

---

## 2. Geometry 생성

### 현재 설정 (2D 사각형 팬텀)

| 항목 | 값 |
|------|-----|
| 단위 | mm |
| 팬텀 형태 | Rectangle (사각형) |
| 크기 | 50 × 50 mm |
| 중심 | (0, 0) |
| 전극 수 | 4개 (원형, 각 모서리) |

### 2-1. 단위 설정

```
Geometry 1 클릭 → Settings 창 → Length unit: mm
```

### 2-2. 사각형 팬텀 추가

```
Geometry 1 우클릭 → Rectangle
```

| 파라미터 | 값 |
|---------|-----|
| Width | 50 mm |
| Height | 50 mm |
| Base | Center |
| x, y | 0, 0 |

→ **Build Selected**

### 2-3. 전극 원 추가 (4개)

각 전극은 팬텀 경계 위에 위치하는 원형 영역이다.  
채널 1 전극 쌍(E1+, E1−)과 채널 2 전극 쌍(E2+, E2−)으로 구성된다.

```
Geometry 1 우클릭 → Circle
```

전극 위치 (대각선 배치):

| 전극 | 역할 | 위치 (x, y) mm | 반지름 |
|------|------|----------------|--------|
| E1+ | CH1 Terminal | (-25, +21) | 2 mm |
| E1− | CH1 Ground   | (+25, −21) | 2 mm |
| E2+ | CH2 Terminal | (+25, +21) | 2 mm |
| E2− | CH2 Ground   | (−25, −21) | 2 mm |

> **Note**: 전극이 팬텀 경계에 걸쳐 있으면 Form Union 후 자동 분리됨

### 2-4. Form Union 적용

```
Geometry 1 우클릭 → Boolean and Partitions → Form Union
→ Build All Objects
```

완료 메시지 확인:
```
Finalized geometry has N domains, M boundaries, and K vertices.
```

전극 원 4개 + 팬텀 1개 = **5 domains** (원이 팬텀 내부에 있을 경우)  
또는 전극이 경계에 걸쳐 있으면 domains 수가 달라질 수 있음.

---

## Material 물성값 참고표

### 수치 신뢰도 분류

| 수치 | 상태 |
|------|------|
| σ_saline = 1.5 S/m | ✅ 확립된 측정값 |
| σ_gray matter = 0.07 S/m (1 kHz) | ✅ Gabriel et al. 1996 측정값 |
| σ_metal ≈ 10⁶ S/m | ✅ 재료공학 표준값 |
| ε_r_saline = 80 | ✅ 확립된 측정값 |
| ε_r_tissue (주파수별) | ⚠️ 연구마다 다름, Gabriel et al. 원문 확인 필요 |

---

### 생리식염수 σ = 1.5 S/m — 근거

0.9% NaCl 용액의 전기전도는 **이온 이동**으로 발생한다.

$$\sigma = \sum_i n_i q_i \mu_i$$

- $n_i$: 이온 농도 (0.9% NaCl → 154 mmol/L)
- $q_i$: 이온 전하
- $\mu_i$: 이온 이동도

**참고문헌 (확립된 측정값)**
- Geddes & Baker (1967) *Medical & Biological Engineering* — 4전극 임피던스 측정
- Horch & Dhillon (2004) *Neuroprosthetics: Theory and Practice*

> ⚠️ 온도 의존: σ는 1°C 상승마다 약 2% 증가 → 체온 37°C에서 σ ≈ 1.7~1.8 S/m

---

### 생체조직 σ — 핵심 참고문헌

**Gabriel et al. (1996)** 이 생체조직 전기적 특성의 표준 데이터베이스다.

> Gabriel S, Lau RW, Gabriel C. (1996)  
> *"The dielectric properties of biological tissues: II. Measurements in the frequency range 10 Hz to 20 GHz"*  
> **Physics in Medicine & Biology, 41(11), 2251–2269**

**1 kHz 기준 측정값:**

| 조직 | σ (S/m) | ε_r |
|------|---------|-----|
| 회백질 (Gray matter) | 0.070 | 1.1 × 10⁷ |
| 백질 (White matter) | 0.050 | 3.7 × 10⁶ |
| 근육 (Muscle) | 0.363 | 1.7 × 10⁶ |
| 뼈 (Cortical bone) | 0.020 | 2.0 × 10⁴ |
| 피부 (Skin) | 0.00045 | 1.1 × 10⁶ |

> ⚠️ **주의**: "σ_brain = 0.33 S/m" 는 일부 논문의 단순화 값이다.  
> Grossman et al. 2017 *Cell*에서 0.33 S/m를 사용했으나, Gabriel et al. 기준 1 kHz 회백질은 0.07 S/m.  
> 본인 시뮬레이션 주파수(1 kHz)에서의 값은 Gabriel et al. 원문에서 직접 확인할 것.

**왜 σ가 주파수마다 다른가?** 생체조직은 분산 매질(dispersive medium)이다:

- 낮은 주파수 (< 10 kHz): 세포막이 전류를 차단 → 세포 외액만 통과 → σ 낮음
- 높은 주파수 (> 1 MHz): 세포막 용량성 임피던스 감소 → 세포 내부까지 통과 → σ 높음

이를 기술하는 모델: **4-Cole-Cole model** (Gabriel et al. 1996)

---

### 금속 전극 σ ≈ 10⁶ S/m — 근거

금속은 자유전자가 전하를 운반하므로 이온 기반 생체조직보다 σ가 수백만 배 높다.

| 재료 | σ (S/m) | 의료기기 사용 여부 |
|------|---------|----------------|
| 백금 (Pt) | 9.43 × 10⁶ | ✅ 임플란트용 표준 |
| 316L 스테인리스강 | 1.35 × 10⁶ | ✅ 수술 기구, 전극 |
| 금 (Au) | 4.10 × 10⁷ | ✅ 마이크로전극 |

> σ_전극 >> σ_조직 조건이 충족되면 전극 내부는 사실상 등전위체(equipotential body)에 가까움.  
> 시뮬레이션에서 1×10⁶ S/m 로 설정해도 결과에 실질적 차이 없음.

---

### 생리식염수 ε_r = 80 — 근거

물 분자는 영구 쌍극자(permanent dipole)를 가지고 있어 전기장에 정렬된다.

$$\varepsilon_r \approx 78\text{–}80 \quad \text{(25°C, 순수 물 기준)}$$

NaCl을 녹여도 ε_r은 크게 변하지 않음 → 생리식염수 ε_r ≈ 80 유지.

> **Stationary study에서는 ε_r이 사용되지 않음.**  
> 전류 보존 방정식: $\nabla \cdot (\sigma \nabla V) = 0$ → σ만 필요.  
> ε_r은 Frequency Domain study에서만 영향을 줌.

---

## 3. Materials 설정 (COMSOL 조작)

현재 모델에는 **2종류의 도메인**이 있다:

```
도메인 종류
├── 팬텀 (Rectangle 내부)  → 생체조직 or 식염수
└── 전극 원 4개 (Circle)   → 금속 전극
```

### 3-1. 팬텀 재료 추가

```
Materials 우클릭 → Blank Material → 이름: "Phantom"
→ Geometric Entity Selection → Domain: Rectangle 내부 선택
→ Material Contents → Electrical conductivity: 1.5  [S/m]
```

### 3-2. 전극 재료 추가

```
Materials 우클릭 → Blank Material → 이름: "Electrode"
→ Domain: 전극 원 4개 선택 (Ctrl+클릭 다중 선택)
→ Electrical conductivity: 1e6  [S/m]
```

### 3-3. 할당 확인

```
Materials 트리 → 각 재료 옆에 ✓ 표시 확인
→ ✗ 또는 노란 경고 표시 = 미할당 도메인 있음
```

---

## 4. 경계조건 (Physics) 설정

### 핵심 원리

2채널 TIS에서는 **Physics 트리에 4개 BC를 모두 정의**하되, **각 Study에서 해당 채널만 활성화**한다.

```
Physics 트리 (전체)          Study 1 (CH1)       Study 2 (CH2)
├── Terminal 1 (E1+)  ──→    ✅ 활성화           ❌ 비활성화
├── Ground 1   (E1-)  ──→    ✅ 활성화           ❌ 비활성화
├── Terminal 2 (E2+)  ──→    ❌ 비활성화         ✅ 활성화
└── Ground 2   (E2-)  ──→    ❌ 비활성화         ✅ 활성화
```

이 제어는 COMSOL의 **"Modify model configuration for study step"** 옵션으로 수행한다.

---

### 4-1. Physics 트리에 BC 4개 추가

**Electric Currents (ec)** 우클릭 → 아래 4개 순서대로 추가:

#### Terminal 1 — CH1 인가 전극

```
Electric Currents → 우클릭 → Terminal
  이름: Terminal 1
  Boundary selection: E1+ 전극의 경계선 선택
  Terminal type: Current
  I₀ = 1e-3  [A]   (= 1 mA)
```

#### Ground 1 — CH1 귀환 전극

```
Electric Currents → 우클릭 → Ground
  이름: Ground 1
  Boundary selection: E1− 전극의 경계선 선택
```

#### Terminal 2 — CH2 인가 전극

```
Electric Currents → 우클릭 → Terminal
  이름: Terminal 2
  Boundary selection: E2+ 전극의 경계선 선택
  Terminal type: Current
  I₀ = 1e-3  [A]
```

#### Ground 2 — CH2 귀환 전극

```
Electric Currents → 우클릭 → Ground
  이름: Ground 2
  Boundary selection: E2− 전극의 경계선 선택
```

완료 후 Physics 트리:

```
Electric Currents (ec)
├── Current Conservation 1   (전체 도메인 — 자동)
├── Electric Insulation 1    (외부 경계 — 자동)
├── Initial Values 1
├── Terminal 1               ← CH1 인가
├── Ground 1                 ← CH1 귀환
├── Terminal 2               ← CH2 인가
└── Ground 2                 ← CH2 귀환
```

---

### 4-2. Study 1에서 CH2 비활성화

```
Study 1 → Stationary 클릭
→ Settings 창 하단 → "Study Extensions" 섹션 펼치기
→ ☑ Modify model configuration for study step  체크
```

체크 후 나타나는 Physics feature 테이블에서:

| Physics Feature | Study 1 설정 |
|----------------|-------------|
| Terminal 1 | (켜짐 — 기본값 유지) |
| Ground 1 | (켜짐 — 기본값 유지) |
| Terminal 2 | **Disable** 선택 |
| Ground 2 | **Disable** 선택 |

---

### 4-3. Study 2 추가 및 CH1 비활성화

```
Home 탭 → Add Study → Stationary
→ Study 2 생성됨

Study 2 → Stationary 클릭
→ Study Extensions → ☑ Modify model configuration for study step
```

| Physics Feature | Study 2 설정 |
|----------------|-------------|
| Terminal 1 | **Disable** |
| Ground 1 | **Disable** |
| Terminal 2 | (켜짐 — 기본값 유지) |
| Ground 2 | (켜짐 — 기본값 유지) |

---

### 4-4. 외부 경계: Electric Insulation 확인

팬텀 외부 경계(전극이 닿지 않는 변)는 전류가 빠져나가지 않아야 한다.

```
Electric Insulation 1 → Settings → Boundary selection 확인
→ 팬텀 4개 변 중 전극 경계를 제외한 나머지가 포함되어 있는지 확인
```

> COMSOL 기본 BC가 Electric Insulation이므로, Terminal/Ground로 명시하지 않은 경계는 자동으로 절연 처리된다.

---

### 4-5. 검증 (계산 전 사전 확인)

Study 1 Stationary 우클릭 → **Get Initial Value** 실행 (Compute 아님):

| 결과 | 원인 |
|------|------|
| 에러 없이 통과 | BC 할당 정상 |
| "No terminal" 에러 | Terminal 경계 미선택 |
| "Conflicting BCs" | 같은 경계에 Terminal+Ground 중복 할당 |

---

## 5. Mesh 설정

```
Mesh 1 → Physics-controlled mesh
→ Element size: Normal (처음) → Fine (검증 후)
→ Build All
```

완료 확인:
```
Complete mesh consists of N domain elements and M boundary elements.
```

> **Mesh convergence**: 나중에 Normal → Fine → Finer 순으로 결과 변화 확인 필요

---

## 6. Study 설정 및 실행

### Study 1: 채널 1

```
Study 1 → Stationary
→ Compute (F8 또는 상단 버튼)
```

### Study 2: 채널 2 추가

```
Home 탭 → Add Study → Stationary
→ Study 2가 생성됨
→ 채널 2 경계조건이 활성화되도록 설정
→ Compute
```

---

## 7. 결과 후처리

### 7-1. Electric Potential Map

```
Results → 2D Plot Group → Surface
→ Expression: V  (또는 ec.V)
→ Unit: V
```

### 7-2. Electric Field Map

```
Results → 2D Plot Group → Surface
→ Expression: ec.normE
→ Unit: V/m
```

전기장 벡터 방향 추가:

```
→ Arrow Surface 추가
→ x-component: ec.Ex  
→ y-component: ec.Ey
```

### 7-3. COMSOL 변수 참조표 (Electric Currents, ec)

| 변수 | 의미 | 단위 |
|------|------|------|
| `ec.V` | Electric potential | V |
| `ec.Ex` | E-field x-component | V/m |
| `ec.Ey` | E-field y-component | V/m |
| `ec.normE` | \|E\| (magnitude) | V/m |
| `ec.Jx` | Current density x | A/m² |
| `ec.Jy` | Current density y | A/m² |
| `ec.normJ` | \|J\| (magnitude) | A/m² |

---

## 8. TIS AM Envelope 계산

### 이론적 배경

채널 1, 2의 전기장 벡터를 **E1**, **E2**라 하면, 시간에 따른 합성 전기장은:

$$\mathbf{E}(t) = \mathbf{E}_1 \cos(2\pi f_1 t) + \mathbf{E}_2 \cos(2\pi f_2 t)$$

beat frequency = $\Delta f = f_2 - f_1$ (여기서는 40 Hz)

### AM Envelope 공식 (Vector 방식)

$$\text{AM}_{\text{vec}} = \|\mathbf{E}_1 + \mathbf{E}_2\| - \|\mathbf{E}_1 - \mathbf{E}_2\|$$

이 값이 양수인 곳 → 신경 활성화 가능 영역

### COMSOL Derived Values / Expression에서 계산

Study 1 결과를 `sol1`, Study 2 결과를 `sol2`로 참조:

```
Ex1 = withsol('sol1', ec.Ex)
Ey1 = withsol('sol1', ec.Ey)
Ex2 = withsol('sol2', ec.Ex)  (Study 3이면 'sol3')
Ey2 = withsol('sol2', ec.Ey)

AM_vector = sqrt((Ex1+Ex2)^2 + (Ey1+Ey2)^2)
           - sqrt((Ex1-Ex2)^2 + (Ey1-Ey2)^2)
```

> **주의**: `withsol('solN', ...)` 구문에서 N은 실제 solution 번호와 일치해야 함  
> COMSOL 6.3에서 확인: Results → Datasets → Study N/Solution N

---

## 검증 체크리스트

- [ ] Form Union 완료 → geometry 도메인 수 확인
- [ ] σ 단위 S/m로 입력됨
- [ ] Study 1 실행 → Electric Potential 분포 좌우 비대칭 확인 (전류 흐름 방향)
- [ ] Study 2 실행 → Study 1과 다른 방향의 전위 분포 확인
- [ ] 두 채널 superposition 후 AM map 중심 집중 여부 확인

---

## 파일 명명 규칙

```
YYYYMMDD_TIS_[설명]_[팬텀크기].mph
예: 20260630_TIS_2ch_rect50x50mm.mph
```

---

## 참고 문헌

- Grossman et al. (2017) *Cell* — TIS 원리 및 AM envelope 정의
- Dmochowski et al. (2017) *J Neural Eng* — 전극 최적화
- COMSOL 6.3 AC/DC Module User Guide
