# Botzanowski et al. (2025) — Focal control of non-invasive deep brain stimulation using multipolar temporal interference

**저널:** Bioelectronic Medicine, 11, 7  
**DOI:** [10.1186/s42234-025-00169-6](https://doi.org/10.1186/s42234-025-00169-6)  
**분류:** n-phase / Multi-electrode — 초점성-강도 독립 제어  
**키워드:** mTI, multipolar, focality-intensity decoupling, NHP, rodent  
**대상:** 히말라야원숭이(NHP) + 설치류 in vivo

---

## Research Question

다극 TI(mTI)로 자극 영역 크기(초점성)와 자극 강도를 독립적으로 제어할 수 있는가? 기존 2쌍 TI의 초점성-강도 연동 한계를 극복할 수 있는가?

## Methods

- **핵심 아이디어:** 여러 carrier 주파수 사용 → 다중 진폭 변조 envelope 생성 → 중첩 패턴 조절로 초점성과 강도 독립 제어
- NHP(히말라야원숭이): 두피 전극 + 피질 기록
- 설치류: 두피 전극 + 해마 LFP 기록
- 전산 시뮬레이션: mTI vs. 2쌍 TI 초점성·강도 정량 비교

## Key Results

- **초점성과 강도의 독립적 제어** 실증 (2쌍 TI에서는 불가능했던 자유도)
- 자극 영역 크기를 강도 유지한 채 축소 가능 → **더 작은 타겟 선택 자극**
- NHP와 설치류 in vivo에서 mTI 유발 신경 반응 확인
- 전산 모델과 생체 측정 일치

## Key Figures

| Figure | 내용 |
|--------|------|
| **Fig. 1** | mTI 개념도. 다중 carrier 주파수로 여러 envelope 생성, 중첩 패턴 조절. 2쌍 TI와 비교. |
| **Fig. 2** | 초점성-강도 트레이드오프 곡선. 2쌍 TI(연동) vs. mTI(독립) 비교 그래프. |
| **Fig. 3** | NHP 피질 기록. mTI 자극 조건별 신경 반응 파형 및 분석. |
| **Fig. 4** | 설치류 해마 LFP. mTI 파라미터 변화에 따른 타겟 특이적 반응. |
| **Fig. 5** | 시뮬레이션 검증. mTI 전기장 분포 — 초점 크기 변화 시뮬레이션 vs. 실측 비교. |

## Limitations

- 여러 carrier 주파수 동시 사용 → 자극기 하드웨어 복잡도 증가
- 최적 carrier 주파수 조합 탐색 미완료
- 인간 대상 검증 없음
- 다중 envelope 간 상호작용 효과 완전히 규명 안됨

## Relevance to nTIS

> **nTIS의 핵심 설계 목표(초점성·강도 독립 제어)를 최초로 실증한 논문.** n-phase의 위상($\phi$) 자유도와 mTI의 다중 carrier 자유도를 결합하면 공간·강도·위상 3차원 동시 최적화 가능. **nTIS 연구 제안서의 직접 출발점.**

---

*Last updated: 2026-06-04*
