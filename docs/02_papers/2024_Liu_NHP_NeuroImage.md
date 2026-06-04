# Liu et al. (2024) — Temporal interference stimulation targets deep primate brain

**저널:** NeuroImage, 290, 120581  
**DOI:** [10.1016/j.neuroimage.2024.120581](https://doi.org/10.1016/j.neuroimage.2024.120581)  
**분류:** Animal Studies — Non-human Primate (Rhesus Monkey)  
**적용 대상:** 마취 상태 히말라야원숭이(Macaca mulatta) — SEEG 심부 전극 이식

---

## Research Question

원숭이 심부 뇌에서 TI 자극의 전기장이 실제로 어느 강도로 침투하는가? 전산 시뮬레이션과 실측값이 일치하는가? 안전 전류 범위 내에서 신경 조절 효과가 있는가?

## Methods

- 마취된 히말라야원숭이 2마리
- SEEG 심부 전극 다수 이식 → 여러 뇌 깊이에서 TI 전기장 직접 기록
- 두피 표면 전극 2쌍으로 TI 자극 인가 (다양한 파라미터 조합)
- FEM 기반 전산 시뮬레이션 결과와 실측값 비교
- 안전 전류(safety current) 수준에서의 electric field 강도 정량

## Key Results

- 안전 전류 범위 내에서 심부 TI 전기장 강도가 **tACS에서 신경 조절 효과가 입증된 역치 수준에 도달**
- FEM 시뮬레이션과 실측 전기장 분포 **양호한 일치** (r > 0.85)
- 표면 대비 심부 envelope 강도 비율이 시뮬레이션 예측과 부합
- 전극 배치·전류 비율에 따른 심부 타겟 steering 실측 확인

## Key Figures

| Figure | 내용 |
|--------|------|
| **Fig. 1** | 실험 설계. 원숭이 두개골 전극 배치 사진·MRI. SEEG 전극 위치 3D 재구성. |
| **Fig. 2** | 깊이별 전기장 강도 프로파일. 표면→심부 거리에 따른 TI envelope 강도 감쇠 곡선. 시뮬레이션(점선) vs. 실측(실선) 비교. |
| **Fig. 3** | 공간 분포 지도. 여러 전극 채널에서 기록된 envelope 강도를 3D 뇌 지도에 투영. |
| **Fig. 4** | Steering 검증. 전류 비율 변경에 따른 최대 envelope 위치 이동. 시뮬레이션 예측과 실측 비교. |
| **Fig. 5** | 안전 전류 역치 분석. 안전 범위 내 전기장 강도와 tACS 신경 조절 역치 비교 도식. |

## Limitations

- 마취 상태 — 각성 시 신경 반응 특성 차이 가능
- 전기장 측정만 수행 — 신경 활성화 직접 확인 없음
- 2마리 소규모
- 원숭이-인간 두부 구조 차이 (스케일링 추가 검증 필요)

## Relevance to nTIS

> **비인간 영장류에서 TI 전기장을 직접 계측하여 시뮬레이션을 검증한 핵심 논문.** n-phase TI 전기장 분포도 동일한 방법론으로 검증 가능. 안전 전류 내 신경 조절 역치 도달 여부가 nTIS 설계의 전류 상한 기준이 됨.

---

*Last updated: 2026-06-04*
