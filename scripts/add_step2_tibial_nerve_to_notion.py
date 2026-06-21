#!/usr/bin/env python3
"""
STEP 2: 경골신경 해부학 & 자극 기전 — Notion 페이지에 추가
Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/add_step2_tibial_nerve_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
NOTION_PAGE_ID = "37d6191a4fdc8035acb1d31b767ac08a"  # TIS_Tibial Nerve 페이지
GITHUB_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/10_tibial_nerve_anatomy_stimulation/"

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


def step2_blocks():
    blocks = []

    blocks.append(divider())
    blocks.append(h2("⚡ STEP 2: 경골신경 해부학 & 자극 기전"))
    blocks.append(callout(
        "커리큘럼 2/13단계. 경골신경 위치·내부 구조 → 전기자극 활성화 원리 → 척수 방광 억제 경로까지.",
        "🦴", "yellow_background"
    ))
    blocks.append(para(
        rt("🔗 GitHub Pages: ", bold=True),
        rt(GITHUB_URL, link=GITHUB_URL)
    ))
    blocks.append(para(
        rt("📄 로컬 파일: ", bold=True),
        rt("docs/01_theory/10_tibial_nerve_anatomy_stimulation.md", code=True)
    ))

    # 1. 위치 & 뿌리
    blocks.append(h3("1. 경골신경 위치 & 척수 뿌리"))
    blocks.append(bullet(rt("주행: 무릎 뒤쪽(오금) → 종아리 안쪽 → 발목 안쪽 복숭아뼈(내과)")))
    blocks.append(bullet(rt("PTNS 자침: 내과에서 손가락 3마디 위 (~5 cm)")))
    blocks.append(bullet(rt("척수 뿌리: L4, L5, S1, S2, S3 → S2-S4 방광 조절과 동일 레벨!")))
    blocks.append(callout(
        "S2, S3 뿌리를 포함 → 방광 부교감신경 출발지 S2-S4와 겹침 → 경골신경 자극이 방광에 영향을 주는 근거",
        "🎯", "green_background"
    ))

    # 2. 내부 구조
    blocks.append(h3("2. 신경 내부 구조"))
    blocks.append(make_table(
        ["구조", "역할"],
        [
            ["Epineurium", "신경 전체 보호 외피"],
            ["Perineurium", "각 다발(Fascicle) 감싸는 막"],
            ["Fascicle", "기능별로 묶인 신경섬유 다발"],
            ["Axon", "실제 전기 신호 전달하는 선"],
            ["Myelin sheath", "축삭 감싸는 절연체 → 신호 빠르게 전달"],
        ]
    ))

    # 3. 신경섬유 종류
    blocks.append(h3("3. 신경섬유 종류 — 자극 반응 순서"))
    blocks.append(make_table(
        ["섬유", "전도속도", "기능", "자극 역치"],
        [
            ["Aα", "70-120 m/s", "근육 운동, 고유감각", "낮음"],
            ["Aβ", "30-70 m/s", "촉각, 압각", "낮음"],
            ["Aδ", "5-30 m/s", "가벼운 통증, 온도", "중간"],
            ["C", "0.5-2 m/s", "깊은 통증, 자율신경", "높음 (무수초)"],
        ]
    ))
    blocks.append(callout(
        "굵을수록 자극 역치 낮음 → 적은 전류로 자극 가능. PTNS는 주로 Aβ, Aδ 섬유 활성화.",
        "💡", "blue_background"
    ))

    # 4. 탈분극 기전
    blocks.append(h3("4. 전기자극 → 탈분극 → 활동전위 발생 기전"))
    blocks.append(toggle("안정막전위 → 탈분극 단계별 설명", [
        bullet(rt("안정 상태: 세포 안쪽 -70 mV (Na+ 바깥 많음, K+ 안쪽 많음)")),
        bullet(rt("전기자극 → 세포막 전위차 감소 → -55 mV (역치) 도달")),
        bullet(rt("Na+ 채널 강제 개방 → Na+ 유입 → 안쪽이 (+)로 역전 = 탈분극")),
        bullet(rt("탈분극 부위(+)가 옆 부위(-) 끌어당김 → 인접 Na+ 채널 개방")),
        bullet(rt("연쇄 전파 = 활동전위 이동 (도미노 원리)")),
    ]))
    blocks.append(toggle("Myelin과 도약 전도 (Saltatory Conduction)", [
        bullet(rt("Myelin = 절연체 → Ranvier node 틈새에서만 탈분극 발생")),
        bullet(rt("신호가 점프하며 이동 → A섬유: 30~120 m/s vs C섬유: 0.5~2 m/s")),
        bullet(rt("TIS 고주파 전류도 이 원리로 Myelin 있는 신경 선택적 자극 가능")),
    ]))

    # 5. 파라미터
    blocks.append(h3("5. 전기자극 핵심 파라미터 (PTNS 표준)"))
    blocks.append(make_table(
        ["파라미터", "PTNS 표준값", "의미"],
        [
            ["주파수", "20 Hz", "1초에 20번 자극"],
            ["펄스폭 (PW)", "200 μs", "각 펄스 지속 시간"],
            ["진폭", "0.5~9 mA", "발가락 움직임 느낄 정도"],
            ["치료 시간", "30분/회, 12주", "표준 치료 기간"],
        ]
    ))

    # 6. 척수 경로
    blocks.append(h3("6. 척수 S2-S4 → 방광 억제 경로"))
    blocks.append(bullet(rt("경골신경 Aδ/Aβ 활성화 → 척수 후각 S2-S4 진입")))
    blocks.append(bullet(rt("GABAergic interneuron 활성화 → 방광 부교감 신호 차단")))
    blocks.append(bullet(rt("상행 경로 → PAG → PMC 게이트 강화 → 배뇨 억제 보강")))
    blocks.append(callout(
        "근거: Tai et al. — 쥐 S2 레벨에서 GABAergic interneuron이 경골신경 자극에 의한 방광 억제를 매개함을 확인.",
        "📄", "gray_background"
    ))

    # 7. 치료 인과 사슬
    blocks.append(h3("7. 치료 효과의 전체 인과 사슬"))
    for step in [
        "전기 자극 인가",
        "경골신경 Na+ 채널 강제 개방",
        "탈분극 → 활동전위 발생",
        "도약 전도로 척수 방향 이동",
        "S2-S4 후각 도달",
        "GABAergic interneuron 활성화",
        "방광 부교감 흥분 신호 차단",
        "방광 과수축 억제",
        "OAB 증상 감소 (빈뇨·절박뇨 개선)",
    ]:
        blocks.append(numbered(step))
    blocks.append(callout(
        "장기 효과: 반복 자극 → 억제 회로 자체 강화 (신경 가소성) → 치료 후 수개월 효과 지속",
        "🔄", "purple_background"
    ))

    # 8. PTNS vs TTNS vs TIS
    blocks.append(h3("8. PTNS vs TTNS vs TIS 비교"))
    blocks.append(make_table(
        ["", "PTNS", "TTNS", "TIS (우리 연구)"],
        [
            ["침습도", "침습 (바늘)", "비침습", "비침습"],
            ["자극 깊이", "깊음 (신경 직접)", "얕음", "깊음 (간섭 집속)"],
            ["피부 불편감", "바늘 통증", "따끔거림", "적음 (고주파)"],
            ["자가 사용", "불가", "가능", "가능"],
            ["신경 경로", "경골신경 → S2-S4", "경골신경 → S2-S4", "경골신경 → S2-S4 (동일)"],
        ]
    ))

    # 자기평가
    blocks.append(h3("자기평가 문항"))
    for q in [
        "경골신경의 척수 뿌리 레벨은? 방광 조절 S2-S4와 어떻게 겹치나?",
        "신경섬유 A섬유와 C섬유의 차이는? 전기자극 시 어떤 것이 먼저 반응하나?",
        "안정막전위 -70 mV에서 전기자극이 어떻게 Na+ 채널을 열고 활동전위를 만드나?",
        "Saltatory conduction이란? Myelin이 있으면 왜 신호가 빠른가?",
        "경골신경 자극이 방광 수축을 억제하는 척수 내 핵심 신경전달물질은?",
        "PTNS, TTNS, TIS의 차이를 침습도와 자극 깊이 관점에서 비교하라.",
    ]:
        blocks.append(numbered(q))

    blocks.append(divider())
    blocks.append(para(rt("작성: 2026-06-21 | 커리큘럼 STEP 2/13 | 다음: STEP 3 — PTNS / TTNS / SNM 기존 기술 분석", color="gray")))

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

    print(f"\n📝  STEP 2 경골신경 블록 추가 중 (페이지 ID: {NOTION_PAGE_ID})...")
    blocks = step2_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, NOTION_PAGE_ID, blocks)

    print("\n✅  완료!")
    print(f"   GitHub Pages: {GITHUB_URL}")


if __name__ == "__main__":
    main()
