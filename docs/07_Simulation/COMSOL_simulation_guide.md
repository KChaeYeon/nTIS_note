# COMSOL TIS 시뮬레이션 사용법

> **환경**: COMSOL Multiphysics 6.3 · AC/DC Module · 2D → 3D 순차 진행  
> **목적**: 2-채널 Temporal Interference Stimulation (TIS) 전기장 시뮬레이션

---

## 목차

1. [새 모델 만들기](#1-새-모델-만들기)
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

## 3. Materials 설정

### 3-1. 팬텀 도메인 재료 추가

```
Materials 우클릭 → Blank Material
```

팬텀(생리식염수 또는 단순 균질 도메인) 물성:

| 물성 | 값 | 단위 |
|------|-----|------|
| Electrical conductivity (σ) | 1.5 | S/m |
| Relative permittivity (ε_r) | 80 | - |

> **Stationary study에서는 σ만 사용됨** (ε_r은 Frequency Domain에서만 영향)

```
Material → Geometric Entity Selection → Domain 선택 (팬텀 영역)
→ Electric → σ 입력
```

---

## 4. 경계조건 (Physics) 설정

### 채널 1 설정

#### 4-1. Terminal (전류 인가 전극)

```
Electric Currents (ec) 우클릭 → Terminal
→ Boundary selection: E1+ 전극 경계 선택
→ Terminal type: Current
→ I0 = 1e-3  [A]  (= 1 mA)
```

#### 4-2. Ground (귀환 전극)

```
Electric Currents (ec) 우클릭 → Ground
→ Boundary selection: E1− 전극 경계 선택
```

### 채널 2 설정 (별도 Study에서)

채널 2는 **Study 2**를 추가하고 동일한 방법으로 설정한다.

```
Electric Currents (ec) 우클릭 → Terminal (CH2용)
→ Boundary: E2+ 선택
→ I0 = 1e-3 [A]

Electric Currents (ec) 우클릭 → Ground (CH2용)
→ Boundary: E2− 선택
```

> **중요**: Study 1 = 채널 1 활성화, Study 2 = 채널 2 활성화  
> 각 Study에서 어떤 Terminal/Ground가 활성화되는지 **Study별 물리 설정**에서 제어

### 4-3. 외부 경계: Electric Insulation

팬텀 외부 경계(전극 제외)는 전류가 흐르지 않도록 절연 처리:

```
Electric Insulation 1 (기본값으로 이미 적용됨)
→ 전극 경계를 제외한 나머지 외부 경계에 자동 적용 확인
```

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
