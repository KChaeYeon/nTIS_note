# Kim 2023 — Optimization Framework for Temporal Interference Current Tibial Nerve Stimulation in Tibial Nerves Based on In-Silico Studies

**Citation:** Kim E, Ye E, Lee J, Kim T, Choi D, Lee K, Park S. Optimization Framework for Temporal Interference Current Tibial Nerve Stimulation in Tibial Nerves Based on In-Silico Studies. *Applied Sciences* 2023;13(4):2430. DOI: [10.3390/app13042430](https://doi.org/10.3390/app13042430)

> 경골신경 TIS의 **개인 맞춤 전극·전류 최적화 프레임워크**를 제시한 직접 선행 FEM 연구.

---

## 초록 (Abstract)

Compared to the existing noninvasive methods, temporal interference (TI) current stimulation is an emerging noninvasive neuromodulation technique that can improve the ability to focus an electrical field on a target nerve. Induced TI field distribution depends on the anatomical structure of individual neurons, and thus the electrode and current optimization to enhance the field focus must reflect these factors. The current study presents a TI field optimization framework for focusing the stimulation energy on the target tibial nerve through extensive electrical simulations, factoring in individual anatomical differences. We conducted large-scale in-silico experiments using realistic models based on magnetic resonance images of human subjects to evaluate the effectiveness of the proposed methods for tibial nerve stimulation considering overactive bladder (OAB) treatment. The electrode position and current intensity were optimized for each subject using an automated algorithm, and the field-focusing performance was evaluated based on the maximum intensity of the electric fields induced at the target nerve compared with the electric fields in the neighboring tissues. Using the proposed optimization framework, the focusing ability increased by 12% when optimizing the electrode position. When optimizing both the electrode position and current, this capability increased by 11% relative to electrode position optimization alone.

---

## 연구 질문

개인마다 다른 발목 해부 구조를 반영해, 경골신경에 TI 전기장을 **최대로 집속**시키는 전극 위치·전류 조합은 무엇이며, 최적화가 집속 성능을 얼마나 개선하는가?

## 방법

- **인체 MRI 기반 realistic FEM**(다수 피험자), quasi-static 전기장 해석
- 자동 최적화 알고리즘으로 **전극 위치**와 **전류 강도**를 피험자별 개인화
- 집속 성능 지표: 표적 신경 유도 전기장 최대 세기 ÷ 주변 조직 전기장(Peak/focality 유사 지표)

## 주요 결과

- **전극 위치 최적화**만으로 집속 능력 **+12%**
- **위치 + 전류 동시 최적화** 시 위치 단독 대비 추가 **+11%**
- 개인 해부 차이를 반영한 맞춤 최적화의 필요성 입증 → 말초신경 개인화 자극 치료로 확장 가능

## 한계점

- **완전 in-silico** — in vivo 검증 전무(핵심 갭 G-TN1)
- 뉴런 활성화 모델 미포함(전기장 세기 ≠ 실제 발화 확률)
- 개인 모델 수·조직 이방성·주파수 의존성의 단순화

## 관련 연구 갭 (nTIS)

경골신경 TIS의 **유일한 직접 FEM 최적화 선행**([2021_Lee_EfficientNoninvasiveNeuromodulation](2021_Lee_EfficientNoninvasiveNeuromodulation.md)의 시뮬레이션 축을 정교화). 그러나 in vivo 검증·뉴런 반응 모델·PTNS 비교가 비어 있어, 본 nTIS 연구의 실험 설계(G-TN1·G-TN2, `01_theory/13_research_gaps.md`)가 이를 메운다. n-phase 확장으로 선택성 추가 개선 여지.
