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
    qHandles = gobjects(nBins, 1);
    for b = 1:nBins
        qHandles(b) = quiver(ax, NaN, NaN, NaN, NaN, 0, ...
            'LineWidth', 0.8, 'AutoScale', 'off');
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
    addlistener(ax, 'Colormap', 'PostSet', @(o, e) update_display(scaleSld.Value));

    update_display(1);  % 초기 렌더 (단일전극 / 전극1 / 배율 1x)

    function render_quiver(coordsSel, Esel, Emag, maxVal, scaleMult)
        % 매 호출마다 전체 bin을 먼저 비운 뒤 다시 채운다 — 이전 선택(전극/페어)의
        % 화살표가 새 선택으로 완전히 대체되지 않고 남는 것을 방지한다.
        for b = 1:nBins
            set(qHandles(b), 'XData', [], 'YData', [], 'UData', [], 'VData', []);
        end

        % 화살표 색상은 axes의 현재 colormap에서 매번 새로 뽑는다 — 툴바 등으로
        % colormap을 바꾸면 화살표 색도 함께 바뀌도록 하기 위함.
        fullCmap = colormap(ax);
        cmapIdx = round(linspace(1, size(fullCmap, 1), nBins));
        cmap = fullCmap(cmapIdx, :);

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
                'UData', Uall(mask), 'VData', Vall(mask), 'Color', cmap(b, :));
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
