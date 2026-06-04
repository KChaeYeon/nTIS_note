# Mirzakhalili et al. (2020) — Biophysics of Temporal Interference Stimulation

**저널:** Cell Systems, 11(6), 557–572  
**DOI:** [10.1016/j.cels.2020.10.004](https://doi.org/10.1016/j.cels.2020.10.004)  
**분류:** Computational Modeling / Biophysics

---

## Research Question

TI stimulation에서 신경세포가 어떤 메커니즘으로 반응하는가? Envelope 주파수·자극 강도·위치에 따라 반응 패턴이 어떻게 달라지는가?

## Methods

- Hodgkin-Huxley 기반 신경세포 모델 (축삭 중심)
- TI 전기장 내에서 축삭 위치(y) 변화에 따른 반응 시뮬레이션
- 파라미터 스윕: 자극 강도, 위치(y), envelope 주파수($\Delta f$)
- 반응 분류 알고리즘 적용

## Key Results

신경 반응은 위치에 따라 3가지 클래스로 분류:

| 위치 | 반응 유형 | 설명 |
|------|----------|------|
| $y = 0.0\,\text{mm}$ (자극 중심) | **Phasic** | 자극 on/off 시 일시적 burst 발생 |
| $y = 1.7\,\text{mm}$ | **Tonic** | 지속적 규칙적 활동전위 발생 |
| $y = 3.5\,\text{mm}$ | **Conduction block** | 활동전위 전파 차단 |

- 고주파 carrier는 표면 신경을 활성화하지 않음 (TI 핵심 원리 수치 확인)
- Envelope 주파수($\Delta f$) 증가 → 자극 효율 감소 경향
- 자극 강도 증가 → Conduction block 영역 확장

## Key Figures

| Figure | 내용 |
|--------|------|
| **Fig. 1** | 시뮬레이션 설정 개요. 축삭 모델과 TI 전기장 배치. 두 전류쌍의 합성 파형 및 envelope 추출 방법 도식화. |
| **Fig. 2** | 위치별 반응 클래스 지도. y축(거리)–자극 강도 2D 파라미터 공간에서 Phasic·Tonic·Block 영역 색상 구분. |
| **Fig. 3** | 각 반응 클래스의 시간 파형. Phasic(burst), Tonic(연속 스파이크), Block(스파이크 없음) 전압 트레이스. |
| **Fig. 4** | Envelope 주파수($\Delta f$) 변화에 따른 반응 변화. $\Delta f$ 증가 시 Tonic 영역 감소, 역치 전류 증가. |
| **Fig. 5** | 고주파 carrier 단독 자극 vs. TI 자극 비교. 동일 강도에서 carrier 단독은 반응 없음 — 선택성 기전 확인. |

## Limitations

- 단순화된 축삭 모델 — 실제 3D 뇌 구조 및 세포 다양성 미반영
- 단일 신경세포 수준 분석 — 네트워크 수준 효과 미포함
- 조직 이방성, 용량성 특성 미포함

## Relevance to nTIS

> n-phase 확장 시 간섭 패턴이 복잡해지므로, 이 논문의 반응 분류 프레임워크(Phasic / Tonic / Block)가 nTIS 효과 예측의 기준점이 됨. 특히 **Tonic 반응 영역의 공간적 확장/축소가 초점성 지표**로 활용 가능.

---

*Last updated: 2026-06-04*
