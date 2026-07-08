# Meng 2025 — Direction of TIS envelope electric field: Perpendicular to the longitudinal axis of the hippocampus

**Citation:** Meng et al. Direction of TIS envelope electric field: Perpendicular to the longitudinal axis of the hippocampus. *Journal of Neuroscience Methods* 2025;423:110416. DOI: [10.1016/j.jneumeth.2025.110416](https://doi.org/10.1016/j.jneumeth.2025.110416)

> TIS 연구에서 소홀했던 **전기장의 방향성**(세기 아닌)을 정량 분석한 방법론 논문. 자극장 축 정렬이 효율을 좌우한다는 nTIS 설계 근거.

---

## 초록 (Abstract)

Background: Temporal Interference Stimulation (TIS) is a non-invasive approach to deep brain stimulation. However, most research has focused on the intensity of modulation, with limited attention given to the directional properties of the induced electric fields, despite their potential importance for precise stimulation. New methods: A novel analytical framework was developed to analyze TIS-induced electric field directions using individual imaging data. For each voxel, the direction corresponding to the maximal modulation depth was calculated. The consistency of these directions within regions of interest (ROIs) and their alignment with the ROI principal axes, derived from principal component analysis (PCA), were assessed. Results: Simulations revealed complex spatial and temporal trajectories of the electric field at the voxel level. In the left putamen, the maximal modulation depth reached 0.241 ± 0.041 V/m, whereas in the target region, the left hippocampus, it was lower (0.15 ± 0.032 V/m). Notably, in the left hippocampus, the directions of maximal modulation depth were predominantly perpendicular to its longitudinal axis (84.547 ± 8.776°). Conclusion: The orientations of maximal modulation depth in the left hippocampus were perpendicular to its longitudinal axis under the current electrode configuration, but shifted to parallel alignment when the electrode pairs were swapped.

---

## 연구 질문

TIS 유도 전기장의 **방향**(단순 세기가 아닌)이 표적 구조의 형태(주축)와 어떻게 정렬되며, 전극 구성으로 이를 제어할 수 있는가?

## 방법

- 개인 영상 기반 분석 프레임워크: voxel마다 **최대 변조깊이(maximal modulation depth) 방향** 계산
- ROI 내 방향 일관성 + **PCA 주축과의 정렬각** 평가
- 전극쌍 구성(기본 vs swap) 비교

## 주요 결과

- 좌 피각(putamen) 최대 변조깊이 **0.241 ± 0.041 V/m**, 표적인 좌 해마는 더 낮음 **0.15 ± 0.032 V/m**
- 좌 해마에서 최대 변조 방향이 **장축에 대체로 수직(84.5 ± 8.8°)** — 전-중-후 구역별 구조 특이성
- **전극쌍을 교환하면 방향이 평행으로 전환** → 전극 구성으로 자극장 방향 제어 가능(상관적)

## 한계점

- 시뮬레이션(in-silico)만 — 방향과 실제 신경 발화 효율의 인과 관계 미검증
- 특정 전극 구성·해마 표적에 한정
- 뉴런 배향(축삭 방향)과 전기장 방향의 상호작용 모델 부재

## 관련 연구 갭 (nTIS)

경골신경은 축(z) 방향으로 주행하고 신경은 **주행축 평행 전기장($E_z$)에 민감**하다([전자기 물리·FEM](../01_theory/05_EM_physics_FEM.md)). 본 논문의 방향성 분석은 nTIS에서 **자극장 방향을 경골신경 축에 정렬**시키는 전극·위상 설계의 정량 근거를 제공한다(n-phase의 방향 제어 이점과 직접 연결).
