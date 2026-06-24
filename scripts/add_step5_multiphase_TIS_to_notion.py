#!/usr/bin/env python3
"""
STEP 5: Multi-source / Multi-channel TIS — 왜 3-phase가 필요한가
Notion 페이지에 추가

Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/add_step5_multiphase_TIS_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
NOTION_PAGE_ID = "37d6191a4fdc8035acb1d31b767ac08a"
GITHUB_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/14_multiphase_TIS_why_3phase/"

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


def step5_blocks():
    blocks = []

    # ── 헤더 ──────────────────────────────────────────────────────
    blocks.append(divider())
    blocks.append(h2("🔀 STEP 5: Multi-source / Multi-channel TIS — 왜 3-phase가 필요한가"))
    blocks.append(callout(
        "커리큘럼 5/13단계. 2-phase TIS의 3가지 근본 한계를 이해하고, "
        "Multi-channel TIS와 3-phase TIS가 왜 개발되었는지 수식과 직관으로 설명할 수 있다.",
        "📡", "yellow_background"
    ))
    blocks.append(para(rt("🔗 GitHub Pages: ", bold=True),
                       rt(GITHUB_URL, link=GITHUB_URL)))
    blocks.append(para(rt("📄 로컬 파일: ", bold=True),
                       rt("docs/01_theory/14_multiphase_TIS_why_3phase.md", code=True)))

    # ── 0. 출발점 ──────────────────────────────────────────────────
    blocks.append(h3("0. 출발점: 2-phase TIS는 무엇을 증명했는가"))
    blocks.append(make_table(
        ["구분", "내용"],
        [
            ["Grossman 2017이 증명한 것 ✅",
             "피부 전극으로 깊은 신경을 비침습적으로 자극할 수 있다"],
            ["Grossman 2017이 증명하지 못한 것 ❌",
             "원하는 신경만 골라서 / 원하는 방향으로 / 어떤 환자에게도 자극할 수 있다"],
        ]
    ))
    blocks.append(callout(
        "이 '못한 것' 세 가지가 2-phase TIS의 3가지 근본 한계다. "
        "3-phase TIS는 이 세 가지를 동시에 해결하기 위해 개발되었다.",
        "🎯", "green_background"
    ))

    # ── 1. 3가지 한계 ─────────────────────────────────────────────
    blocks.append(h3("1. 2-phase TIS의 3가지 근본 한계"))

    # 한계 1
    blocks.append(para(rt("한계 1: 자극 영역이 너무 넓다 (Focality 부족)", bold=True)))
    blocks.append(callout(
        "AM = 2 × min(|E₁|, |E₂|)\n"
        "→ 두 전기장이 '둘 다 충분히 강한' 곳에서 자극 발생\n"
        "→ 전기장은 전극에서 멀어질수록 서서히 감소 → 충분한 구역이 뭉툭하게 넓음\n"
        "→ 두 구역의 교집합도 넓음 → 자극 영역이 덩어리(blob)로 형성",
        "⚠️", "red_background"
    ))
    blocks.append(code_block(
        "경골신경 자극 시 문제:\n"
        "  경골신경: 직경 2~3mm\n"
        "  2-phase 자극 영역: 수 cm²\n\n"
        "  → 주변 근육 수축\n"
        "  → 다른 신경(비복신경 등) 동시 활성화\n"
        "  → 환자 불쾌감·부작용 발생"
    ))

    # 한계 2
    blocks.append(para(rt("한계 2: 표적을 전자적으로 3D 이동할 수 없다 (Steering 제한)", bold=True)))
    blocks.append(callout(
        "I₁:I₂ 비율 변경으로 표적 이동 가능 — 단, 두 전극쌍을 잇는 축 방향(1D)만 가능.\n"
        "다른 방향(상하·전후)으로 이동하려면 전극을 물리적으로 다시 붙여야 함.\n\n"
        "3-phase: 3개 전류 파라미터 조절만으로 3D 전방향 표적 이동 가능.",
        "↔️", "orange_background"
    ))

    # 한계 3
    blocks.append(para(rt("한계 3: 자극 방향을 바꿀 수 없다 (Direction 제어 불가)", bold=True)))
    blocks.append(callout(
        "E⃗(t) = E⃗₁·cos(ω₁t) + E⃗₂·cos(ω₂t)\n\n"
        "E⃗₁, E⃗₂가 전극 배치로 고정 → E⃗(t)는 span{E⃗₁, E⃗₂} = 2D 평면 밖으로 못 나감\n"
        "→ 한 점에서 전기장 궤적 = 직선 (왔다 갔다)\n"
        "→ AM_max 방향(u₁)이 이 2D 평면 안에서만 존재 가능\n\n"
        "경골신경이 z축 방향인데 전기장이 x-y 평면에 있으면 → 자극 비효율",
        "🔄", "purple_background"
    ))
    blocks.append(para(
        rt("📢 회의록 참조 (260618, 참석자 1, 14:55): ", bold=True),
        rt('"3상은 직선으로 안 나타나. 벡터가 이렇게 됐다가 이렇게 됐다가 이렇게 되는 거지."')
    ))

    # 비교표
    blocks.append(h3("2-phase vs 3-phase 비교표"))
    blocks.append(make_table(
        ["구분", "2-phase TIS", "3-phase TIS"],
        [
            ["① 자극 영역", "넓음 (blob) — 신경 주변까지 자극",
             "좁음 — 신경 위주로 집중"],
            ["② Steering", "1D (선 방향만) — 전극 이동 필요",
             "3D (전방향) — 전류 파라미터만 조정"],
            ["③ 자극 방향", "고정 (전극 배치로 결정)",
             "임의 3D 방향 — 신경 축에 맞게 조정 가능"],
            ["전극 수", "4개 (2쌍)", "3개"],
            ["전류 합", "각 쌍이 별도로 0", "3전극 합 = 0 자동 만족 (Kirchhoff)"],
        ]
    ))

    # ── 2. 채널 수와 초점성 ──────────────────────────────────────
    blocks.append(h3("2. 왜 채널 수가 늘면 자극 영역이 좁아지는가"))
    blocks.append(callout(
        "핵심 원리: '제약 조건 교집합'\n\n"
        "2채널: AM > T ⟺ |E₁| > T/2 AND |E₂| > T/2  → 넓은 교집합\n"
        "n채널: AM > T ⟺ |E₁| > T/n AND ... AND |Eₙ| > T/n  → 조건 n개, 교집합 좁아짐\n\n"
        "비유 — GPS 위성:\n"
        "  위성 2개 → 위치가 두 점 중 하나 (넓음)\n"
        "  위성 3개 → 위치가 정확히 한 점 (좁음)",
        "📐", "blue_background"
    ))
    blocks.append(code_block(
        "구체적 숫자 예시:\n\n"
        "표적 r*: E₁=5, E₂=5 → AM = 2×min(5,5) = 10 V/m ✓\n\n"
        "표적에서 1cm 이동 (2채널):\n"
        "  E₁=6, E₂=4 → AM = 2×min(6,4) = 8 V/m  (80%, 여전히 강함)\n\n"
        "표적에서 1cm 이동 (4채널):\n"
        "  E₁=6, E₂=4, E₃=4, E₄=3 → AM = 2×min(6,4,4,3) = 6 V/m  (60%, 약해짐)\n\n"
        "→ 더 많은 채널 = 어떤 방향으로 이동해도 멀어지는 채널 존재 → AM 더 빠르게 감소"
    ))

    # ── 3. 직선 vs 타원 ──────────────────────────────────────────
    blocks.append(h3("3. 직선 vs 타원 — 전기장 궤적의 근본 차이"))
    blocks.append(para(rt("2-phase: 직선 궤적 (2D 평면에 갇힘)", bold=True)))
    blocks.append(code_block(
        "E⃗(t) = E⃗₁·cos(ω₁t) + E⃗₂·cos(ω₂t)\n\n"
        "E⃗₁, E⃗₂ 두 벡터의 선형결합\n"
        "→ span{E⃗₁, E⃗₂} = 2D 평면 밖으로 절대 못 나감\n\n"
        "한 점에서 궤적:\n"
        "  E_y\n"
        "   ↑\n"
        "   │\n"
        "   │  ←────────────────→   (직선으로 왔다 갔다)\n"
        "   │\n"
        "   └──────────────────────→ E_x\n\n"
        "AM_max 방향 u₁: span{E⃗₁, E⃗₂} 평면 안에서만 존재"
    ))
    blocks.append(para(rt("3-phase: 타원 궤적 (3D 전방향 가능)", bold=True)))
    blocks.append(code_block(
        "Iₐ = I·cos(ωt + 0°)\n"
        "Ib = I·cos(ωt + 120°)   ← 120° 뒤처짐\n"
        "Ic = I·cos(ωt + 240°)   ← 240° 뒤처짐\n\n"
        "세 전류는 동시에 최대가 되지 않음 → 합벡터가 돈다\n\n"
        "한 점에서 궤적:\n"
        "  E_y\n"
        "   ↑\n"
        "   │    ╭──────────╮\n"
        "   │  ╱   ←──←──←  ╲\n"
        "   │ │↙               ↑│\n"
        "   ●─│─────────────────│──→ E_x\n"
        "   │ │↖               ↓│\n"
        "   │  ╲   →──→──→  ╱\n"
        "   │    ╰──────────╯\n\n"
        "타원 장축 방향 = AM_max 방향 (u₁)\n"
        "→ 전극 배치 + 전류 최적화로 임의 3D 방향 선택 가능"
    ))

    # SVD 관점
    blocks.append(callout(
        "SVD 관점:\n\n"
        "2-phase: M = [Re(Ẽ₁), Im(Ẽ₁), Re(Ẽ₂), Im(Ẽ₂)]  (3×4)\n"
        "  열공간 = span{E⃗₁, E⃗₂} = 최대 2D\n\n"
        "3-phase: M = [Re(Ẽ₁), Im(Ẽ₁), Re(Ẽ₂), Im(Ẽ₂), Re(Ẽ₃), Im(Ẽ₃)]  (3×6)\n"
        "  열공간 = span{E⃗₁, E⃗₂, E⃗₃} = 3D (세 벡터가 선형독립이면)\n\n"
        "AM_max = 2·σ₁(M)\n"
        "u₁ = M의 첫 번째 좌특이벡터 = AM_max 방향",
        "🔢", "blue_background"
    ))

    # ── 4. 위상 선택 ─────────────────────────────────────────────
    blocks.append(h3("4. 위상이 반드시 0°/120°/240° 이어야 하는가?"))
    blocks.append(callout(
        "아니다. 0°/120°/240°는 하나의 특수 선택일 뿐이다.\n\n"
        "이 선택의 장점:\n"
        "  ① 전류 균형 자동 만족: Iₐ+Ib+Ic = I·[1+(-1/2)+(-1/2)] = 0\n"
        "     → Ground 전극 불필요, 전극 1개 절약\n"
        "  ② 복소평면을 균등 분할 → 등방성(isotropic) 자극\n\n"
        "다른 위상 선택:\n"
        "  → 표적 위치·신경 방향·조직 형태에 따라 최적화로 결정\n"
        "  → 0°/120°/240°는 편리한 초기값, 필수 조건 아님",
        "⚙️", "gray_background"
    ))

    # ── 5. 전극 선형독립 ─────────────────────────────────────────
    blocks.append(h3("5. 전극 선형독립 조건 — 3D AM_max 달성의 핵심"))
    blocks.append(callout(
        "3D AM_max 달성 조건:\n"
        "  span{E⃗₁(r*), E⃗₂(r*), E⃗₃(r*)} = ℝ³\n"
        "  → 세 전극 쌍의 전기장 벡터가 표적 r*에서 선형독립이어야 함",
        "📐", "purple_background"
    ))
    blocks.append(toggle("실패 케이스 (3-phase여도 3D 안 되는 경우)", [
        bullet(rt("실패 1: 모든 전극 쌍이 평행 → span = 1D (직선만)")),
        bullet(rt("실패 2: 모든 전극 쌍이 transverse 평면에만 배치 → span = 2D, z축 성분 없음")),
        bullet(rt("실패 3: 두 쌍이 너무 가까움 → E⃗₁ ≈ E⃗₂ → 사실상 2-channel")),
    ]))
    blocks.append(callout(
        "Lead Field 행렬 F(r*) = [E⃗₁ | E⃗₂ | E⃗₃]  (3×3)\n\n"
        "rank(F) = 1: 모두 평행 (최악)\n"
        "rank(F) = 2: 한 평면 (2D만)\n"
        "rank(F) = 3: 선형독립 (3D 완전 제어) ← 목표\n\n"
        "경골신경 발목 적용:\n"
        "  쌍 1, 쌍 2: transverse 방향 (x-y 평면)\n"
        "  쌍 3: longitudinal 방향 (z축 성분 포함)\n"
        "  → rank(F) = 3 달성 가능\n\n"
        "→ 김대용 260518_Leadfield 연구의 핵심 문제",
        "🎯", "green_background"
    ))

    # ── 6. 전체 논리 ─────────────────────────────────────────────
    blocks.append(h3("6. 전체 논리 지도"))
    blocks.append(code_block(
        "Grossman 2017: 2-phase TIS\n"
        "  ✅ 증명: 깊은 곳을 비침습으로 자극할 수 있다\n"
        "  ❌ 한계: 넓은 blob / 1D steering / 방향 고정\n"
        "           ↓\n"
        "해결: 채널 수 증가 (Multi-channel TIS)\n"
        "  → 더 많은 채널 = 더 많은 조건 교집합 = 좁은 자극 영역\n"
        "           ↓\n"
        "3-phase TIS (3쌍, 120° 위상 간격)\n"
        "  ① 자극 영역 좁힘   → '원하는 곳만' 해결\n"
        "  ② 3D 전자 조향     → '어떤 환자에게도' 해결\n"
        "  ③ 방향 제어        → '원하는 방향으로' 해결\n"
        "           ↓\n"
        "수식: AM_max = 2·σ₁(M)\n"
        "  M 열공간 = 3D (전극 선형독립 조건 충족 시)\n"
        "  → u₁ 방향을 경골신경 축으로 정렬 가능"
    ))
    blocks.append(callout(
        "핵심 한 줄 요약:\n\n"
        "2-phase TIS: '깊은 곳을 자극할 수 있다' 증명 ✅ — '원하는 곳만, 원하는 방향으로, 어떤 환자에게도' ❌\n"
        "3-phase TIS: 위 세 가지를 동시에 해결하기 위해 개발됨.",
        "💎", "green_background"
    ))

    # ── 자기평가 ─────────────────────────────────────────────────
    blocks.append(h3("자기평가 문항"))
    for q in [
        "[Lv.1] 2-phase TIS의 3가지 한계를 각각 한 문장으로 설명하라.",
        "[Lv.2] 'AM_max 방향이 2D 평면에 갇힌다'는 것을 span{E⃗₁, E⃗₂} 언어로 설명하라.",
        "[Lv.2] 0°/120°/240° 위상이 아닌 다른 위상을 쓸 수 있는 이유는?",
        "[Lv.3] 채널 수 2→4→8 증가 시 자극 영역이 좁아지는 이유를 '조건 교집합' 원리로 설명하라.",
        "[Lv.4] 발목에 3-phase TIS 적용 시 rank(F)=3이 되려면 전극을 어떻게 배치해야 하는가?",
        "[Lv.4] 4채널 TIS와 3-phase TIS는 다른 개념인가? 차이점은?",
    ]:
        blocks.append(numbered(q))

    blocks.append(divider())
    blocks.append(para(rt(
        "작성: 2026-06-23 | 커리큘럼 STEP 5/13 | "
        "참고: 회의록 260618_180422, 송솔웅(nTIS 전기장 계산 2026), 김대용(Leadfield 260518) | "
        "다음: STEP 6 — 3-phase TIS 수식 심화 및 COMSOL 구현",
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

    print(f"\n📝  STEP 5 Multi-source TIS 블록 추가 중...")
    blocks = step5_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, NOTION_PAGE_ID, blocks)

    print("\n✅  완료!")
    print(f"   GitHub Pages: {GITHUB_URL}")


if __name__ == "__main__":
    main()
