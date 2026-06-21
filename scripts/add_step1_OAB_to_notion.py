#!/usr/bin/env python3
"""
STEP 1: OAB 병태생리학 — Notion 페이지에 추가
Usage:
  export NOTION_TOKEN=secret_xxxx
  python3 scripts/add_step1_OAB_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
GITHUB_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/09_OAB_pathophysiology/"

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

def code_block(text, language="plain text"):
    return {"object": "block", "type": "code",
            "code": {"rich_text": [rt(text)], "language": language}}


def step1_blocks():
    blocks = []

    blocks.append(divider())
    blocks.append(h2("📖 STEP 1: OAB 병태생리학 (Overactive Bladder Pathophysiology)"))
    blocks.append(callout(
        "커리큘럼 1/13단계. 경골신경 TIS 자극이 OAB를 조절하는 원리를 이해하기 위한 기초.",
        "🧠", "yellow_background"
    ))
    blocks.append(para(
        rt("🔗 GitHub Pages: ", bold=True),
        rt(GITHUB_URL, link=GITHUB_URL)
    ))
    blocks.append(para(
        rt("📄 로컬 파일: ", bold=True),
        rt("docs/01_theory/09_OAB_pathophysiology.md", code=True)
    ))

    # 1. 정의 & 역학
    blocks.append(h3("1. OAB 정의 & 역학"))
    blocks.append(callout(
        "ICS 정의 (2002): Urgency, with or without urge incontinence, usually with frequency and nocturia — 요로감염 등 명백한 병인 없이",
        "📌", "gray_background"
    ))
    blocks.append(make_table(
        ["증상", "정의", "비고"],
        [
            ["Urgency (절박뇨)", "갑작스럽고 참기 어려운 요의", "OAB 필수 증상"],
            ["Frequency (빈뇨)", "≥8회/day", ""],
            ["Nocturia (야간뇨)", "≥1회/night", ""],
            ["Urge incontinence", "urgency와 함께 오는 불수의적 요누출", "OAB-wet"],
        ]
    ))
    blocks.append(bullet(rt("전세계 유병률: ~11% (Milsom 2001) / 한국: ~12.2% (40세 이상)")))
    blocks.append(bullet(rt("40대 ~8% → 75세+ ~31% (나이와 강한 상관)")))
    blocks.append(callout(
        "핵심 구분: OAB는 증상 기반 진단. Urodynamic DO 확인은 ~50~60%에 불과 → OAB ≠ DO",
        "⚠️", "red_background"
    ))

    # 2. 방광 해부학
    blocks.append(h3("2. 방광 해부학"))
    blocks.append(make_table(
        ["구조", "종류", "역할"],
        [
            ["Urothelium", "상피", "방광 팽창 감지 → ATP·ACh 분비 (능동 센서)"],
            ["Lamina propria", "결합조직", "Interstitial cells 위치, 신호 전달"],
            ["Detrusor muscle", "평활근", "부교감→수축(배뇨), 교감→이완(저장)"],
            ["IUS", "평활근", "교감신경 지배, 불수의적"],
            ["EUS", "횡문근", "음부신경 지배, 수의적 조절"],
        ]
    ))

    # 3. 신경 3가지 경로
    blocks.append(h3("3. 방광 조절 신경 3가지 경로"))
    blocks.append(callout(
        "리모컨 1: 교감신경 → 저장 / 리모컨 2: 부교감신경 → 배뇨 / 리모컨 3: 체성신경 → 수의 조절",
        "🎮", "blue_background"
    ))
    blocks.append(make_table(
        ["경로", "출발지", "신경", "수용체", "역할"],
        [
            ["교감 (Sympathetic)", "T10-L2", "Hypogastric nerve", "β3 / α1", "Detrusor 이완 / IUS 수축 (저장)"],
            ["부교감 (Parasympathetic)", "S2-S4", "Pelvic nerve", "M3 (무스카린)", "Detrusor 수축 (배뇨)"],
            ["체성 (Somatic)", "S2-S4", "Pudendal nerve", "nAChR", "EUS 수의 조절"],
        ]
    ))
    blocks.append(make_table(
        ["상태", "교감", "부교감", "체성", "결과"],
        [
            ["저장기", "ON (이완+잠금)", "OFF", "ON (EUS 잠금)", "소변 저장"],
            ["배뇨기", "OFF", "ON (M3 수축)", "OFF (EUS 열림)", "배뇨"],
        ]
    ))

    # 4. 뇌-방광 경로
    blocks.append(h3("4. 뇌-방광 신경 조절 경로"))
    blocks.append(make_table(
        ["뇌 구조", "역할"],
        [
            ["PFC (전전두피질)", "수의적 억제 — '참아야지'"],
            ["ACC (전대상피질)", "긴박감 인지"],
            ["PAG (수도관주위회색질)", "배뇨 게이트 — 상황 판단"],
            ["PMC (뇌교 배뇨중추)", "배뇨 ON/OFF 최종 스위치"],
        ]
    ))
    blocks.append(callout(
        "배뇨 스위치는 척수가 아닌 뇌간 PMC에 있다. 척수 손상 환자 배뇨 불능의 이유. 경골신경 자극이 S2-S4에서 작용하는 근거.",
        "💡", "blue_background"
    ))

    # 5. 경골신경 연결
    blocks.append(h3("5. 경골신경 → 방광 연결 (연구 핵심 근거)"))
    blocks.append(bullet(rt("경골신경 (Tibial nerve): 발목 안쪽 주행, 뿌리 L4-S3")))
    blocks.append(bullet(rt("척수 진입 위치: S2-S4 ← 부교감신경(배뇨) 출발지와 동일 레벨")))
    blocks.append(bullet(rt("체성 구심성 신호 → 방광 부교감 반사 억제 → 방광 과활성 감소")))
    blocks.append(make_table(
        ["", "PTNS (기존)", "TIS (우리 연구)"],
        [
            ["자극 방법", "발목에 바늘 삽입", "피부 전극 4개"],
            ["침습도", "침습 (바늘)", "비침습"],
            ["빈도", "주 1회 병원 방문", "자가 적용 가능"],
            ["신경 경로", "경골신경 → S2-S4", "경골신경 → S2-S4 (동일)"],
        ]
    ))

    # 6. OAB 발생 기전
    blocks.append(h3("6. OAB 발생 기전 3가지 가설"))
    blocks.append(toggle("① 근원성 (Myogenic)", [
        bullet(rt("노화·허혈 → Gap junction (Connexin 43) 증가")),
        bullet(rt("국소 자발 수축 → 전체 Detrusor 전파 → DO")),
        bullet(rt("비유: 도미노처럼 혼자 무너짐")),
    ]))
    blocks.append(toggle("② 신경성 (Neurogenic)", [
        bullet(rt("중추 억제 손상 (뇌졸중·PD·척수 손상)")),
        bullet(rt("C-fiber 민감화 (역치 하강)")),
        bullet(rt("PMC 억제 gate 실패 → 조기 배뇨반사")),
        bullet(rt("비유: 브레이크가 고장난 차")),
    ]))
    blocks.append(toggle("③ 요로상피성 (Urothelial) ← 최근 주목", [
        bullet(rt("방광 팽창 → Urothelium → ATP 과다 분비")),
        bullet(rt("P2X3 purinergic receptor 활성화 → 구심성 신경 과자극 → Urgency")),
        bullet(rt("항무스카린 무반응 환자 (~30%)에서 이 기전 우세 가능성")),
        bullet(rt("비유: 화재경보기 민감도가 너무 높아 밥 냄새에도 울림")),
    ]))

    # 7. 치료 옵션
    blocks.append(h3("7. 현재 치료 옵션 & 한계"))
    blocks.append(make_table(
        ["치료", "기전", "한계"],
        [
            ["생활습관 교정", "수분·카페인 조절", "효과 제한적"],
            ["항무스카린제 (Oxybutynin)", "M3 차단 → Detrusor 이완", "구강건조·인지장애, 6개월 순응도 ~30%"],
            ["β3 작용제 (Mirabegron)", "β3 → Detrusor 이완", "고혈압 부작용, 비용"],
            ["PTNS", "경골신경 경피 자극 (바늘)", "침습, 주 1회 병원 방문"],
            ["SNM", "천수 이식형 자극기", "수술·비용·감염 위험"],
            ["Botox 방광 주사", "신경근 접합부 차단", "반복 시술, 요저류 위험"],
        ]
    ))
    blocks.append(callout(
        "신경조절 등장 배경: 약물 부작용 + 낮은 순응도 → PTNS/SNM 효과 입증 → 비침습화 필요 → TIS 접근 동기",
        "🎯", "green_background"
    ))

    # 자기평가
    blocks.append(h3("자기평가 문항"))
    for q in [
        "OAB 진단에 필수인 증상은? OAB와 DO의 차이는?",
        "배뇨 ON/OFF 스위치 역할을 하는 뇌 구조물은?",
        "교감·부교감·체성신경이 저장기/배뇨기에 각각 어떻게 작동하나?",
        "경골신경 자극이 방광에 영향을 미치는 신경해부학적 경로를 설명하라.",
        "항무스카린제 무반응 환자에서 어떤 OAB 발생 기전이 우세한가?",
        "PTNS 대비 TIS 접근의 이론적 장점은?",
    ]:
        blocks.append(numbered(q))

    blocks.append(divider())
    blocks.append(para(rt("작성: 2026-06-21 | 커리큘럼 STEP 1/13 | 다음: STEP 2 — 경골신경 해부학 & 자극 기전", color="gray")))

    return blocks


NOTION_PAGE_ID = "37d6191a4fdc8035acb1d31b767ac08a"  # TIS_Tibial-Nerve 페이지

def find_ntis_page(tok):
    print(f"  페이지 ID 사용: {NOTION_PAGE_ID}")
    return NOTION_PAGE_ID


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
        print("    ! export NOTION_TOKEN=secret_xxxx")
        sys.exit(1)

    r = requests.get(f"{API}/users/me", headers=H(tok))
    if r.status_code != 200:
        print(f"❌  인증 실패 ({r.status_code})")
        sys.exit(1)
    print(f"✅  인증 성공 — {r.json().get('name','?')}")

    print("\n🔍  nTIS_Tibial nerve 페이지 검색 중...")
    page_id = find_ntis_page(tok)

    if not page_id:
        page_id = input("\n페이지 ID를 직접 입력하세요 (32자리 UUID): ").strip().replace("-", "")
        if len(page_id) != 32:
            print("❌  유효하지 않은 페이지 ID")
            sys.exit(1)

    print(f"\n📝  STEP 1 OAB 병태생리학 블록 추가 중 (페이지 ID: {page_id})...")
    blocks = step1_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, page_id, blocks)

    print("\n✅  완료!")
    print(f"   GitHub Pages: {GITHUB_URL}")


if __name__ == "__main__":
    main()
