# Zhu et al. (2019) — Multi-Point Temporal Interference Stimulation by Using Each Electrode to Carry Different Frequency Currents

**저널:** IEEE Access, 7, 168839–168848  
**DOI:** [10.1109/ACCESS.2019.2947857](https://doi.org/10.1109/ACCESS.2019.2947857)  
**분류:** n-phase / Multi-electrode — 최초 개념 제안  
**키워드:** MTI, multi-point, multi-frequency, network stimulation

---

## Research Question

각 전극이 서로 다른 주파수 전류를 전달하면 뇌 네트워크의 여러 지점을 동시에 선택적으로 자극할 수 있는가?

## Methods

- **핵심 아이디어:** 각 단일 전극에 서로 다른 주파수($f_i$)를 할당 → 전극 쌍이 아닌 **전극 개별** 주파수 설계
- n개 전극 → $\binom{n}{2}$개의 간섭 지점 생성 가능
- 전류 주파수·진폭 최적화로 원하는 지점에서만 자극 활성화
- 검증: 기하학적 모델, MRI 인간 두부 모델, 조직 팬텀(tissue phantom)
- 생쥐 실험: 해마 선택적 자극 확인

## Key Results

- **다중 지점(multi-point) 동시 자극** 가능성 이론·시뮬레이션 검증
- 각 자극 지점 **독립적 조절** 가능 (steering)
- 4전극 → 최대 6개 간섭 지점, 각 지점 전류 조합으로 활성화 제어
- 팬텀 실험에서 원하는 위치 envelope 확인

## Key Figures

| Figure | 내용 |
|--------|------|
| **Fig. 1** | MTI 개념도. 각 전극 주파수 할당 방식과 간섭 지점 형성 원리 다이어그램. |
| **Fig. 2** | 기하학적 모델 시뮬레이션. n=4 전극 배치에서 6개 간섭 지점 전기장 분포. |
| **Fig. 3** | MRI 인간 두부 모델. 해마 및 다중 타겟 동시 활성화 전기장 시뮬레이션. |
| **Fig. 4** | 조직 팬텀 실험. 전기장 맵핑. 예측 위치에서 envelope 강도 피크 확인. |

## Limitations

- 이론·시뮬레이션·팬텀 검증 위주 — 동물·인간 생체 실험 미실시
- 전극 수 증가 시 최적화 복잡도 급증
- 다중 지점 동시 자극의 신경 생리 효과 미검증

## Relevance to nTIS

> **nTIS 아이디어의 직접적 선행 논문.** 각 전극에 독립적 주파수를 부여하는 MTI 개념은 n-phase TI의 가장 일반화된 형태. 이 프레임워크를 위상($\phi$) 차원으로 확장한 것이 n-phase TI. **네트워크 수준 동시 자극**이라는 새로운 응용 방향 제시.

---

*Last updated: 2026-06-04*
