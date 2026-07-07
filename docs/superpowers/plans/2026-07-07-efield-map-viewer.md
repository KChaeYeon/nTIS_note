# E-field Map Viewer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a MATLAB GUI (`efield_map_viewer.m`) that visualizes a single electrode's lead-field E-vector map (phantom boundary, electrode markers, magnitude-scaled and magnitude-colored quiver arrows) from a COMSOL CSV export, with a dropdown to switch electrodes and a slider to scale arrow size in real time.

**Architecture:** Single self-contained MATLAB function file, `uifigure`-based (App Designer-style programmatic UI), following the exact structural conventions of the file it replaces (`efield_flux_slider_tool.m`): a main function with nested update callbacks, plus a reused local helper function for CSV parsing.

**Tech Stack:** MATLAB (R2022a+ assumed — uses `uifigure`, `uiaxes`, `uidropdown`, `uislider`, `clim`). No toolboxes beyond base MATLAB.

## Global Constraints

- Data source (fixed for this plan): `D:\00_Project\nTIS\docs\07_Simulation\Result\COMSOL_Efield_Base_X50_Y50_leadField_f1.csv`.
- Phantom: 50×50mm rectangle centered at (0,0), derived from `X50_Y50` in the filename.
- Electrode coordinates: reuse the `electrodeTable` lookup from `efield_flux_slider_tool.m` — for `(50,50)`: 전극1 (idx=1) = `(-25, +20)`, 전극2 (idx=2) = `(-25, -20)`.
- Axis limits: `xlim = ylim = [-(max(phantomX,phantomY)/2 + 10), +(max(phantomX,phantomY)/2 + 10)]` = `[-35, 35]`, fixed regardless of UI interaction.
- Arrow length: linear in `|E|`. Arrow color: `|E|` mapped through `parula` colormap with a colorbar.
- Length AND color normalization is fixed across both electrodes (computed once from `max(|E1|, |E2|)`), so switching electrodes doesn't rescale the visual encoding.
- Scale slider range `[0.2, 20]`, default `1` — same convention as the file being replaced.
- **No MATLAB/Octave runner exists in this environment** (verified: neither `matlab` nor `octave` is on PATH). Every task's verification step is therefore a **manual procedure the user runs in their own Windows MATLAB** — the implementing agent cannot execute `.m` files itself. Each task must still leave the file in a syntactically complete, runnable state so the user can verify incrementally.
- Delete `docs/05_Code/Simulation/efield_flux_slider_tool.m` as part of this plan (superseded; different purpose — flux/current verification, not in scope here).

---

### Task 1: Data loading + electrode geometry (console-only, no GUI yet)

**Files:**
- Create: `docs/05_Code/Simulation/efield_map_viewer.m`

**Interfaces:**
- Produces: `load_leadfield_2d(filepath)` → `[coords (Nx2 double), Etensor (numElectrodes x N x 2 double)]`. Later tasks call this and index `Etensor(1,:,:)` / `Etensor(2,:,:)`.
- Produces (in main function scope, used by later tasks): `coords`, `E1`, `E2`, `Emag1`, `Emag2`, `maxEmag`, `elec1`, `elec2`, `phantomX`, `phantomY`, `baseScaleLen`.

- [ ] **Step 1: Write `efield_map_viewer.m` with loader + geometry lookup only**

```matlab
function efield_map_viewer()
%EFIELD_MAP_VIEWER Interactive single-electrode lead-field map viewer.
%
%   실행: MATLAB 커맨드 창에서 efield_map_viewer
%   (이 단계에서는 데이터 로딩 및 좌표 계산만 수행하고 콘솔에 출력한다.
%    GUI는 다음 태스크에서 추가된다.)

    %% ---- 경로 설정 ----
    simDir   = 'D:\00_Project\nTIS\docs\07_Simulation\Result';
    baseName = 'COMSOL_Efield_Base_X50_Y50';
    leadFile = fullfile(simDir, [baseName '_leadField_f1.csv']);

    if ~isfile(leadFile)
        error('파일을 찾을 수 없습니다: %s\n simDir/baseName을 확인하세요.', leadFile);
    end

    [coords, Etensor] = load_leadfield_2d(leadFile);

    % ── 전극 좌표: phantom 크기 → 전극 오프셋 실측 lookup ──
    electrodeTable = [ ...
        50 50 25 20; ...
        30 50 15 20; ...
        10 50  5 20; ...
        50 30 20 15; ...
        50 10 20  5; ...
        30 30 15 10; ...
        10 10  5  2.5];

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

    elec1 = [-ex, ey];    % 전극1 (idx=1)
    elec2 = [-ex, -ey];   % 전극2 (idx=2)

    fprintf('전극1: (%.2f, %.2f) mm,  전극2: (%.2f, %.2f) mm\n', ...
        elec1(1), elec1(2), elec2(1), elec2(2));

    E1 = squeeze(Etensor(1, :, :));   % 전극1 단독 필드 (N x 2)
    E2 = squeeze(Etensor(2, :, :));   % 전극2 단독 필드 (N x 2)

    Emag1 = sqrt(sum(E1.^2, 2));
    Emag2 = sqrt(sum(E2.^2, 2));
    maxEmag = max([Emag1; Emag2]);   % 두 전극 통틀어 최댓값 — 길이/색상 정규화 기준 고정
    baseScaleLen = 3 / maxEmag;      % 배율 1x, |E|=maxEmag일 때 화살표 길이 = 3mm

    fprintf('노드 수 = %d, max|E| = %.6g V/m\n', size(coords, 1), maxEmag);
end


function [coords, Etensor] = load_leadfield_2d(filepath)
%LOAD_LEADFIELD_2D Load a COMSOL 2D lead-field CSV.
%   '%'로 시작하는 줄은 주석, 나머지는 x,y,그리고 전극별 (Ex,Ey) 복소수 쌍.
%   준정적 근사이므로 실수부만 사용한다.
%   (efield_flux_slider_tool.m의 동일 함수를 그대로 재사용)

    fid = fopen(filepath, 'rt');
    if fid == -1
        error('Cannot open file: %s', filepath);
    end

    rows = {};
    while true
        line = fgetl(fid);
        if ~ischar(line)
            break;
        end
        line = strtrim(line);
        if isempty(line) || startsWith(line, '%')
            continue;
        end
        rows{end + 1} = line; %#ok<AGROW>
    end
    fclose(fid);

    numRows = numel(rows);
    if numRows == 0
        error('No data rows found in %s', filepath);
    end

    numCols = numel(strsplit(rows{1}, ','));
    numeric = nan(numRows, numCols);

    for r = 1:numRows
        parts = strsplit(rows{r}, ',');
        for c = 1:min(numCols, numel(parts))
            s = strrep(strtrim(parts{c}), ' ', '');
            if isempty(s)
                continue;
            end
            v = str2num(s); %#ok<ST2NM>  % "1.23-4.56i" 형태의 복소수 리터럴도 처리
            if ~isempty(v)
                numeric(r, c) = real(v);
            end
        end
    end

    valid = ~any(isnan(numeric), 2);
    numeric = numeric(valid, :);

    coords = numeric(:, 1:2);
    fieldCols = numeric(:, 3:end);
    numElectrodes = floor(size(fieldCols, 2) / 2);
    N = size(numeric, 1);

    Etensor = zeros(numElectrodes, N, 2);
    for e = 1:numElectrodes
        Etensor(e, :, 1) = fieldCols(:, (e - 1) * 2 + 1);
        Etensor(e, :, 2) = fieldCols(:, (e - 1) * 2 + 2);
    end

    fprintf('Loaded %s — 전극 %d개, 유효 노드 %d개\n', filepath, numElectrodes, N);
end
```

- [ ] **Step 2: Manual verification (run in Windows MATLAB)**

Run: `efield_map_viewer` in the MATLAB command window (with `docs/05_Code/Simulation` on the path or as current folder).

Expected console output (numbers may vary slightly in the `max|E|` line, but must be present and finite):
```
Loaded D:\00_Project\nTIS\docs\07_Simulation\Result\COMSOL_Efield_Base_X50_Y50_leadField_f1.csv — 전극 2개, 유효 노드 713개
전극1: (-25.00, 20.00) mm,  전극2: (-25.00, -20.00) mm
노드 수 = 713, max|E| = <a positive finite number> V/m
```
Confirm: no errors thrown, node count is exactly 713, electrode coordinates match exactly.

- [ ] **Step 3: Commit**

```bash
git add docs/05_Code/Simulation/efield_map_viewer.m
git commit -m "feat: add e-field map viewer data loading + electrode geometry"
```

---

### Task 2: Static GUI shell — phantom boundary, electrode markers, fixed axis limits

**Files:**
- Modify: `docs/05_Code/Simulation/efield_map_viewer.m`

**Interfaces:**
- Consumes: `coords`, `elec1`, `elec2`, `phantomX`, `phantomY`, `maxEmag` from Task 1.
- Produces: `ax` (uiaxes handle), `elecH1`, `elecH2` (electrode marker plot handles) — later tasks restyle these on selection change.

- [ ] **Step 1: Insert GUI shell code into `efield_map_viewer.m`**

Replace the last two lines of the main function (the `fprintf('노드 수 = ...')` line and the closing `end`) with:

```matlab
    fprintf('노드 수 = %d, max|E| = %.6g V/m\n', size(coords, 1), maxEmag);

    %% ---- 축 범위: phantom 최대 좌표 + 10mm 고정 ----
    axLim = max(phantomX, phantomY) / 2 + 10;

    %% ---- Figure / Axes ----
    fig = uifigure('Name', 'E-field Map Viewer (Base_X50_Y50, single electrode)', ...
        'Position', [100 80 950 820]);
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
    cb.Label.String = '|E| [V/m]';
    clim(ax, [0, maxEmag]);

    % 팬텀 경계(검정 실선 사각형)
    rectangle(ax, 'Position', [-phantomX / 2, -phantomY / 2, phantomX, phantomY], ...
        'EdgeColor', 'k', 'LineWidth', 1.5);

    % 전극(검정 점, 선택된 쪽은 빨간 테두리로 강조 — 강조 로직은 Task 4에서 추가)
    elecH1 = plot(ax, elec1(1), elec1(2), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 10, 'LineWidth', 1);
    elecH2 = plot(ax, elec2(1), elec2(2), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 10, 'LineWidth', 1);
    text(ax, elec1(1) + 1.5, elec1(2), '전극1');
    text(ax, elec2(1) + 1.5, elec2(2), '전극2');
end
```

- [ ] **Step 2: Manual verification (run in Windows MATLAB)**

Run: `efield_map_viewer`.

Confirm visually:
- A `uifigure` window opens titled "E-field Map Viewer (Base_X50_Y50, single electrode)".
- A black solid-line square is drawn from (-25,-25) to (25,25).
- Two black dots appear at (-25, 20) and (-25, -20), labeled "전극1"/"전극2" without overlapping the axis border.
- Axis limits are exactly [-35, 35] on both x and y (check via zoom/pan reset or axes properties).
- A colorbar labeled "|E| [V/m]" is visible next to the axes.
- Console output matches Task 1's verification (no regression).

- [ ] **Step 3: Commit**

```bash
git add docs/05_Code/Simulation/efield_map_viewer.m
git commit -m "feat: add static phantom/electrode GUI shell with fixed axis limits"
```

---

### Task 3: Magnitude-colored, magnitude-scaled quiver arrows for electrode 1

**Files:**
- Modify: `docs/05_Code/Simulation/efield_map_viewer.m`

**Interfaces:**
- Consumes: `ax`, `coords`, `E1`, `Emag1`, `maxEmag`, `baseScaleLen` from Tasks 1–2.
- Produces: `qHandles` (1×20 `gobjects` array of quiver handles), `nBins`, `binEdges` — reused unchanged by Tasks 4–5.

**Design note:** MATLAB's `quiver` only supports one color per quiver object, so per-arrow magnitude coloring is done by splitting the 713 nodes into 20 fixed magnitude bins (edges spanning `[0, maxEmag]`, same edges regardless of which electrode is shown) and drawing one `quiver` object per bin, each colored by sampling `parula(20)`.

- [ ] **Step 1: Insert binned-quiver rendering, replacing the final `end` of the main function**

```matlab
    text(ax, elec1(1) + 1.5, elec1(2), '전극1');
    text(ax, elec2(1) + 1.5, elec2(2), '전극2');

    %% ---- |E| 크기별 색상 quiver (nBins개 그룹, 색상은 고정 [0, maxEmag] 스케일) ----
    nBins = 20;
    cmap = parula(nBins);
    binEdges = linspace(0, maxEmag, nBins + 1);
    qHandles = gobjects(nBins, 1);
    for b = 1:nBins
        qHandles(b) = quiver(ax, NaN, NaN, NaN, NaN, 0, ...
            'Color', cmap(b, :), 'LineWidth', 0.8, 'AutoScale', 'off');
    end

    % 전극1 데이터로 초기 렌더 (드롭다운/슬라이더는 Task 4-5에서 추가)
    Uall = E1(:, 1) * baseScaleLen;
    Vall = E1(:, 2) * baseScaleLen;
    for b = 1:nBins
        if b < nBins
            mask = Emag1 >= binEdges(b) & Emag1 < binEdges(b + 1);
        else
            mask = Emag1 >= binEdges(b) & Emag1 <= binEdges(b + 1);
        end
        set(qHandles(b), 'XData', coords(mask, 1), 'YData', coords(mask, 2), ...
            'UData', Uall(mask), 'VData', Vall(mask));
    end
end
```

- [ ] **Step 2: Manual verification (run in Windows MATLAB)**

Run: `efield_map_viewer`.

Confirm visually:
- Arrows appear at (approximately) all 713 mesh node positions, pointing outward/around 전극1 at (-25, 20) (전극1 is a current source in the lead-field sense — arrows should radiate from its vicinity).
- Arrows near 전극1 are visibly longer and colored toward the yellow end of `parula`; arrows far away are short and colored toward the dark blue end.
- No arrows appear at NaN/origin — i.e., no stray arrow at (0,0) from the initial `gobjects` placeholder.
- No MATLAB errors/warnings in the console.

- [ ] **Step 3: Commit**

```bash
git add docs/05_Code/Simulation/efield_map_viewer.m
git commit -m "feat: render magnitude-scaled and magnitude-colored quiver arrows for electrode 1"
```

---

### Task 4: Electrode selection dropdown

**Files:**
- Modify: `docs/05_Code/Simulation/efield_map_viewer.m`

**Interfaces:**
- Consumes: `qHandles`, `nBins`, `binEdges`, `coords`, `E1`, `E2`, `Emag1`, `Emag2`, `elecH1`, `elecH2`, `baseScaleLen` from Tasks 1–3.
- Produces: nested function `update_arrows(scaleMult)` — Task 5's slider callback calls this by name with a numeric argument.

- [ ] **Step 1: Replace the fixed-electrode-1 rendering block with a dropdown + `update_arrows` nested function**

Replace the block added in Task 3 (from `% 전극1 데이터로 초기 렌더 ...` through the closing `end` of the main function) with:

```matlab
    %% ---- 컨트롤 ----
    uilabel(fig, 'Position', [60 205 120 22], 'Text', '전극 선택:');
    elecDropdown = uidropdown(fig, 'Position', [190 205 150 22], ...
        'Items', {'전극1', '전극2'}, 'Value', '전극1');

    elecDropdown.ValueChangedFcn = @(src, event) update_arrows();

    update_arrows(1);  % 초기 렌더 (배율 1x, 전극1)

    function update_arrows(scaleMult)
        if nargin < 1 || isempty(scaleMult)
            scaleMult = 1;
        end
        if strcmp(elecDropdown.Value, '전극1')
            Esel = E1;
            Emag = Emag1;
            set(elecH1, 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
            set(elecH2, 'MarkerEdgeColor', 'k', 'LineWidth', 1);
        else
            Esel = E2;
            Emag = Emag2;
            set(elecH2, 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
            set(elecH1, 'MarkerEdgeColor', 'k', 'LineWidth', 1);
        end

        scaleLen = baseScaleLen * scaleMult;
        Uall = Esel(:, 1) * scaleLen;
        Vall = Esel(:, 2) * scaleLen;

        for b = 1:nBins
            if b < nBins
                mask = Emag >= binEdges(b) & Emag < binEdges(b + 1);
            else
                mask = Emag >= binEdges(b) & Emag <= binEdges(b + 1);
            end
            set(qHandles(b), 'XData', coords(mask, 1), 'YData', coords(mask, 2), ...
                'UData', Uall(mask), 'VData', Vall(mask));
        end
    end
end
```

- [ ] **Step 2: Manual verification (run in Windows MATLAB)**

Run: `efield_map_viewer`.

Confirm visually:
- A dropdown labeled "전극 선택:" appears below the axes, defaulting to "전극1", and 전극1's marker has a red edge (전극2's is plain black).
- Switching the dropdown to "전극2" immediately redraws arrows around (-25, -20) instead, and 전극2's marker turns red while 전극1's returns to black.
- The arrow pattern for 전극2 is the mirror image (across y=0) of 전극1's pattern, since the electrode geometry is mirrored — sanity-check this by eye.
- Axis limits remain [-35, 35] after switching (unchanged).
- No console errors.

- [ ] **Step 3: Commit**

```bash
git add docs/05_Code/Simulation/efield_map_viewer.m
git commit -m "feat: add electrode selection dropdown with live arrow update"
```

---

### Task 5: Arrow scale-factor slider

**Files:**
- Modify: `docs/05_Code/Simulation/efield_map_viewer.m`

**Interfaces:**
- Consumes: `update_arrows(scaleMult)` from Task 4.
- Produces: none consumed by later tasks (this is the final interactive feature).

- [ ] **Step 1: Add the scale slider and wire it to `update_arrows`**

Replace:

```matlab
    elecDropdown.ValueChangedFcn = @(src, event) update_arrows();

    update_arrows(1);  % 초기 렌더 (배율 1x, 전극1)
```

with:

```matlab
    uilabel(fig, 'Position', [60 150 300 22], 'Text', '화살표 크기 배율:');
    scaleSld = uislider(fig, 'Position', [90 115 700 3], 'Limits', [0.2 20], 'Value', 1);
    scaleSld.MajorTicks = [];
    scaleSld.MinorTicks = [];
    scaleLbl = uilabel(fig, 'Position', [90 80 700 22], 'FontSize', 13);

    elecDropdown.ValueChangedFcn = @(src, event) update_arrows(scaleSld.Value);
    scaleSld.ValueChangingFcn = @(src, event) update_arrows(event.Value);

    update_arrows(1);  % 초기 렌더 (배율 1x, 전극1)
```

And inside `update_arrows`, replace:

```matlab
    function update_arrows(scaleMult)
        if nargin < 1 || isempty(scaleMult)
            scaleMult = 1;
        end
```

with:

```matlab
    function update_arrows(scaleMult)
        if nargin < 1 || isempty(scaleMult)
            scaleMult = scaleSld.Value;
        end
```

and append, right before the final `end` that closes `update_arrows` (i.e. as the last line inside the function body, after the `for b = 1:nBins ... end` loop):

```matlab
        scaleLbl.Text = sprintf('배율: %.2fx', scaleMult);
```

- [ ] **Step 2: Manual verification (run in Windows MATLAB)**

Run: `efield_map_viewer`.

Confirm visually:
- A slider labeled "화살표 크기 배율:" appears below the electrode dropdown, with a live-updating label reading e.g. "배율: 1.00x".
- Dragging the slider smoothly grows/shrinks every arrow in real time (no lag, no flicker of unrelated elements).
- Dragging to the minimum (0.2) produces visibly tiny arrows; dragging to the maximum (20) produces large arrows that may extend beyond the phantom boundary — this is expected and acceptable (axis limits stay fixed at [-35,35], arrows are simply allowed to overflow visually).
- Switching electrodes via dropdown while the slider is not at 1.0 preserves the current scale (does not reset to 1x).
- No console errors during dragging.

- [ ] **Step 3: Commit**

```bash
git add docs/05_Code/Simulation/efield_map_viewer.m
git commit -m "feat: add real-time arrow scale-factor slider"
```

---

### Task 6: Remove superseded flux-verification tool, final integrated QA

**Files:**
- Delete: `docs/05_Code/Simulation/efield_flux_slider_tool.m`
- Modify: `docs/05_Code/Simulation/efield_map_viewer.m` (no further code changes expected — this task is verification + cleanup)

**Interfaces:** None (terminal task).

- [ ] **Step 1: Delete the superseded file**

```bash
git rm docs/05_Code/Simulation/efield_flux_slider_tool.m
```

- [ ] **Step 2: Final integrated manual verification (run in Windows MATLAB)**

Run: `efield_map_viewer`, and walk through the original requirements end-to-end:

1. Phantom (black square) and both electrodes (black dots) render before any interaction. ✅ (Task 2)
2. Arrows represent the E-field vector at every mesh node for the selected electrode; arrow direction = field direction, arrow length ∝ |E|. ✅ (Task 3)
3. Axis limits are fixed at phantom max coordinate + 10mm ([-35,35]) and do not change when switching electrodes or moving the slider. ✅ (Tasks 2, 4, 5)
4. Dropdown switches between 전극1/전극2 in real time, with no overlapping labels anywhere in the figure (check the 전극1/전극2 text labels, the dropdown label, the slider label, and the scale readout — none should visually overlap at the default window size). ✅ (Tasks 2, 4, 5)
5. Slider scales all arrows proportionally in real time, comparably across both electrodes (since normalization is fixed to the combined max). ✅ (Task 5)
6. Confirm `docs/05_Code/Simulation/efield_flux_slider_tool.m` no longer exists in the working tree.

- [ ] **Step 3: Commit**

```bash
git add docs/05_Code/Simulation/efield_map_viewer.m
git commit -m "chore: remove superseded flux-verification tool, viewer complete"
```
