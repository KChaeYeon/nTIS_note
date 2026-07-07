# E-field Map Viewer — Multi-Mode Extension (Single / Pair / AM) — Design

## 배경 & 목적

기존 `efield_map_viewer.m`(전극1/전극2 단독 lead field 뷰어)을 확장해, 사용자가 새로 진행한
COMSOL 시뮬레이션(4전극 각각 단독 인가) 데이터를 기반으로 세 가지 관점을 하나의 GUI에서
전환하며 볼 수 있게 한다:

- **단일전극**: 전극1~4 중 하나를 단독으로 봄 (기존 기능의 4전극 확장판)
- **페어**: CH1 페어(전극1−전극2, dipole 합성장) 또는 CH2 페어(전극3−전극4)
- **AM**: CH1 페어 + CH2 페어를 합쳐 TI(temporal interference) envelope modulation 깊이를 계산

## 입력 데이터

새로 제공된 4개 파일 (`docs/07_Simulation/Result/`), 각각 순수 단일전극 COMSOL 시뮬레이션 결과:

| 파일 | 전극 | 채널/주파수 | 노드 수(실측) |
|------|------|------------|--------------|
| `20260626_TI_field_Base_X50_Y50_leadField_f1_Ch1.csv` | 전극1 | CH1 (f1) | 864 |
| `20260626_TI_field_Base_X50_Y50_leadField_f1_Ch2.csv` | 전극2 | CH1 (f1) | 874 |
| `20260626_TI_field_Base_X50_Y50_leadField_f2_Ch3.csv` | 전극3 | CH2 (f2) | 861 |
| `20260626_TI_field_Base_X50_Y50_leadField_f2_Ch4.csv` | 전극4 | CH2 (f2) | 868 |

각 파일은 컬럼 `x,y,ec.Ex (V/m) @ idx=N,ec.Ey (V/m) @ idx=N` (4컬럼, 단일 전극)로, 기존
`load_leadfield_2d` 로더가 컬럼 수로 전극 개수를 자동 판별하므로 **수정 없이 그대로 재사용**
가능하다(단일 파일당 `numElectrodes=1`).

**중요**: 4개 파일은 COMSOL이 각각 독립적으로 재메싱한 결과라 **좌표(mesh)가 서로 다르다**
(864/874/861/868개로 노드 수부터 다름). 두 전극 데이터를 점별로 결합해야 하는 페어·AM
계산에서는 반드시 보간이 필요하다.

전극 좌표(phantom 50×50 기준, 기존 `electrodeTable`과 동일):
- 전극1 = (−25, +20), 전극2 = (−25, −20) — CH1
- 전극3 = (+25, +20), 전극4 = (+25, −20) — CH2 (phantom 우측, 기존 electrodeTable 좌우 대칭)

## 데이터 파이프라인

1. 4개 파일을 각각 `load_leadfield_2d`로 로드 → `coords_ch{i}`, `E_ch{i}` (i=1..4), `Emag_ch{i}`.
2. **CH1 페어**: 전극1의 mesh(`coords_ch1`)를 기준 좌표로 삼아, 전극2 필드를
   `scatteredInterpolant`(linear, nearest-extrapolation — 기존 `efield_flux_slider_tool.m`의
   검증된 보간 패턴과 동일)로 `coords_ch1`에 보간한 뒤 `E_pair1 = E_ch1 - E2_interp`.
3. **CH2 페어**: 전극3의 mesh(`coords_ch3`)를 기준으로 동일하게
   `E_pair2 = E_ch3 - E4_interp`.
4. **AM**: `coords_ch1`을 공통 기준 좌표로 삼아 `E_pair2`를 다시 `coords_ch1`에 보간한 뒤,
   같은 좌표 집합에서 노드별로 `compute_AM(Ex1,Ey1,Ex2,Ey2)`를 벡터화 호출.

## AM 공식 — 사용자 작성

TI envelope modulation 공식은 연구 이해의 핵심이므로 값 채워 넣기는 사용자가 직접 한다.
시그니처는 기존 코드 스타일(전부 벡터화 연산)과 맞춰 **Nx1 벡터 입출력**으로 고정한다:

```matlab
function AM = compute_AM(Ex1, Ey1, Ex2, Ey2)
%COMPUTE_AM TI amplitude-modulation (envelope) depth from two dipole fields.
%   Ex1,Ey1 : CH1 pair field components (Nx1 V/m, coords_ch1 기준)
%   Ex2,Ey2 : CH2 pair field components, coords_ch1에 보간된 값 (Nx1 V/m)
%   AM      : 각 노드의 envelope modulation depth (Nx1 V/m)
%
%   TODO(user): TI envelope 공식을 벡터화 연산으로 작성하세요.
    error('compute_AM: 공식을 아직 작성하지 않았습니다.');
end
```

GUI는 이 함수가 `error`를 던지면(아직 미구현) AM 모드 진입 시 그 메시지를 그대로
`uialert`로 보여주고, 나머지 모드(단일전극/페어)는 정상 동작해야 한다.

## GUI 변경

- **"보기 모드" 드롭다운** (그래프 위, 기존 전극 선택 드롭다운 자리 그대로 재사용):
  `단일전극 / 페어 / AM`
- **"대상 선택" 드롭다운** (그 옆, 새로 추가): 모드에 따라 `Items`가 동적으로 바뀜
  - 단일전극 → `전극1 / 전극2 / 전극3 / 전극4`
  - 페어 → `CH1 페어(1-2) / CH2 페어(3-4)`
  - AM → 비활성화(`Enable = 'off'`, 표시할 항목 없음 — 항상 두 페어 다 사용)
- **화살표 크기 슬라이더**: 단일전극/페어 모드에서는 그대로 표시(quiver 배율), AM
  모드에서는 `Visible='off'`로 숨김(점 크기 고정, 화살표 없음)
- **렌더링 방식**:
  - 단일전극/페어: 기존과 동일한 20-bin 색상 quiver(길이 ∝ |E|, 색상 ∝ |E|)
  - AM: 화살표 없이 `scatter(ax, x, y, 20, AM, 'filled')` 점 색상맵만 사용(길이 개념 없음)
- **정규화 기준(길이/색상 clim)은 모드별로 독립적으로 재계산**:
  - 단일전극 모드: 전극1~4 통합 `max(|E1|,|E2|,|E3|,|E4|)` (4개 mesh가 다르므로 각 파일 내
    최댓값들의 최댓값)
  - 페어 모드: 두 페어 통합 `max(|E_pair1|, |E_pair2|)`
  - AM 모드: `max(AM)` 하나
- 축 범위([-35,35], phantom 사각형, 전극 마커 4개 위치 표시)는 모드와 무관하게 항상 고정.

## 에러 처리

- 4개 CSV 파일 중 하나라도 없으면, 기존 패턴과 동일하게 파일 경로를 포함한 한국어
  에러 메시지로 즉시 실패.
- `compute_AM`이 미구현 상태(`error` 발생)일 때 AM 모드를 선택하면 GUI가 크래시하지 않고
  `uialert`로 "아직 구현되지 않았습니다" 메시지를 보여주고 이전 모드로 되돌아간다.

## 파일 계획

- Modify: `docs/05_Code/Simulation/efield_map_viewer.m` (기존 파일 확장, 새 파일 생성 없음)

## 범위 밖 (Out of Scope)

- AM 공식 자체의 구현(사용자 담당)
- 4개 파일이 아직 없을 때의 자동 재시도/폴링 (사용자가 파일을 준비한 뒤 실행하는 것을 전제)
- CH1/CH2 외 추가 채널, n-phase(3개 이상 전극) 확장
