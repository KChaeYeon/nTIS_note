# Rampersad et al. (2019) — Prospects for transcranial temporal interference stimulation in humans: A computational study

**저널:** NeuroImage, 202, 116124  
**DOI:** [10.1016/j.neuroimage.2019.116124](https://doi.org/10.1016/j.neuroimage.2019.116124)  
**분류:** Computational Modeling

---

## Research Question

인간 두부 모델에서 TI stimulation이 심부 구조(해마, 담창구, 운동피질)를 효과적으로 타겟할 수 있는가? 전극 배치 최적화는 어떻게 수행하는가?

## Methods

- MRI 기반 인간 두부 FEM(Finite Element Method) 모델 구성 (9가지 조직층 구분)
- 타겟: 해마(hippocampus), 담창구(globus pallidus), 운동피질(motor cortex)
- 전극 배치 및 전류 강도 최적화 알고리즘 적용
- tACS(conventional)와 TI stimulation 전기장 강도 및 초점성(focality) 비교

## Key Results

- TI stimulation은 tACS 대비 **초점성(focality) 현저히 우수**
- 단, 심부 타겟에서의 **전기장 강도는 tACS보다 약함**
- 해마 타겟 시 최적 전극 위치와 전류 비율 제시
- Steering(자극 위치 이동) 가능성 전산 검증

## Key Figures

| Figure | 내용 |
|--------|------|
| **Fig. 1** | 인간 두부 FEM 모델 구성. MRI 기반 9층 조직 분류(두피, 두개골, 뇌척수액, 피질 등). 3D 렌더링 시각화. |
| **Fig. 2** | 해마 타겟 전기장 분포. TI vs. tACS 비교. TI는 심부 해마에서만 높은 envelope 강도, tACS는 표면 포함 광범위 분포. |
| **Fig. 3** | 담창구(globus pallidus) 타겟. 최적 전극 위치 및 전류 조합. 초점성 지표(focality index) 정량 비교 그래프. |
| **Fig. 4** | 운동피질 타겟. 표면 타겟에서는 TI와 tACS 초점성 차이 감소. 심부일수록 TI 우위 확대. |
| **Fig. 5** | 전기장 강도 vs. 초점성 트레이드오프 곡선. TI는 초점성 축에서 우위, tACS는 강도 축에서 우위. |

## Limitations

- 전산 모델 — 실제 뇌 조직의 이방성·개인차 단순화
- 실험적 검증(동물·인간) 없음
- 단일 인간 두부 모델 사용 (개인간 변동성 미반영)

## Relevance to nTIS

> 인간에서 TI의 초점성 우위를 정량적으로 보인 첫 전산 연구. n-phase 확장 시 초점성이 추가로 향상되는지 시뮬레이션으로 검증하는 것이 자연스러운 다음 단계. **초점성-강도 트레이드오프**가 핵심 설계 문제.

---

*Last updated: 2026-06-04*
