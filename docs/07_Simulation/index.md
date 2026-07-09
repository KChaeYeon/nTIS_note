# Simulation

경골신경 nTIS의 **COMSOL FEM 전기장 시뮬레이션** 관련 문서·데이터를 모은다.
환경: COMSOL Multiphysics 6.3 · AC/DC Module · 2D → 3D 순차 진행.

---

## 페이지 구성 (한눈에)

<div class="grid cards" markdown>

-   **1. COMSOL TIS 시뮬레이션 사용법**

    ---

    모델 설정부터 후처리까지 — 지오메트리·물성·경계조건·메시·솔버·결과 추출의 단계별 워크플로우.

    [사용법 열기](COMSOL_simulation_guide.md)

-   **2. AM_vector COMSOL 변수 체계**

    ---

    `2D_2phase_max.txt` 기반 — COMSOL Variables로 등록하는 AM_max·벡터 변수 정의 체계.

    [변수 체계 열기](AM_vector_variable_system.md)

</div>

---

## 데이터 & 결과물 (좌측 nav 미노출)

시뮬레이션 원본·산출물은 문서가 아닌 파일로 저장되어 있으며, 저장소에서 직접 확인한다.

| 항목 | 위치 | 내용 |
|------|------|------|
| 변수 원본 | `2D_2phase_max.txt` | COMSOL Variables 등록용 AM_vector 정의 |
| 테스트 모델 | `260626_test.mph` (+ `.avi` / `.gif`) | 2-phase TI 필드 애니메이션 테스트 |
| 결과물 | `Result/` | E-field AM map·프로파일·leadField CSV·검증 그림 |

---

*문서 순서: **① COMSOL 사용법 → ② AM_vector 변수 체계** (선행 학습 흐름에 맞춰 배치).*
