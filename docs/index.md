# nTIS Research Notebook

**Topic:** n-phase Temporal Interference Electrical Stimulation

---

## Research Overview

Temporal Interference (TI) stimulation is a non-invasive deep brain stimulation technique
that uses the interference of two high-frequency sinusoidal currents (at slightly different
frequencies) to generate a low-frequency envelope within deep tissue, without stimulating
overlying regions.

**n-phase TI** extends the classic 2-electrode setup to *n* sets of electrodes with
phase-shifted carrier signals, enabling improved spatial focality and directional control.

---

## 탭 구성 (한눈에)

이 노트북은 아래 5개 탭으로 구성된다. 각 탭이 무엇을 담는지 한눈에 확인하고 필요한 곳으로 바로 이동한다.

<div class="tab-grid" markdown>
<div class="grid cards" markdown>

-   **Background**

    ---

    연구의 이론적 배경 전체 흐름. **4 STEP**으로 정리:

    - STEP 1 — 연구 동기 (OAB·경골신경·기존 기술 한계)
    - STEP 2 — 원리 & 설계 (물리·FEM·TIS·AM_max·n-phase)
    - STEP 3 — 적용 & 레퍼런스 (Rat 실험·종합 참고)
    - STEP 4 — 연구 갭 & 제안 (갭 분석 + 제안서)

    [Background 열기](01_theory/index.md)

-   **Simulation**

    ---

    COMSOL FEM 전기장 시뮬레이션.

    - COMSOL TIS 시뮬레이션 사용법
    - AM_vector COMSOL 변수 체계
    - 데이터·결과물(`Result/`)

    [Simulation 열기](07_Simulation/index.md)

-   **Experiment**

    ---

    실험 데이터 및 분석 결과 기록.

    - 파일 규칙 `YYYYMMDD_ExperimentName.md`
    - Rat OAB in vivo 실험 착수 후 축적 예정

    [Experiment 열기](06_Exp/index.md)

-   **Meeting**

    ---

    연구 회의록·발표 자료.

    - 연구 방향·문헌 서베이·세션 인계 기록
    - 협력 미팅·팀 내부 미팅·발표 스크립트

    [Meeting 열기](07_Meeting/index.md)

-   **Reference**

    ---

    선행 논문 요약 라이브러리 (9개 카테고리).

    - Foundational · Computational · Human · Rodent · NHP
    - Reviews · n-phase 확장 · TN-OAB · 말초/경골 TIS

    [Reference 열기](02_papers/index.md)

</div>
</div>

---

*단계 A(Theory) → B(Gaps) → C(Proposal)는 완료되어 **Background** 탭의 STEP 4로 통합되었고, 현재는 D(Execution) — 경골신경 TIS in vivo Rat OAB 실험 착수 단계다. 상세 제안은 [연구 제안서](01_theory/14_research_proposal.md) 참조.*
