# E-field Map Viewer (단일 전극 lead field 시각화) — Design

## 배경 & 목적

전극 배치에 따른 전기장 map 변화를 lead field 기반으로 역산하며 이해하기 위한 학습/분석 도구.
1단계로 COMSOL에서 1kHz, 1mA 단일 전극 인가 시뮬레이션 결과(`*_leadField_f1.csv`)를 MATLAB GUI로
시각화한다. 대상 파일은 `docs/07_Simulation/Result/COMSOL_Efield_Base_X50_Y50_leadField_f1.csv` 하나로
먼저 검증한다.

기존 `docs/05_Code/Simulation/efield_flux_slider_tool.m`은 전류(flux) 보존 검증용 도구로 목적이
다르므로 삭제하고, 이 설계 문서를 기반으로 새 파일을 처음부터 작성한다.

## 데이터

- 입력: `COMSOL_Efield_Base_X50_Y50_leadField_f1.csv`
  - 형식: `%`로 시작하는 헤더/주석 줄 + `x, y, ec.Ex(idx=1), ec.Ey(idx=1), ec.Ex(idx=2), ec.Ey(idx=2)`
  - 좌표 단위 mm, 값은 복소수 문자열(예: `3.02e-4-7.85e-10i`) — 준정적 근사이므로 실수부만 사용
  - 713개 비균일(unstructured) FEM mesh 노드 (전극 근처 촘촘, 먼 영역 성김)
  - idx=1, idx=2는 서로 다른 전극(단독 전류원)의 lead field
- 로더는 기존 `efield_flux_slider_tool.m`의 `load_leadfield_2d` 파싱 로직을 그대로 재사용한다
  (주석 skip, `str2num`으로 복소수 리터럴 파싱 후 `real()` 취득 — 이미 검증된 로직).

## 좌표계 (Phantom / 전극)

- 파일명 `Base_X50_Y50`에서 정규식 `X(\d+)_Y(\d+)$`로 `(50, 50)` 추출.
- Phantom 사각형: `[-X/2, X/2] × [-Y/2, Y/2]` mm (50×50mm → [-25,25]×[-25,25]).
  CSV mesh 노드의 실제 x,y 범위(-25~25)와 일치함을 확인함.
- 전극 좌표: 기존 코드의 `electrodeTable`(phantom 크기 → 전극 오프셋 실측 lookup)을 그대로 재사용.
  Base_X50_Y50 기준: 전극1(idx=1) = (-25, +20) mm, 전극2(idx=2) = (-25, -20) mm.
- 축 범위: `xlim = ylim = phantom 최대 좌표 절대값 + 10mm` (예: [-35, 35])로 고정.
  드롭다운 전환, 스케일 슬라이더 조작과 무관하게 절대 변경되지 않는다.

## GUI 구성 (uifigure 기반)

레이아웃은 기존 `efield_flux_slider_tool.m`과 동일한 `uifigure`/`uiaxes`/`uilabel`/`uislider` 스타일을
따르되, flux 검증용 우측 패널(테이블, 클릭 조회 등)은 제거하고 단순화한다.

- **axes**: 검은 실선 사각형(phantom 경계), 두 전극 위치를 항상 검은 점(●)으로 표시하고
  현재 선택된 전극은 강조색(예: 빨강) 테두리로 구분.
- **전극 선택 드롭다운** (`uidropdown`): "전극1", "전극2" 두 옵션. 변경 시 해당 전극의
  713개 노드 전체에 대해 quiver를 즉시 갱신.
- **화살표 스케일 슬라이더** (`uislider`, 기존 코드처럼 `ValueChangingFcn`으로 실시간 반응):
  배율 범위는 기존 코드와 동일하게 `[0.2, 20]`, 기본값 1.
- **화살표 인코딩**:
  - 길이 = `|E| × scaleLen × sliderMultiplier` (선형 비례)
  - 색상 = `|E|` 크기를 colormap(parula)으로 매핑, `colorbar` 1개 표시
  - 길이 정규화 기준(`baseScaleLen`)은 **전극1·전극2 통틀어 최댓값 |E|** 하나로 고정 →
    드롭다운으로 전극을 바꿔도 화살표 길이 스케일이 유지되어 두 전극 간 시각적 비교가 가능함.
  - colormap의 색상 범위(`caxis`/`clim`)도 동일하게 두 전극 통틀어 최댓값 기준으로 고정.
- **라벨 겹침 방지**: 기존 코드에서 이미 검증된 방식(고정 폭 `uilabel` + cell array 여러 줄 텍스트,
  각 컨트롤 사이 충분한 y-offset 간격)을 그대로 따른다.

## 에러 처리

- CSV 파일이 없으면 명확한 한국어 에러 메시지(파일 경로 포함)로 즉시 실패 — 기존 코드 패턴 유지.
- 파일명에서 `X##_Y##` 패턴을 못 찾거나 `electrodeTable`에 없는 phantom 크기면 에러.
- 그 외 방어적 코드(빈 데이터, NaN 처리 등)는 기존 로더의 `isnan` 필터링만으로 충분 — 추가 검증 없음.

## 파일 계획

- **삭제**: `docs/05_Code/Simulation/efield_flux_slider_tool.m`
- **신규 작성**: `docs/05_Code/Simulation/efield_map_viewer.m`
  - 단일 self-contained 함수 파일 (진입점 함수 + 로컬 함수들), 인자 없이
    `efield_map_viewer` 커맨드로 바로 실행.

## 범위 밖 (Out of Scope)

- flux/전류 보존 검증 로직 (기존 코드에 있던 기능, 이번엔 제외)
- Base_X50_Y50 외 다른 phantom 파일들 자동 순회 (전극 오프셋 lookup 테이블은 재사용하되,
  파일 선택 자체는 스크립트 상단 `baseName` 변수 수정 방식으로 기존과 동일하게 유지)
- AM_vector, Arrow.csv 등 다른 CSV 포맷 지원 (이번엔 leadField_f1.csv만)
