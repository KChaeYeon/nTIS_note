# Theory — 학습 로드맵

TIS(Temporal Interference Stimulation) 이론을 아래 순서로 학습합니다.
각 페이지는 독립적으로도 읽을 수 있으나, 순서대로 읽으면 체계적으로 이해할 수 있습니다.

---

## 학습 경로

```
① TIS 기초 원리          ② 전기장 모델 & FEM          ③ n-Phase 확장
   비전공자 설명               수식 유도·선형중첩              n개 전극 일반화
   AM라디오 비유               포락선 도출·경계조건
   Δf / 캐리어 / envelope      PR 개요
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ↓
                      ④ TIS 물리 & FEM 심층
                         모식도 중심 완전 가이드
                         PR 최적화 · Budde 2023 논쟁
                                    ↓
               ┌────────────────────┴────────────────────┐
               ↓                                         ↓
   ⑤ 경골신경 TIS 연구                     ⑥ 경골신경 지식 백과
      실험 설계 · 프로토콜                    해부학 · 임상근거 · 산업현황
      통계 · 연구 로드맵
               │
               └───────────────────────────┐
                                           ↓
                         [STEP 4] TIS 원리 심화 (12)
                            beat·AM_max·SVD·COMSOL
                            2-phase vs 3-phase 비교
                                           ↓
                         [STEP 5] Multi-channel TIS (14)
                            2-phase 3가지 한계
                            초점성·Steering·방향 제어
                            전극 선형독립·Lead Field rank
                                           ↓
                         [STEP 6] AM_max & 최대 진폭 축 (15) ← 현재
                            Grossman 2017 FEM 방법론
                            타원 궤적 직관 + SVD 수식
                            물리적 검증 방법
                                           ↓
                         [STEP 7~] 3-phase 수식 심화 (예정)
                            COMSOL 3-phase 구현
```

---

## 파일 목록

| # | 파일 | 내용 | 대상 독자 |
|---|------|------|---------|
| 1 | [TIS 기초 원리](01_basic_principles.md) | TIS 원리, 수식, 뇌 vs. 말초 메커니즘 | 비전공자 포함 |
| 2 | [전기장 모델 & FEM](02_electric_field.md) | Maxwell→Quasi-static, 선형중첩, 포락선 도출 | 수식 이해 필요 |
| 3 | [n-Phase 확장](03_nphase_extension.md) | n개 전극 일반화, 초점성·방향성 개선 | 연구자 |
| 4 | [TIS 물리 & FEM 심층](07_TIS_physics_FEM.md) | 모식도 중심 완전 가이드, PR 최적화 | 초등학생~연구자 |
| 5 | [경골신경 TIS 연구](05_tibial_nerve_TIS.md) | FEM→Rat 실험 전체 파이프라인 | 연구자 |
| 6 | [경골신경 지식 백과](06_tibial_nerve_complete_knowledge.md) | 해부학, 임상근거, 기전, 산업 현황 | 연구자 |
| — | [TIS 원리 심화 ★STEP 4](12_TIS_principle.md) | beat 주파수, AM_max, SVD, COMSOL 파이프라인, 2/3-phase 비교 | 연구자 |
| — | [3-phase TIS 완전 가이드](13_3phase_TIS_complete_guide.md) | EM 기초부터 COMSOL 구현까지, PR 지표, 3-phase 심화 | 연구자 |
| — | [Multi-channel TIS — 왜 3-phase가 필요한가 ★STEP 5](14_multiphase_TIS_why_3phase.md) | 2-phase 3가지 한계, 채널 수와 초점성, 직선 vs 타원, Lead Field rank | 연구자 |
| — | [AM_max & 최대 진폭 축 ★STEP 6](15_AM_max_amplitude_modulation.md) | Grossman 2017 FEM, 타원 궤적 직관, SVD 수식 유도, 물리적 검증 | 연구자 |

---

## 빠른 참조

| 궁금한 것 | 찾아볼 곳 |
|---------|---------|
| TIS가 뭔가요? | [01 — 섹션 1](01_basic_principles.md) |
| 맥놀이 수식이 어떻게 나왔나요? | [01 — 섹션 2](01_basic_principles.md), [02 — 섹션 3](02_electric_field.md) |
| FEM에서 선형중첩이 뭔가요? | [02 — 섹션 2](02_electric_field.md) |
| Peak Ratio(PR)가 뭔가요? | [07 — Part 4](07_TIS_physics_FEM.md) |
| Budde 2023 논쟁이 뭔가요? | [07 — Part 5](07_TIS_physics_FEM.md) |
| 경골신경 발목 해부학 | [06 — PART I](06_tibial_nerve_complete_knowledge.md) |
| Rat 실험 프로토콜 | [05 — 섹션 7-8](05_tibial_nerve_TIS.md) |
| PTNS 임상 근거 (RCT) | [06 — PART IV](06_tibial_nerve_complete_knowledge.md) |
| Kim 2023 FEM 결과 | [05 — 섹션 5](05_tibial_nerve_TIS.md) |
| AM_max = 2σ₁ 유도 | [12 — 섹션 4](12_TIS_principle.md) |
| COMSOL 주파수 도메인 워크플로우 | [12 — 섹션 5](12_TIS_principle.md) |
| 2-phase TIS의 3가지 한계 | [14 — 섹션 1](14_multiphase_TIS_why_3phase.md) |
| 왜 채널 수를 늘리면 초점성이 좋아지나요? | [14 — 섹션 2](14_multiphase_TIS_why_3phase.md) |
| 직선 vs 타원 (2D vs 3D 궤적) | [14 — 섹션 3](14_multiphase_TIS_why_3phase.md) |
| 3-phase에서 0°/120°/240° 위상이 필수인가요? | [14 — 섹션 4](14_multiphase_TIS_why_3phase.md) |
| Lead Field rank 조건 | [14 — 섹션 5](14_multiphase_TIS_why_3phase.md) |
| 왜 단방향 AM이 불충분한가 | [15 — 섹션 2](15_AM_max_amplitude_modulation.md) |
| 타원 궤적 직관 (AM_max 물리적 의미) | [15 — 섹션 5](15_AM_max_amplitude_modulation.md) |
| SVD로 AM_max 계산하는 방법 | [15 — 섹션 6](15_AM_max_amplitude_modulation.md) |
| Grossman 2017 FEM 파이프라인 | [15 — 섹션 1](15_AM_max_amplitude_modulation.md) |
