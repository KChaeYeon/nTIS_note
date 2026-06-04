# Grossman et al. (2017) — Noninvasive deep brain stimulation via temporally interfering electric fields

**저널:** Cell, 169(6), 1029–1041  
**DOI:** [10.1016/j.cell.2017.05.024](https://doi.org/10.1016/j.cell.2017.05.024)  
**분류:** Foundational

---

## Research Question

두피 표면을 자극하지 않고 심부 뇌 구조만 선택적으로 비침습적 자극할 수 있는가?

## Methods

- 두 쌍의 전극에 각각 $f_1 = 2000\,\text{Hz}$, $f_2 = 2040\,\text{Hz}$ 사인파 전류 인가
- 간섭 지점에서 $\Delta f = 40\,\text{Hz}$ envelope 생성
- 생쥐 모델: 해마(CA1), 소뇌, 운동피질 타겟
- 전극 위치 조정으로 자극 위치 steering 실험

## Key Results

- 표면 뉴런은 고주파($f_1$)에 반응하지 않아 활성화 없음
- 간섭 지점 심부 뉴런은 $\Delta f = 40\,\text{Hz}$ envelope에 반응하여 선택적 활성화
- 전극 전류 비율 조정으로 자극 위치를 이동 가능 (steering 실증)
- 해마 자극 시 생쥐 운동 유발, 소뇌 자극 시 체위 변화 유발

## Key Figures

| Figure | 내용 |
|--------|------|
| **Fig. 1** | TI stimulation 개념도. 두 고주파 사인파(f₁, f₂)의 수학적 합성으로 진폭 변조 envelope(Δf) 생성. 표면-심부 전기장 분포 도식화. |
| **Fig. 2** | 구형 도체 모델 및 FEM 시뮬레이션. 두 전류 쌍의 최대 간섭 지점에서만 Δf envelope 형성됨을 전기장 맵으로 시각화. |
| **Fig. 3** | In vitro 해마 슬라이스 실험. 단일 신경세포 패치클램프. 고주파(2 kHz) 단독 → 반응 없음 / 두 전류 간섭(Δf=10 Hz) → 활동전위 발생 확인. |
| **Fig. 4** | 생쥐 in vivo. 해마 자극 시 장소세포(place cell) 활성화 및 운동 유발. LFP 신호로 자극 효과 확인. |
| **Fig. 5** | Steering 실험. 전극 전류 비율 변경(예: 1:1 → 2:1)으로 자극 초점 위치 이동. 운동피질 vs. 소뇌 선택적 활성화. |
| **Fig. 6** | 두피 및 표면 조직에서 불필요한 자극 없음 확인. 표면 뉴런 활동전위 기록으로 선택성 검증. |

## Limitations

- 설치류 동물 모델 — 인간 두개골 두께·조직 복잡도에서 동일 결과 보장 불가
- 단일 envelope 주파수(40 Hz) 위주 검증
- 전기장 강도의 정량적 인간 적용 가능성 미검증

## Relevance to nTIS

> 이 논문이 TI stimulation의 출발점. 2전극 쌍(2-phase)에서 n-phase로 확장할 경우 초점성과 steering 자유도 향상 가능 — **nTIS 연구의 직접적 동기**.

---

*Last updated: 2026-06-04*
