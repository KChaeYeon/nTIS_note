# E-field Map Viewer Multi-Mode Extension Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `docs/05_Code/Simulation/efield_map_viewer.m` so it loads 4 independent single-electrode COMSOL CSVs and lets the user switch between three views in one GUI: 단일전극 (any of 4 electrodes alone), 페어 (CH1 dipole or CH2 dipole), and AM (TI envelope modulation depth computed from both pairs, via a user-authored formula stub).

**Architecture:** Same single self-contained MATLAB function file as before. The main function's data-loading/computation section grows to load 4 files and derive pair/AM fields via `scatteredInterpolant`; the GUI section gains a second "target" dropdown whose `Items` change based on a new "mode" dropdown, and a scatter-plot fallback for AM (since AM has no direction, only magnitude). `compute_AM` is a new local function left as a stub for the user to fill in.

**Tech Stack:** MATLAB (R2022a+, as before). No new toolboxes.

## Global Constraints

- Input files (already placed by the user, exact paths verified to exist):
  - `D:\00_Project\nTIS\docs\07_Simulation\Result\20260626_TI_field_Base_X50_Y50_leadField_f1_Ch1.csv` (전극1, CH1)
  - `..._leadField_f1_Ch2.csv` (전극2, CH1)
  - `..._leadField_f2_Ch3.csv` (전극3, CH2)
  - `..._leadField_f2_Ch4.csv` (전극4, CH2)
  - Each file has 4 columns (`x,y,ec.Ex,ec.Ey`, single electrode — `load_leadfield_2d` already handles this via automatic column-count detection, no loader changes needed).
  - The 4 files have **different node counts** (864/874/861/868) — they are independently meshed. Any code that combines two channels' fields pointwise MUST interpolate one onto the other's coordinates first, via `scatteredInterpolant(..., 'linear', 'nearest')` (same pattern already used and reviewed in `efield_flux_slider_tool.m`).
- Electrode coordinates (phantom 50×50, existing `electrodeTable` lookup, `ex=25, ey=20`):
  전극1=(−25,+20), 전극2=(−25,−20), 전극3=(+25,+20), 전극4=(+25,−20).
- CH1 페어 = `E_ch1 - E2_interpolated_onto_coords_ch1`, defined on `coords_ch1`.
  CH2 페어 = `E_ch3 - E4_interpolated_onto_coords_ch3`, defined on `coords_ch3`.
  AM는 CH2 페어를 `coords_ch1`에 다시 보간한 뒤, `coords_ch1` 위에서 계산한다.
- `compute_AM(Ex1, Ey1, Ex2, Ey2)` is a new **local function** (vectorized Nx1 in/out) that currently just `error(...)` — the user will fill in the formula later. It must NOT be implemented by the plan/implementer; only the stub + call site + error handling are in scope.
- If `compute_AM` throws (stub not yet implemented), entering AM mode must show a `uialert` with the thrown message and fall back to 단일전극 mode — it must NOT crash the GUI.
- Axis limits stay fixed at `[-35, 35]` regardless of mode/target/slider — unchanged from before.
- Normalization (arrow length + `clim` color scale) is computed independently per mode: 단일전극 → `max(Emag_ch1,...,Emag_ch4)` combined; 페어 → `max(Emag_pair1, Emag_pair2)` combined; AM → `max(AM)` alone.
- Scale slider (`[0.2, 20]`, default `1`) and its two labels stay visible for 단일전극/페어, and are hidden (`Visible='off'`) for AM (AM uses a fixed-size scatter marker, no arrows).
- No MATLAB/Octave runner exists in this environment. Every verification step is a manual procedure the user runs in Windows MATLAB — the implementing agent cannot execute `.m` files itself.

---

### Task 1: Multi-mode data pipeline + GUI rewrite

**Files:**
- Modify: `docs/05_Code/Simulation/efield_map_viewer.m`

**Interfaces:**
- Produces: local function `compute_AM(Ex1, Ey1, Ex2, Ey2)` — stub, throws until the user implements it.
- No other file depends on this one; this is the whole feature in a single self-contained rewrite of the main function (the `load_leadfield_2d` local function at the bottom of the file is unchanged and untouched).

This task replaces the ENTIRE main function `efield_map_viewer()` (currently lines 1–145 of the file, from `function efield_map_viewer()` down to the `end` that closes it — everything before the two blank lines that precede `function [coords, Etensor] = load_leadfield_2d(filepath)`) with the code below. The `load_leadfield_2d` function itself, and the blank lines separating it from the main function, are NOT touched.

- [ ] **Step 1: Replace the entire main function with the multi-mode version**

Replace everything from the file's first line (`function efield_map_viewer()`) through the `end` that closes that function (i.e. everything before the blank lines preceding `function [coords, Etensor] = load_leadfield_2d(filepath)`) with:

```matlab
function efield_map_viewer()
%EFIELD_MAP_VIEWER Multi-mode E-field map viewer (single electrode / pair / AM).
%
%   4개 COMSOL 단일전극 lead-field CSV(전극1~4 각각 단독 인가, 준정적 근사이므로
%   실수부만 사용)를 읽어 phantom 경계 + 전극 위치 위에 전기장을 시각화한다.
%   "보기 모드" 드롭다운으로 단일전극/페어/AM을 전환하고, "대상 선택" 드롭다운으로
%   모드별 대상을 고르며, 슬라이더로 화살표 크기를 조절한다(AM 모드는 화살표 없음).
%
%   실행: MATLAB 커맨드 창에서 efield_map_viewer

    %% ---- 경로 설정 ----
    simDir = 'D:\00_Project\nTIS\docs\07_Simulation\Result';
    ch1File = fullfile(simDir, '20260626_TI_field_Base_X50_Y50_leadField_f1_Ch1.csv');
    ch2File = fullfile(simDir, '20260626_TI_field_Base_X50_Y50_leadField_f1_Ch2.csv');
    ch3File = fullfile(simDir, '20260626_TI_field_Base_X50_Y50_leadField_f2_Ch3.csv');
    ch4File = fullfile(simDir, '20260626_TI_field_Base_X50_Y50_leadField_f2_Ch4.csv');

    channelFiles = {ch1File, ch2File, ch3File, ch4File};
    for i = 1:numel(channelFiles)
        if ~isfile(channelFiles{i})
            error('파일을 찾을 수 없습니다: %s\n simDir/파일명을 확인하세요.', channelFiles{i});
        end
    end

    [coords_ch1, Etensor1] = load_leadfield_2d(ch1File);
    [coords_ch2, Etensor2] = load_leadfield_2d(ch2File);
    [coords_ch3, Etensor3] = load_leadfield_2d(ch3File);
    [coords_ch4, Etensor4] = load_leadfield_2d(ch4File);

    E_ch1 = squeeze(Etensor1(1, :, :));
    E_ch2 = squeeze(Etensor2(1, :, :));
    E_ch3 = squeeze(Etensor3(1, :, :));
    E_ch4 = squeeze(Etensor4(1, :, :));

    Emag_ch1 = sqrt(sum(E_ch1.^2, 2));
    Emag_ch2 = sqrt(sum(E_ch2.^2, 2));
    Emag_ch3 = sqrt(sum(E_ch3.^2, 2));
    Emag_ch4 = sqrt(sum(E_ch4.^2, 2));

    % ── 전극 좌표: phantom 크기 → 전극 오프셋 실측 lookup (기존과 동일) ──
    electrodeTable = [ ...
        50 50 25 20; ...
        30 50 15 20; ...
        10 50  5 20; ...
        50 30 20 15; ...
        50 10 20  5; ...
        30 30 15 10; ...
        10 10  5  2.5];

    baseName = 'COMSOL_Efield_Base_X50_Y50';
    xyMatch = regexp(baseName, 'X(\d+)_Y(\d+)$', 'tokens');
    if isempty(xyMatch)
        error('baseName ''%s''에서 X##_Y## 패턴을 찾을 수 없습니다.', baseName);
    end
    phantomX = str2double(xyMatch{1}{1});
    phantomY = str2double(xyMatch{1}{2});

    rowMatch = electrodeTable(:, 1) == phantomX & electrodeTable(:, 2) == phantomY;
    if ~any(rowMatch)
        error('팬텀 크기 (%d, %d)에 대한 전극 좌표가 electrodeTable에 없습니다.', phantomX, phantomY);
    end
    ex = electrodeTable(rowMatch, 3);
    ey = electrodeTable(rowMatch, 4);

    elec1 = [-ex, ey];    % 전극1 (CH1)
    elec2 = [-ex, -ey];   % 전극2 (CH1)
    elec3 = [ex, ey];     % 전극3 (CH2)
    elec4 = [ex, -ey];    % 전극4 (CH2)

    fprintf('전극1: (%.2f, %.2f) mm,  전극2: (%.2f, %.2f) mm,  전극3: (%.2f, %.2f) mm,  전극4: (%.2f, %.2f) mm\n', ...
        elec1(1), elec1(2), elec2(1), elec2(2), elec3(1), elec3(2), elec4(1), elec4(2));

    %% ---- 페어(다이폴) 합성: 서로 다른 mesh를 보간해 결합 ----
    F2x = scatteredInterpolant(coords_ch2(:, 1), coords_ch2(:, 2), E_ch2(:, 1), 'linear', 'nearest');
    F2y = scatteredInterpolant(coords_ch2(:, 1), coords_ch2(:, 2), E_ch2(:, 2), 'linear', 'nearest');
    E2_on1 = [F2x(coords_ch1(:, 1), coords_ch1(:, 2)), F2y(coords_ch1(:, 1), coords_ch1(:, 2))];
    E_pair1 = E_ch1 - E2_on1;              % CH1 페어, coords_ch1 기준
    Emag_pair1 = sqrt(sum(E_pair1.^2, 2));

    F4x = scatteredInterpolant(coords_ch4(:, 1), coords_ch4(:, 2), E_ch4(:, 1), 'linear', 'nearest');
    F4y = scatteredInterpolant(coords_ch4(:, 1), coords_ch4(:, 2), E_ch4(:, 2), 'linear', 'nearest');
    E4_on3 = [F4x(coords_ch3(:, 1), coords_ch3(:, 2)), F4y(coords_ch3(:, 1), coords_ch3(:, 2))];
    E_pair2 = E_ch3 - E4_on3;              % CH2 페어, coords_ch3 기준
    Emag_pair2 = sqrt(sum(E_pair2.^2, 2));

    %% ---- AM: CH2 페어를 coords_ch1에 보간 후 노드별 계산 ----
    Fp2x = scatteredInterpolant(coords_ch3(:, 1), coords_ch3(:, 2), E_pair2(:, 1), 'linear', 'nearest');
    Fp2y = scatteredInterpolant(coords_ch3(:, 1), coords_ch3(:, 2), E_pair2(:, 2), 'linear', 'nearest');
    E_pair2_on1 = [Fp2x(coords_ch1(:, 1), coords_ch1(:, 2)), Fp2y(coords_ch1(:, 1), coords_ch1(:, 2))];

    try
        AM = compute_AM(E_pair1(:, 1), E_pair1(:, 2), E_pair2_on1(:, 1), E_pair2_on1(:, 2));
        amReady = true;
        amErrMsg = '';
    catch amErr
        AM = [];
        amReady = false;
        amErrMsg = amErr.message;
    end

    %% ---- 모드별 정규화 기준(길이/색상 clim) ----
    maxEmagSingle = max([Emag_ch1; Emag_ch2; Emag_ch3; Emag_ch4]);
    maxEmagPair = max([Emag_pair1; Emag_pair2]);
    if amReady
        maxAM = max(AM);
    else
        maxAM = 1;   % 플레이스홀더 — AM 모드는 uialert로 막히므로 실제로 쓰이지 않음
    end

    fprintf('단일전극 max|E| = %.6g V/m,  페어 max|E| = %.6g V/m\n', maxEmagSingle, maxEmagPair);

    %% ---- 축 범위: phantom 최대 좌표 + 10mm 고정 ----
    axLim = max(phantomX, phantomY) / 2 + 10;

    %% ---- Figure / Axes ----
    fig = uifigure('Name', 'E-field Map Viewer (Base_X50_Y50, multi-mode)', ...
        'Position', [100 80 950 860]);
    ax = uiaxes(fig, 'Position', [60 260 700 540]);
    axis(ax, 'equal');
    xlim(ax, [-axLim, axLim]);
    ylim(ax, [-axLim, axLim]);
    hold(ax, 'on');
    grid(ax, 'on');
    xlabel(ax, 'x [mm]');
    ylabel(ax, 'y [mm]');
    colormap(ax, 'parula');
    cb = colorbar(ax);
    clim(ax, [0, maxEmagSingle]);

    % 팬텀 경계(검정 실선 사각형)
    rectangle(ax, 'Position', [-phantomX / 2, -phantomY / 2, phantomX, phantomY], ...
        'EdgeColor', 'k', 'LineWidth', 1.5);

    % 전극 4개(검정 점, 선택된 쪽은 빨간 테두리로 강조)
    elecH1 = plot(ax, elec1(1), elec1(2), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 10, 'LineWidth', 1);
    elecH2 = plot(ax, elec2(1), elec2(2), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 10, 'LineWidth', 1);
    elecH3 = plot(ax, elec3(1), elec3(2), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 10, 'LineWidth', 1);
    elecH4 = plot(ax, elec4(1), elec4(2), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 10, 'LineWidth', 1);
    text(ax, elec1(1) + 1.5, elec1(2), '전극1');
    text(ax, elec2(1) + 1.5, elec2(2), '전극2');
    text(ax, elec3(1) + 1.5, elec3(2), '전극3');
    text(ax, elec4(1) + 1.5, elec4(2), '전극4');
    elecHandles = [elecH1, elecH2, elecH3, elecH4];

    %% ---- |E| 크기별 색상 quiver (nBins개 그룹) + AM용 scatter ----
    nBins = 20;
    cmap = parula(nBins);
    qHandles = gobjects(nBins, 1);
    for b = 1:nBins
        qHandles(b) = quiver(ax, NaN, NaN, NaN, NaN, 0, ...
            'Color', cmap(b, :), 'LineWidth', 0.8, 'AutoScale', 'off');
    end
    amScatter = scatter(ax, NaN, NaN, 20, [0 0 0], 'filled');
    amScatter.Visible = 'off';

    %% ---- 컨트롤: 보기 모드 + 대상 선택은 그래프 바로 위쪽(축 밖)에 배치 ----
    uilabel(fig, 'Position', [60 810 90 22], 'Text', '보기 모드:');
    modeDropdown = uidropdown(fig, 'Position', [150 810 130 22], ...
        'Items', {'단일전극', '페어', 'AM'}, 'Value', '단일전극');

    uilabel(fig, 'Position', [300 810 90 22], 'Text', '대상 선택:');
    targetDropdown = uidropdown(fig, 'Position', [390 810 160 22], ...
        'Items', {'전극1', '전극2', '전극3', '전극4'}, 'Value', '전극1');

    scaleLabelUi = uilabel(fig, 'Position', [60 205 300 22], 'Text', '화살표 크기 배율:');
    scaleSld = uislider(fig, 'Position', [90 170 700 3], 'Limits', [0.2 20], 'Value', 1);
    scaleSld.MajorTicks = [];
    scaleSld.MinorTicks = [];
    scaleLbl = uilabel(fig, 'Position', [90 135 700 22], 'FontSize', 13);

    modeDropdown.ValueChangedFcn = @(src, event) on_mode_changed();
    targetDropdown.ValueChangedFcn = @(src, event) update_display(scaleSld.Value);
    scaleSld.ValueChangingFcn = @(src, event) update_display(event.Value);

    update_display(1);  % 초기 렌더 (단일전극 / 전극1 / 배율 1x)

    function render_quiver(coordsSel, Esel, Emag, maxVal, scaleMult)
        binEdges = linspace(0, maxVal, nBins + 1);
        clim(ax, [0, maxVal]);
        cb.Label.String = '|E| [V/m]';
        scaleLen = (3 / maxVal) * scaleMult;
        Uall = Esel(:, 1) * scaleLen;
        Vall = Esel(:, 2) * scaleLen;
        for b = 1:nBins
            if b < nBins
                mask = Emag >= binEdges(b) & Emag < binEdges(b + 1);
            else
                mask = Emag >= binEdges(b) & Emag <= binEdges(b + 1);
            end
            set(qHandles(b), 'XData', coordsSel(mask, 1), 'YData', coordsSel(mask, 2), ...
                'UData', Uall(mask), 'VData', Vall(mask));
        end
    end

    function update_display(scaleMult)
        if nargin < 1 || isempty(scaleMult)
            scaleMult = scaleSld.Value;
        end

        set(elecHandles, 'MarkerEdgeColor', 'k', 'LineWidth', 1);

        switch modeDropdown.Value
            case '단일전극'
                switch targetDropdown.Value
                    case '전극1'
                        coordsSel = coords_ch1; Esel = E_ch1; Emag = Emag_ch1; hi = 1;
                    case '전극2'
                        coordsSel = coords_ch2; Esel = E_ch2; Emag = Emag_ch2; hi = 2;
                    case '전극3'
                        coordsSel = coords_ch3; Esel = E_ch3; Emag = Emag_ch3; hi = 3;
                    otherwise
                        coordsSel = coords_ch4; Esel = E_ch4; Emag = Emag_ch4; hi = 4;
                end
                set(elecHandles(hi), 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
                render_quiver(coordsSel, Esel, Emag, maxEmagSingle, scaleMult);
                amScatter.Visible = 'off';

            case '페어'
                if strcmp(targetDropdown.Value, 'CH1 페어(1-2)')
                    coordsSel = coords_ch1; Esel = E_pair1; Emag = Emag_pair1;
                    set(elecHandles([1 2]), 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
                else
                    coordsSel = coords_ch3; Esel = E_pair2; Emag = Emag_pair2;
                    set(elecHandles([3 4]), 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
                end
                render_quiver(coordsSel, Esel, Emag, maxEmagPair, scaleMult);
                amScatter.Visible = 'off';

            case 'AM'
                set(elecHandles, 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
                for b = 1:nBins
                    set(qHandles(b), 'XData', [], 'YData', [], 'UData', [], 'VData', []);
                end
                clim(ax, [0, maxAM]);
                cb.Label.String = 'AM envelope depth [V/m]';
                amScatter.XData = coords_ch1(:, 1);
                amScatter.YData = coords_ch1(:, 2);
                amScatter.CData = AM;
                amScatter.Visible = 'on';
        end

        scaleLbl.Text = sprintf('배율: %.2fx', scaleMult);
    end

    function on_mode_changed()
        switch modeDropdown.Value
            case '단일전극'
                targetDropdown.Items = {'전극1', '전극2', '전극3', '전극4'};
                targetDropdown.Value = '전극1';
                targetDropdown.Enable = 'on';
                scaleLabelUi.Visible = 'on';
                scaleSld.Visible = 'on';
                scaleLbl.Visible = 'on';
            case '페어'
                targetDropdown.Items = {'CH1 페어(1-2)', 'CH2 페어(3-4)'};
                targetDropdown.Value = 'CH1 페어(1-2)';
                targetDropdown.Enable = 'on';
                scaleLabelUi.Visible = 'on';
                scaleSld.Visible = 'on';
                scaleLbl.Visible = 'on';
            case 'AM'
                if ~amReady
                    uialert(fig, amErrMsg, 'AM 계산 미구현');
                    modeDropdown.Value = '단일전극';
                    on_mode_changed();
                    return;
                end
                targetDropdown.Enable = 'off';
                scaleLabelUi.Visible = 'off';
                scaleSld.Visible = 'off';
                scaleLbl.Visible = 'off';
        end
        update_display(scaleSld.Value);
    end

    function AM = compute_AM(Ex1, Ey1, Ex2, Ey2)
    %COMPUTE_AM TI amplitude-modulation (envelope) depth from two dipole fields.
    %   Ex1,Ey1 : CH1 pair field components (Nx1 V/m, coords_ch1 기준)
    %   Ex2,Ey2 : CH2 pair field components, coords_ch1에 보간된 값 (Nx1 V/m)
    %   AM      : 각 노드의 envelope modulation depth (Nx1 V/m)
    %
    %   TODO(user): TI envelope 공식을 벡터화 연산으로 작성하세요.
        error('compute_AM: 공식을 아직 작성하지 않았습니다.');
    end
end
```

- [ ] **Step 2: Manual verification (run in Windows MATLAB)**

Run: `efield_map_viewer`.

Expected console output (electrode coordinates must match exactly; the two max-magnitude numbers will vary but must be positive finite values):
```
전극1: (-25.00, 20.00) mm,  전극2: (-25.00, -20.00) mm,  전극3: (25.00, 20.00) mm,  전극4: (25.00, -20.00) mm
단일전극 max|E| = <positive number> V/m,  페어 max|E| = <positive number> V/m
```

Confirm visually:
1. **단일전극 모드 (기본값)**: 4개 전극 점이 모두 표시되고, "대상 선택"에 전극1~4가 보이며, 기본값 전극1의 마커가 빨간 테두리. 화살표는 전극1 위치 주변에 집중되어 나타난다.
2. **대상 선택을 전극3으로 변경**: 화살표가 즉시 전극3(우측 상단, `(25,20)`) 주변으로 다시 그려지고, 전극3 마커만 빨간 테두리가 된다. 축 범위는 여전히 `[-35,35]`.
3. **보기 모드를 "페어"로 변경**: "대상 선택"이 `CH1 페어(1-2)` / `CH2 페어(3-4)`로 바뀌고, 기본값 CH1 페어에서 전극1·전극2 마커가 둘 다 빨간 테두리가 되며, 다이폴 형태의 화살표 패턴이 나타난다.
4. **보기 모드를 "AM"으로 변경**: `compute_AM`이 아직 구현되지 않았으므로 "AM 계산 미구현"이라는 제목의 알림창(`uialert`)이 뜨고, 모드가 자동으로 "단일전극"으로 되돌아간다. GUI가 멈추거나 에러로 죽지 않아야 한다.
5. **화살표 크기 슬라이더**: 단일전극/페어 모드에서는 정상적으로 화살표 크기를 실시간 조절한다.
6. 콘솔에 MATLAB 에러/경고가 없어야 한다.

- [ ] **Step 3: Commit**

```bash
git add docs/05_Code/Simulation/efield_map_viewer.m
git commit -m "feat: add multi-mode (single/pair/AM) view switching to e-field viewer"
```

---

### Task 2: Final integrated manual QA

**Files:**
- Modify: `docs/05_Code/Simulation/efield_map_viewer.m` (no further code changes expected — this task is verification only, unless Task 1's review surfaced fixes that still need a human-confirmed re-check)

**Interfaces:** None (terminal task).

- [ ] **Step 1: Final integrated manual verification (run in Windows MATLAB)**

Run: `efield_map_viewer`, and walk through all three modes end-to-end, confirming every item in Task 1 Step 2's checklist still holds, plus:

1. Switch 단일전극 → 페어 → 단일전극 → 페어 repeatedly; confirm no leftover arrows from the previous mode linger (the previous mode's quiver bins or the AM scatter must be fully cleared/hidden each time).
2. Switch to 페어 mode, move the scale slider to e.g. 5x, then switch target from CH1 페어 to CH2 페어 — confirm the 5x scale is preserved (not reset to 1x), matching the same "preserve scale across target switch" behavior as the original single-electrode dropdown.
3. Confirm the colorbar label reads "|E| [V/m]" in 단일전극/페어 modes.
4. Note down (for future reference, not required to complete now) that once `compute_AM` is implemented by the user, AM mode should be re-tested for: colorbar label "AM envelope depth [V/m]", scatter dot colors spanning the AM value range, and the scale slider/labels correctly hidden.

- [ ] **Step 2: Commit (only if Step 1 required any fix)**

If Step 1's checklist passes with no code changes needed, skip this step — Task 1's commit already captures the final state. If a fix was needed, commit it with a message describing the specific defect fixed.
