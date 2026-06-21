#!/usr/bin/env python3
"""
STEP 4: Temporal Interference Stimulation (TIS) 원리 — Notion 페이지에 추가
Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/add_step4_TIS_principle_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
NOTION_PAGE_ID = "37d6191a4fdc8035acb1d31b767ac08a"
GITHUB_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/12_TIS_principle/"

def H(tok):
    return {"Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
            "Notion-Version": VER}

def rt(text, bold=False, code=False, color="default", link=None):
    ann = {"bold": bold, "code": code, "color": color,
           "italic": False, "strikethrough": False, "underline": False}
    obj = {"type": "text", "text": {"content": text}, "annotations": ann}
    if link:
        obj["text"]["link"] = {"url": link}
    return obj

def h2(text):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [rt(text)], "is_toggleable": False}}

def h3(text):
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [rt(text)], "is_toggleable": False}}

def callout(text, emoji="💡", color="blue_background"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [rt(text)],
                        "icon": {"type": "emoji", "emoji": emoji},
                        "color": color}}

def bullet(*rts):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": list(rts)}}

def numbered(text):
    return {"object": "block", "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [rt(text)]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def make_table(headers, rows):
    n = len(headers)
    def cell(txt): return [rt(str(txt))]
    hr = {"object": "block", "type": "table_row",
          "table_row": {"cells": [[rt(h, bold=True)] for h in headers]}}
    drs = [{"object": "block", "type": "table_row",
            "table_row": {"cells": [cell(c) for c in row]}} for row in rows]
    return {"object": "block", "type": "table",
            "table": {"table_width": n, "has_column_header": True,
                      "has_row_header": False, "children": [hr] + drs}}

def toggle(title, children=None):
    return {"object": "block", "type": "toggle",
            "toggle": {"rich_text": [rt(title, bold=True)],
                       "children": children or []}}

def para(*rts):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": list(rts)}}

def code_block(text, lang="plain text"):
    return {"object": "block", "type": "code",
            "code": {"rich_text": [rt(text)], "language": lang}}


def step4_blocks():
    blocks = []

    # 헤더
    blocks.append(divider())
    blocks.append(h2("⚡ STEP 4: Temporal Interference Stimulation (TIS) 원리"))
    blocks.append(callout(
        "커리큘럼 4/13단계. TIS의 물리적 원리를 파동 간섭 → 전기장 수식 → COMSOL 파이프라인까지 연속된 흐름으로 이해하고, "
        "2-phase vs 3-phase TIS 차이를 AM_max 계산 관점에서 설명한다.",
        "📡", "yellow_background"
    ))
    blocks.append(para(rt("🔗 GitHub Pages: ", bold=True), rt(GITHUB_URL, link=GITHUB_URL)))
    blocks.append(para(rt("📄 로컬 파일: ", bold=True),
                       rt("docs/01_theory/12_TIS_principle.md", code=True)))

    # 핵심 통찰
    blocks.append(callout(
        "핵심 통찰: '자극은 envelope이 한다. kHz 고주파 자체는 신경을 통과할 뿐.' "
        "— 두 kHz 전류의 간섭으로 내부에서만 저주파 envelope 생성 → 비침습 심부 자극",
        "🎯", "green_background"
    ))

    # 1. TIS 탄생 배경
    blocks.append(h3("1. TIS 탄생 배경 — 왜 기존 방법은 실패했는가?"))
    blocks.append(callout(
        "기존 tDCS/tACS 딜레마: 내부 표적까지 충분한 전류를 보내려면 표면에서 너무 강해져 통증·화상 유발. "
        "두개골 conductivity ≈ 0.01 S/m (근육의 1/40) → 대부분 전류가 표면 경로 이동.",
        "⚠️", "red_background"
    ))
    blocks.append(para(rt("Grossman et al. 2017 (Cell) — TIS 최초 제안", bold=True)))
    blocks.append(make_table(
        ["항목", "내용"],
        [
            ["핵심 아이디어", "주파수가 조금 다른 두 kHz 전류 인가 → 표면에서 고주파만 존재(무자극) → 내부에서 중첩 → 저주파 envelope → 신경 발화"],
            ["동물 실험", "마취 마우스 운동피질·해마 선택적 자극 확인"],
            ["파라미터", "f1=2000Hz, f2=2001Hz → 1Hz beat / 마우스 발에서 움직임 관찰"],
            ["참조", "Grossman N et al., Cell 2017; 169(6):1029–1041"],
        ]
    ))

    # 2. 맥놀이
    blocks.append(h3("2. 물리적 직관: 맥놀이(Beat) 현상"))
    blocks.append(callout(
        "피아노 440Hz + 442Hz 동시 → '웅~웅~' 2Hz 떨림(맥놀이). TIS는 이 원리를 전기장에 적용. "
        "맥놀이 주파수 = |f1 - f2|",
        "🎵", "gray_background"
    ))
    blocks.append(code_block(
        "파동 1 (f1=2000Hz):   ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿\n"
        "파동 2 (f2=2002Hz):   ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿\n\n"
        "중첩 결과 envelope:\n"
        "         ╭──────╮              ╭──────╮\n"
        "∿∿∿∿╭∿∿∿∿∿∿∿∿∿╮∿∿∿∿╭∿∿∿∿∿∿∿∿∿╮∿∿∿∿\n"
        "     ╰──────────╯              ╰──────────╯\n"
        "맥놀이 = 2Hz,  carrier = 2001Hz"
    ))

    # 3. 수학
    blocks.append(h3("3. 수학적 표현"))
    blocks.append(para(rt("3.1 1D 스칼라 (E₁ = E₂ = E₀인 경우)", bold=True)))
    blocks.append(callout(
        "E(t) = E₁cos(ω₁t) + E₂cos(ω₂t)\n"
        "     = 2E₀ · cos(π·Δf·t) · cos(2π·f̄·t)\n"
        "     = [느린 envelope] × [빠른 carrier]\n\n"
        "Envelope 진폭 = |2E₀ cos(π·Δf·t)|,  beat freq = |f₁ - f₂|",
        "📐", "blue_background"
    ))
    blocks.append(make_table(
        ["항", "수식", "주파수", "역할"],
        [
            ["Carrier", "cos(2π·f̄·t)", "f̄=(f₁+f₂)/2 ≈ kHz", "조직 통과, 신경 자극 없음"],
            ["Envelope", "2E₀·cos(π·Δf·t)", "Δf=|f₁-f₂| = Hz", "신경막 반응 → 발화 유도"],
        ]
    ))
    blocks.append(para(rt("팀 실험 파라미터 (하이퍼틱스 2026): ", bold=True),
                       rt("f1=5000Hz, f2=5002Hz → Δf=2Hz beat / 진폭 1.6mA → 쥐 spike firing rate 증가 확인")))

    blocks.append(para(rt("3.2 E₁ ≠ E₂ 일반 경우", bold=True)))
    blocks.append(bullet(rt("최대 envelope = E₁ + E₂ (보강 간섭)")))
    blocks.append(bullet(rt("최소 envelope = |E₁ - E₂| (소상 간섭)")))
    blocks.append(bullet(rt("AM 깊이 = 2·min(E₁, E₂)")))

    blocks.append(para(rt("3.3 3D 벡터 전기장 (실제 조직)", bold=True)))
    blocks.append(callout(
        "E⃗(t) = E⃗₁·cos(ω₁t + φ₁) + E⃗₂·cos(ω₂t + φ₂)\n"
        "공간의 각 점에서 E⃗(t)는 시간에 따라 '타원 궤적(elliptical trajectory)'을 그린다.",
        "🔵", "purple_background"
    ))

    # 4. 타원 궤적
    blocks.append(h3("4. 전기장 벡터의 타원 궤적"))
    blocks.append(code_block(
        "E_y\n"
        " ↑\n"
        " │    ╭────────╮\n"
        " │   ╱  타원   ╲\n"
        " │  │     ●     │  ← E(t) 벡터 끝이 타원을 그리며 회전\n"
        " │  │           │\n"
        " │   ╲         ╱\n"
        " │    ╰────────╯\n"
        " └──────────────→ E_x\n\n"
        "장반경 a: 가장 강한 자극 방향\n"
        "단반경 b: 수직 방향\n"
        "b=0: 선형 (특정 방향만 자극)\n"
        "a=b: 원형 (모든 방향 균등)\n\n"
        "2-phase TIS: 타원이 한 평면 내 제한\n"
        "3-phase TIS: 타원이 3D 공간에서 임의 방향 가능"
    ))

    # 5. AM_max
    blocks.append(h3("5. AM_max 계산 — 최대 자극 방향 탐색"))
    blocks.append(callout(
        "문제: 어느 방향 n̂*이 AM 진폭을 최대화하는가?\n"
        "AM_max = max_{‖n̂‖=1} AM(n̂)\n\n"
        "해답 (송솔웅 2026, Lagrange 승수법):\n"
        "AM_max = σ₁  (field tensor M의 최대 특이값)\n"
        "최적 방향: n̂* = u₁ (SVD의 첫 번째 좌특이벡터)",
        "🔢", "blue_background"
    ))
    blocks.append(code_block(
        "AM_max 계산 알고리즘 (MATLAB, nTIS_3D_260331.m):\n\n"
        "입력: E_phasor_f1.txt, E_phasor_f2.txt (COMSOL export)\n\n"
        "for each spatial point:\n"
        "    Ẽ₁ = (Ex1+jEx1i, Ey1+jEy1i, Ez1+jEz1i)  % complex phasor f1\n"
        "    Ẽ₂ = (Ex2+jEx2i, Ey2+jEy2i, Ez2+jEz2i)  % complex phasor f2\n"
        "    M = [Re(Ẽ₁), Im(Ẽ₁), Re(Ẽ₂), Im(Ẽ₂)]  % 3×4 real matrix\n"
        "    [U, S, V] = svd(M)\n"
        "    AM_max(point) = 2 * S(1,1)               % ×2: peak-to-peak\n"
        "    n_optimal(point) = U(:,1)                 % 최적 자극 방향\n\n"
        "출력: AM_max 3D 분포 → Scatter / Slice / Isosurface 시각화\n"
        "      → COMSOL Global Definitions Interpolation으로 재import"
    ))

    # 6. 안티페이즈
    blocks.append(h3("6. 안티페이즈(Anti-phase) 전극 구성 원리"))
    blocks.append(make_table(
        ["구성", "설명", "결과"],
        [
            ["단순 2전극 (❌)", "전류가 표면 경로 집중", "전극 근처 과도 전류밀도 → 통증·화상"],
            ["안티페이즈 전극쌍 (✅)", "각 쌍: 동일 진폭, 반대 위상 / 쌍 전류 합=0", "표면 전류 소거 / 내부 교차 영역에서만 envelope 생성"],
        ]
    ))
    blocks.append(callout(
        "전극쌍 1: (+f1) ──── (-f1)  |  전극쌍 2: (+f2) ──── (-f2)\n"
        "각 쌍의 전류 합 = 0 → 외부 유출 없음 → 내부 교차 영역에서만 beat 생성\n\n"
        "팀 관찰 (김대용 2025.10): GND 공유 시 cross-talk 발생 → anti-phase 차동 구동 권장",
        "⚡", "orange_background" if False else "gray_background"
    ))
    blocks.append(para(rt("Kwak et al., Brain Stimulation, 2023: ", bold=True),
                       rt("f1=2000Hz(0.95mA) + f2=2002Hz(1.05mA), beat=2Hz → 마우스 선조체 도파민 조절 확인")))

    # 7. COMSOL 파이프라인
    blocks.append(h3("7. COMSOL 시뮬레이션 워크플로우 (팀 방법론)"))
    blocks.append(make_table(
        ["단계", "내용", "비고"],
        [
            ["STEP 1: 조직 모델 구축", "MRI/CT 세그멘테이션 → STL → COMSOL import", "IT'IS MIDA + Z-anatomy 병합"],
            ["STEP 2: 물질 속성", "σ 할당: 피부 0.4–1.0, 지방 0.04, 근육 0.2–0.4, 신경 0.1–0.3, 뼈 0.02 S/m", "이방성 근육 고려"],
            ["STEP 3: 주파수 도메인 해석", "AC/DC → Electric Currents / ∇·(σ∇V)=0 (quasi-static)", "f1, f2 각각 별도 계산"],
            ["STEP 4: phasor export", "각 주파수별 (Ex,Ey,Ez) 복소수 txt 파일 2개 export", "경계 artifact 주의 (binary mask로 해결)"],
            ["STEP 5: MATLAB AM_max", "nTIS_3D_260331.m → SVD → AM_max 3D 분포", "Scatter / Slice / Isosurface"],
            ["STEP 6: COMSOL 재import", "Global Definitions → Interpolation 함수 생성 → 조직 위에 겹쳐 시각화", ""]
        ]
    ))
    blocks.append(toggle("경계 Artifact 문제 및 해결 (김대용 2025.09–10)", [
        bullet(rt("문제: 전극 표면 근처에서 AM_max 계산 시 비현실적 큰 값 출현 (case-based 계산 불연속)")),
        bullet(rt("해결: Binary mask via boundary → 전극 근방 영역 제외 후 AM 계산 → ground truth와 일치")),
    ]))

    # 8. 2-phase vs 3-phase
    blocks.append(h3("8. 2-phase TIS vs 3-phase TIS 비교"))
    blocks.append(make_table(
        ["항목", "2-phase TIS", "3-phase TIS"],
        [
            ["전극 수", "4개 (2쌍)", "3개"],
            ["자극 평면", "2D (평면적)", "3D (입체적)"],
            ["Steering 방향", "좌/우만", "상/하/좌/우/앞/뒤 전 방향"],
            ["AM_max 계산", "상대적 단순", "SVD 필요 (팀 Lagrange 풀이)"],
            ["타원 방향", "전극 배치로 고정", "전류 비율로 소프트웨어 조절"],
            ["전류 합", "각 쌍이 별도로 0", "3전극 합 = 0 (120° 위상 분리)"],
        ]
    ))
    blocks.append(callout(
        "3-phase 전류 합 = I[cos(0°)+cos(120°)+cos(240°)] = 0\n"
        "→ Kirchhoff 전류 법칙 자동 만족 / 전극 1개 절약 / 3D 조향 가능\n\n"
        "팀 COMSOL 관찰: 중심부 전기장 궤적이 2-phase(선형) vs 3-phase(원형에 가까움)",
        "🔄", "purple_background"
    ))

    # 9. 조향
    blocks.append(h3("9. 자극 조향(Steering) — 전극 이동 없이 표적 이동"))
    blocks.append(callout(
        "2-phase: I₁=I₀+ΔI, I₂=I₀-ΔI → 진폭 비율로 표적 좌/우 이동\n"
        "3-phase: 3전류 크기/위상 조합 → 상하/좌우/사선 전 방향 이동\n\n"
        "응용 (경골신경 OAB): 발목 전극 고정 + 전류 파라미터만 변경 → 방광지배 섬유 선택적 활성화 탐색",
        "🎯", "green_background"
    ))

    # 10. 왜 kHz에 무반응인가
    blocks.append(h3("10. 신경이 kHz를 무시하고 envelope에만 반응하는 이유"))
    blocks.append(make_table(
        ["신호", "신경막 RC 시상수 τ vs 신호 주기 T", "결과"],
        [
            ["kHz carrier (e.g. 2000Hz)", "T=0.5ms << τ(1–10ms) → 막전위 미반응", "신경 발화 없음 — 안전한 통과"],
            ["Beat envelope (e.g. 2Hz)", "T=500ms >> τ → 막전위 서서히 변화", "역치 초과 → 신경 발화"],
        ]
    ))
    blocks.append(para(rt("참조: Hutcheon B & Yarom Y, Trends Neurosciences, 2000 — 뉴런 공명주파수 및 내재 주파수 선호도")))

    # 11. 팀 COMSOL 결과
    blocks.append(h3("11. 팀 COMSOL 시뮬레이션 결과 요약"))
    blocks.append(para(rt("설하신경(HGN) 모델 — 경골신경 연구 선행 검증 케이스 (김대용 팀)", bold=True)))
    blocks.append(make_table(
        ["파라미터", "값"],
        [
            ["전극 직경", "1mm (추정값)"],
            ["전극 간 거리", "2cm center-to-center, 정사각형 배치"],
            ["주파수", "f1=5kHz + f2=5.05kHz (beat=50Hz) 또는 6kHz+6.05kHz"],
            ["전류", "남성 7.86±1.46mA / 여성 4.6±1.34mA"],
            ["3-TIS AM_max (전극 근처)", "Config 1: 2.401×10⁴ V/m at (-0.1,-0.1,-0.001)m"],
            ["3-TIS AM_max (전극 근처)", "Config 2: 1.610×10⁴ V/m at (0.1,-0.1,0.001)m"],
        ]
    ))
    blocks.append(para(rt("전극 최적화 결과 (김대용 260420): ", bold=True),
                       rt("17,290개 후보 탐색 → Pareto 다목적 최적화 → Nerve max 1.04→3.35 V/m (선택성 추가 연구 중)")))

    # 12. 지식 맵
    blocks.append(h3("12. 지식 맵: TIS → OAB 연결"))
    blocks.append(code_block(
        "[OAB 병태생리 — STEP 1] 방광 과활성 = 신경조절 문제\n"
        "         ↓\n"
        "[경골신경 해부 — STEP 2] S2-S4 천수 반사궁 억제 경로\n"
        "         ↓\n"
        "[PTNS/TTNS/SNM 한계 — STEP 3] 비침습 + 깊은 표적화 필요\n"
        "         ↓\n"
        "[TIS 원리 — STEP 4 ← 현재] 비침습 심부 자극 가능\n"
        "         ↓\n"
        "[Multi-source TIS — STEP 5]\n"
        "         ↓\n"
        "[3-phase TIS — STEP 6] 팀 핵심 연구\n"
        "         ↓\n"
        "[COMSOL 최적화 — STEP 7–8] 경골신경 특화\n"
        "         ↓\n"
        "[임상 중개 — STEP 10]"
    ))

    # 확립 vs 불확실
    blocks.append(h3("13. 확립된 지식 vs 연구 갭"))
    blocks.append(toggle("✅ 확립된 지식 (논문 검증)", [
        bullet(rt("TIS로 마우스 운동피질·해마 선택적 자극 가능 (Grossman 2017, Cell)")),
        bullet(rt("kHz 고주파는 신경막 RC 시상수로 인해 자극 없이 통과 (Hutcheon & Yarom 2000)")),
        bullet(rt("Anti-phase 전극 구성이 표면 자극 최소화에 효과적 (하이퍼틱스 팀 COMSOL 확인)")),
        bullet(rt("3-phase TIS의 3D 조향 수학적 원리 증명 (팀 내부, 2025–2026)")),
        bullet(rt("SVD 기반 AM_max 계산이 time-domain ground truth와 일치 (김대용 팀 검증)")),
    ]))
    blocks.append(toggle("❓ 아직 불확실한 것 (연구 갭)", [
        bullet(rt("경골신경에서 TIS envelope이 실제 신경 발화를 유도하는 최소 역치 (in vivo 미확인)")),
        bullet(rt("3-phase TIS의 조향 분해능이 경골신경 단면(직경 3–5mm)에서 충분한지")),
        bullet(rt("피하 지방층 두께 개인차가 AM_max 분포에 미치는 영향")),
        bullet(rt("만성 OAB 환자에서의 반복 자극 효과 및 장기 안전성")),
    ]))

    # 핵심 논문
    blocks.append(h3("14. 핵심 논문 목록"))
    blocks.append(make_table(
        ["논문", "핵심 내용", "관련성"],
        [
            ["Grossman N et al., Cell 2017", "TIS 개념 최초 제안, 마우스 DBS 실증", "TIS 원리 전체 기반"],
            ["Hutcheon B & Yarom Y, Trends Neurosci 2000", "뉴런 공명주파수, 내재 주파수 선호도", "kHz 무반응 근거"],
            ["Conta J et al., Sci Rep 2021", "인체 tTIS 개인차 전기장 분포", "인체 적용 가변성"],
            ["Kwak Y et al., Brain Stimulation 2023", "TIS로 선조체 도파민 조절", "말초 적용·전기화학"],
        ]
    ))

    # 자기평가
    blocks.append(h3("자기평가 문항"))
    for i, q in enumerate([
        "[Level 1] TIS에서 신경을 실제로 자극하는 것은 kHz 고주파인가, beat frequency인가? 이유는?",
        "[Level 1] f1=3000Hz, f2=3005Hz일 때 beat frequency는?",
        "[Level 2] E₁=E₂=E₀일 때 TIS envelope 공식을 유도하라. 어떤 삼각 공식을 사용하는가?",
        "[Level 2] 안티페이즈 전극 구성이 표면 자극을 줄이는 이유를 수학적으로 설명하라.",
        "[Level 3] COMSOL에서 2-phase TIS 시뮬레이션 시, 왜 f1과 f2를 따로 두 번 계산해야 하는가?",
        "[Level 3] AM_max와 단일 방향 AM의 차이를 설명하고, 언제 AM_max가 더 중요한가?",
        "[Level 4] 3-phase TIS에서 전류의 합이 0이 되는 이유를 phasor로 설명하라.",
        "[Level 4] SVD를 이용한 AM_max 계산에서 최대 특이값이 AM_max인 이유를 증명하라.",
        "[Level 5] 팀 COMSOL 결과에서 전극 최적화 후에도 신경/비표적 선택성이 개선되지 않은 원인을 분석하고 개선 전략을 제안하라.",
    ], 1):
        blocks.append(numbered(q))

    blocks.append(divider())
    blocks.append(para(rt(
        "작성: 2026-06-21 | 커리큘럼 STEP 4/13 | 참고: 송솔웅(nTIS 전기장 계산 2026), 김대용(COMSOL 2025–2026), 하이퍼틱스 OAB 발표자료 | 다음: STEP 5 — Multi-source / Multi-channel TIS",
        color="gray"
    )))

    return blocks


def append_blocks(tok, page_id, blocks, chunk=90):
    for i in range(0, len(blocks), chunk):
        c = blocks[i:i+chunk]
        r = requests.patch(f"{API}/blocks/{page_id}/children",
                           headers=H(tok), json={"children": c})
        if r.status_code not in (200, 201):
            print(f"  ⚠️  chunk {i}: {r.status_code} {r.text[:300]}")
        else:
            print(f"  ✅ blocks {i+1}–{i+len(c)}")
        time.sleep(0.35)


def main():
    tok = os.environ.get("NOTION_TOKEN")
    if not tok:
        print("❌  NOTION_TOKEN이 설정되지 않았습니다.")
        sys.exit(1)

    r = requests.get(f"{API}/users/me", headers=H(tok))
    if r.status_code != 200:
        print(f"❌  인증 실패 ({r.status_code})")
        sys.exit(1)
    print(f"✅  인증 성공 — {r.json().get('name','?')}")

    print(f"\n📝  STEP 4 TIS 원리 블록 추가 중...")
    blocks = step4_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, NOTION_PAGE_ID, blocks)

    print("\n✅  완료!")
    print(f"   GitHub Pages: {GITHUB_URL}")


if __name__ == "__main__":
    main()
