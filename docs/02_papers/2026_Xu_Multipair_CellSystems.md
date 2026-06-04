# Xu et al. (2026) — Multipair phase-modulated temporal interference electrical stimulation combined with fMRI

**저널:** Cell Systems (정식 게재)  
**DOI:** [10.1016/j.cels.2026.101610](https://doi.org/10.1016/j.cels.2026.101610)  
**Preprint (2023):** [10.1101/2023.12.21.571679](https://doi.org/10.1101/2023.12.21.571679)  
**분류:** n-phase / Multi-electrode — 위상 변조 + fMRI 동시 측정  
**키워드:** multipair, phase-modulation, antiphase, fMRI, focality, PFC

---

## Research Question

3쌍 전극에 위상 변조(antiphase)를 적용하면 초점성을 향상시킬 수 있는가? fMRI와 동시 사용 시 전전두엽(PFC) 신경 활성화 및 혈역학 반응을 확인할 수 있는가?

## Methods

- 3쌍 전극: 2쌍은 표준 TI, 1쌍은 180° antiphase 적용
- EEG 위치 AF3/AF7 및 AF4/AF8 기반 최적 전극 배치
- 전전두엽(PFC) 타겟
- fMRI 동시 획득 + 아티팩트 제거 알고리즘
- in vivo 전기생리 기록 + 파이버 포토메트리(칼슘 이미징), fMRI BOLD 측정

## Key Results

- Antiphase 전극 추가 → **off-target 영역 전기장 상쇄, 초점성 향상**
- PFC에서 TI 유발 **신경 활성화(진폭 변조 확인), 신경세포 entrainment, BOLD 반응** 동시 검증
- fMRI와 TI stimulation **동시 적용 프로토콜** 확립
- 해부학 기반 전극 최적화 방법론 제시

## Key Figures

| Figure | 내용 |
|--------|------|
| **Fig. 1** | 실험 설계. 3쌍 전극 배치, antiphase 개념도, fMRI 동시 획득 타임라인. |
| **Fig. 2** | 전기장 시뮬레이션. 2쌍 vs. 3쌍(antiphase) 전기장 분포 비교. off-target 감소 시각화. |
| **Fig. 3** | 전기생리 결과. 진폭 변조 확인, 신경세포 Δf phase-locking 시계열. |
| **Fig. 4** | 파이버 포토메트리. PFC 칼슘 신호 변화. TI 자극 구간 선택적 증가. |
| **Fig. 5** | fMRI BOLD 결과. PFC 타겟 선택적 활성화. antiphase 조건 vs. 대조 비교. |

## Limitations

- Antiphase 추가에 따른 전기장 강도 감소 트레이드오프
- 3쌍 전극 파라미터 최적화 탐색 공간 넓음
- 인간 대상 적용 미검증

## Relevance to nTIS

> **위상($\phi$) 자유도를 활용한 n-phase TI의 핵심 구현 논문.** fMRI 동시 측정 프로토콜은 nTIS 효과의 혈역학·신경 동시 검증 방법론으로 직접 활용 가능. Antiphase 전극의 초점성 향상 원리가 n-phase 일반 이론의 특수 사례.

---

*Last updated: 2026-06-04*
