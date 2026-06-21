#!/usr/bin/env python3
"""
STEP 1~3 누락 모식도 보완 — Notion 페이지에 추가
Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/add_diagrams_supplement_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
NOTION_PAGE_ID = "37d6191a4fdc8035acb1d31b767ac08a"

def H(tok):
    return {"Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
            "Notion-Version": VER}

def rt(text, bold=False, code=False, color="default"):
    ann = {"bold": bold, "code": code, "color": color,
           "italic": False, "strikethrough": False, "underline": False}
    return {"type": "text", "text": {"content": text}, "annotations": ann}

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

def code_block(text):
    return {"object": "block", "type": "code",
            "code": {"rich_text": [rt(text)], "language": "plain text"}}

def bullet(*rts):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": list(rts)}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def para(*rts):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": list(rts)}}

def toggle(title, children=None):
    return {"object": "block", "type": "toggle",
            "toggle": {"rich_text": [rt(title, bold=True)],
                       "children": children or []}}


def diagram_blocks():
    blocks = []

    blocks.append(divider())
    blocks.append(h2("📐 STEP 1~3 모식도 보완 (ASCII 다이어그램)"))
    blocks.append(callout(
        "GitHub 파일 업데이트에 포함된 누락 모식도를 Notion에 추가. 각 STEP의 핵심 개념을 시각적으로 보완.",
        "🖼️", "yellow_background"
    ))

    # ── STEP 1 보완 ──
    blocks.append(h3("▶ STEP 1 보완: 방광 해부학 & 신경 3경로 상세 모식도"))

    blocks.append(para(rt("① 방광 = 풍선 비유", bold=True)))
    blocks.append(code_block(
        "[풍선 = 방광]\n\n"
        "┌──────────────────────┐\n"
        "│  안쪽 벽 (Urothelium) │ ← 소변을 감지하는 능동 센서\n"
        "│                      │   (방광 팽창 → ATP 분비)\n"
        "│  근육층 (Detrusor)    │ ← 조이고 풀리는 근육\n"
        "│                      │   (부교감: 수축 / 교감: 이완)\n"
        "└──────────┬───────────┘\n"
        "           │\n"
        "        수도꼭지 1 (IUS) ← 자동, 평활근, 교감신경 지배\n"
        "           │\n"
        "        수도꼭지 2 (EUS) ← 내가 직접 조이는 것, 횡문근"
    ))

    blocks.append(para(rt("② 교감신경 경로 상세 (리모컨 1 — 저장)", bold=True)))
    blocks.append(code_block(
        "허리 척수 (T10-L2)\n"
        "        │\n"
        "        └─► 하복신경 (Hypogastric nerve)\n"
        "                 │\n"
        "        ┌────────┴────────┐\n"
        "        ▼                 ▼\n"
        "  방광 근육 (β3-AR)    요도 입구 (α1-AR)\n"
        "        │                 │\n"
        "   '이완해!' →        '잠가!' →\n"
        "   방광이 늘어남        소변 못 나감\n"
        "   (소변 저장)         (소변 저장)\n\n"
        "비유: 풍선 불 때 풍선 입구 막아주는 손"
    ))

    blocks.append(para(rt("③ 부교감신경 경로 상세 (리모컨 2 — 배뇨)", bold=True)))
    blocks.append(code_block(
        "엉치 척수 (S2-S4)\n"
        "        │\n"
        "        └─► 골반신경 (Pelvic nerve)\n"
        "                 │\n"
        "                 ▼\n"
        "           방광 근육 M3 수용체 (무스카린 수용체)\n"
        "                 │\n"
        "            '수축해!' →\n"
        "            방광이 조여짐 → 소변 배출\n\n"
        "항무스카린제 → M3 차단 → 방광 수축 억제 (구강건조 부작용: 침샘도 M3)\n"
        "비유: 풍선 손 놓으면서 바람 나오게 하는 것"
    ))

    blocks.append(para(rt("④ 체성신경 경로 상세 (리모컨 3 — 수의 조절)", bold=True)))
    blocks.append(code_block(
        "엉치 척수 (S2-S4)\n"
        "        │\n"
        "        └─► 음부신경 (Pudendal nerve)\n"
        "                 │\n"
        "                 ▼\n"
        "           외요도괄약근 (EUS) [횡문근]\n"
        "                 │\n"
        "         '꽉 잡아!' or '놔줘!'\n"
        "         (화장실 참기 or 배뇨)\n\n"
        "비유: 내가 직접 쥐고 있는 밸브"
    ))

    # ── STEP 2 보완 ──
    blocks.append(h3("▶ STEP 2 보완: 탈분극 세포막 이온 분포 상세"))

    blocks.append(para(rt("① 안정막전위 이온 분포 (평소)", bold=True)))
    blocks.append(code_block(
        "세포 바깥:  Na+ 많음\n"
        "    +   +   +   +   +   +   +\n"
        "    ━━━━━━━━━━━━━━━━━━━━━━━━━  ← 세포막\n"
        "    -   -   -   -   -   -   -\n"
        "세포 안쪽:  K+, 단백질 많음\n\n"
        "→ 전위차: 안쪽이 -70 mV (더 음전하)\n"
        "→ Na+ 채널: 닫혀 있음"
    ))

    blocks.append(para(rt("② 전기자극 → Na+ 채널 개방 → 탈분극", bold=True)))
    blocks.append(code_block(
        "전극 (음극) 근처 전류 흐름\n"
        "        ↓\n"
        "안팎 전위차 감소: -70 mV → -55 mV (역치)\n"
        "        ↓\n"
        "Na+ 채널 강제 개방!\n\n"
        "     ← Na+ 유입 ←\n"
        "    +   +  [채널]  +   +\n"
        "    ━━━━━━━━↓━━━━━━━━━━━  ← 세포막\n"
        "    -   -  Na+→   -   -\n"
        "               ↓\n"
        "        안쪽이 (+)로 역전 = 탈분극"
    ))

    blocks.append(para(rt("③ 활동전위 전파 도미노 원리", bold=True)))
    blocks.append(code_block(
        "자극 지점  위치 1    위치 2    위치 3\n"
        "           [+++]  →  [---]  →  [---]   처음\n\n"
        "           [재분극] → [+++]  →  [---]   이동\n\n"
        "           [끝남]  → [재분극] → [+++]   계속 전파\n\n"
        "탈분극된(+) 부위가 옆 부위(-) 끌어당김 → 연쇄 Na+ 채널 개방"
    ))

    blocks.append(para(rt("④ Myelin 유무에 따른 전도 속도 비교", bold=True)))
    blocks.append(code_block(
        "Myelin 없는 C섬유 (느림):\n"
        "●─────────────────────────→  0.5~2 m/s\n"
        "  모든 구간 탈분극\n\n"
        "Myelin 있는 A섬유 (빠름):\n"
        "●══════╗  ╔══════╗  ╔══════→  30~120 m/s\n"
        "       ↓  ↓      ↓  ↓\n"
        "      [+]        [+]        [+]\n"
        "  ↑Ranvier node에서만 탈분극 → 점프 전도 (Saltatory)"
    ))

    # ── STEP 3 보완 ──
    blocks.append(h3("▶ STEP 3 보완: SNM 신체 모식도 & PTNS/TTNS/TIS 단면 비교"))

    blocks.append(para(rt("① SNM 신체 삽입 전체 모식도", bold=True)))
    blocks.append(code_block(
        "        [뇌]\n"
        "          │\n"
        "        [척수]\n"
        "          │\n"
        "     허리 S3 레벨 ← 전극 삽입 위치\n"
        "     ┌────┴─────┐\n"
        "     │  전극    │──── 리드선\n"
        "     └──────────┘         │\n"
        "                    ┌─────┴──────┐\n"
        "                    │  배터리    │ ← 엉덩이 위쪽 피하 이식\n"
        "                    │  (IPG)     │   (약 성인 손바닥 크기)\n"
        "                    └────────────┘\n"
        "                          │\n"
        "                    환자 리모컨으로 ON/OFF 조절"
    ))

    blocks.append(para(rt("② PTNS / TTNS / TIS 자극 방식 단면 비교", bold=True)))
    blocks.append(code_block(
        "── PTNS (경피 바늘) ────────────────────\n"
        "  [지면 전극]\n"
        "       │\n"
        "  ─────┼──────────────────  ← 피부 표면\n"
        "       │\n"
        "  ─────┼──────────────────  ← 피하 지방\n"
        "       │\n"
        "     [바늘 끝] ←──────────  ← 경골신경 바로 옆 (~3~5 mm)\n"
        "  장점: 정확 / 단점: 침습, 병원 방문\n\n"
        "── TTNS (표면 전극) ─────────────────────\n"
        "  [전극A]        [전극B]\n"
        "     │                │\n"
        "  ───┼────────────────┼───  ← 피부 (전류 일부 흡수)\n"
        "     │ ~~~~~~~~~~~~~~│\n"
        "  ───┼────────────────┼───  ← 지방 (전류 손실)\n"
        "     └───────┬────────┘\n"
        "             ▼\n"
        "      경골신경 (전류 일부 도달)\n"
        "  장점: 비침습 / 단점: 깊이·선택성 낮음\n\n"
        "── TIS (간섭 집속) ──────────────────────\n"
        "  [A1] f1=2000Hz          [A2] f1=2000Hz\n"
        "    │   고주파 → 피부 안전  │\n"
        "  ──┼──────────────────────┼──  ← 피부\n"
        "    │  ↘                ↙  │\n"
        "  ──┼────────────✕─────────┼──  ← 경골신경 위치\n"
        "    │  ↗  (간섭=20Hz)  ↖  │       저주파 envelope만!\n"
        "  [B1] f2=2020Hz          [B2] f2=2020Hz\n"
        "  장점: 비침습 + 깊이 + 선택성 동시 달성"
    ))

    blocks.append(callout(
        "핵심 정리: SNM(수술·강효) → PTNS(바늘·안전) → TTNS(비침습·약점있음) → TIS(비침습+깊이+선택성) 기술 발전 흐름",
        "🚀", "green_background"
    ))

    blocks.append(divider())
    blocks.append(para(rt("모식도 보완 추가: 2026-06-21 | GitHub 업데이트 반영", color="gray")))

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

    print(f"\n📐  STEP 1~3 누락 모식도 추가 중...")
    blocks = diagram_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, NOTION_PAGE_ID, blocks)
    print("\n✅  완료!")


if __name__ == "__main__":
    main()
