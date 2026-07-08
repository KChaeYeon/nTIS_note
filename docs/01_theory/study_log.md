# TI 전기장 이론 학습 로그 (세션 간 이어쓰기)

`ti-efield-theory` 스킬 / `theory-mentor` 에이전트가 세션 시작 시 이 파일을 먼저 읽고,
세션 종료 시(또는 체크포인트 통과 시) 갱신한다. 자유 형식이 아니라 아래 표 형식을 유지할 것.

## 현재 위치

| 항목 | 내용 |
|------|------|
| 학습 단계 | 0단계 — 단일 전극/단일 채널 기초 (TIS AM modulation 이전 선행 단계) |
| 참조 노트 | `05_EM_physics_FEM.md` (기존 노트는 TIS 중첩부터 시작 — 단일 전극 기초는 신규 보강 대상) |
| 마지막 체크포인트 | (진행 중) |
| 막힌 지점 | — |
| 다음 시작점 | (A) 이론: 3D(반구) flux 적분로 확장 — 반구 표면적 공식부터 시작해 2D(1/r) vs 3D(1/r²) 스케일링 비교. (B) 코드: `efield_flux_slider_tool.m`을 MATLAB에서 실제 실행해서 GUI(반지름 슬라이더/배율 슬라이더/클릭 조회/우측 테이블/상단 검증 라벨)가 정상 동작하는지, 레이아웃 겹침·잘림이 완전히 해결됐는지 확인부터. 그 다음 `efield_analysis.ipynb`의 `flux_at_radius`도 electrode geometry 반영 버전으로 실행해 실제 데이터 검증 |

## 세션 기록

<!-- 세션마다 아래 형식으로 한 줄씩 추가 (최신이 위) -->

| 날짜 | 다룬 주제 | 도달 지점 | 특이사항 |
|------|-----------|-----------|----------|
| 2026-07-07 | (이어서) MATLAB GUI 실전 검증 도구 완성 — Arrow.csv(실제 COMSOL J 데이터)로 flux 계산 전환, 우측 테이블(|J|/방향/기여도), 화살표 배율 슬라이더, 클릭 조회, 레이아웃 정리 | 코드 도구 완성 단계 (MATLAB에서 미실행 — 사용자 실행 확인 필요) | `efield_flux_slider_tool.m`을 Arrow.csv(x,y,ec.Jx,ec.Jy) 기반으로 전면 개편. leadField(E)와 교차검증(실제 데이터로 cosθ≈0.9975, σ≈1.46 S/m 확인, Python 재현 테스트 통과). flux 반지름 무관성도 실제 COMSOL 데이터로 확인(r=7~31mm에서 flux≈0.90~0.95로 안정). 전극 좌표는 ELECTRODE_XY_TABLE(4번 셀과 동일 geometry) 사용, argmax 추정 아님. 화살표는 서브샘플링 없이 CSV 전체 노드 표시 |
| 2026-07-07 | J=σE, 연속방정식, 2D point-source flux 적분(전류 보존) 이론 + 실제 COMSOL lead field 데이터로 코드 검증 도구 제작 | flux 적분 개념 완료, 코드 실습 단계 | `efield_analysis.ipynb`에 `flux_at_radius` 함수 구현(TODO 아님, 직접 완성) + `efield_flux_slider_tool.ipynb`/`.m` (반지름 슬라이더 인터랙티브 검증 도구) 신규 생성 |
| 2026-07-07 | 0단계 시작 — 단일 전극 전류 인가 시 전기장/전류밀도 기초 (비전공자 설명) | 시작 | 사용자가 TIS AM modulation보다 먼저 단일 채널 기초를 원함 — 학습 순서를 0단계로 재조정 |
| 2026-07-07 | 세팅 (에이전트/스킬/로그 확인) | 학습 시작 전 — 세팅 완료 | 기존 `theory-mentor` 에이전트 + `ti-efield-theory` 스킬 재사용, 신규 스킬 생성 없음 |

## 표기법 고정 (세션 전체 통일)

```
전극쌍 1: I1 = A·sin(2πf1·t),  전극쌍 2: I2 = A·sin(2πf2·t)   (f1 > f2, Δf = f1 - f2)
중첩 전기장: E(t) = E1·sin(2πf1·t + φ1) + E2·sin(2πf2·t + φ2)
Envelope 진폭: |E_AM(t)|
n-phase 일반화: E(t) = Σ_{k=1}^{n} E_k·sin(2πf_k·t + φ_k)
```

(`ti-efield-theory` 스킬 "핵심 수식 골격"과 동일 — 여기서 재확인만 함)
