# Grossman 2017 — Noninvasive Deep Brain Stimulation via Temporally Interfering Electric Fields

**Citation:** Grossman N, Bono D, Dedic N, et al. Noninvasive Deep Brain Stimulation via Temporally Interfering Electric Fields. *Cell* 2017;169(6):1029–1041. DOI: [10.1016/j.cell.2017.05.024](https://doi.org/10.1016/j.cell.2017.05.024)

> TI stimulation 개념을 최초로 제안·실증한 landmark 논문. nTIS 연구의 원리적 출발점.

---

## 초록 (Abstract)

We report a noninvasive strategy for electrically stimulating neurons at depth. By delivering to the brain multiple electric fields at frequencies too high to recruit neural firing, but which differ by a frequency within the dynamic range of neural firing, we can electrically stimulate neurons throughout a region where interference between the multiple fields results in a prominent electric field envelope modulated at the difference frequency. We validated this temporal interference (TI) concept via modeling and physics experiments, and verified that neurons in the living mouse brain could follow the electric field envelope. We demonstrate the utility of TI stimulation by stimulating neurons in the hippocampus of living mice without recruiting neurons of the overlying cortex. Finally, we show that by altering the currents delivered to a set of immobile electrodes, we can steerably evoke different motor patterns in living mice.

---

## 연구 질문

수술·이식 없이(비침습) 두피 전극만으로, 표면 조직을 자극하지 않으면서 **심부 뉴런을 선택적으로** 활성화할 수 있는가?

## 방법

- 주파수가 근소하게 다른 두 kHz 전기장($f_1$, $f_2$, $\Delta f = |f_1-f_2|$이 신경 발화 대역) 동시 인가
- 검증 3단계: (1) 전기장 모델링, (2) 물리(팬텀) 실험, (3) 마취 생쥐 in vivo — 전기생리 기록 + c-Fos 면역염색으로 활성 뉴런 위치 확인
- steering: 고정된 전극 세트의 전류 비율만 바꿔 자극 초점 이동

## 주요 결과

- 두 kHz 장의 간섭 영역에서 $\Delta f$로 변조된 **envelope**이 생성되고, 생쥐 뉴런이 이 envelope을 따라 발화함(상관적 관찰)
- **해마 뉴런을 선택적으로 활성화하면서 상부 피질 뉴런은 동원하지 않음** — 심부 선택성 실증
- 전류 비율 조절만으로 서로 다른 운동 패턴을 유발(전극 이동 없는 소프트웨어 steering)

## 한계점

- 마취 생쥐 모델 — 각성·행동 상태 미검증
- 소동물 스케일: 인체는 두개골·조직 두께·전기장 감쇠가 크게 달라 그대로 외삽 불가
- "신경이 envelope을 추출한다"는 전제는 이후 **말초신경에서 반박됨**([2023_Budde_TIS_Not_Envelope_JNE](2023_Budde_TIS_Not_Envelope_JNE.md), [2025_Opancar_TIS_kHz_NatComm](2025_Opancar_TIS_kHz_NatComm.md)) — 뇌(긴 막 시간상수)와 말초(짧은 막 시간상수)의 기전 차이 주의

## 관련 연구 갭 (nTIS)

nTIS의 이론적 토대. 다만 (1) **인체 스케일** 검증, (2) **말초·경골신경** 적용, (3) 말초에서의 실제 활성화 기전(envelope vs. 순간 진폭)은 별도 갭으로 남으며, 이는 [2021_Lee_EfficientNoninvasiveNeuromodulation](2021_Lee_EfficientNoninvasiveNeuromodulation.md)·[2023_Kim_OptimizationFrameworkTemporal](2023_Kim_OptimizationFrameworkTemporal.md) 및 `03_gaps/gap_analysis.md`의 G-TN1~G-TN3로 이어진다.
