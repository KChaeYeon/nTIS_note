#!/usr/bin/env python3
"""
STEP 7: 전극 위치에 따른 AM 전기장 맵 변화 (2026-06-29)
Notion 페이지에 추가

Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/add_step7_electrode_position_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
NOTION_PAGE_ID = "37d6191a4fdc8035acb1d31b767ac08a"

GITHUB_RAW = (
    "https://raw.githubusercontent.com/KChaeYeon/nTIS_note/main/"
    "docs/06_Meeting/nTIS_%ED%94%84%EB%A6%AC%EC%A0%A0%ED%85%8C%EC%9D%B4%EC%85%98/"
    "%EC%86%A1%EC%86%94%EC%9B%85/Figures/"
)
GITHUB_PAGE_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/16_electrode_position_AM_field/"


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


def para(*rts):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": list(rts)}}


def code_block(text, lang="plain text"):
    return {"object": "block", "type": "code",
            "code": {"rich_text": [rt(text)], "language": lang}}


def img(url, caption=""):
    block = {
        "object": "block",
        "type": "image",
        "image": {
            "type": "external",
            "external": {"url": url}
        }
    }
    if caption:
        block["image"]["caption"] = [rt(caption)]
    return block


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


def step7_blocks():
    blocks = []

    # ── 헤더 ──────────────────────────────────────────────────────
    blocks.append(divider())
    blocks.append(h2("🔬 STEP 7: 전극 위치에 따른 AM 전기장 맵 변화"))
    blocks.append(callout(
        "커리큘럼 7/13단계 | 작성: 2026-06-29\n"
        "학습 목표:\n"
        "1. 표준 4전극 TIS 중심점에서 E₁∥E₂를 유도할 수 있다\n"
        "2. X축 수렴 시 AM zone이 좁은 수직 컬럼으로 집속되는 이유를 설명할 수 있다\n"
        "3. Y축 수렴 시 AM이 약해지는 이유를 p=I·d로 설명할 수 있다\n"
        "4. COMSOL 시뮬레이션 결과 맵을 물리적으로 해석할 수 있다",
        "📡", "yellow_background"
    ))
    blocks.append(para(rt("🔗 GitHub Pages: ", bold=True),
                       rt(GITHUB_PAGE_URL, link=GITHUB_PAGE_URL)))
    blocks.append(para(rt("📄 로컬 파일: ", bold=True),
                       rt("docs/01_theory/16_electrode_position_AM_field.md", code=True)))

    # ── COMSOL 시뮬레이션 설정 ────────────────────────────────────
    blocks.append(h3("1. COMSOL 시뮬레이션 설정"))
    blocks.append(code_block(
        "원형 단면 팬텀 (균일 σ)\n"
        "  Ch1: 좌측 수직 쌍극자 (1,000 Hz)\n"
        "  Ch2: 우측 수직 쌍극자 (1,040 Hz)  →  Δf = 40 Hz envelope\n"
        "  지배방정식: ∇·(σ∇φ) = 0  (준정적 근사)\n"
        "  AM_max: max_{n̂} 2·min(|E₁·n̂|, |E₂·n̂|)\n\n"
        "시뮬레이션 시리즈:\n"
        "  Horizontal/ (1→17): 전극 X축 이동\n"
        "  Vertical/   (1→34): 전극 Y축 이동"
    ))

    # ── 기초 물리 ─────────────────────────────────────────────────
    blocks.append(h3("2. 기초 물리"))
    blocks.append(callout(
        "쌍극자 원거리 전기장:\n"
        "  E_far ∝ p/r³ = (I × d) / r³\n\n"
        "AM_max 조건:\n"
        "  E₁ ∥ E₂  →  AM_max = 2·min(|E₁|, |E₂|)  (최대)\n"
        "  E₁ ⊥ E₂  →  AM ≈ 0\n\n"
        "표준 4전극 중심점:\n"
        "  E₁ = E₂ = (0, -kₑqd/L³)  →  -y 방향 평행  →  AM 최대",
        "⚡", "gray_background"
    ))

    # ── X축 수렴 ──────────────────────────────────────────────────
    blocks.append(h3("3. X축 수렴 — 집속(Focusing) 효과"))
    blocks.append(para(rt("채널 간 거리 L 감소  →  E ∝ 1/L³ 급증  →  좁고 밝은 수직 컬럼", bold=True)))
    blocks.append(make_table(
        ["L", "전기장 비율"],
        [["20 mm", "×1 (기준)"],
         ["10 mm", "×8 (2³)"],
         ["5 mm",  "×64 (4³)"]]
    ))
    blocks.append(callout(
        "수직 컬럼 형성 이유:\n"
        "중심선 위 임의 점 (0,y)에서:\n"
        "  x성분: E₁ₓ = -E₂ₓ  →  상쇄 (AM 기여 없음)\n"
        "  y성분: E₁ᵧ = E₂ᵧ   →  평행 보강 (AM 활성)\n"
        "→ AM 활성 영역이 수직 띠 형태로 집속",
        "📐", "blue_background"
    ))

    # ── X축 이미지 ────────────────────────────────────────────────
    blocks.append(h3("3-1. COMSOL 시뮬레이션: Horizontal 시리즈"))
    blocks.append(para(rt("baseline (대칭 배치) — AM zone 중앙 수직 타원")))
    blocks.append(img(GITHUB_RAW + "Horizontal/1.png",
                      "Horizontal/1.png — 기준 배치: AM zone 중앙 대칭"))
    blocks.append(para(rt("X축 이동 중간 — AM zone 우측으로 이동")))
    blocks.append(img(GITHUB_RAW + "Horizontal/9.png",
                      "Horizontal/9.png — 전극 우측 이동: AM zone 우측 집속"))
    blocks.append(para(rt("X축 이동 극단 — AM zone 좌측 경계로 이동")))
    blocks.append(img(GITHUB_RAW + "Horizontal/17.png",
                      "Horizontal/17.png — 전극 최대 이동: AM zone 좌측 경계"))

    # ── Y축 수렴 ──────────────────────────────────────────────────
    blocks.append(h3("4. Y축 수렴 — 소멸(Defocusing) 효과"))
    blocks.append(para(rt("쌍극자 내부 간격 d 감소  →  p = I·d 감소  →  원거리 E 약화  →  AM 소멸", bold=True)))
    blocks.append(make_table(
        ["d", "p (기준=1)", "원거리 E", "AM_max"],
        [["20 mm", "1.0", "기준", "기준"],
         ["10 mm", "0.5", "1/2", "1/2"],
         ["5 mm",  "0.25","1/4", "1/4"],
         ["→ 0",  "→ 0", "→ 0", "→ 0"]]
    ))
    blocks.append(callout(
        "주의: 전극 바로 옆은 전기장이 강해지지만 AM은 발생하지 않는다.\n"
        "AM은 E₁과 E₂가 동시에 겹치는 지점에서만 발생.\n"
        "전극 직근방에는 상대 채널 E₂가 없으므로 AM = 0.",
        "⚠️", "red_background"
    ))

    # ── Y축 이미지 ────────────────────────────────────────────────
    blocks.append(h3("4-1. COMSOL 시뮬레이션: Vertical 시리즈"))
    blocks.append(para(rt("Y축 이동 중간 — AM zone 상방 이동, 크기 감소")))
    blocks.append(img(GITHUB_RAW + "Vertical/17.png",
                      "Vertical/17.png — 전극 상방 이동: AM zone 축소 및 이동"))
    blocks.append(para(rt("Y축 이동 극단 — AM zone 상단, 매우 작고 어두움")))
    blocks.append(img(GITHUB_RAW + "Vertical/34.png",
                      "Vertical/34.png — 전극 최대 상방: AM zone 거의 소멸"))

    # ── 실제 해부학 모델 ──────────────────────────────────────────
    blocks.append(h3("5. 실제 해부학 팬텀 (Rat 경골 단면)"))
    blocks.append(img(GITHUB_RAW + "1to5.png",
                      "1to5.png — Rat 경골 단면 + tibial nerve 위치 + AM 전기장 오버레이"))
    blocks.append(callout(
        "실제 해부학 모델에서는:\n"
        "  - 조직별 σ(전도율) 불균일 → 전기장 굴절/집중 발생\n"
        "  - 뼈(σ=0.0035 S/m), 근육(σ=0.265 S/m), 피부(σ=0.02 S/m)\n"
        "  - AM zone 위치가 원형 팬텀 예측과 다를 수 있음",
        "🦴", "gray_background"
    ))

    # ── 최종 비교표 ───────────────────────────────────────────────
    blocks.append(h3("6. 비교 요약"))
    blocks.append(make_table(
        ["구분", "X축 수렴 (L↓)", "Y축 수렴 (d↓)"],
        [["변화 대상",   "채널 간 거리 L",     "쌍극자 내부 간격 d"],
         ["전기장 방향", "E₁∥E₂ 유지 ✓",       "E₁∥E₂ 유지 ✓"],
         ["전기장 세기", "∝ 1/L³ → 급증 ↑↑",  "∝ I·d → 감소 ↓↓"],
         ["AM_max",     "증가, 집속",           "감소, 소멸"],
         ["맵 모양",    "좁고 밝은 수직 컬럼",  "전반적으로 어두운 영역"],
         ["물리적 본질","두 파원 중첩 강화",    "파원 자체 세기 감소"]]
    ))
    blocks.append(callout(
        "핵심 한 줄:\n"
        "X축 수렴 = '두 채널이 만나는 점에서 필드가 강해지는' 집속 효과\n"
        "Y축 수렴 = '각 채널 원천 자체가 약해지는' 소멸 효과\n"
        "두 경우 모두 E₁∥E₂는 유지 → AM 방향성 동일, 세기만 달라짐",
        "✅", "green_background"
    ))

    # ── 다음 단계 ─────────────────────────────────────────────────
    blocks.append(h3("7. 다음 단계"))
    blocks.append(bullet(rt("COMSOL dual overlay map 구현 (AM zone + Inhibition zone)")))
    blocks.append(bullet(rt("E_th 결정: 교수님 실측값 (Rheobase=25V, Chronaxie=30μs) vs HH 모델")))
    blocks.append(bullet(rt("전극 간격 파라미터 스위프 (L, d 체계적 변화)")))

    return blocks


def post_blocks(tok, page_id, blocks, chunk=100):
    url = f"{API}/blocks/{page_id}/children"
    for i in range(0, len(blocks), chunk):
        r = requests.patch(url, headers=H(tok), json={"children": blocks[i:i+chunk]})
        if r.status_code not in (200, 201):
            print(f"Error {r.status_code}: {r.text}")
            sys.exit(1)
        print(f"  Uploaded blocks {i+1}–{min(i+chunk, len(blocks))}")
        time.sleep(0.3)


def main():
    tok = os.environ.get("NOTION_TOKEN")
    if not tok:
        print("Error: NOTION_TOKEN 환경변수가 없습니다.")
        print("Usage: NOTION_TOKEN=ntn_xxx python3 scripts/add_step7_electrode_position_to_notion.py")
        sys.exit(1)

    print("STEP 7: 전극 위치에 따른 AM 전기장 맵 변화 → Notion 업로드 중...")
    blocks = step7_blocks()
    print(f"  총 {len(blocks)}개 블록 준비 완료")
    post_blocks(tok, NOTION_PAGE_ID, blocks)
    print("✓ 완료!")


if __name__ == "__main__":
    main()
