#!/usr/bin/env python3
"""
STEP 6: TIS Amplitude Modulation과 AM_max — 완전 이해 (2026-06-26 통합 업데이트)
Notion 페이지에 추가

Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/add_step6_AM_max_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
NOTION_PAGE_ID = "37d6191a4fdc8035acb1d31b767ac08a"
GITHUB_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/15_AM_max_amplitude_modulation/"


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


def para(*rts):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": list(rts)}}


def code_block(text, lang="plain text"):
    return {"object": "block", "type": "code",
            "code": {"rich_text": [rt(text)], "language": lang}}


def step6_blocks():
    blocks = []

    # ── 헤더 ──────────────────────────────────────────────────────
    blocks.append(divider())
    blocks.append(h2("📐 STEP 6: TIS Amplitude Modulation과 AM_max — 완전 이해"))
    blocks.append(callout(
        "커리큘럼 6/13단계 | 업데이트: 2026-06-26\n"
        "학습 목표:\n"
        "1. Quasi-static FEM이 왜 성립하는지 정량적으로 이해한다\n"
        "2. ∇·(σ∇φ) = 0을 기초 물리법칙 3개로 유도할 수 있다\n"
        "3. AM = 2·min(|a|,|b|) 공식을 직접 증명할 수 있다\n"
        "4. E_AM_max piecewise 공식의 두 경우를 수식·기하·물리 세 관점에서 설명할 수 있다\n"
        "5. Case 2의 최적 방향이 삼각형 높이와 같음을 넓이 공식으로 유도할 수 있다\n"
        "6. SVD가 E_AM_max와 연결되는 이유를 설명할 수 있다",
        "📡", "yellow_background"
    ))
    blocks.append(para(rt("🔗 GitHub Pages: ", bold=True),
                       rt(GITHUB_URL, link=GITHUB_URL)))
    blocks.append(para(rt("📄 로컬 파일: ", bold=True),
                       rt("docs/01_theory/15_AM_max_amplitude_modulation.md", code=True)))

    # ── 0. 전체 학습 지도 ─────────────────────────────────────────
    blocks.append(h3("0. 전체 학습 지도"))
    blocks.append(code_block(
        "[기초층]\n"
        "  ① 왜 준정적 근사인가? (λ = 50 km >> 몸 크기)\n"
        "  ② FEM이 실제로 뭘 푸는가? (∇·(σ∇φ) = 0 유도)\n\n"
        "[중간층]\n"
        "  ③ 두 고주파 전기장 → 시간 표현\n"
        "  ④ 뉴런 방향 n̂으로 투영 → 1D 문제로 변환\n"
        "  ⑤ 1D AM 포락선 → AM = 2·min(|a|,|b|) 증명\n\n"
        "[핵심층]\n"
        "  ⑥ E_AM_max 최적화 문제 정의\n"
        "  ⑦ Case 1: 약한 field가 명확히 병목 → 2|E⃗₂|\n"
        "  ⑧ Case 2: 삼각형 높이 → 2|E⃗₁×E⃗₂|/|E⃗₁-E⃗₂|\n\n"
        "[계산층]\n"
        "  ⑨ 타원 궤적 직관\n"
        "  ⑩ SVD: AM_max = 2σ₁, n̂* = u₁\n"
        "  ⑪ 정의 A vs B 비교\n\n"
        "[응용층]\n"
        "  ⑫ FEM 파이프라인 + Steering + 한계"
    ))

    # ── 1. FEM 기초 ───────────────────────────────────────────────
    blocks.append(h3("1. Quasi-electrostatic FEM 기초"))
    blocks.append(callout(
        "왜 준정적 근사인가 — 정량적 확인:\n\n"
        "λ = v / f = 1×10⁸ m/s ÷ 2000 Hz = 50,000 m = 50 km\n"
        "사람 몸통 크기: ~0.5 m  →  λ/몸 = 100,000배\n\n"
        "Displacement current vs Ohmic current 비율:\n"
        "  |Displacement| / |Ohmic| = ωε / σ\n"
        "  = (2π × 2000 × 7×10⁻¹⁰) / 0.2 ≈ 4.4×10⁻⁵\n"
        "  → Displacement current = Ohmic의 0.004%  ← 완전 무시 가능\n\n"
        "결론: 파동 전파 효과 없음 → 단순 전류 흐름 문제로 취급",
        "⚡", "gray_background"
    ))
    blocks.append(h3("1-1. Grossman 2017 모델"))
    blocks.append(make_table(
        ["층", "반지름", "σ (S/m)", "역할"],
        [
            ["두피 (scalp)", "r=8.5 mm", "0.465", "전극 부착 위치"],
            ["두개골 (skull)", "r=8.0 mm", "0.010", "전류 흐름 제한 ← 핵심"],
            ["CSF", "r=7.5 mm", "1.650", "전류 확산 경로"],
            ["뇌 (brain)", "r=7.0 mm", "0.276", "표적 조직"],
        ]
    ))
    blocks.append(h3("1-2. FEM 지배 방정식 — 기초 물리법칙 3개로 유도"))
    blocks.append(code_block(
        "법칙 1 — 전하 보존 (Current Continuity):\n"
        "  ∇·J⃗ = 0  (정상상태에서 전하 축적 없음)\n\n"
        "법칙 2 — Ohm's Law:\n"
        "  J⃗ = σ E⃗  (σ 클수록 전류 잘 흐름)\n\n"
        "법칙 3 — 전위와 전기장:\n"
        "  E⃗ = -∇φ  (전기장 = 전위의 공간 기울기)\n\n"
        "세 법칙 조합:\n"
        "  (3) → (2):  J⃗ = -σ∇φ\n"
        "  (1) 대입:   ∇·(-σ∇φ) = 0\n\n"
        "  ∴  ∇·(σ∇φ) = 0  ← FEM solver가 푸는 지배 방정식\n\n"
        "σ 균일하면:  ∇²φ = 0  (Laplace 방정식)\n"
        "→ 각 점의 전위 = 주변 점들의 평균값 (전하가 균일하게 퍼지려는 경향)"
    ))

    # ── 2. 두 고주파 전기장 시간 표현 ────────────────────────────
    blocks.append(h3("2. 두 고주파 전기장의 시간 표현"))
    blocks.append(code_block(
        "FEM으로 각 전극쌍의 공간 분포를 별도 계산:\n\n"
        "전극쌍 1 (f₁ = 2000 Hz):  E⃗₁(r⃗, t) = E⃗₁(r⃗) · cos(2πf₁t)\n"
        "전극쌍 2 (f₂ = 2001 Hz):  E⃗₂(r⃗, t) = E⃗₂(r⃗) · cos(2πf₂t)\n\n"
        "합성 전기장:\n"
        "  E⃗_total(r⃗, t) = E⃗₁(r⃗)cos(2πf₁t) + E⃗₂(r⃗)cos(2πf₂t)\n\n"
        "중요: E⃗₁(r⃗)은 FEM의 정적 공간 분포, cos(2πf₁t)는 시간 변동\n"
        "→ 공간과 시간이 분리됨\n\n"
        "Δf = f₂ - f₁ = 1 Hz의 역할:\n"
        "  각 채널(2000, 2001 Hz)은 뉴런이 직접 따라가기 불가\n"
        "  하지만 Δf = 1 Hz로 진폭이 변조(AM)됨\n"
        "  → 뉴런이 1 Hz 리듬으로 반응 가능!"
    ))
    blocks.append(callout(
        "TIS의 핵심 트릭:\n"
        "깊은 조직에서 두 고주파 전기장이 만나면\n"
        "그 차이 주파수(Δf)로 진동하는 envelope가 생긴다.\n"
        "겉에서는 kHz 자극 → 안에서는 Δf Hz로 뉴런이 반응.",
        "🎯", "green_background"
    ))

    # ── 3. 뉴런 방향 투영 ────────────────────────────────────────
    blocks.append(h3("3. 뉴런 방향 n̂으로의 투영 → 1D 문제"))
    blocks.append(code_block(
        "뉴런의 막전위 변화는 전기장 방향이 뉴런과 일치할 때 최대\n"
        "→ 실제 자극 강도 = E⃗ · n̂  (투영)\n\n"
        "n̂ 방향에서 뉴런이 느끼는 신호:\n\n"
        "  E_n(t) = E⃗_total · n̂\n"
        "         = (E⃗₁·n̂)cos(ω₁t) + (E⃗₂·n̂)cos(ω₂t)\n\n"
        "약칭:\n"
        "  a = E⃗₁·n̂  (실수, 음수 가능)\n"
        "  b = E⃗₂·n̂  (실수, 음수 가능)\n\n"
        "E_n(t) = a·cos(ω₁t) + b·cos(ω₂t)\n\n"
        "← 3D 벡터 문제가 두 코사인의 합으로 단순화됨!"
    ))

    # ── 4. 1D AM 포락선 완전 유도 ─────────────────────────────────
    blocks.append(h3("4. 1D AM 포락선 — AM = 2·min(|a|,|b|) 완전 유도"))
    blocks.append(code_block(
        "포락선 진폭 A(t):\n\n"
        "  A(t)² = (a+b)²cos²(Δω·t/2) + (a-b)²sin²(Δω·t/2)\n\n"
        "  τ = Δω·t/2 (느리게 변하는 위상)\n\n"
        "  τ = 0    → A_max = |a+b|\n"
        "  τ = π/2  → A_min = |a-b|\n\n"
        "(a > b > 0인 경우):\n"
        "  AM = A_max - A_min = (a+b) - (a-b) = 2b = 2·min(a,b)\n\n"
        "  a = b:  AM = 2a  (A_min = 0, 완전 변조!)\n"
        "  a > 0, b < 0:  n̂ → -n̂ 뒤집으면 동일\n\n"
        "∴  AM(n̂) = 2·min(|E⃗₁·n̂|, |E⃗₂·n̂|)"
    ))
    blocks.append(callout(
        "직관 — 두 소방관 비유:\n"
        "소방관 A (a=8): 강하게 당김\n"
        "소방관 B (b=3): 약하게 당김\n\n"
        "최강 순간 (동위상): A+B = 11\n"
        "최약 순간 (역위상): A-B = 5  ← 5가 남는다!\n"
        "진동 폭 = 11-5 = 6 = 2×3 = 2×b\n\n"
        "→ B(약한 쪽)가 최솟값을 5로 '올려놓아서' AM이 2b로 제한됨\n"
        "→ A를 아무리 키워도 AM = 2b로 고정!",
        "🧲", "orange_background"
    ))

    # ── 5. E_AM 정의 ──────────────────────────────────────────────
    blocks.append(h3("5. E_AM 정의 — 한 방향에서의 envelope 진폭"))
    blocks.append(code_block(
        "특정 n̂ 방향에서:\n\n"
        "  E_AM(n̂, r⃗) = 2·min(|E⃗₁(r⃗)·n̂|, |E⃗₂(r⃗)·n̂|)\n\n"
        "n̂ = E⃗₁ 방향  → E⃗₂·n̂ 매우 작음 → AM ≈ 0\n"
        "n̂ = E⃗₂ 방향  → E⃗₁·n̂ 매우 작음 → AM ≈ 0\n"
        "n̂ = 중간 방향 → 둘 다 적당히 큼 → AM 최대 가능"
    ))

    # ── 6. E_AM_max 최적화 ────────────────────────────────────────
    blocks.append(h3("6. E_AM_max — 최적화 문제 정의"))
    blocks.append(callout(
        "E_AM_max(r⃗) = max over all unit n̂ of: 2·min(|E⃗₁·n̂|, |E⃗₂·n̂|)\n\n"
        "물음: 위치 r⃗에서 어떤 방향의 뉴런이든 있다고 할 때\n"
        "     받을 수 있는 최대 envelope modulation amplitude는?\n\n"
        "가정 (일반성 손실 없음):\n"
        "  |E⃗₁| ≥ |E⃗₂|  (채널 번호를 바꿔 항상 만족)\n"
        "  α = ∠(E⃗₁, E⃗₂) ∈ [0°, 90°)  (E⃗₂ 부호를 뒤집어 만족)",
        "🎯", "blue_background"
    ))
    blocks.append(h3("6-1. 두 조건으로 나뉘는 이유"))
    blocks.append(code_block(
        "핵심 질문: n̂을 E⃗₂ 방향으로 잡는 것이 항상 최선인가?\n\n"
        "n̂ = E⃗₂/|E⃗₂|로 고정하면:\n"
        "  |E⃗₂·n̂| = |E⃗₂|              ← E⃗₂ 그림자 = 최대!\n"
        "  |E⃗₁·n̂| = |E⃗₁|cosα          ← E⃗₁ 그림자\n\n"
        "두 그림자 비교:\n"
        "  Case 1: |E⃗₁|cosα > |E⃗₂|\n"
        "    → E⃗₂ 방향에서도 E⃗₁ 그림자 > E⃗₂ 그림자\n"
        "    → min = |E⃗₂|  (E⃗₂가 항상 병목)\n"
        "    → n̂ = E⃗₂ 방향이 최선!\n\n"
        "  Case 2: |E⃗₁|cosα ≤ |E⃗₂|\n"
        "    → E⃗₂ 방향에서 오히려 E⃗₁ 그림자 ≤ E⃗₂ 그림자\n"
        "    → min = |E⃗₁|cosα  (E⃗₁이 병목!)\n"
        "    → 더 좋은 방향이 반드시 존재\n\n"
        "경계: |E⃗₂| = |E⃗₁|cosα"
    ))

    # ── 7. Case 1 ─────────────────────────────────────────────────
    blocks.append(h3("7. Case 1: |E⃗₂| < |E⃗₁|cosα"))
    blocks.append(callout(
        "조건의 기하학적 의미:\n"
        "  |E⃗₁|cosα = E⃗₁을 E⃗₂ 방향으로 투영한 길이\n"
        "  |E⃗₂| < |E⃗₁|cosα\n"
        "  → E⃗₂가 E⃗₁의 그림자 안에 완전히 들어온다!\n"
        "  → 어느 방향에서 보아도 E⃗₂가 항상 더 작은 값",
        "📐", "gray_background"
    ))
    blocks.append(code_block(
        "증명:\n"
        "  n̂ = E⃗₂ 방향에서:\n"
        "    |E⃗₂·n̂| = |E⃗₂|           (최대)\n"
        "    |E⃗₁·n̂| = |E⃗₁|cosα       (항상 > |E⃗₂|)\n"
        "    min = |E⃗₂|,  AM = 2|E⃗₂|\n\n"
        "  n̂을 E⃗₂ 방향에서 벗어나면:\n"
        "    |E⃗₂·n̂| = |E⃗₂|cos(δ) < |E⃗₂|  (δ = 벗어난 각도)\n"
        "    AM < 2|E⃗₂|\n\n"
        "∴  n̂* = E⃗₂ 방향,  E_AM_max = 2|E⃗₂|\n\n"
        "물리적 의미:\n"
        "  두 채널이 심하게 불균형 → 약한 채널이 AM을 결정\n"
        "  강한 채널을 아무리 키워도 AM = 2|E⃗₂|로 고정\n"
        "  설계 교훈: 약한 채널의 전류를 키워야 한다!"
    ))

    # ── 8. Case 2 ─────────────────────────────────────────────────
    blocks.append(h3("8. Case 2: |E⃗₂| ≥ |E⃗₁|cosα — 삼각형 높이"))
    blocks.append(h3("8-1. 등사영 조건 도출"))
    blocks.append(code_block(
        "Case 2 조건: |E⃗₂| ≥ |E⃗₁|cosα\n"
        "→ E⃗₁ 방향 근처에서는 E⃗₂가 병목\n"
        "→ E⃗₂ 방향 근처에서는 E⃗₁이 병목\n"
        "→ 중간에 a = b인 방향이 반드시 존재!\n\n"
        "max-min 분석:\n"
        "  a > b인 구간: AM = 2b → n̂ 조금 움직여 b↑ → AM↑\n"
        "  이 과정은 a = b에 도달할 때까지 계속 가능\n"
        "  a = b를 지나면 min = a → a 줄면 AM↓\n\n"
        "최적 조건: |E⃗₁·n̂*| = |E⃗₂·n̂*|  (등사영 조건)\n\n"
        "→ (E⃗₁ - E⃗₂)·n̂* = 0\n\n"
        "★  n̂* ⊥ (E⃗₁ - E⃗₂)\n"
        "   최적 방향은 두 전기장의 차이 벡터에 수직!"
    ))
    blocks.append(h3("8-2. 기하학적 해석 — 삼각형 높이"))
    blocks.append(callout(
        "세 점:\n"
        "  O = 원점,  A = E⃗₁의 끝점,  B = E⃗₂의 끝점\n"
        "  BA⃗ = E⃗₁ - E⃗₂  ← 두 끝점을 잇는 선분\n\n"
        "n̂* = BA에 수직인 방향 = O에서 BA로 내린 수선의 방향\n"
        "h = 수선의 길이 (삼각형 OAB의 높이)\n\n"
        "O에서 A, B까지의 n̂* 방향 성분이 모두 h로 같다:\n"
        "  E⃗₁·n̂* = h  =  E⃗₂·n̂*  ← 등사영 확인!\n\n"
        "∴  E_AM_max = 2h",
        "📐", "purple_background"
    ))
    blocks.append(h3("8-3. 삼각형 높이 h 계산 — 넓이 공식"))
    blocks.append(code_block(
        "삼각형 OAB의 넓이를 두 방법으로 계산:\n\n"
        "방법 1 — 외적:\n"
        "  넓이 = (1/2)|E⃗₁ × E⃗₂|\n"
        "  (|E⃗₁×E⃗₂| = |E⃗₁||E⃗₂|sinα = 평행사변형 넓이)\n\n"
        "방법 2 — 밑변 × 높이:\n"
        "  밑변 = |E⃗₁ - E⃗₂|,  높이 = h\n"
        "  넓이 = (1/2)|E⃗₁ - E⃗₂| × h\n\n"
        "같다고 놓으면:\n"
        "  h = |E⃗₁ × E⃗₂| / |E⃗₁ - E⃗₂|\n\n"
        "∴  E_AM_max = 2h = 2|E⃗₁ × E⃗₂| / |E⃗₁ - E⃗₂|\n\n"
        "물리적 의미:\n"
        "  두 채널이 균형을 맞출 수 있는 상황\n"
        "  → 최적 방향에서 완전 변조에 가까운 상태\n"
        "  → '두 소방관이 정확히 같은 힘으로 당겼다 놓는다'"
    ))

    # ── 9. 두 조건 비교표 ─────────────────────────────────────────
    blocks.append(h3("9. 두 조건 완전 비교"))
    blocks.append(make_table(
        ["항목", "Case 1", "Case 2"],
        [
            ["조건", "|E⃗₂| < |E⃗₁|cosα", "|E⃗₂| ≥ |E⃗₁|cosα"],
            ["물리", "E⃗₂가 항상 병목", "균형 방향이 존재"],
            ["최적 n̂*", "E⃗₂ 방향", "E⃗₁-E⃗₂에 수직"],
            ["E_AM_max", "2|E⃗₂|", "2|E⃗₁×E⃗₂|/|E⃗₁-E⃗₂|"],
            ["기하 의미", "E⃗₂ 크기의 두 배", "삼각형 OAB 높이의 두 배"],
            ["설계 교훈", "약한 채널이 결정함", "균형 방향 ↔ 신경 방향 정렬"],
        ]
    ))
    blocks.append(h3("9-1. 경계에서 두 수식이 연속"))
    blocks.append(code_block(
        "경계: |E⃗₂| = |E⃗₁|cosα\n\n"
        "Case 1: E_AM_max = 2|E⃗₂|\n\n"
        "Case 2 수식에 경계 조건 대입:\n"
        "  |E⃗₁ × E⃗₂| = |E⃗₁||E⃗₂|sinα\n"
        "  |E⃗₁ - E⃗₂|² = |E⃗₁|²sin²α  (경계 조건 대입 후)\n"
        "  → |E⃗₁ - E⃗₂| = |E⃗₁|sinα\n\n"
        "  Case 2 수식:\n"
        "    2 × |E⃗₁||E⃗₂|sinα / |E⃗₁|sinα = 2|E⃗₂|  ✓\n\n"
        "두 수식은 경계에서 연속적으로 이어진다."
    ))

    # ── 10. 수치 예시 ─────────────────────────────────────────────
    blocks.append(h3("10. 수치 예시"))
    blocks.append(code_block(
        "예시 A — Case 1:\n"
        "  |E⃗₁|=10 V/m, |E⃗₂|=3 V/m, α=30°\n"
        "  |E⃗₁|cosα = 10×0.866 = 8.66\n"
        "  3 < 8.66 → Case 1 ✓\n"
        "  E_AM_max = 2×3 = 6 V/m\n\n"
        "예시 B — Case 2:\n"
        "  |E⃗₁|=10 V/m, |E⃗₂|=8 V/m, α=60°\n"
        "  |E⃗₁|cosα = 10×0.5 = 5\n"
        "  8 ≥ 5 → Case 2 ✓\n"
        "  |E⃗₁×E⃗₂| = 10×8×sin60° = 69.28\n"
        "  |E⃗₁-E⃗₂| = √(100+64-80) = √84 = 9.17\n"
        "  E_AM_max = 2×69.28/9.17 = 15.12 V/m\n"
        "  (비교: E⃗₂ 방향만 보면 AM = 2×5 = 10 V/m → 51% 개선!)\n\n"
        "예시 C — 직교 케이스 손 계산:\n"
        "  E⃗₁=(3,0,0), E⃗₂=(0,4,0)\n"
        "  α=90° → |E⃗₁|cosα=0 → Case 2 ✓\n"
        "  등사영: 3cosφ = 4sinφ → tanφ* = 3/4 → φ*=36.87°\n"
        "  n̂* = (0.800, 0.600, 0)\n"
        "  E⃗₁·n̂* = 3×0.8 = 2.4,  E⃗₂·n̂* = 4×0.6 = 2.4  ✓\n"
        "  E_AM_max = 2×2.4 = 4.8 V/m\n"
        "  = 2×(3×4)/5 = 2×12/5 = 4.8 V/m  ✓"
    ))

    # ── 11. 타원 궤적 ─────────────────────────────────────────────
    blocks.append(h3("11. 타원 궤적 — 핵심 물리적 직관"))
    blocks.append(callout(
        "E⃗(t) 벡터 끝점의 궤적:\n"
        "  f₁ ≈ f₂일 때, E⃗(t)는 carrier 주기로 타원을 그린다.\n\n"
        "  a = 장반경 → 가장 강한 방향의 크기\n"
        "  b = 단반경\n\n"
        "타원을 n̂ 방향으로 투영:\n"
        "  n̂ = 장반경 방향 → 투영 최대 = a\n\n"
        "⭐ AM_max = 타원 장반경 a\n"
        "   최적 방향 n̂* = 장반경 방향",
        "🔵", "blue_background"
    ))
    blocks.append(code_block(
        "왜 타원이 생기나:\n\n"
        "  고정 slow-time τ에서:\n"
        "    E⃗(t|τ) = A⃗(τ)·cos(ω̄t) + B⃗(τ)·sin(ω̄t)\n"
        "    A⃗(τ) = (E⃗₁+E⃗₂)cos(τ)  ← 타원 한 축\n"
        "    B⃗(τ) = (E⃗₂-E⃗₁)sin(τ)  ← 타원 다른 축\n"
        "    A⃗cos + B⃗sin 형태 = 타원 ✓"
    ))

    # ── 12. SVD ───────────────────────────────────────────────────
    blocks.append(h3("12. SVD — 타원 장반경을 계산하는 방법"))
    blocks.append(code_block(
        "행렬 구성 (COMSOL phasor export 후):\n\n"
        "  M = [ Re(Ẽ₁x)  Im(Ẽ₁x)  Re(Ẽ₂x)  Im(Ẽ₂x) ]\n"
        "      [ Re(Ẽ₁y)  Im(Ẽ₁y)  Re(Ẽ₂y)  Im(Ẽ₂y) ]\n"
        "      [ Re(Ẽ₁z)  Im(Ẽ₁z)  Re(Ẽ₂z)  Im(Ẽ₂z) ]\n\n"
        "  M ∈ R^{3×4}\n"
        "  (실수 phasor: Im=0 → M=[E⃗₁,E⃗₂] ∈ R^{3×2})\n\n"
        "SVD:  M = U Σ Vᵀ\n\n"
        "결과:\n"
        "  AM_max  = 2 × σ₁\n"
        "  n̂*     = u₁  (U 첫 번째 열)"
    ))
    blocks.append(code_block(
        "MATLAB 코드 (팀 실제 코드, 송솔웅 2026):\n\n"
        "E1 = [E1x; E1y; E1z];  % complex 3x1\n"
        "E2 = [E2x; E2y; E2z];  % complex 3x1\n"
        "M = [real(E1), imag(E1), real(E2), imag(E2)];  % 3x4\n"
        "[U, S, V] = svd(M, 'econ');\n"
        "AM_max = 2 * S(1,1);\n"
        "n_opt  = U(:,1);",
        "matlab"
    ))

    # ── 13. 정의 A vs B ───────────────────────────────────────────
    blocks.append(h3("13. AM_max 두 가지 정의 비교"))
    blocks.append(make_table(
        ["정의", "수식", "특징", "SVD 연결"],
        [
            ["A — Modulation Depth",
             "2 × min(|E⃗₁·n̂|, |E⃗₂·n̂|)",
             "약한 쪽이 결정 / E_AM_max piecewise 공식 기반",
             "간접적"],
            ["B — Envelope Peak (팀 MATLAB)",
             "sqrt((E⃗₁·n̂)² + (E⃗₂·n̂)²)",
             "carrier 크기 / SVD 직접 연결",
             "AM_B_max = 2σ₁"],
        ]
    ))
    blocks.append(callout(
        "E⃗₁ ⊥ E⃗₂ 예시 (E⃗₁=(3,0), E⃗₂=(0,4)):\n"
        "  Def A: n̂* = (0.8,0.6),  AM = 4.80\n"
        "  Def B: n̂* = (0,1,0),    AM = 8.00  ← 서로 다르다!\n\n"
        "팀 코드(MATLAB): 정의 B 사용 → SVD 직접 적용",
        "📌", "orange_background"
    ))

    # ── 14. FEM 파이프라인 ────────────────────────────────────────
    blocks.append(h3("14. Grossman FEM 파이프라인"))
    blocks.append(code_block(
        "COMSOL (f₁) → Ẽ₁(r⃗) 복소 phasor\n"
        "COMSOL (f₂) → Ẽ₂(r⃗) 복소 phasor\n"
        "               ↓\n"
        "각 공간점 r⃗에서:\n"
        "  ① |E⃗₁|, |E⃗₂|, cosα 계산\n"
        "  ② 조건 확인: |E⃗₂| < |E⃗₁|cosα?\n"
        "  ③-a YES → E_AM_max = 2|E⃗₂|\n"
        "  ③-b NO  → E_AM_max = 2|E⃗₁×E⃗₂|/|E⃗₁-E⃗₂|\n"
        "     (또는 SVD: M=[ReẼ₁,ImẼ₁,ReẼ₂,ImẼ₂], AM=2σ₁)\n"
        "               ↓\n"
        "E_AM_max 3D 분포 맵 생성\n"
        "  → Slice 단면 시각화\n"
        "  → Isosurface (등값면) 시각화\n"
        "  → 신경 위치에서의 E_AM_max 추출"
    ))

    # ── 15. Steering ──────────────────────────────────────────────
    blocks.append(h3("15. Steering 원리"))
    blocks.append(callout(
        "전극 위치 또는 전류 비율 변경\n"
        "  → E⃗₁(r⃗), E⃗₂(r⃗) 공간 분포 변화\n"
        "  → 각 위치에서 |E⃗₁|, |E⃗₂|, α 모두 변화\n"
        "  → E_AM_max(r⃗) 분포 변화 → 최대값 위치 이동 = Steering!\n\n"
        "Grossman 2017 발견:\n"
        "  전류 비율만 바꾸면(전극 이동 없이) envelope peak가 이동한다.\n\n"
        "경골신경 TIS 설계 목표:\n"
        "  1. 경골신경 위치에서 E_AM_max ≥ 자극 역치\n"
        "  2. n̂*이 신경 주행 방향과 ≤ 30° 오차\n"
        "  3. 주변 조직에서 E_AM_max << 역치 (선택성)",
        "🎛️", "green_background"
    ))

    # ── 16. 한계 ──────────────────────────────────────────────────
    blocks.append(h3("16. E_AM_max의 한계"))
    blocks.append(callout(
        "E_AM_max는 '최적 방향 뉴런이 있다면'의 이론적 상한\n\n"
        "실제 자극 = E_AM_max × cos(θ_mismatch)\n"
        "  θ_mismatch = n̂*와 실제 뉴런 방향의 각도\n\n"
        "추가 한계:\n"
        "  • 세포 유형별 역치 차이 (motor vs sensory vs C-fiber)\n"
        "  • 조직 비등방성 (DTI 기반 백질 섬유 방향성)\n"
        "  • 네트워크 효과 (단일 뉴런 모델 불충분)\n"
        "  • 환자별 해부학 차이\n\n"
        "Grossman 2017 명시: '모델이 세포 유형, 지역별 흥분성 차이를 완전히 반영하지 않는다'",
        "⚠️", "red_background"
    ))

    # ── 17. 물리적 검증 ───────────────────────────────────────────
    blocks.append(h3("17. 물리적 검증 방법"))
    blocks.append(code_block(
        "Python Brute-force vs SVD 비교:\n\n"
        "import numpy as np\n\n"
        "E1 = np.array([3., 0., 0.])\n"
        "E2 = np.array([0., 4., 0.])\n\n"
        "# SVD (정의 B)\n"
        "M = np.column_stack([E1, E2])\n"
        "_, s, _ = np.linalg.svd(M, full_matrices=False)\n"
        "AM_svd = 2 * s[0]\n\n"
        "# Brute-force (정의 A)\n"
        "max_am = 0\n"
        "for theta in np.linspace(0, np.pi, 1000):\n"
        "    for phi in np.linspace(0, 2*np.pi, 1000):\n"
        "        n = np.array([np.sin(theta)*np.cos(phi),\n"
        "                      np.sin(theta)*np.sin(phi), np.cos(theta)])\n"
        "        am = 2 * min(abs(E1@n), abs(E2@n))\n"
        "        if am > max_am: max_am = am\n\n"
        "print(f'SVD(정의B):    {AM_svd:.4f} V/m')\n"
        "print(f'Brute-force(A): {max_am:.4f} V/m')",
        "python"
    ))

    # ── 18. 개념 요약 ─────────────────────────────────────────────
    blocks.append(h3("18. 핵심 요약"))
    blocks.append(code_block(
        "[FEM 기초]\n"
        "  ∇·(σ∇φ) = 0  ← ∇·J⃗=0 + J⃗=σE⃗ + E⃗=-∇φ 조합\n"
        "  준정적: λ=50km >> 몸, Displacement current 무시\n"
        "  → 두 전극쌍 독립 계산 → E⃗₁(r⃗), E⃗₂(r⃗) 획득\n\n"
        "[AM 포락선]\n"
        "  AM(n̂) = 2·min(|E⃗₁·n̂|, |E⃗₂·n̂|)  ← 약한 쪽의 두 배\n\n"
        "[E_AM_max 최적화]\n"
        "  Case 1: |E⃗₂| < |E⃗₁|cosα\n"
        "    n̂* = E⃗₂ 방향,  E_AM_max = 2|E⃗₂|\n\n"
        "  Case 2: |E⃗₂| ≥ |E⃗₁|cosα\n"
        "    n̂* ⊥ (E⃗₁-E⃗₂),  E_AM_max = 2|E⃗₁×E⃗₂|/|E⃗₁-E⃗₂|\n"
        "    = 삼각형 OAB 높이의 두 배\n\n"
        "[계산]\n"
        "  타원 직관: AM_max = 장반경\n"
        "  SVD: M=[ReẼ₁,ImẼ₁,ReẼ₂,ImẼ₂] → AM=2σ₁, n̂*=u₁\n\n"
        "[핵심 직관]\n"
        "  '두 채널의 투영을 같게 만드는 방향이 최적'\n"
        "  '한쪽이 너무 약하면 그 방향이 최선'\n"
        "  '균형이 가능하면 삼각형 높이 방향이 최선'"
    ))

    # ── 19. 자기평가 ──────────────────────────────────────────────
    blocks.append(h3("19. 자기평가 문항"))
    blocks.append(make_table(
        ["Level", "문항"],
        [
            ["L1", "준정적 근사에서 변위전류를 무시할 수 있는 이유를 수치로 설명하라."],
            ["L1", "AM(n̂) = 2min(E₁n, E₂n)에서 E₁n=3, E₂n=1 V/m일 때 AM은?"],
            ["L2", "최적 n̂*에서 반드시 E₁n = E₂n이 되어야 하는 이유를 직관적으로 설명하라."],
            ["L2", "|E⃗₁|=10, |E⃗₂|=3, α=30°일 때 Case 1/2 판정 후 E_AM_max를 계산하라."],
            ["L3", "Case 2에서 왜 n̂*가 (E⃗₁-E⃗₂)에 수직인지 등사영 조건으로 유도하라."],
            ["L3", "E⃗₁=(10,0), E⃗₂=(0,8) V/m일 때 Case 판정, E_AM_max, n̂* 각도를 구하라."],
            ["L4", "Case 2의 E_AM_max = 2|E⃗₁×E⃗₂|/|E⃗₁-E⃗₂|가 삼각형 높이의 두 배임을 유도하라."],
            ["L4", "경계(|E⃗₂|=|E⃗₁|cosα)에서 두 수식이 같은 값을 줌을 대수적으로 증명하라."],
            ["L5", "SVD에서 σ₁이 타원 장반경과 같은 이유를 ||Mv|| 최대화 관점에서 설명하라."],
            ["L5", "경골신경(z축 주행)에 대해 E_AM_max와 AM_z 중 어느 것이 더 적절한가? 임상적 의미를 논하라."],
        ]
    ))

    # ── 꼬리말 ────────────────────────────────────────────────────
    blocks.append(divider())
    blocks.append(para(rt(
        "작성: 2026-06-24 | 업데이트: 2026-06-26 | 커리큘럼 STEP 6/13 | "
        "참고: Grossman N et al. Cell 2017, 송솔웅(nTIS 전기장 계산 2026), 김대용(COMSOL 2025-2026) | "
        "다음: STEP 7 — COMSOL 3-phase TIS 구현 및 E_AM_max 3D 맵 생성",
        color="gray"
    )))

    return blocks


def append_blocks(tok, page_id, blocks, chunk=90):
    for i in range(0, len(blocks), chunk):
        c = blocks[i:i + chunk]
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

    print(f"\n📝  STEP 6 AM_max 통합 업데이트 블록 추가 중...")
    blocks = step6_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, NOTION_PAGE_ID, blocks)

    print("\n✅  완료!")
    print(f"   GitHub Pages: {GITHUB_URL}")


if __name__ == "__main__":
    main()
