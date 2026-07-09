# Background — 연구 배경

경골신경 **n-phase Temporal Interference Stimulation (nTIS)** 연구의 이론적 배경을 하나의 연속된 이야기로 정리한다.
**임상 문제 → 표적 신경 → 기존 기술의 한계 → TIS 원리 → 전자기 물리 → 자극장 설계 → n-phase 확장 → 실험 적용 → 연구 갭 → 제안**이 끊김 없이 이어진다.

각 장은 독립적으로도 읽을 수 있으나, 아래 흐름 순서대로 읽는 것을 권장한다.

---

## 한눈에 보는 흐름 (4 STEP)

<div class="grid cards" markdown>

-   :material-stethoscope:{ .lg .middle } &nbsp;**STEP 1 — 연구 동기**

    ---

    *왜 경골신경 TIS인가*

    임상 문제(OAB) → 표적 신경(경골신경) → 기존 신경조절 기술(SNM/PTNS/TTNS)의 공통 한계

    → **"비침습 + 심부 선택성"** 필요

    [:octicons-arrow-right-24: 아래 STEP 1](#step-1)

-   :material-sine-wave:{ .lg .middle } &nbsp;**STEP 2 — 원리 & 설계**

    ---

    *TIS는 어떻게 작동하고, 자극장을 어떻게 만드는가*

    전자기 물리·FEM → 전극 위치별 AM 전기장 → TIS 원리(맥놀이) → AM_max 축 → 자극 3구역 → n-phase 확장

    [:octicons-arrow-right-24: 아래 STEP 2](#step-2)

-   :material-flask:{ .lg .middle } &nbsp;**STEP 3 — 적용 & 레퍼런스**

    ---

    *이론을 실험으로 옮기기*

    경골신경 TIS 시뮬레이션 → Rat 실험 프로토콜 → 종합 레퍼런스 → 전하 보존 Q&A

    [:octicons-arrow-right-24: 아래 STEP 3](#step-3)

-   :material-target:{ .lg .middle } &nbsp;**STEP 4 — 연구 갭 & 제안**

    ---

    *무엇이 비어 있고, 무엇을 할 것인가*

    5분류 갭 분석 → 최종 연구 주제 결정(경골신경 TIS in vivo) → 대안 후보 → COMSOL 제안서

    [:octicons-arrow-right-24: 아래 STEP 4](#step-4)

</div>

```
STEP 1  임상 배경(OAB) ─▶ 표적 신경(경골신경) ─▶ 기존 기술 한계
                                                        │  "비침습 + 심부 선택성" 필요
                                                        ▼
STEP 2  전자기 물리·FEM ─▶ 전극 위치별 AM ─▶ TIS 원리 ─▶ AM_max ─▶ 자극 3구역 ─▶ n-phase
                                                        │
                                                        ▼
STEP 3  경골신경 TIS 시뮬레이션 → Rat 실험  |  종합 레퍼런스  |  전하 보존 Q&A
                                                        │
                                                        ▼
STEP 4  5분류 갭 분석 ─▶ 연구 주제 결정 ─▶ 제안서
```

---

## STEP 1 — 연구 동기 {#step-1}

*왜 경골신경 TIS인가*

| 장 | 제목 | 핵심 내용 |
|----|------|-----------|
| 1 | [임상 배경 — OAB 병태생리](01_clinical_OAB.md) | 과민성 방광 역학·배뇨 신경회로·치료 한계, 신경조절이 필요한 이유 |
| 2 | [표적 신경 — 경골신경 해부 & 자극 기전](02_tibial_nerve.md) | 경골신경 해부·신경섬유·전기자극 원리, S2–S4 방광 억제 3-Level 기전 |
| 3 | [기존 신경조절 기술 — SNM / PTNS / TTNS](03_existing_neuromodulation.md) | 세 기술의 기전·임상근거(RCT)·공통 한계 → TIS의 필요성 |

---

## STEP 2 — 원리 & 설계 {#step-2}

*TIS는 어떻게 작동하고, 자극장을 어떻게 만들고 조향하는가* — 물리 기초에서 시작해 n-phase 확장으로 이어지는 순서로 읽는다.

| 순서 | 제목 | 핵심 내용 |
|:----:|------|-----------|
| 1 | [전자기 물리 & FEM](05_EM_physics_FEM.md) | Electroquasistatic·$E=-\nabla\phi$·Laplace 방정식·활성화 함수·포락선 유도·TENS vs TIS |
| 2 | [전극 위치별 AM 전기장 맵](08_electrode_position_AM.md) | 전극 배치 변화에 따른 AM 전기장 분포 변화 |
| 3 | [TIS 원리](04_TIS_principle.md) | 맥놀이(beat)·타원 궤적·AM_max·SVD·COMSOL 워크플로우·2-phase vs 3-phase·steering |
| 4 | [AM_max & 최대 진폭 축](07_AM_max.md) | Grossman 2017 FEM, 타원 궤적 직관, SVD 기반 AM_max 유도, 물리적 검증 |
| 5 | [자극 공간 3구역 분류](09_stimulation_zones.md) | TI 자극/억제/비자극 공간 구역화 |
| 6 | [n-phase / Multi-channel TIS](06_nphase_multichannel.md) | 2-phase의 한계, 채널 수와 초점성, 직선 vs 타원, Lead Field rank |

---

## STEP 3 — 적용 & 레퍼런스 {#step-3}

| 장 | 제목 | 핵심 내용 |
|----|------|-----------|
| 10 | [경골신경 TIS — 시뮬레이션 → Rat 실험](10_tibial_TIS_simulation.md) | Kim 2023 FEM 분석, Rat OAB 모델·자극 프로토콜·통계 설계·로드맵 |
| 11 | [종합 레퍼런스 — 경골신경 & TNS 완전 종합](11_comprehensive_reference.md) | 해부·임상 RCT 데이터·이식형 기기·산업/규제 현황·완전 참고문헌 |
| 12 | [부록 — 전류·전기장·전하 보존 Q&A](12_charge_conservation_QA.md) | 전류–전류밀도–전기장 관계와 전하 보존 정리 |

---

## STEP 4 — 연구 갭 & 제안 {#step-4}

*선행연구 정리 후 발견된 미해결 문제와, 그로부터 도출한 연구 제안을 한 곳에 모았다.*

| 문서 | 제목 | 핵심 내용 |
|------|------|-----------|
| 갭 | [연구 갭 분석](13_research_gaps.md) | 5분류 갭(Knowledge/Methodological/Evidence/Contradictory/Application) + 분야별·nTIS 고유 갭 |
| 제안 | [연구 제안서 (최종 결정)](14_research_proposal.md) | **경골신경 TIS in vivo — Rat OAB 조절** (2026-06-16 확정), RQ·방법론·타임라인 |
| 대안 | [제안 후보 — Phrenic / Tibial / Glymphatic](15_proposal_alternatives.md) | FINES 평가 기반 10개 후보 상세 비교 |
| COMSOL | [COMSOL nTIS × OAB 제안서](16_comsol_proposal.md) | 2-phase/n-phase FEM 시뮬레이션 + in vivo 검증 설계 |

---

## 빠른 참조

| 궁금한 것 | 찾아볼 곳 |
|-----------|-----------|
| OAB가 왜 신경조절로 치료되나? | [임상 배경](01_clinical_OAB.md) |
| 경골신경 자극이 방광을 억제하는 경로 | [표적 신경 (3-Level 기전)](02_tibial_nerve.md) |
| PTNS / TTNS / SNM 임상 근거(RCT) | [기존 신경조절 기술](03_existing_neuromodulation.md) · [종합 레퍼런스 PART IV](11_comprehensive_reference.md) |
| 맥놀이(beat) envelope 수식 유도 | [TIS 원리](04_TIS_principle.md) · [전자기 물리 & FEM](05_EM_physics_FEM.md) |
| $E=-\nabla\phi$ 와 Laplace 방정식 | [전자기 물리 & FEM](05_EM_physics_FEM.md) |
| AM_max = 2σ₁ (SVD) 유도 | [TIS 원리](04_TIS_principle.md) · [AM_max](07_AM_max.md) |
| 왜 3-phase가 필요한가 | [n-phase / Multi-channel](06_nphase_multichannel.md) |
| 말초신경 TIS ≠ envelope (Budde 2023) | [종합 레퍼런스 PART VI](11_comprehensive_reference.md) |
| Rat 실험 프로토콜·통계 설계 | [경골신경 TIS 시뮬레이션 §7–9](10_tibial_TIS_simulation.md) |
| 현재 확정 연구 주제·제안 | [연구 제안서](14_research_proposal.md) |
| 미해결 갭 목록 | [연구 갭 분석](13_research_gaps.md) |

---

*이 배경 문서는 개별 학습 노트를 하나의 연속된 연구 배경으로 통합·재정리한 결과다 (2026-07). 원리(구 2부)와 설계(구 3부)는 하나의 STEP 2로 통합되었고, 연구 갭·제안은 STEP 4로 편입되었다. 이전 판의 중복 문서는 더 깊은 정본 장으로 병합되었으며 git 히스토리에 보존되어 있다.*
