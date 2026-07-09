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
    elecCoordsAll = [elec1; elec2; elec3; elec4];

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

    % update_display()의 '단일전극' 분기에서 채워지며 update_current_calc()가 참조한다.
    curCoordsSel = [];
    curEsel = [];
    curCenter = [0, 0];

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

    % update_current_calc()가 매번 갱신 — Show Detail 창을 새로 열 때 재계산 없이 바로 쓴다.
    lastDetailTbl = [];
    lastR = NaN;
    lastSigma = NaN;
    lastI_mA = NaN;
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

    curResultLbl = uilabel(fig, 'Position', [780 628 500 50], 'FontSize', 13, 'FontWeight', 'bold', ...
        'WordWrap', 'on');

    showDetailBtn = uibutton(fig, 'Position', [780 590 150 28], 'Text', 'Show Detail', ...
        'ButtonPushedFcn', @(src, event) open_detail_view());

    selTableLabelUi = uilabel(fig, 'Position', [780 565 300 22], 'Text', '선택된 arrow 값 (폐곡선 위):');
    selTable = uitable(fig, 'Position', [780 60 500 500], ...
        'ColumnName', {'#', 'θ[deg]', 'x[mm]', 'y[mm]', 'Ex[V/m]', 'Ey[V/m]', '|E|[V/m]', 'J·n[A/m^2]'}, ...
        'ColumnWidth', {30, 55, 55, 55, 65, 65, 65, 80});

    curPanelHandles = [curPanelTitle, curRadiusLabelUi, curRadiusSld, curRadiusLbl, ...
        condLabelUi, condEdit, curResultLbl, showDetailBtn, selTableLabelUi, selTable];

    curRadiusSld.ValueChangingFcn = @(src, event) update_current_calc(event.Value);
    condEdit.ValueChangedFcn = @(src, event) update_current_calc(curRadiusSld.Value);

    modeDropdown.ValueChangedFcn = @(src, event) on_mode_changed();
    targetDropdown.ValueChangedFcn = @(src, event) update_display(scaleSld.Value);
    scaleSld.ValueChangingFcn = @(src, event) update_display(event.Value);
    addlistener(ax, 'Colormap', 'PostSet', @(o, e) update_display(scaleSld.Value));

    update_display(1);  % 초기 렌더 (단일전극 / 전극1 / 배율 1x)

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
                'Color', cmap(b, :), 'LineWidth', 0.8, 'AutoScale', 'off');
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

                curCoordsSel = coordsSel;
                curEsel = Esel;
                curCenter = elecCoordsAll(hi, :);
                update_current_calc(curRadiusSld.Value);

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
        % 그 원 근처의 실제 mesh 노드(arrow)만을 뽑아 J = sigma*E를 계산한 뒤
        % 각도에 대해 J·n̂ 을 선적분(∮ J·n̂ dl)해서 폐곡선을 관통하는 전류를 구한다.
        % 등방성 매질 가정이므로 sigma는 스칼라.
        if nargin < 1 || isempty(R)
            R = curRadiusSld.Value;
        end
        curRadiusLbl.Text = sprintf('R = %.2f mm', R);

        if isempty(curCoordsSel)
            drawnow;
            return;
        end

        sigma = condEdit.Value;
        [I, tbl, circXY, coverageDeg, detailTbl] = compute_circle_current(curCoordsSel, curEsel, curCenter, R, sigma);

        circOverlay.XData = circXY(:, 1);
        circOverlay.YData = circXY(:, 2);

        if isempty(tbl)
            set(selMarkers, 'XData', NaN, 'YData', NaN);
            selTable.Data = {};
            curResultLbl.Text = '선택된 노드 없음 — R을 조정하세요 (mesh 밀도 대비 반지름 확인)';
        else
            set(selMarkers, 'XData', tbl(:, 3), 'YData', tbl(:, 4));
            selTable.Data = tbl;
            curResultLbl.Text = sprintf(['I = %.6g mA/m  (단위 depth 가정, N=%d, 적분 범위 %.0f°/360°)\n' ...
                '전극이 팬텀 경계 위에 있어 개곡선 적분 — R을 바꿔도 값이 안정적인지 확인'], ...
                I * 1e3, size(tbl, 1), coverageDeg);
        end

        lastDetailTbl = detailTbl;
        lastR = R;
        lastSigma = sigma;
        lastI_mA = I * 1e3;
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
                'Text', 'J = σE,   n̂ = (cosθ, sinθ),   J·n̂ = Jx·nx + Jy·ny,   ΔI = (J·n̂)·(R·Δθ_rad)·10^3 [mA/m]');
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
            cla(detailAx);
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
        detailTextArea.Value = build_formula_report(detailTbl, pickIdx, R, lastSigma, lastI_mA);
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


function [I, tbl, circXY, coverageDeg, detailTbl] = compute_circle_current(coords, Efield, center, R, sigma, nSectors, tolFrac)
%COMPUTE_CIRCLE_CURRENT Estimate current through a circle around an electrode
%   from a discrete E-field node cloud (irregular FEM mesh).
%
%   coords, Efield : Nx2 노드 좌표[mm] / E-field[V/m] (준정적 근사, 실수부)
%   center         : 1x2 원 중심[mm] (선택된 전극 좌표)
%   R              : 원 반지름[mm]
%   sigma          : 등방성 전도도[S/m]
%   nSectors       : 각도 구간 수(기본 3600 = 0.1도 간격) — 폐곡선을 따라 최대한
%                    고르고 촘촘하게 노드를 뽑기 위함(반지름 band 필터는 mesh
%                    밀도가 불균일한 영역에서 한쪽으로 몰리거나 비는 문제가
%                    있어 사용하지 않음). 구간이 이 정도로 촘촘하면(0.1°) 실제
%                    mesh 노드 두 개가 같은 구간에 들어갈 확률이 거의 없으므로,
%                    사실상 "반지름 허용오차(tolFrac) 안의 노드는 전부 선택"에
%                    가까워져 선택 오차가 최소화된다. 아래 선택 로직은 구간마다
%                    루프를 도는 대신 후보를 한 번에 뽑아 구간별로 그룹화하는
%                    벡터화 방식이라 nSectors를 키워도 느려지지 않는다.
%   tolFrac        : 반지름 허용 오차 비율(기본 0.1) — 각 구간에서
%                    |r-R| <= tolFrac*R 인 노드 중 원에 가장 가까운 것만 채택.
%                    전극 근처는 |E|~1/r로 급변하므로 너무 넓게 잡으면(예 0.25)
%                    반지름에서 벗어난 노드가 섞여 편향이 생긴다 — 좁게 유지할 것.
%
%   I : 폐곡선(혹은 아래 설명처럼 경계에 막힌 개곡선)을 관통하는 전류밀도
%       선적분 ∮ J·n̂ dl = sigma * ∮ E·n̂ dl [A/m]
%       (엄밀히는 단위 out-of-plane depth당 전류. 2D 단면 모델이 실제로 두께
%        1 m인 압출 형상일 때만 A 값 그대로 실제 주입 전류와 비교 가능하고,
%        일반적인 3D 전극 단면이라면 절대값 비교보다 "R을 바꿔도 I가 거의
%        일정한가"라는 전하보존(∇·J=0) 기반 R-불변성 자체가 검증 지표다)
%   tbl : 선택된 노드를 각도순 정렬한 표 [#, theta_deg, x, y, Ex, Ey, |E|, J·n]
%   circXY : 원 둘레 좌표(오버레이 표시용, mm)
%   coverageDeg : 실제로 적분에 쓰인 각도 범위 합[deg] (경계 밖 빈 구간 제외) —
%                 이 값이 360°보다 훨씬 작으면 전극이 phantom 경계 위에 있어
%                 원의 절반 가량이 도메인 밖(데이터 없음)이라는 뜻이다.
%
%   ※ 경계 전극 처리: 이 모델의 전극 4개는 모두 phantom 가장자리(x=±25mm)
%   위에 놓여 있어(전극이 "표면"에 접촉한다는 물리적 의미), 중심을 전극에
%   두고 원을 그리면 그 절반은 항상 도메인 밖(메시가 없는 영역)이다. 각도
%   구간을 sector로 나눠 순회할 때 데이터가 없는 구간은 애초에 selIdx에
%   들어오지 않으므로, 정렬된 선택 노드들 사이 각도 간격(dtheta) 중 하나가
%   비정상적으로 크게 튄다(= 도메인 경계를 건너뛰는 구간). 이 큰 간격을
%   보통의 호(arc)처럼 적분에 포함시키면 그 경계 바로 앞 노드 하나의 J·n̂
%   값이 실제로는 데이터가 없는 원의 절반 전체에 곱해져 반지름에 매우 민감한
%   과대/과소 값이 나온다. 절연 경계(도메인 밖=전류가 흐를 매질이 없음)라고
%   가정해 그 구간의 기여를 0으로 처리하면, 남은 반원 호만 적분하게 되고 이는
%   실제로 전극에서 도메인 안쪽으로 유입되는 전류를 근사하는 물리적으로 맞는
%   개곡선 적분이 된다(직선 경계 구간 자체는 절연이므로 그쪽 플럭스는 0).
    boundaryGapDeg = 30;   % 이보다 큰 각도 간격은 "도메인 밖(데이터 없음)"으로 간주해 제외

    if nargin < 6 || isempty(nSectors)
        nSectors = 3600;
    end
    if nargin < 7 || isempty(tolFrac)
        tolFrac = 0.05;
    end

    rel = coords - center;
    r = hypot(rel(:, 1), rel(:, 2));
    theta = atan2(rel(:, 2), rel(:, 1));   % (-pi, pi]

    circAngles = linspace(-pi, pi, 73)';
    circXY = R * [cos(circAngles), sin(circAngles)] + center;

    % 후보(반지름 허용오차 안의 노드)를 한 번에 뽑은 뒤 구간별로 그룹화한다 —
    % 구간마다 전체 노드를 훑는 for-loop(예전 방식)는 nSectors=3600에서 너무
    % 느려지므로, 반지름 조건으로 먼저 걸러낸 소수의 후보만 정렬/그룹화한다.
    tol = tolFrac * R;
    candIdx = find(abs(r - R) <= tol);
    if isempty(candIdx)
        I = NaN;
        tbl = [];
        coverageDeg = 0;
        detailTbl = [];
        return;
    end
    candTheta = theta(candIdx);
    candResid = abs(r(candIdx) - R);
    candSector = min(nSectors, max(1, floor((candTheta + pi) / (2 * pi) * nSectors) + 1));

    [~, ord] = sort(candResid, 'ascend');
    candIdxOrd = candIdx(ord);
    candSectorOrd = candSector(ord);
    [~, firstPos] = unique(candSectorOrd, 'stable');   % 정렬 후 첫 등장 = 그 구간에서 원에 가장 가까운 노드
    selIdx = candIdxOrd(firstPos);

    [thetaSorted, order] = sort(theta(selIdx));
    idxSorted = selIdx(order);

    Esel = Efield(idxSorted, :);
    coordsSelPts = coords(idxSorted, :);
    Jsel = sigma * Esel;
    nHat = [cos(thetaSorted), sin(thetaSorted)];
    Jn = sum(Jsel .* nHat, 2);

    m = numel(thetaSorted);
    dtheta = zeros(m, 1);
    for k = 1:m
        if k < m
            dtheta(k) = thetaSorted(k + 1) - thetaSorted(k);
        else
            dtheta(k) = (thetaSorted(1) + 2 * pi) - thetaSorted(k);
        end
    end

    isBoundaryGap = dtheta > deg2rad(boundaryGapDeg);
    dtheta(isBoundaryGap) = 0;   % 도메인 밖(절연 경계) 구간은 기여 없음으로 처리
    coverageDeg = rad2deg(sum(dtheta));

    Rm = R * 1e-3;                  % mm -> m (J는 A/m^2이므로 선적분 길이는 m 단위 필요)
    arcLen = Rm * dtheta;
    I = sum(Jn .* arcLen);

    Emag = sqrt(sum(Esel.^2, 2));
    tbl = [(1:m)', rad2deg(thetaSorted), coordsSelPts, Esel, Emag, Jn];

    % Show Detail 창용: 각 노드가 어떻게 n̂을 만들고 J·n̂, 기여분(ΔI)을 계산했는지
    % 전 과정을 그대로 노출하는 표 — [#, θ, x, y, Ex, Ey, nx, ny, Jx, Jy, J·n, Δθ, arc, ΔI]
    dImA = Jn .* arcLen * 1e3;   % 이 노드가 최종 I(mA/m)에 기여한 몫
    detailTbl = [(1:m)', rad2deg(thetaSorted), coordsSelPts, Esel, nHat, Jsel, Jn, ...
        rad2deg(dtheta), R .* dtheta, dImA];
end


function lines = build_formula_report(detailTbl, pickIdx, R, sigma, Itotal_mA)
%BUILD_FORMULA_REPORT Show-Detail 창에 표시할, 노드별 계산 과정을 그대로
%   풀어 쓴 텍스트를 만든다. detailTbl 열 순서:
%   [#, θdeg, x, y, Ex, Ey, nx, ny, Jx, Jy, J·n, Δθdeg, arc_mm, ΔI_mA]
    mTotal = size(detailTbl, 1);
    lines = {};
    lines{end + 1} = sprintf('전체 결정된 arrow N_total = %d개  |  σ = %.4g S/m  |  R = %.3f mm', ...
        mTotal, sigma, R);
    lines{end + 1} = '공식:  J = σE   n̂ = (cosθ, sinθ)   J·n̂ = Jx·nx + Jy·ny   ΔI = (J·n̂)·(R·Δθ_rad)·10^3 [mA/m]';
    lines{end + 1} = '';

    for kk = 1:numel(pickIdx)
        row = detailTbl(pickIdx(kk), :);
        idx = row(1); thetaDeg = row(2); x = row(3); y = row(4);
        Ex = row(5); Ey = row(6); nx = row(7); ny = row(8);
        Jx = row(9); Jy = row(10); Jn = row(11);
        dThetaDeg = row(12); arcMm = row(13); dImA = row(14);

        Emag = hypot(Ex, Ey);
        Edir = atan2d(Ey, Ex);
        arcM = arcMm * 1e-3;

        lines{end + 1} = sprintf('── Arrow #%d (원본 노드 #%d)  θ = %.2f°,  위치 (x,y) = (%.2f, %.2f) mm ──', ...
            kk, idx, thetaDeg, x, y); %#ok<AGROW>
        lines{end + 1} = sprintf('  1) 전기장:  E = (%.4g, %.4g) V/m   →  |E| = %.4g V/m,  방향 = %.1f°', ...
            Ex, Ey, Emag, Edir); %#ok<AGROW>
        lines{end + 1} = sprintf('  2) 법선벡터: 원 중심 → 이 노드 방향 θ=%.2f° 그대로 사용 →  n̂ = (cos%.2f°, sin%.2f°) = (%.4f, %.4f)', ...
            thetaDeg, thetaDeg, thetaDeg, nx, ny); %#ok<AGROW>
        lines{end + 1} = sprintf('  3) 전류밀도: J = σE = %.4g × (%.4g, %.4g) = (%.4g, %.4g) A/m²', ...
            sigma, Ex, Ey, Jx, Jy); %#ok<AGROW>
        lines{end + 1} = sprintf('  4) 법선 성분: J·n̂ = (%.4g)×(%.4f) + (%.4g)×(%.4f) = %.4g A/m²', ...
            Jx, nx, Jy, ny, Jn); %#ok<AGROW>
        lines{end + 1} = sprintf('  5) 호 길이:  Δθ = %.3f° = %.5f rad  →  arc = R·Δθ = %.3f mm × %.5f rad = %.4g mm (= %.4g m)', ...
            dThetaDeg, deg2rad(dThetaDeg), R, deg2rad(dThetaDeg), arcMm, arcM); %#ok<AGROW>
        lines{end + 1} = sprintf('  6) 기여분:  ΔI = (J·n̂) × arc[m] × 1000 = %.4g × %.4g × 1000 = %.4g mA/m', ...
            Jn, arcM, dImA); %#ok<AGROW>
        lines{end + 1} = ''; %#ok<AGROW>
    end

    lines{end + 1} = '──────────────────────────────────────────';
    lines{end + 1} = sprintf('전체 arrow(N=%d개, 위 %d개만 상세 표시)의 ΔI를 모두 더하면 → I = ΣΔI = %.6g mA/m', ...
        mTotal, numel(pickIdx), Itotal_mA);
end
