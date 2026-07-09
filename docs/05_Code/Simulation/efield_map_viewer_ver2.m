function efield_map_viewer_ver2()
%EFIELD_MAP_VIEWER_VER2 Multi-mode E-field map viewer (single electrode / pair / AM).
%
%   4개 COMSOL 단일전극 lead-field CSV(전극1~4 각각 단독 인가, 준정적 근사이므로
%   실수부만 사용)를 읽어 phantom 경계 + 전극 위치 위에 전기장을 시각화한다.
%   "보기 모드" 드롭다운으로 단일전극/페어/AM을 전환하고, "대상 선택" 드롭다운으로
%   모드별 대상을 고르며, 슬라이더로 화살표 크기를 조절한다(AM 모드는 화살표 없음).
%
%   [ver2] efield_map_viewer.m 대비 변경점:
%     - 화살표(단일전극/페어 모드)를 원본 FEM mesh 노드에서 직접 그리지 않고,
%       scatteredInterpolant로 phantom 내부에 만든 정규 격자(기본 30x30)에서
%       전기장을 평가해 그린다. "보간 격자 크기" 슬라이더로 격자 밀도를
%       실시간 조절할 수 있다.
%     - 격자는 phantom 경계선(x=±phantomX/2, y=±phantomY/2) 자체는 포함하지
%       않는 내부(interior) 점들로만 구성된다.
%     - 폐곡선 전류 적분(compute_circle_current)의 후보 노드 선택 시에도
%       phantom 경계선 위에 정확히 놓인 노드는 명시적으로 제외해, 내부에
%       존재하는 점만 적분에 쓰이도록 한다.
%
%   실행: MATLAB 커맨드 창에서 efield_map_viewer_ver2

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
    elecCoordsAll = [elec1; elec2; elec3; elec4];

    fprintf('전극1: (%.2f, %.2f) mm,  전극2: (%.2f, %.2f) mm,  전극3: (%.2f, %.2f) mm,  전극4: (%.2f, %.2f) mm\n', ...
        elec1(1), elec1(2), elec2(1), elec2(2), elec3(1), elec3(2), elec4(1), elec4(2));

    %% ---- 단일전극 보간용 scatteredInterpolant (4채널 전부) ----
    % render_quiver에 원본 mesh 노드를 그대로 넘기지 않고, get_grid_field()가
    % phantom 내부 정규 격자에서 이 보간자로 Ex/Ey를 평가해 넘긴다.
    F1x = scatteredInterpolant(coords_ch1(:, 1), coords_ch1(:, 2), E_ch1(:, 1), 'linear', 'nearest');
    F1y = scatteredInterpolant(coords_ch1(:, 1), coords_ch1(:, 2), E_ch1(:, 2), 'linear', 'nearest');
    F2x = scatteredInterpolant(coords_ch2(:, 1), coords_ch2(:, 2), E_ch2(:, 1), 'linear', 'nearest');
    F2y = scatteredInterpolant(coords_ch2(:, 1), coords_ch2(:, 2), E_ch2(:, 2), 'linear', 'nearest');
    F3x = scatteredInterpolant(coords_ch3(:, 1), coords_ch3(:, 2), E_ch3(:, 1), 'linear', 'nearest');
    F3y = scatteredInterpolant(coords_ch3(:, 1), coords_ch3(:, 2), E_ch3(:, 2), 'linear', 'nearest');
    F4x = scatteredInterpolant(coords_ch4(:, 1), coords_ch4(:, 2), E_ch4(:, 1), 'linear', 'nearest');
    F4y = scatteredInterpolant(coords_ch4(:, 1), coords_ch4(:, 2), E_ch4(:, 2), 'linear', 'nearest');

    %% ---- 페어(다이폴) 합성: 서로 다른 mesh를 보간해 결합 ----
    E2_on1 = [F2x(coords_ch1(:, 1), coords_ch1(:, 2)), F2y(coords_ch1(:, 1), coords_ch1(:, 2))];
    E_pair1 = E_ch1 - E2_on1;              % CH1 페어, coords_ch1 기준
    Emag_pair1 = sqrt(sum(E_pair1.^2, 2));

    E4_on3 = [F4x(coords_ch3(:, 1), coords_ch3(:, 2)), F4y(coords_ch3(:, 1), coords_ch3(:, 2))];
    E_pair2 = E_ch3 - E4_on3;              % CH2 페어, coords_ch3 기준
    Emag_pair2 = sqrt(sum(E_pair2.^2, 2));

    % 페어 모드 격자 보간용 — pair1은 coords_ch1 위에서 새로 만들고,
    % pair2는 AM 계산에도 쓰이는 아래 Fp2x/Fp2y를 그대로 재사용한다.
    Fp1x = scatteredInterpolant(coords_ch1(:, 1), coords_ch1(:, 2), E_pair1(:, 1), 'linear', 'nearest');
    Fp1y = scatteredInterpolant(coords_ch1(:, 1), coords_ch1(:, 2), E_pair1(:, 2), 'linear', 'nearest');

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
    fig = uifigure('Name', 'E-field Map Viewer ver2 (Base_X50_Y50, 격자 보간)', ...
        'Position', [100 80 1300 860]);
    % GUI 전체가 절대 픽셀 Position으로 배치돼 있어, 창 크기를 조절하면 uifigure
    % 기본값인 AutoResizeChildren이 각 컴포넌트를 비율대로 늘리거나 줄이면서
    % 서로 다른 비율로 어긋나(예: 전극3/4 라벨이 그래프 영역을 벗어나 보이거나
    % 그래프 자체가 쪼그라듦) 레이아웃이 깨진다. 꺼서 모든 컴포넌트가 창 크기와
    % 무관하게 지정한 픽셀 위치/크기 그대로 고정되도록 한다.
    fig.AutoResizeChildren = 'off';
    % 그래프 영역(Position)을 정사각형으로 맞춘다 — 데이터 범위가 항상 정사각형
    % (-axLim~axLim, x/y 동일)인데 axis equal과 함께 직사각형 Position을 쓰면
    % MATLAB이 내부적으로 여백(letterbox)을 자동 계산해 채우고, 확대/축소로 그
    % 여백이 달라지면서 실제 그려지는 영역이 움직이는 것처럼 보인다.
    ax = uiaxes(fig, 'Position', [60 260 540 540]);
    % PositionConstraint를 'innerposition'으로 두면 Position이 "실제 그려지는
    % 플롯 박스"를 가리키게 되어, 확대/축소로 눈금 숫자 자릿수가 바뀌어 눈금
    % 라벨 폭이 변해도 그 여백은 플롯 박스 바깥에서만 늘고 줄 뿐, 플롯 박스
    % 자체(그래프가 실제로 그려지는 사각형)는 항상 고정된 픽셀 위치/크기를
    % 유지한다.
    ax.PositionConstraint = 'innerposition';
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
    qHandles = gobjects(nBins, 1);   % render_quiver가 매번 delete 후 새로 생성한다
    amScatter = scatter(ax, NaN, NaN, 20, [0 0 0], 'filled');
    amScatter.Visible = 'off';

    % ---- 전류 계산용 오버레이: 적분 원(폐곡선) + 선택된 노드 강조 ----
    circOverlay = plot(ax, NaN, NaN, 'm--', 'LineWidth', 1.5);
    selMarkers = scatter(ax, NaN, NaN, 40, [1 0 1], 'filled', 'MarkerEdgeColor', 'k');

    curCenter = [0, 0];

    % '단일전극' 모드에서 선택된 전극의 scatteredInterpolant 핸들 — 전류 계산은
    % 이 원본 보간자를 폐곡선 위에서 직접 평가해서 하고, 화면 격자(nGridVal)는
    % 전혀 참조하지 않는다(update_current_calc/compute_circle_current 참고).
    curFx = [];
    curFy = [];

    % 보간 격자 밀도(N x N, 경계선 제외 내부 점 개수) — 격자 슬라이더가 갱신한다.
    nGridVal = 30;

    % Show Detail 창(선택 노드들의 실시간 적분 계산 과정) — 열려 있을 때만 사용
    detailFig = gobjects(0);
    detailNEdit = gobjects(0);
    detailCountLbl = gobjects(0);
    detailTextArea = gobjects(0);
    detailFormulaLbl = gobjects(0);

    % 메인 axes 위 "결정된 arrow" 오버레이(전체=검정, 강조 N개=빨강+번호표) —
    % 개수가 매번 바뀌므로 quiver 잔상 버그를 피하려면 항상 delete 후 재생성한다.
    boundaryQuiverAll = gobjects(0);
    boundaryQuiverHi = gobjects(0);
    boundaryLabels = gobjects(0);

    % COMSOL 2D Electric Currents 해석의 out-of-plane thickness(고정값, UI 없음).
    % compute_circle_current()는 depth를 곱하지 않은 2D line-integral 값(A/m)만
    % 반환하고, 이 depth_m은 update_current_calc()에서 총 전류(A/M→mA)로 바꿀 때만 쓴다.
    depth_m = 1.0;   % d = 1 m — COMSOL 모델 설정과 항상 일치시킬 것

    % update_current_calc()가 매번 갱신 — Show Detail 창을 새로 열 때 재계산 없이 바로 쓴다.
    lastDetailTbl = [];
    lastR = NaN;
    lastSigma = NaN;
    lastDepth_m = depth_m;
    lastI_mA_total = NaN;   % depth 반영 총 전류 [mA] — 화면 주 출력값
    lastI_mA_per_m = NaN;   % 2D line-integral 값 [mA/m] — 보조 참고용
    % update_display()가 매번 갱신 — refresh_detail_view()는 이 값을 쓴다(scaleSld.Value를
    % 직접 읽지 않는다). 슬라이더를 드래그하는 동안 ValueChangingFcn의 event.Value가
    % 실제 값이고, scaleSld.Value 자체는 드래그가 끝나야 갱신되므로 직접 읽으면 한 박자
    % 늦게 반영된다.
    lastScaleMult = 1;

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

    % 보간 격자 크기 슬라이더 — 값이 바뀌는 동안(드래그 중) 실시간으로
    % get_grid_field()를 다시 호출해 화면을 갱신한다.
    gridLabelUi = uilabel(fig, 'Position', [60 95 300 22], 'Text', '보간 격자 크기 (N x N):');
    gridSld = uislider(fig, 'Position', [90 60 660 3], 'Limits', [10 100], 'Value', nGridVal);
    gridSld.MajorTicks = [];
    gridSld.MinorTicks = [];
    gridLbl = uilabel(fig, 'Position', [90 25 660 22], 'FontSize', 13, ...
        'Text', sprintf('격자: %d x %d (경계선 제외 내부 점)', nGridVal, nGridVal));

    %% ---- 컨트롤: 전류 계산 패널(선택 전극 기준, 단일전극 모드 전용) — 오른쪽 배치 ----
    curPanelTitle = uilabel(fig, 'Position', [780 810 300 22], ...
        'Text', '전류 계산 (선택 전극 기준)', 'FontWeight', 'bold');

    curRadiusLabelUi = uilabel(fig, 'Position', [780 775 220 22], 'Text', '적분 반지름 R [mm]:');
    curRadiusSld = uislider(fig, 'Position', [790 755 460 3], ...
        'Limits', [1, max(axLim - 2, 2)], 'Value', min(ex, ey) * 0.6);
    curRadiusSld.MajorTicks = [];
    curRadiusSld.MinorTicks = [];
    curRadiusLbl = uilabel(fig, 'Position', [790 725 460 22], 'FontSize', 12);

    condLabelUi = uilabel(fig, 'Position', [780 690 220 22], 'Text', '전도도 σ [S/m] (등방성):');
    condEdit = uieditfield(fig, 'numeric', 'Position', [1010 690 100 22], ...
        'Value', 1.5, 'Limits', [0, Inf]);

    curResultLbl = uilabel(fig, 'Position', [780 608 500 66], 'FontSize', 13, 'FontWeight', 'bold', ...
        'WordWrap', 'on');

    showDetailBtn = uibutton(fig, 'Position', [780 572 150 28], 'Text', 'Show Detail', ...
        'ButtonPushedFcn', @(src, event) open_detail_view());

    selTableLabelUi = uilabel(fig, 'Position', [780 547 300 22], 'Text', '선택된 arrow 값 (폐곡선 위):');
    % 'RowHeight'는 App Designer uitable(matlab.ui.control.Table)에 없는
    % 속성이라 대신 FontSize를 줄여 행을 촘촘하게 만든다 — uitable은 폰트
    % 크기에 비례해 행 높이를 자동으로 계산하므로 같은 세로 공간에 더 많은
    % arrow가 잘리지 않고 보이게 된다.
    selTable = uitable(fig, 'Position', [780 60 500 482], 'FontSize', 10, ...
        'ColumnName', {'#', 'θ[deg]', 'x[mm]', 'y[mm]', 'Ex[V/m]', 'Ey[V/m]', '|E|[V/m]', 'J·n[A/m^2]'}, ...
        'ColumnWidth', {30, 55, 55, 55, 65, 65, 65, 80});

    curPanelHandles = [curPanelTitle, curRadiusLabelUi, curRadiusSld, curRadiusLbl, ...
        condLabelUi, condEdit, curResultLbl, showDetailBtn, selTableLabelUi, selTable];

    curRadiusSld.ValueChangingFcn = @(src, event) update_current_calc(event.Value);
    condEdit.ValueChangedFcn = @(src, event) update_current_calc(curRadiusSld.Value);

    modeDropdown.ValueChangedFcn = @(src, event) on_mode_changed();
    targetDropdown.ValueChangedFcn = @(src, event) update_display(scaleSld.Value);
    scaleSld.ValueChangingFcn = @(src, event) update_display(event.Value);
    gridSld.ValueChangingFcn = @(src, event) set_grid_and_redraw(event.Value);
    addlistener(ax, 'Colormap', 'PostSet', @(o, e) update_display(scaleSld.Value));

    update_display(1);  % 초기 렌더 (단일전극 / 전극1 / 배율 1x / 격자 30x30)

    function [gridCoords, gridE, gridEmag] = get_grid_field(Fx, Fy, nGrid)
        % phantom 내부(interior) 정규 격자에서 Fx/Fy 보간자로 전기장을 평가한다.
        % linspace를 경계보다 두 칸 넓게(nGrid+2) 잡고 양 끝(정확히 경계선 위)을
        % 버리면, 격자점이 phantom 경계선(x=±phantomX/2, y=±phantomY/2) 위에
        % 정확히 놓이는 경우가 애초에 생기지 않는다 — "폐곡선 후보 선택 시
        % 경계 위 arrow는 제외"라는 요구사항을 격자 자체의 구성으로 만족시킨다.
        gx = linspace(-phantomX / 2, phantomX / 2, nGrid + 2);
        gy = linspace(-phantomY / 2, phantomY / 2, nGrid + 2);
        gx = gx(2:end - 1);
        gy = gy(2:end - 1);
        [GX, GY] = meshgrid(gx, gy);
        gridCoords = [GX(:), GY(:)];
        Ex = Fx(gridCoords(:, 1), gridCoords(:, 2));
        Ey = Fy(gridCoords(:, 1), gridCoords(:, 2));
        gridE = [Ex, Ey];
        gridEmag = hypot(Ex, Ey);
    end

    function set_grid_and_redraw(nGridRaw)
        nGridVal = max(10, min(100, round(nGridRaw)));
        gridLbl.Text = sprintf('격자: %d x %d (경계선 제외 내부 점)', nGridVal, nGridVal);
        update_display(scaleSld.Value);
    end

    function render_quiver(coordsSel, Esel, Emag, maxVal, scaleMult)
        % set()으로 재사용하는 대신, 기존 화살표 그래픽 객체를 완전히 삭제하고
        % 매번 처음부터 다시 생성한다 — 이전 선택의 화살표가 남을 가능성을
        % 구조적으로 없앤다(재사용 잔상 의심을 원천 차단).
        delete(qHandles(isgraphics(qHandles)));
        qHandles = gobjects(nBins, 1);

        % 화살표 색상은 axes의 현재 colormap에서 매번 새로 뽑는다 — 툴바 등으로
        % colormap을 바꾸면 화살표 색도 함께 바뀌도록 하기 위함.
        fullCmap = colormap(ax);
        cmapIdx = round(linspace(1, size(fullCmap, 1), nBins));
        cmap = fullCmap(cmapIdx, :);

        % 화살표 두께도 크기 구간(bin)에 비례해서 굵어지도록 한다 — 길이(아래
        % scaleLen으로 이미 |E|에 비례)에 더해, 두께로도 |E|가 커질수록
        % 시각적으로 더 강조되게 하기 위함. bin 인덱스가 클수록(=|E| 클수록)
        % minLineWidth~maxLineWidth 사이에서 선형으로 굵어진다.
        minLineWidth = 0.5;
        maxLineWidth = 3.0;
        widthPerBin = linspace(minLineWidth, maxLineWidth, nBins);

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
            qHandles(b) = quiver(ax, coordsSel(mask, 1), coordsSel(mask, 2), ...
                Uall(mask), Vall(mask), 0, ...
                'Color', cmap(b, :), 'LineWidth', widthPerBin(b), 'AutoScale', 'off');
        end
    end

    function update_display(scaleMult)
        if nargin < 1 || isempty(scaleMult)
            scaleMult = scaleSld.Value;
        end
        lastScaleMult = scaleMult;   % 드래그 중 실시간 값 — refresh_detail_view가 이걸 쓴다

        set(elecHandles, 'MarkerEdgeColor', 'k', 'LineWidth', 1);

        switch modeDropdown.Value
            case '단일전극'
                switch targetDropdown.Value
                    case '전극1'
                        Fx = F1x; Fy = F1y; hi = 1;
                    case '전극2'
                        Fx = F2x; Fy = F2y; hi = 2;
                    case '전극3'
                        Fx = F3x; Fy = F3y; hi = 3;
                    otherwise
                        Fx = F4x; Fy = F4y; hi = 4;
                end
                set(elecHandles(hi), 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
                [gridCoords, gridE, gridEmag] = get_grid_field(Fx, Fy, nGridVal);
                render_quiver(gridCoords, gridE, gridEmag, maxEmagSingle, scaleMult);
                amScatter.Visible = 'off';

                curCenter = elecCoordsAll(hi, :);
                curFx = Fx;
                curFy = Fy;
                update_current_calc(curRadiusSld.Value);

            case '페어'
                if strcmp(targetDropdown.Value, 'CH1 페어(1-2)')
                    Fx = Fp1x; Fy = Fp1y;
                    set(elecHandles([1 2]), 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
                else
                    Fx = Fp2x; Fy = Fp2y;
                    set(elecHandles([3 4]), 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
                end
                [gridCoords, gridE, gridEmag] = get_grid_field(Fx, Fy, nGridVal);
                render_quiver(gridCoords, gridE, gridEmag, maxEmagPair, scaleMult);
                amScatter.Visible = 'off';

            case 'AM'
                set(elecHandles, 'MarkerEdgeColor', 'r', 'LineWidth', 2.5);
                delete(qHandles(isgraphics(qHandles)));
                qHandles = gobjects(nBins, 1);
                clim(ax, [0, maxAM]);
                cb.Label.String = 'AM envelope depth [V/m]';
                amScatter.XData = coords_ch1(:, 1);
                amScatter.YData = coords_ch1(:, 2);
                amScatter.CData = AM;
                amScatter.Visible = 'on';
        end

        scaleLbl.Text = sprintf('배율: %.2fx', scaleMult);

        % uiaxes는 내부적으로 비동기 렌더링을 하기 때문에, 여러 속성을 빠르게 바꾼 뒤
        % 화면이 마지막 상태로 완전히 갱신되기 전에 이전 프레임 잔상이 잠깐 보일 수
        % 있다. drawnow로 렌더링 큐를 강제로 비워 화면을 항상 최신 상태로 동기화한다.
        drawnow;
    end

    function update_current_calc(R)
        % 선택된 전극(curCenter)을 중심으로 반지름 R[mm]인 폐곡선(원)을 그리고,
        % 그 원 위에 균일 간격으로 만든 nTheta개 contour point에서 curFx/curFy
        % (원본 COMSOL mesh 기반 scatteredInterpolant)를 직접 평가해 J = sigma*E를
        % 계산한 뒤 J·n̂ 을 선적분(∮ J·n̂ dl)해서 폐곡선을 관통하는 전류를 구한다.
        % 화면 표시용 보간 격자(nGridVal, gridCoords/gridE)는 전혀 쓰지 않는다
        % — 그래야 전류 계산 결과가 화면 격자 해상도와 무관해진다.
        % 등방성 매질 가정이므로 sigma는 스칼라.
        if nargin < 1 || isempty(R)
            R = curRadiusSld.Value;
        end
        curRadiusLbl.Text = sprintf('R = %.2f mm', R);

        if isempty(curFx)
            drawnow;
            return;
        end

        sigma = condEdit.Value;
        % compute_circle_current()는 depth를 곱하지 않은 2D line-integral 값만
        % 반환한다 — I_A_per_m = ∮ J·n̂ dl [A/m]. 총 전류로의 변환(depth_m 적용)은
        % 여기서만 한다.
        [I_A_per_m, tbl, circXY, coverageDeg, detailTbl] = compute_circle_current( ...
            curFx, curFy, curCenter, R, sigma, phantomX / 2, phantomY / 2);

        circOverlay.XData = circXY(:, 1);
        circOverlay.YData = circXY(:, 2);

        % I_total[A] = I_line[A/m] × depth_m[m] (COMSOL out-of-plane thickness).
        % depth_m = 1.0으로 고정이므로 수치는 I_line과 같지만, 화면에는 반드시
        % 총 전류 단위(mA)로 표시한다.
        I_A_total = I_A_per_m * depth_m;
        I_mA_total = I_A_total * 1e3;
        I_mA_per_m = I_A_per_m * 1e3;   % 내부 확인/보조 표시용

        if isempty(tbl)
            set(selMarkers, 'XData', NaN, 'YData', NaN);
            selTable.Data = {};
            curResultLbl.Text = '선택된 노드 없음 — R 또는 보간 격자 크기를 조정하세요';
        else
            set(selMarkers, 'XData', tbl(:, 3), 'YData', tbl(:, 4));
            selTable.Data = tbl;
            errPct = (abs(I_mA_total) - 1) / 1 * 100;   % Terminal current 1 mA 대비 오차
            % 3줄로 압축 — 박스 높이(66px)에 잘리지 않고 다 보이도록 한다.
            curResultLbl.Text = sprintf([ ...
                'Integrated current = %.6g mA  (d = %.1f m)\n' ...
                'Signed I_total = %.6g mA   |I_total| = %.6g mA   1mA 대비 오차 = %.2f%%\n' ...
                'N=%d, 적분 범위 %.0f°/360°  (I_line = %.6g mA/m, 보조)'], ...
                I_mA_total, depth_m, I_mA_total, ...
                abs(I_mA_total), errPct, size(tbl, 1), coverageDeg, I_mA_per_m);
        end

        lastDetailTbl = detailTbl;
        lastR = R;
        lastSigma = sigma;
        lastDepth_m = depth_m;
        lastI_mA_total = I_mA_total;
        lastI_mA_per_m = I_mA_per_m;
        refresh_detail_view();
        drawnow;
    end

    function open_detail_view()
        if isempty(detailFig) || ~isvalid(detailFig)
            detailFig = uifigure('Name', 'Show Detail — 선택 arrow 적분 계산 과정', ...
                'Position', [150 80 760 700]);
            detailFig.CloseRequestFcn = @(src, event) on_detail_closed();

            % uigridlayout을 쓰면 창 크기를 자유롭게 바꿔도 위 두 줄(수식/컨트롤)은
            % 고정 높이를 유지하고, 텍스트 박스가 있는 마지막 행만 '1x'로 남는
            % 공간을 전부 채우도록 자동으로 늘고 줄어든다(uifigure의 기본
            % AutoResizeChildren 비례 확대처럼 컴포넌트가 서로 어긋나지 않는다).
            gl = uigridlayout(detailFig, [3, 4]);
            gl.RowHeight = {30, 30, '1x'};
            gl.ColumnWidth = {150, 70, 110, '1x'};

            detailFormulaLbl = uilabel(gl, 'FontSize', 12, ...
                'Text', 'J = σE,   n̂ = (cosθ, sinθ),   J·n̂ = Jx·nx + Jy·ny,   ΔI_total = (J·n̂)·(R·Δθ_rad)·d·10^3 [mA]  (d = 1 m)');
            detailFormulaLbl.Layout.Row = 1;
            detailFormulaLbl.Layout.Column = [1, 4];

            nLbl = uilabel(gl, 'Text', '강조해서 볼 개수 N:');
            nLbl.Layout.Row = 2;
            nLbl.Layout.Column = 1;

            detailNEdit = uieditfield(gl, 'numeric', 'Value', 5, 'Limits', [1, Inf], ...
                'RoundFractionalValues', 'on', 'ValueChangedFcn', @(src, event) refresh_detail_view());
            detailNEdit.Layout.Row = 2;
            detailNEdit.Layout.Column = 2;

            detailCountLbl = uilabel(gl, 'FontWeight', 'bold');
            detailCountLbl.Layout.Row = 2;
            detailCountLbl.Layout.Column = 3;

            noteLbl = uilabel(gl, 'Text', '(검정=전체, 빨강=강조 N개 — 가운데 arrow부터 선택)');
            noteLbl.Layout.Row = 2;
            noteLbl.Layout.Column = 4;

            detailTextArea = uitextarea(gl, 'Editable', 'off', 'FontName', 'Consolas', 'FontSize', 12);
            detailTextArea.Layout.Row = 3;
            detailTextArea.Layout.Column = [1, 4];
        end
        figure(detailFig);
        refresh_detail_view();
    end

    function on_detail_closed()
        clear_boundary_overlay();
        delete(detailFig);
    end

    function clear_boundary_overlay()
        delete(boundaryQuiverAll(isgraphics(boundaryQuiverAll)));
        delete(boundaryQuiverHi(isgraphics(boundaryQuiverHi)));
        delete(boundaryLabels(isgraphics(boundaryLabels)));
        boundaryQuiverAll = gobjects(0);
        boundaryQuiverHi = gobjects(0);
        boundaryLabels = gobjects(0);
    end

    function refresh_detail_view()
        % Show Detail 창이 열려 있을 때만 동작 — 메인 axes 위와 Show Detail 왼쪽의
        % 전용 축에 "결정된 모든 arrow"를 검정색으로, 그중 N개를 빨간색+번호로
        % 강조하고(원 중심에서 각도상 가장 가까운 "가운데" arrow부터 우선 선택),
        % 그 N개에 대해 E 크기/방향 -> n̂ -> J -> J·n̂ -> ΔI 로 이어지는 계산을
        % 수식 텍스트로 보여준다. 메인 창의 화살표 배율(scaleSld)을 그대로 읽어
        % 쓰므로 메인 창에서 배율을 바꾸면(그 콜백이 결국 이 함수를 다시 부른다)
        % Show Detail의 왼쪽 그래프도 같이 갱신된다.
        if isempty(detailFig) || ~isvalid(detailFig)
            clear_boundary_overlay();
            return;
        end
        if isempty(lastDetailTbl)
            clear_boundary_overlay();
            detailTextArea.Value = {'선택된 노드 없음 — R을 조정하세요.'};
            return;
        end

        detailTbl = lastDetailTbl;
        R = lastR;
        mTotal = size(detailTbl, 1);

        detailNEdit.Limits = [1, mTotal];
        N = max(1, min(mTotal, round(detailNEdit.Value)));

        % ---- "가운데" arrow부터 우선 선택: 정렬된 목록의 중앙 인덱스에 가장 가까운
        % 것부터 N개를 채택한다(첫 인덱스부터 균등 간격으로 뽑던 이전 방식 대체) ----
        centerIdx = (1 + mTotal) / 2;
        [~, distOrd] = sort(abs((1:mTotal)' - centerIdx));
        pickIdx = sort(distOrd(1:N));
        detailNEdit.Value = numel(pickIdx);
        detailCountLbl.Text = sprintf('/ %d (최대)', mTotal);

        % ---- 메인 axes 오버레이: 전체 검정 + 강조 N개 빨강 ----
        clear_boundary_overlay();
        scaleLen = (3 / maxEmagSingle) * lastScaleMult;
        allXY = detailTbl(:, 3:4);
        allE = detailTbl(:, 5:6);
        boundaryQuiverAll = quiver(ax, allXY(:, 1), allXY(:, 2), ...
            allE(:, 1) * scaleLen, allE(:, 2) * scaleLen, 0, ...
            'Color', 'k', 'LineWidth', 1.0, 'AutoScale', 'off');

        hiXY = detailTbl(pickIdx, 3:4);
        hiE = detailTbl(pickIdx, 5:6);
        boundaryQuiverHi = quiver(ax, hiXY(:, 1), hiXY(:, 2), ...
            hiE(:, 1) * scaleLen, hiE(:, 2) * scaleLen, 0, ...
            'Color', 'r', 'LineWidth', 2.2, 'AutoScale', 'off');

        boundaryLabels = gobjects(numel(pickIdx), 1);
        for k = 1:numel(pickIdx)
            boundaryLabels(k) = text(ax, hiXY(k, 1), hiXY(k, 2), sprintf('  #%d', k), ...
                'Color', 'r', 'FontWeight', 'bold', 'FontSize', 10);
        end

        % ---- 수식 텍스트 ----
        detailTextArea.Value = build_formula_report( ...
            detailTbl, pickIdx, R, lastSigma, lastDepth_m, lastI_mA_total);
        drawnow;
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
                set(curPanelHandles, 'Visible', 'on');
                circOverlay.Visible = 'on';
                selMarkers.Visible = 'on';
            case '페어'
                targetDropdown.Items = {'CH1 페어(1-2)', 'CH2 페어(3-4)'};
                targetDropdown.Value = 'CH1 페어(1-2)';
                targetDropdown.Enable = 'on';
                scaleLabelUi.Visible = 'on';
                scaleSld.Visible = 'on';
                scaleLbl.Visible = 'on';
                set(curPanelHandles, 'Visible', 'off');
                circOverlay.Visible = 'off';
                selMarkers.Visible = 'off';
                clear_boundary_overlay();
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
                set(curPanelHandles, 'Visible', 'off');
                circOverlay.Visible = 'off';
                selMarkers.Visible = 'off';
                clear_boundary_overlay();
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


function [I, tbl, circXY, coverageDeg, detailTbl] = compute_circle_current( ...
    Fx, Fy, center, R, sigma, phantomHalfX, phantomHalfY, nTheta)
%COMPUTE_CIRCLE_CURRENT Estimate current through a circle around an electrode
%   by sampling the ORIGINAL COMSOL scatteredInterpolant directly on nTheta
%   uniform contour points placed on the circle itself.
%
%   [ver2 재설계] 예전 버전은 화면 표시용 보간 격자(get_grid_field가 만든
%   N x N 정규 격자)에서 "반지름 R 근처에 우연히 있는 격자점"을 찾아 그걸로
%   적분했다. 격자점은 원 둘레 위에 놓이도록 만들어진 게 아니라 그냥 바둑판
%   배치이기 때문에, 화면 격자 해상도(nGridVal)가 바뀌면 원 근처에 걸리는
%   점의 개수·각도 간격이 완전히 달라져 계산된 전류가 격자 해상도에 종속되는
%   문제가 있었다(예: N=10일 때 I_total≈0.2mA, N=100일 때 ≈0.9mA 이상).
%   이 함수는 화면 격자를 전혀 참조하지 않는다 — 대신:
%     1) 폐곡선(반지름 R인 원) 위에 균일 간격 contour point를 nTheta개 직접 만든다.
%     2) 그 점에서 원본 COMSOL mesh 기반 scatteredInterpolant(Fx,Fy)로 Ex,Ey를 평가한다.
%     3) J = sigma*E를 계산한다.
%     4) J·n̂을 적분한다.
%   이러면 화면에 20x20을 보든 100x100을 보든(nGridVal), 전류 계산 결과는
%   nTheta(폐곡선 자체의 분할 수)에만 의존하고 화면 격자 해상도와는 무관하다.
%
%   Fx, Fy   : 이 전극의 Ex(x,y), Ey(x,y) scatteredInterpolant 핸들(원본 COMSOL
%              mesh로 시작 시 한 번만 만든 것 — F1x/F1y ... F4x/F4y).
%   center   : 1x2 원 중심[mm] (선택된 전극 좌표)
%   R        : 원 반지름[mm]
%   sigma    : 등방성 전도도[S/m]
%   phantomHalfX, phantomHalfY : phantom 반폭[mm] (phantomX/2, phantomY/2).
%              전극이 phantom 가장자리 위에 있어 원의 일부가 도메인 밖으로
%              나가므로, 그 바깥(또는 경계선 위)에 놓이는 contour point는
%              절연 경계로 간주해 적분 기여를 0으로 처리한다.
%   nTheta   : 폐곡선을 등분할하는 contour point 개수(기본 720 = 0.5° 간격).
%              항상 균일 간격이므로 Δθ = 2π/nTheta로 모든 점에서 동일하다
%              (예전처럼 "선택된 점들 사이 간격이 들쭉날쭉해서 경계 감지용
%              큰 gap을 찾는" 로직이 필요 없다 — 도메인 밖 여부는 각 점의
%              좌표를 phantom 사각형과 직접 비교해서 판정한다).
%
%   I : 폐곡선을 관통하는 전류밀도 선적분 ∮ J·n̂ dl = sigma * ∮ E·n̂ dl [A/m] —
%       depth(out-of-plane thickness)를 곱하지 않은 순수 2D line-integral 값이다.
%       호출부(update_current_calc)에서 I_A_per_m으로 받아 depth_m(COMSOL 설정값,
%       고정 1 m)을 곱해야 실제 총 전류[A 또는 mA]가 된다.
%       ("R을 바꿔도, nTheta를 바꿔도 I가 거의 일정한가"라는 전하보존(∇·J=0)
%        기반 불변성이 이 계산이 맞았다는 검증 지표다)
%   tbl : 도메인 내부에 있는 contour point만 각도순으로 담은 표
%         [#, theta_deg, x, y, Ex, Ey, |E|, J·n]
%   circXY : 원 둘레 좌표(오버레이 표시용, mm, 전체 360°)
%   coverageDeg : 실제로 적분에 쓰인(도메인 내부) 각도 범위 합[deg] — 이 값이
%                 360°보다 훨씬 작으면 전극이 phantom 경계 위에 있어 원의
%                 절반 가량이 도메인 밖이라는 뜻이다.
    if nargin < 8 || isempty(nTheta)
        nTheta = 720;
    end

    theta = linspace(-pi, pi, nTheta + 1)';
    theta(end) = [];                    % 마지막 점은 첫 점과 중복(-pi==pi)이라 제거
    dtheta = 2 * pi / nTheta;           % 균일 분할이므로 모든 점에서 동일

    circAngles = linspace(-pi, pi, 73)';
    circXY = R * [cos(circAngles), sin(circAngles)] + center;

    pts = center + R * [cos(theta), sin(theta)];

    % phantom 경계선 위 또는 그 바깥에 있는 contour point는 절연 경계 밖(전류가
    % 흐를 매질이 없음)이므로 적분 기여를 0으로 두고 완전히 제외한다.
    boundaryTol = 1e-6 * max(phantomHalfX, phantomHalfY);
    inside = (abs(pts(:, 1)) < phantomHalfX - boundaryTol) & ...
             (abs(pts(:, 2)) < phantomHalfY - boundaryTol);

    Ex = Fx(pts(:, 1), pts(:, 2));
    Ey = Fy(pts(:, 1), pts(:, 2));
    Esel = [Ex, Ey];
    Jsel = sigma * Esel;
    nHat = [cos(theta), sin(theta)];
    Jn = sum(Jsel .* nHat, 2);

    Rm = R * 1e-3;                       % mm -> m
    arcLen = Rm * dtheta;                % 균일 분할이라 스칼라(모든 점 동일)
    contrib = Jn * arcLen;
    contrib(~inside) = 0;

    I = sum(contrib);
    coverageDeg = sum(inside) * rad2deg(dtheta);

    idxIn = find(inside);
    m = numel(idxIn);
    Emag = sqrt(sum(Esel(idxIn, :).^2, 2));
    tbl = [(1:m)', rad2deg(theta(idxIn)), pts(idxIn, :), Esel(idxIn, :), Emag, Jn(idxIn)];

    % Show Detail 창용: 각 contour point가 어떻게 n̂을 만들고 J·n̂, 기여분(ΔI)을
    % 계산했는지 전 과정을 그대로 노출하는 표 —
    % [#, θ, x, y, Ex, Ey, nx, ny, Jx, Jy, J·n, Δθ, arc, ΔI_line]
    % 이 함수는 depth를 곱하지 않은 2D line-integral 기여분(mA/m)까지만 계산한다 —
    % depth_m을 곱해 mA(총 전류)로 바꾸는 것은 build_formula_report()의 몫이다.
    dI_line_mA_per_m = contrib(idxIn) * 1e3;   % 이 점이 I_line(mA/m)에 기여한 몫
    detailTbl = [(1:m)', rad2deg(theta(idxIn)), pts(idxIn, :), Esel(idxIn, :), ...
        nHat(idxIn, :), Jsel(idxIn, :), Jn(idxIn), ...
        repmat(rad2deg(dtheta), m, 1), repmat(R * dtheta, m, 1), dI_line_mA_per_m];
end


function lines = build_formula_report(detailTbl, pickIdx, R, sigma, depth_m, I_mA_total)
%BUILD_FORMULA_REPORT Show-Detail 창에 표시할, 노드별 계산 과정을 그대로
%   풀어 쓴 텍스트를 만든다. detailTbl 열 순서:
%   [#, θdeg, x, y, Ex, Ey, nx, ny, Jx, Jy, J·n, Δθdeg, arc_mm, ΔI_line_mA_per_m]
%   depth_m : COMSOL out-of-plane thickness[m] (고정값 1.0) — 여기서만 곱해
%             ΔI_line(mA/m)을 ΔI_total(mA, 총 전류 기여분)로 바꾼다.
%   I_mA_total : depth 반영 총 전류[mA] (update_current_calc()에서 계산한 값)
    mTotal = size(detailTbl, 1);
    lines = {};
    lines{end + 1} = sprintf('전체 결정된 arrow N_total = %d개  |  σ = %.4g S/m  |  R = %.3f mm  |  d = %.1f m', ...
        mTotal, sigma, R, depth_m);
    lines{end + 1} = '공식:  J = σE   n̂ = (cosθ, sinθ)   J·n̂ = Jx·nx + Jy·ny   ΔI_total = (J·n̂)·(R·Δθ_rad)·d·10^3 [mA]';
    lines{end + 1} = '';

    for kk = 1:numel(pickIdx)
        row = detailTbl(pickIdx(kk), :);
        idx = row(1); thetaDeg = row(2); x = row(3); y = row(4);
        Ex = row(5); Ey = row(6); nx = row(7); ny = row(8);
        Jx = row(9); Jy = row(10); Jn = row(11);
        dThetaDeg = row(12); arcMm = row(13); dI_line_mA_per_m = row(14);

        Emag = hypot(Ex, Ey);
        Edir = atan2d(Ey, Ex);
        arcM = arcMm * 1e-3;
        dI_total_mA = dI_line_mA_per_m * depth_m;

        % 원래 7단계(E/n̂/J/J·n̂/호길이/ΔI_line/ΔI_total)를 arrow 한 개당 4줄로
        % 압축 — Show Detail 텍스트 박스 안에 더 많은 arrow가 한 번에 보이도록.
        lines{end + 1} = sprintf('── Arrow #%d (노드 #%d)  θ=%.2f°  위치=(%.2f, %.2f) mm ──', ...
            kk, idx, thetaDeg, x, y); %#ok<AGROW>
        lines{end + 1} = sprintf('  E=(%.4g,%.4g) V/m  |E|=%.4g∠%.1f°   n̂=(cos%.1f°,sin%.1f°)=(%.4f,%.4f)', ...
            Ex, Ey, Emag, Edir, thetaDeg, thetaDeg, nx, ny); %#ok<AGROW>
        lines{end + 1} = sprintf('  J=σE=(%.4g,%.4g) A/m²   J·n̂=%.4g A/m²', ...
            Jx, Jy, Jn); %#ok<AGROW>
        lines{end + 1} = sprintf('  arc=R·Δθ=%.3fmm×%.5frad=%.4gmm(%.4gm)', ...
            R, deg2rad(dThetaDeg), arcMm, arcM); %#ok<AGROW>
        lines{end + 1} = sprintf('  ΔI_line=(J·n̂)×arc=%.4g mA/m   →   ΔI_total=ΔI_line×d=%.4g mA', ...
            dI_line_mA_per_m, dI_total_mA); %#ok<AGROW>
        lines{end + 1} = ''; %#ok<AGROW>
    end

    lines{end + 1} = '──────────────────────────────────────────';
    lines{end + 1} = sprintf('전체 arrow(N=%d개, 위 %d개만 상세 표시)의 ΔI_total을 모두 더하면 → I_total = ΣΔI_total = %.6g mA', ...
        mTotal, numel(pickIdx), I_mA_total);
end
