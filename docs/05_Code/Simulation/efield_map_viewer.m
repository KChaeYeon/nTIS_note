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

    %% ---- 축 범위: phantom 최대 좌표 + 10mm 고정 ----
    axLim = max(phantomX, phantomY) / 2 + 10;

    %% ---- Figure / Axes ----
    fig = uifigure('Name', 'E-field Map Viewer (Base_X50_Y50, single electrode)', ...
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

    %% ---- |E| 크기별 색상 quiver (nBins개 그룹, 색상은 고정 [0, maxEmag] 스케일) ----
    nBins = 20;
    cmap = parula(nBins);
    binEdges = linspace(0, maxEmag, nBins + 1);
    qHandles = gobjects(nBins, 1);
    for b = 1:nBins
        qHandles(b) = quiver(ax, NaN, NaN, NaN, NaN, 0, ...
            'Color', cmap(b, :), 'LineWidth', 0.8, 'AutoScale', 'off');
    end

    %% ---- 컨트롤: 전극 선택은 그래프 바로 위쪽(축 밖)에 배치 ----
    uilabel(fig, 'Position', [60 810 120 22], 'Text', '전극 선택:');
    elecDropdown = uidropdown(fig, 'Position', [190 810 150 22], ...
        'Items', {'전극1', '전극2'}, 'Value', '전극1');

    uilabel(fig, 'Position', [60 205 300 22], 'Text', '화살표 크기 배율:');
    scaleSld = uislider(fig, 'Position', [90 170 700 3], 'Limits', [0.2 20], 'Value', 1);
    scaleSld.MajorTicks = [];
    scaleSld.MinorTicks = [];
    scaleLbl = uilabel(fig, 'Position', [90 135 700 22], 'FontSize', 13);

    elecDropdown.ValueChangedFcn = @(src, event) update_arrows(scaleSld.Value);
    scaleSld.ValueChangingFcn = @(src, event) update_arrows(event.Value);

    update_arrows(1);  % 초기 렌더 (배율 1x, 전극1)

    function update_arrows(scaleMult)
        if nargin < 1 || isempty(scaleMult)
            scaleMult = scaleSld.Value;
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
        scaleLbl.Text = sprintf('배율: %.2fx', scaleMult);
    end
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
