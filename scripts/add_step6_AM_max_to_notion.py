#!/usr/bin/env python3
"""
STEP 6: TIS Amplitude Modulation과 AM_max — 최대 진폭 축 완전 이해
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
    blocks.append(h2("📐 STEP 6: TIS Amplitude Modulation과 AM_max — 최대 진폭 축 완전 이해"))
    blocks.append(callout(
        "커리큘럼 6/13단계. 단방향 AM이 왜 불충분한지 이해하고, "
        "최대 진폭 축(AM_max 방향 n*)을 타원 궤적 직관 + SVD 수식으로 도출하며, "
        "Grossman 2017 FEM 방법론을 구체적으로 파악할 수 있다.",
        "📡", "yellow_background"
    ))
    blocks.append(para(rt("🔗 GitHub Pages: ", bold=True),
                       rt(GITHUB_URL, link=GITHUB_URL)))
    blocks.append(para(rt("📄 로컬 파일: ", bold=True),
                       rt("docs/01_theory/15_AM_max_amplitude_modulation.md", code=True)))

    # ── 0. Grossman 2017 FEM ──────────────────────────────────────
    blocks.append(h3("0. Grossman 2017 FEM 시뮬레이션 파악"))
    blocks.append(callout(
        "Grossman N et al., Cell 2017; 169(6):1029-1041\n"
        "TIS의 첫 번째 정량적 증명 논문. FEM 시뮬레이션 + 동물 실험으로 '실제로 깊은 곳만 자극된다'를 동시에 증명.\n"
        "FEM 파트의 핵심 기여: AM_max를 방향 최적화 문제로 정의.",
        "📄", "gray_background"
    ))
    blocks.append(make_table(
        ["항목", "내용"],
        [
            ["모델", "4층 동심구(concentric sphere): 두피(σ=0.465) / 두개골(σ=0.01) / CSF(σ=1.65) / 뇌(σ=0.276) S/m"],
            ["지배 방정식", "∇·(σ∇V) = 0  (Quasi-static Laplace, 파장 150km >> 인체 0.3m)"],
            ["해석 방식", "Frequency domain 2회: f1 → E⃗₁(r), f2 → E⃗₂(r)"],
            ["핵심 결과", "표적 뇌심부: AM_max 높음 / 두피·두개골: AM_max 낮음 → 선택적 심부 자극 증명"],
        ]
    ))

    # ── 1. 왜 단방향 AM이 불충분한가 ─────────────────────────────
    blocks.append(h3("1. 왜 단방향 AM이 불충분한가"))
    blocks.append(callout(
        "실제 조직에서 각 공간점 P에 두 벡터가 존재:\n"
        "  전극쌍 1 (f1): E⃗₁ = (E₁x, E₁y, E₁z)  V/m\n"
        "  전극쌍 2 (f2): E⃗₂ = (E₂x, E₂y, E₂z)  V/m\n\n"
        "두 벡터의 방향이 서로 다를 수 있다!\n"
        "→ x방향만 보면: y, z 정보 버림 → AM 과소평가\n"
        "→ 실제 최대 AM 방향이 사선이면 단방향 측정은 모두 틀림",
        "⚠️", "red_background"
    ))
    blocks.append(code_block(
        "x방향 측정: AM_x = f(E₁x, E₂x)  → y, z 정보 버림\n"
        "y방향 측정: AM_y = f(E₁y, E₂y)  → x, z 정보 버림\n\n"
        "실제 최대 AM 방향이 사선이라면:\n"
        "  AM_x < AM_max   (과소 평가)\n"
        "  AM_y < AM_max   (과소 평가)\n\n"
        "→ x, y 방향 AM만 보면 실제 자극 강도를 과소평가한다"
    ))

    # ── 2. 1D AM 공식 복습 ────────────────────────────────────────
    blocks.append(h3("2. 1D AM 공식 복습 (단방향)"))
    blocks.append(code_block(
        "방향 단위벡터 n̂이 주어졌을 때:\n\n"
        "  E_n(t) = E⃗(t)·n̂\n"
        "         = (E⃗₁·n̂)·cos(ω₁t) + (E⃗₂·n̂)·cos(ω₂t)\n"
        "         =  E₁n   ·cos(ω₁t) +  E₂n   ·cos(ω₂t)\n\n"
        "E₁n ≥ E₂n > 0 일 때 포락선:\n"
        "  최대 = E₁n + E₂n\n"
        "  최소 = E₁n - E₂n\n"
        "  AM 깊이 = 2 × min(E₁n, E₂n)\n\n"
        "n̂을 바꾸면 E₁n, E₂n이 바뀌고 AM도 달라진다."
    ))

    # ── 3. 최적화 문제 ────────────────────────────────────────────
    blocks.append(h3("3. 최적화 문제 공식화"))
    blocks.append(callout(
        "AM_max = max_{||n̂||=1}  2 × min(E⃗₁·n̂, E⃗₂·n̂)\n\n"
        "직관:\n"
        "  n̂ = E⃗₁ 방향 → E₂n 매우 작음 → AM 작음\n"
        "  n̂ = E⃗₂ 방향 → E₁n 매우 작음 → AM 작음\n"
        "  n̂ = 두 벡터 '중간' → 둘 다 적당히 큼 → AM 최대!\n\n"
        "⭐ 최적 n̂*은 E₁n = E₂n이 되는 방향 (균등 기여)",
        "🎯", "green_background"
    ))

    # ── 4. 타원 궤적 ─────────────────────────────────────────────
    blocks.append(h3("4. 타원 궤적 — 핵심 물리적 직관"))
    blocks.append(callout(
        "3D 공간에서 E⃗(t) 벡터 끝점의 궤적:\n"
        "f₁ ≈ f₂일 때 (beat period >> carrier period), E⃗(t)는 타원을 그린다.\n\n"
        "  a = 장반경 (semi-major axis) → 가장 강한 방향의 크기\n"
        "  b = 단반경 (semi-minor axis) → 두 번째 방향\n\n"
        "타원을 n̂ 방향으로 투영:\n"
        "  n̂ = 장반경 방향 → 투영 최대 = a\n"
        "  n̂ = 단반경 방향 → 투영 최소 = b\n\n"
        "⭐ AM_max = 타원 장반경 a\n"
        "   최적 방향 n̂* = 장반경 방향",
        "🔵", "blue_background"
    ))
    blocks.append(code_block(
        "왜 타원이 생기나:\n\n"
        "  ω₁ = ω̄ + Δω/2,  ω₂ = ω̄ - Δω/2  (Δω << ω̄)\n\n"
        "  E⃗(t) = E⃗₁·cos(ω₁t) + E⃗₂·cos(ω₂t)\n"
        "       = cos(ω̄t)·[(E⃗₁+E⃗₂)cos(Δωt/2)]   ← in-phase 성분\n"
        "       + sin(ω̄t)·[(E⃗₂-E⃗₁)sin(Δωt/2)]   ← quadrature 성분\n\n"
        "  고정 slow-time τ에서:\n"
        "    E⃗(t|τ) = A⃗(τ)·cos(ω̄t) + B⃗(τ)·sin(ω̄t)\n"
        "    A⃗(τ) = (E⃗₁+E⃗₂)cos(τ)  ← 타원 한 축 벡터\n"
        "    B⃗(τ) = (E⃗₂-E⃗₁)sin(τ)  ← 타원 다른 축 벡터\n\n"
        "    A⃗cos + B⃗sin 형태 = 타원 ✓"
    ))

    # ── 5. SVD ────────────────────────────────────────────────────
    blocks.append(h3("5. SVD — 타원 장반경을 계산하는 방법"))
    blocks.append(code_block(
        "행렬 구성 (COMSOL phasor export 후):\n\n"
        "  M = [ Re(Ẽ₁x)  Im(Ẽ₁x)  Re(Ẽ₂x)  Im(Ẽ₂x) ]\n"
        "      [ Re(Ẽ₁y)  Im(Ẽ₁y)  Re(Ẽ₂y)  Im(Ẽ₂y) ]\n"
        "      [ Re(Ẽ₁z)  Im(Ẽ₁z)  Re(Ẽ₂z)  Im(Ẽ₂z) ]\n\n"
        "  M ∈ R^{3×4}\n"
        "  (실수 phasor면: Im = 0 → M = [E⃗₁, E⃗₂] ∈ R^{3×2})\n\n"
        "SVD 분해:\n"
        "  M = U Σ Vᵀ\n"
        "  σ₁ ≥ σ₂ ≥ σ₃ ≥ 0\n\n"
        "결과:\n"
        "  AM_max  = 2 × σ₁       (피크-투-피크)\n"
        "  최적 방향 n̂* = u₁      (U 행렬 첫 번째 열)"
    ))
    blocks.append(callout(
        "왜 인수 2인가?\n"
        "타원의 최대 투영 = 장반경 a = σ₁\n"
        "피크-투-피크 진폭 = 2a = 2σ₁\n"
        "(carrier가 +a에서 −a까지 왕복하므로)",
        "❓", "purple_background"
    ))
    blocks.append(code_block(
        "MATLAB 코드 (팀 실제 코드, 송솔웅 2026):\n\n"
        "% 각 점에서 복소 phasor (COMSOL export)\n"
        "E1 = [E1x; E1y; E1z];  % complex 3x1\n"
        "E2 = [E2x; E2y; E2z];  % complex 3x1\n\n"
        "% 행렬 구성\n"
        "M = [real(E1), imag(E1), real(E2), imag(E2)];  % 3x4 real\n\n"
        "% SVD\n"
        "[U, S, V] = svd(M, 'econ');\n\n"
        "% AM_max\n"
        "AM_max = 2 * S(1,1);\n"
        "n_opt  = U(:,1);      % 최적 방향",
        "matlab"
    ))

    # ── 6. AM_max 두 가지 정의 비교 ──────────────────────────────
    blocks.append(h3("6. AM_max 두 가지 정의 비교"))
    blocks.append(make_table(
        ["정의", "수식", "특징", "SVD 연결"],
        [
            ["A — Modulation Depth",
             "AM_A(n̂) = 2 × min(|E⃗₁·n̂|, |E⃗₂·n̂|)",
             "두 소스의 '약한 쪽'이 결정 / 최적 조건: E₁n = E₂n",
             "간접적"],
            ["B — Envelope Peak (Grossman / 팀 MATLAB)",
             "AM_B(n̂) = sqrt((E⃗₁·n̂)² + (E⃗₂·n̂)²)",
             "carrier 진폭의 크기 / SVD와 직접 연결",
             "AM_B_max = 2σ₁"],
        ]
    ))
    blocks.append(callout(
        "E⃗₁ ∥ E⃗₂인 경우: 두 정의가 같은 방향을 최적으로 선택\n"
        "E⃗₁ ⊥ E⃗₂인 경우: 최적 n̂*가 서로 달라질 수 있음\n\n"
        "팀 코드(MATLAB): 정의 B 사용 → SVD 직접 적용",
        "📌", "orange_background"
    ))

    # ── 7. 물리적 검증 ────────────────────────────────────────────
    blocks.append(h3("7. 물리적 검증 방법"))
    blocks.append(code_block(
        "Python Brute-force vs SVD 비교:\n\n"
        "import numpy as np\n\n"
        "E1 = np.array([3., 0., 0.])\n"
        "E2 = np.array([0., 4., 0.])\n\n"
        "# SVD 방법\n"
        "M = np.column_stack([E1, E2])\n"
        "_, s, _ = np.linalg.svd(M, full_matrices=False)\n"
        "AM_svd = 2 * s[0]\n\n"
        "# Brute-force (수천 방향 탐색)\n"
        "max_am = 0\n"
        "for theta in np.linspace(0, np.pi, 1000):\n"
        "    for phi in np.linspace(0, 2*np.pi, 1000):\n"
        "        n = np.array([np.sin(theta)*np.cos(phi),\n"
        "                      np.sin(theta)*np.sin(phi),\n"
        "                      np.cos(theta)])\n"
        "        am = np.sqrt((E1@n)**2 + (E2@n)**2)\n"
        "        if am > max_am: max_am = am\n\n"
        "print(f'SVD:         {AM_svd:.4f} V/m')\n"
        "print(f'Brute-force: {2*max_am:.4f} V/m')\n"
        "# 두 값이 같으면 SVD 공식 검증 완료",
        "python"
    ))
    blocks.append(callout(
        "COMSOL 시각적 검증:\n"
        "1. AM_max 맵 생성 (SVD 기반)\n"
        "2. 같은 점에서 AM_x, AM_y, AM_z 각각 계산\n"
        "3. 반드시: AM_max >= AM_x, AM_y, AM_z 확인\n"
        "4. 신경 주행 방향(z축)과 AM_max 방향 비교\n\n"
        "평가 기준:\n"
        "  AM_z   → 보수적 (실제 신경 주행 방향)\n"
        "  AM_max → 공정한 상한선 (어떤 방향 신경이든 최대 받을 수 있는 값)",
        "✅", "green_background"
    ))

    # ── 8. 개념 요약 ──────────────────────────────────────────────
    blocks.append(h3("8. 전체 개념 요약"))
    blocks.append(code_block(
        "AM_max 핵심 흐름:\n\n"
        "1D 단방향 AM\n"
        "  E_n(t) = E₁n·cos(ω₁t) + E₂n·cos(ω₂t)\n"
        "  AM = 2×min(E₁n, E₂n)\n"
        "  → n̂ 방향에 따라 값이 달라진다\n"
        "         ↓\n"
        "3D 최적화 문제\n"
        "  max_{||n̂||=1} AM(n̂) = AM_max\n"
        "  최적 조건: E⃗₁·n̂ = E⃗₂·n̂  (균등 기여)\n"
        "         ↓\n"
        "타원 궤적 직관\n"
        "  E⃗(t)가 carrier 주기로 타원을 그린다\n"
        "  AM_max = 장반경 a / 최적 방향 = 장반경 방향\n"
        "         ↓\n"
        "SVD로 계산\n"
        "  M = [Re(Ẽ₁), Im(Ẽ₁), Re(Ẽ₂), Im(Ẽ₂)]\n"
        "  SVD: σ₁ = 장반경\n"
        "  AM_max = 2σ₁,  n̂* = u₁"
    ))

    # ── 9. 자기평가 ───────────────────────────────────────────────
    blocks.append(h3("9. 자기평가 문항"))
    blocks.append(make_table(
        ["Level", "문항"],
        [
            ["L1", "공간의 한 점에서 x방향 AM과 y방향 AM이 다른 이유는?"],
            ["L1", "AM(n̂) = 2min(E₁n, E₂n)에서 E₁n=3, E₂n=1 V/m일 때 AM은?"],
            ["L2", "최적 n̂*에서 반드시 E₁n = E₂n이 되어야 하는 이유를 직관적으로 설명하라."],
            ["L3", "타원 장반경 방향으로 투영했을 때 AM이 최대인 이유를 기하학적으로 설명하라."],
            ["L4", "SVD에서 σ₁이 타원 장반경과 같은 이유를 ||Mv|| 최대화 관점에서 설명하라."],
            ["L5", "E⃗₁=(3,0,0), E⃗₂=(0,4,0) V/m일 때 AM_max 및 n̂*를 직접 계산하라."],
        ]
    ))

    # ── 꼬리말 ────────────────────────────────────────────────────
    blocks.append(divider())
    blocks.append(para(rt(
        "작성: 2026-06-24 | 커리큘럼 STEP 6/13 | "
        "참고: Grossman N et al. Cell 2017, 송솔웅(nTIS 전기장 계산 2026), 김대용(COMSOL 2025-2026) | "
        "다음: STEP 7 — COMSOL 3-phase TIS 구현 및 AM_max 3D 맵 생성",
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

    print(f"\n📝  STEP 6 AM_max 블록 추가 중...")
    blocks = step6_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, NOTION_PAGE_ID, blocks)

    print("\n✅  완료!")
    print(f"   GitHub Pages: {GITHUB_URL}")


if __name__ == "__main__":
    main()
