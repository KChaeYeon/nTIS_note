# Mirzakhalili et al. (2020) — Biophysics of Temporal Interference Stimulation

**저널:** Cell Systems, 11(6), 557–572  
**DOI:** [10.1016/j.cels.2020.10.004](https://doi.org/10.1016/j.cels.2020.10.004)  
**분류:** Computational Modeling / Biophysics

---

## Research Question

TI stimulation에서 신경세포가 어떤 메커니즘으로 반응하는가? envelope 주파수·자극 강도·위치에 따라 반응 패턴이 어떻게 달라지는가?

## Methods

- Hodgkin-Huxley 기반 신경세포 모델
- 축삭(axon) 모델로 TI 전기장 내 반응 시뮬레이션
- 자극 강도, 전극으로부터의 거리(y), envelope 주파수 변화에 따른 반응 분류

## Key Results

- 신경 반응은 위치에 따라 3가지 클래스로 분류:
  - **Phasic**: 자극 on/off 시 일시적 반응 (y = 0.0 mm, 자극 중심)
  - **Tonic**: 지속적 활성화 (y = 1.7 mm)
  - **Conduction block**: 활동전위 전파 차단 (y = 3.5 mm)
- 고주파 carrier는 표면 신경을 활성화하지 않음 (TI의 핵심 원리 확인)
- Envelope 주파수 증가 → 자극 효율 감소 경향

## Limitations

- 단순화된 축삭 모델 — 실제 3D 뇌 구조 및 세포 다양성 미반영
- 단일 신경세포 수준 분석 — 네트워크 수준 효과 미포함

## Relevance to nTIS

> n-phase 확장 시 간섭 패턴이 복잡해지므로, 이 논문의 반응 분류 프레임워크가 nTIS 효과 예측의 기준점이 됨. Tonic vs. Phasic 반응 제어가 nTIS 설계 목표 중 하나가 될 수 있음.

---

*Last updated: 2026-06-04*
