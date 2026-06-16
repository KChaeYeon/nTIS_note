# MRI 기반 TI 시뮬레이션 방법론

> 작성일: 2026-06-12  
> 주제: 발목 tibial nerve를 대상으로 한 Temporal Interference(TI) 전기자극 시뮬레이션 파이프라인 정리

---

## 1. 시뮬레이션 전체 흐름

```
MRI 촬영
   ↓
조직 분할 (segmentation)  — iSeg + Sim4Life
   ↓
전극 배치 (24-electrode array)
   ↓
FEM 전계 해석  — Ohmic Quasi-Static solver (Sim4Life)
   ↓
독립 전계 합성 → TI 포락선(envelope) 계산
   ↓
Peak Ratio 최적화  — MATLAB 전수탐색
```

**데이터 개요**

| 항목 | 내용 |
|------|------|
| 피험자 수 | 29명 |
| MRI 종류 | T1/T2 axial |
| 슬라이스 두께 | 2 mm |
| 촬영 범위 | 내측 복사뼈(medial malleolus) 근위 3–6 cm |

---

## 2. 조직 분할 (Tissue Segmentation)

8종 조직으로 분할:

| # | 조직 |
|---|------|
| 1 | 피부 (skin) |
| 2 | 지방 (fat) |
| 3 | 근육 (muscle) |
| 4 | 건·인대 (tendon / ligament) |
| 5 | 혈관 (blood vessel) |
| 6 | 신경 (nerve) |
| 7 | 뼈 (bone) |
| 8 | 골수 (bone marrow) |

각 조직에는 **전기전도도** $\sigma$ (S/m)를 할당하며, 이 값이 FEM 해석의 핵심 매개변수가 된다.

---

## 3. 전극 배치 (24-Electrode Array)

- **전극 크기**: 7 × 7 × 0.5 mm (가상 전극)
- **배치**: 발목 주위에 24개를 균등 배치
- **기준 전극 (Reference Electrode)**: 내측 복사뼈에 1개 — 전위 $V = 0\,\text{V}$ 고정

### 기준 전극의 역할: 시뮬레이션 횟수 절감

모든 능동 전극 쌍의 조합 수: $\binom{24}{2} = 276$쌍 이상  
→ 각 조합마다 FEM을 새로 돌리면 수백 회 시뮬레이션 필요

**해법 — 선형 중첩 원리 (Linear Superposition)**

기준 전극 대비 각 전극의 전계를 단독으로 해석하면:

$$
\mathbf{E}_{A\text{-}Ref},\quad \mathbf{E}_{B\text{-}Ref},\quad \mathbf{E}_{C\text{-}Ref},\;\ldots \quad (24\text{회})
$$

임의의 A→B 전류 경로의 전계는 뺄셈으로 복원:

$$
\mathbf{E}_{A\to B} = \mathbf{E}_{A\text{-}Ref} - \mathbf{E}_{B\text{-}Ref}
$$

**기준 전극 항이 소거되는 이유**: FEM은 선형 시스템이므로, 동일한 경계조건(기준 전극의 $V=0$)을 공유한 두 해를 빼면 기준점의 기여가 정확히 사라진다.

> **결론**: 24회 FEM → 10,626가지 이상의 전극 조합 모두 계산 가능

---

## 4. 유한요소법 (FEM)

### 4.1 메싱 (Meshing)

발목 3D 모델을 수백만 개의 작은 요소(tetrahedra 등)로 분할한다.  
복잡한 곡면 경계(피부, 신경, 혈관 등)를 정확히 표현하기 위해 **불규칙 메시**를 사용하며, 신경 등 관심 영역에는 **세밀한 메시**를 적용한다.

### 4.2 지배방정식

각 노드에서 전기 전위 $V$를 구하는 방정식:

$$
\nabla \cdot (\sigma \nabla V) = 0
$$

- $\sigma$: 조직별 전기전도도 (S/m)  
- FEM은 이 편미분방정식을 각 요소에서 이산화하여 대형 선형시스템 $[K]\{V\} = \{f\}$ 으로 변환·풀이한다.

### 4.3 경계조건

| 경계 | 조건 | 유형 |
|------|------|------|
| 능동 전극 | $V = 1\,\text{V}$ | Dirichlet |
| 기준 전극 | $V = 0\,\text{V}$ | Dirichlet |
| 모델 외부 경계 | 법선 전류 = 0 ($\mathbf{J}\cdot\hat{n}=0$) | Neumann |

---

## 5. Ohmic Quasi-Static 솔버 (Sim4Life)

### 5.1 왜 Quasi-Static인가?

TI 자극 주파수는 수 kHz 수준으로, 이 범위에서는:

- 전자기파의 파장 $\gg$ 모델 크기 → 복사(radiation) 효과 무시 가능
- 전류는 순수 **저항성(Ohmic)** 전도만으로 기술

따라서 시간 미분 항을 제거한 Quasi-Static 근사가 성립하며, 앞서 기술한 $\nabla\cdot(\sigma\nabla V)=0$ 이 지배방정식이 된다.

### 5.2 전류 정규화

FEM 해는 1 V 인가 시의 전위 분포 $V$를 준다.  
실제 주입 전류를 **1 mA** 로 맞추기 위해 아래와 같이 정규화한다:

$$
\mathbf{E}_{\text{normalized}} = \frac{\mathbf{E}_{1\,\text{V}}}{I_{\text{computed}}} \times 1\,\text{mA}
$$

여기서 $I_{\text{computed}}$는 1 V 인가 시 능동 전극에서 계산된 전체 전류다.

---

## 6. 독립 전계 합성 및 TI 포락선 수식

### 6.1 두 전류 경로의 독립 전계

TI 자극에는 두 쌍의 전극이 필요하다:

- 경로 1: A → B, 반송파 $f_1$
- 경로 2: C → D, 반송파 $f_2$  ($f_1 \neq f_2$, 차이 = 자극 주파수 $\Delta f$)

선형 중첩으로 각 경로의 전계 벡터를 구한다:

$$
\mathbf{E}_1 = \mathbf{E}_{A\text{-}Ref} - \mathbf{E}_{B\text{-}Ref}
$$

$$
\mathbf{E}_2 = \mathbf{E}_{C\text{-}Ref} - \mathbf{E}_{D\text{-}Ref}
$$

### 6.2 TI 포락선 공식 도출

두 고주파 전계의 중첩은 **맥놀이(beat)** 현상을 만든다. 시간에 따른 합성 전계의 크기는:

$$
|\mathbf{E}_{total}(t)| = |\mathbf{E}_1 \cos(2\pi f_1 t) + \mathbf{E}_2 \cos(2\pi f_2 t)|
$$

이때 진폭(포락선)의 최대·최솟값은:

$$
E_{\max} = |\mathbf{E}_1 + \mathbf{E}_2|, \qquad E_{\min} = \bigl||\mathbf{E}_1| - |\mathbf{E}_2|\bigr|
$$

따라서 **TI 자극 포락선** (저주파 성분의 진폭):

$$
\boxed{E_{TI} = E_{\max} - E_{\min} = \bigl||\mathbf{E}_1 + \mathbf{E}_2| - |\mathbf{E}_1 - \mathbf{E}_2|\bigr|}
$$

- $\mathbf{E}_1 = \mathbf{E}_2$ 인 곳: $E_{TI} = 2|\mathbf{E}_1|$ (최대 변조)
- $\mathbf{E}_1 \gg \mathbf{E}_2$ 또는 수직인 곳: $E_{TI} \approx 0$ (변조 없음)

---

## 7. Peak Ratio (PR) 최적화 지표

### 7.1 정의

$$
\boxed{PR = \frac{E_{\text{target}}}{E_{\text{total}}}}
$$

| 항목 | 정의 |
|------|------|
| $E_{\text{target}}$ | **tibial nerve 영역** (약 100–750 mm³) 내 체적 평균 TI 전계 (V/m) |
| $E_{\text{total}}$ | **전체 다리 모델** (약 150,000–480,000 mm³) 내 체적 평균 TI 전계 (V/m) |

각 항은 **자신의 체적으로 정규화**된 평균값이므로, 단위는 동일하게 V/m이며 단순 비율로 해석 가능하다.

### 7.2 의미

PR은 자극의 **초점성(focality)** 지표다:

- PR이 클수록 → 전체 조직 대비 신경 영역에 에너지가 집중됨 (원하는 상태)
- PR이 1에 가까울수록 → 자극이 분산됨

### 7.3 최적화 절차 (MATLAB)

1. 전체 전극 조합 탐색: $\binom{24}{4} = 10{,}626$ 가지 (4전극 = 경로 1의 2개 + 경로 2의 2개)
2. 각 조합에서 총 전류 **2 mA** 고정 하에 경로 1 : 경로 2 전류 비율을 0.1 mA 단위로 조정
3. 각 배분에서 $E_{TI}$ 분포 계산 → $E_{\text{target}}$, $E_{\text{total}}$ 추출 → PR 산출
4. PR이 최대인 조합 및 전류 배분 선택

---

## 8. 핵심 개념 요약

| 개념 | 핵심 |
|------|------|
| 기준 전극 | $V=0$ 고정점 → 24회 FEM으로 모든 쌍 복원 가능 |
| 선형 중첩 | $\mathbf{E}_{A\to B} = \mathbf{E}_{A\text{-}Ref} - \mathbf{E}_{B\text{-}Ref}$ |
| Quasi-Static | kHz 대역 → 복사 무시, 순수 Ohmic 전도 |
| TI 포락선 | 맥놀이의 진폭 변화분 = $\||\mathbf{E}_1+\mathbf{E}_2| - |\mathbf{E}_1-\mathbf{E}_2|\|$ |
| Peak Ratio | $E_{\text{target}} / E_{\text{total}}$ — 신경 집중도 지표 |

---

*관련 파일:*  
- `01_theory/TI_principles.md` — TI 원리 기초  
- `03_gaps/gap_analysis.md` — 미해결 연구 문제  
- `04_proposal/` — 연구 제안서
