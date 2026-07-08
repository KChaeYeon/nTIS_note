# Theory — 연구 배경 (Research Background)

경골신경 **n-phase Temporal Interference Stimulation (nTIS)** 연구의 이론적 배경을 하나의 연속된 이야기로 정리한다.
아래 순서대로 읽으면 **임상 문제 → 표적 신경 → 기존 기술의 한계 → TIS 원리 → 전자기 물리 → n-phase 확장 → 자극장 설계 → 실험 적용**이 끊김 없이 이어진다.

각 장은 독립적으로도 읽을 수 있으나, 순서대로 읽는 것을 권장한다.

---

## 전체 흐름

```
[왜 이 연구인가]
 01 임상 배경(OAB) ──▶ 02 표적 신경(경골신경) ──▶ 03 기존 신경조절 기술의 한계
                                                              │
                                                    "비침습 + 심부 선택성" 필요
                                                              ▼
[어떻게 푸는가 — 원리]
 04 TIS 원리 ──▶ 05 전자기 물리 & FEM ──▶ 06 n-phase / multi-channel
                                                              │
[어떻게 설계·검증하는가]
 07 AM_max(최대 자극 축) ──▶ 08 전극 위치별 자극장 ──▶ 09 자극 공간 3구역
                                                              │
                                                              ▼
 10 경골신경 TIS 시뮬레이션 → Rat 실험   |   11 종합 레퍼런스   |   12 부록(Q&A)
```

---

## 장 구성

### 1부. 연구 동기 — 왜 경골신경 TIS인가

| 장 | 제목 | 핵심 내용 |
|----|------|-----------|
| 1 | [임상 배경 — OAB 병태생리](01_clinical_OAB.md) | 과민성 방광 역학·배뇨 신경회로·치료 한계, 신경조절이 필요한 이유 |
| 2 | [표적 신경 — 경골신경 해부 & 자극 기전](02_tibial_nerve.md) | 경골신경 해부·신경섬유·전기자극 원리, S2–S4 방광 억제 3-Level 기전 |
| 3 | [기존 신경조절 기술 — SNM / PTNS / TTNS](03_existing_neuromodulation.md) | 세 기술의 기전·임상근거(RCT)·공통 한계 → TIS의 필요성 |

### 2부. 원리 — TIS는 어떻게 작동하는가

| 장 | 제목 | 핵심 내용 |
|----|------|-----------|
| 4 | [TIS 원리](04_TIS_principle.md) | 맥놀이(beat)·타원 궤적·AM_max·SVD·COMSOL 워크플로우·2-phase vs 3-phase·steering |
| 5 | [전자기 물리 & FEM](05_EM_physics_FEM.md) | Electroquasistatic·$E=-\nabla\phi$·Laplace 방정식·활성화 함수·포락선 유도·TENS vs TIS |
| 6 | [n-phase / Multi-channel TIS](06_nphase_multichannel.md) | 2-phase의 한계, 채널 수와 초점성, 직선 vs 타원, Lead Field rank |

### 3부. 설계 — 자극장을 어떻게 만들고 조향하는가

| 장 | 제목 | 핵심 내용 |
|----|------|-----------|
| 7 | [AM_max & 최대 진폭 축](07_AM_max.md) | Grossman 2017 FEM, 타원 궤적 직관, SVD 기반 AM_max 유도, 물리적 검증 |
| 8 | [전극 위치별 AM 전기장 맵](08_electrode_position_AM.md) | 전극 배치 변화에 따른 AM 전기장 분포 변화 |
| 9 | [자극 공간 3구역 분류](09_stimulation_zones.md) | TI 자극/억제/비자극 공간 구역화 |

### 4부. 적용 & 레퍼런스

| 장 | 제목 | 핵심 내용 |
|----|------|-----------|
| 10 | [경골신경 TIS — 시뮬레이션 → Rat 실험](10_tibial_TIS_simulation.md) | Kim 2023 FEM 분석, Rat OAB 모델·자극 프로토콜·통계 설계·로드맵 |
| 11 | [종합 레퍼런스 — 경골신경 & TNS 완전 종합](11_comprehensive_reference.md) | 해부·임상 RCT 데이터·이식형 기기·산업/규제 현황·완전 참고문헌 |
| 12 | [부록 — 전류·전기장·전하 보존 Q&A](12_charge_conservation_QA.md) | 전류–전류밀도–전기장 관계와 전하 보존 정리 |

---

## 빠른 참조

| 궁금한 것 | 찾아볼 곳 |
|-----------|-----------|
| OAB가 왜 신경조절로 치료되나? | [1장 §6](01_clinical_OAB.md) |
| 경골신경 자극이 방광을 억제하는 경로 | [2장 §10 (3-Level 기전)](02_tibial_nerve.md) |
| PTNS / TTNS / SNM 임상 근거(RCT) | [3장](03_existing_neuromodulation.md) · [11장 PART IV](11_comprehensive_reference.md) |
| 맥놀이(beat) envelope 수식 유도 | [4장 §3](04_TIS_principle.md) · [5장 7장](05_EM_physics_FEM.md) |
| $E=-\nabla\phi$ 와 Laplace 방정식 | [5장 2–5장](05_EM_physics_FEM.md) |
| AM_max = 2σ₁ (SVD) 유도 | [4장 §5](04_TIS_principle.md) · [7장](07_AM_max.md) |
| 왜 3-phase가 필요한가 | [6장](06_nphase_multichannel.md) |
| 말초신경 TIS ≠ envelope (Budde 2023) | [11장 PART VI](11_comprehensive_reference.md) |
| Rat 실험 프로토콜·통계 설계 | [10장 §7–9](10_tibial_TIS_simulation.md) |
| FDA 승인 기기·시장 현황 | [11장 PART VII](11_comprehensive_reference.md) |

---

*이 배경 문서는 개별 학습 노트를 하나의 연속된 연구 배경으로 통합·재정리한 결과다 (2026-07). 이전 판의 중복 문서(기초 원리·전기장 모델·n-phase 스텁·TIS 물리 FEM·3-phase 통합 가이드)는 더 깊은 정본 장으로 병합되었으며 git 히스토리에 보존되어 있다.*
