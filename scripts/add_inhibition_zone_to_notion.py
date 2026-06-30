#!/usr/bin/env python3
"""
nTIS Notion 페이지에 TI 자극 공간 3구역 분류 섹션 추가
Usage:
  export NOTION_TOKEN=ntn_xxxx
  python3 scripts/add_inhibition_zone_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
SITE_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/17_inhibition_zone_3regions/"


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
    def cell(txt):
        return [rt(str(txt))]
    hr = {"object": "block", "type": "table_row",
          "table_row": {"cells": [[rt(h, bold=True)] for h in headers]}}
    drs = [{"object": "block", "type": "table_row",
            "table_row": {"cells": [cell(c) for c in row]}} for row in rows]
    return {"object": "block", "type": "table",
            "table": {"table_width": n, "has_column_header": True,
                      "has_row_header": False, "children": [hr] + drs}}

def code_block(text, language="plain text"):
    return {"object": "block", "type": "code",
            "code": {"rich_text": [rt(text)], "language": language}}

def eq(expr):
    return {"object": "block", "type": "equation",
            "equation": {"expression": expr}}

def para(*rts):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": list(rts)}}


def inhibition_zone_blocks():
    blocks = []

    blocks.append(divider())
    blocks.append(h2("📐 TI 자극 공간 3구역 분류 — Activation / Inhibition / Subthreshold"))
    blocks.append(callout(
        "LED phantom 실험에서 관찰되는 '항상 ON / 40Hz 깜박임 / 항상 OFF'를 "
        "AM 포락선 수식과 신경생리 기전으로 완전히 설명한다.",
        "🔬", "blue_background"
    ))
    blocks.append(para(rt("🔗 GitHub Pages: ", bold=True),
                       rt(SITE_URL, link=SITE_URL)))
    blocks.append(para(rt("📄 로컬 파일: ", bold=True),
                       rt("docs/01_theory/17_inhibition_zone_3regions.md", code=True)))

    # 핵심 변수
    blocks.append(h3("핵심 변수"))
    blocks.append(para(rt("AM 포락선 최댓값·최솟값 (위치 r마다 결정):")))
    blocks.append(eq(r"E_{\max}(\mathbf{r}) = A_1 + A_2 \quad \text{(보강 간섭)}"))
    blocks.append(eq(r"E_{\min}(\mathbf{r}) = |A_1 - A_2| \quad \text{(상쇄 간섭)}"))
    blocks.append(bullet(rt("전극 근처: "), rt("A1 >> A2", code=True), rt(" → E_min 높음, 변조 깊이 낮음")))
    blocks.append(bullet(rt("중심부: "), rt("A1 ≈ A2", code=True), rt(" → E_min ≈ 0, 포락선이 0까지 내려감")))

    # 3구역 분류 표
    blocks.append(h3("3구역 분류표"))
    blocks.append(make_table(
        ["구역", "조건", "LED", "신경 반응", "위치"],
        [
            ["Activation Zone", "E_min < E_th < E_max", "40Hz 깜박임", "40Hz 발화", "중심부 (표적)"],
            ["Inhibition Zone", "E_th ≤ E_min", "항상 ON", "HFB — 억제", "전극 근처"],
            ["Subthreshold Zone", "E_max < E_th", "항상 OFF", "무반응", "외곽"],
        ]
    ))

    # Activation Zone
    blocks.append(h3("① Activation Zone"))
    blocks.append(para(rt("신경막 = 저역통과 필터 (τ_membrane ≈ 5–20 ms):")))
    blocks.append(bullet(rt("1 kHz 캐리어 주기 = 1 ms ≪ τ → 추적 불가 → 반응 없음")))
    blocks.append(bullet(rt("40 Hz 포락선 주기 = 25 ms ≈ τ → 추적 가능 → 발화")))
    blocks.append(callout(
        "핵심 통찰: 신경은 캐리어(1 kHz)를 무시하고, 포락선(40 Hz)만 '본다'.",
        "💡", "yellow_background"
    ))

    # Inhibition Zone
    blocks.append(h3("② Inhibition Zone"))
    blocks.append(para(rt("조건: E_min = |A1 - A2| ≥ E_th → 포락선 최솟값조차 역치 이상 → LED 항상 ON")))
    blocks.append(para(rt("신경에 일어나는 기전:", bold=True)))
    blocks.append(bullet(
        rt("High-Frequency Block (HFB): ", bold=True),
        rt("~1kHz 연속 자극 → 전압개폐형 Na+ 채널 비활성화(inactivated) 상태에 갇힘 → AP 발생 불가")
    ))
    blocks.append(bullet(
        rt("Wedensky Inhibition: ", bold=True),
        rt("지속적 탈분극 → 막전위가 역치 근방에 갇힘 → AP 생성 기전 마비")
    ))
    blocks.append(code_block(
        "정상:  -70 mV → threshold(-55 mV) → 발화 → 재분극\n"
        "HFB:   -70 mV → kHz 연속 자극 → Na+ 채널 비활성화\n"
        "              → 재분극 기회 없음 → 발화 불가"
    ))
    blocks.append(callout(
        "TIS 설계 이점: 피질 표면(전극 근처) = Inhibition Zone → 자극 없음 / "
        "심부 표적 = Activation Zone → 40Hz 선택적 자극 → 두개골 절개 없이 심부 자극 가능",
        "✅", "green_background"
    ))

    # Subthreshold Zone
    blocks.append(h3("③ Subthreshold Zone"))
    blocks.append(para(rt("조건: E_max = A1 + A2 < E_th → 보강 간섭 최대치도 역치 미달 → 무반응")))
    blocks.append(para(rt(
        "소형 phantom에서는 존재하지 않을 수 있음. 실제 뇌·말초신경 볼륨에서는 외곽에 반드시 존재."
    )))

    # 공식 정의
    blocks.append(h3("Inhibition Zone 공식 정의"))
    blocks.append(callout(
        "Inhibition Zone: AM 포락선 최솟값 E_min = |A1 − A2| 가 신경 활성화 역치 E_th를 초과하는 공간 영역. "
        "이 영역의 신경은 ~kHz 연속 자극에 의한 전압개폐형 Na+ 채널 비활성화 "
        "(HFB / Wedensky inhibition)로 기능적으로 억제된다.",
        "📌", "red_background"
    ))

    # 다음 단계
    blocks.append(h3("다음 단계"))
    blocks.append(bullet(rt("COMSOL에서 E_min, E_max 맵 계산 및 3구역 경계 시각화")))
    blocks.append(bullet(rt("E_th 결정 방법: Strength-Duration Curve 기반")))
    blocks.append(bullet(rt("dual overlay map (activation + inhibition 동시 표시) Python 구현")))

    return blocks


def find_ntis_page(tok):
    r = requests.post(f"{API}/search", headers=H(tok),
                      json={"query": "nTIS", "filter": {"value": "page", "property": "object"}})
    if r.status_code != 200:
        print(f"❌ 검색 실패: {r.status_code} {r.text[:300]}")
        return None
    results = r.json().get("results", [])
    for page in results:
        props = page.get("properties", {})
        for pval in props.values():
            if pval.get("type") == "title":
                title_parts = pval.get("title", [])
                if title_parts:
                    title = title_parts[0].get("text", {}).get("content", "")
                    if any(k in title for k in ["TIS", "nTIS", "Tibial"]):
                        print(f"  찾음: '{title}' (ID: {page['id']})")
                        return page["id"]
    print("  자동 검색 실패 — 후보 목록:")
    for p in results[:5]:
        props = p.get("properties", {})
        for pval in props.values():
            if pval.get("type") == "title":
                title_parts = pval.get("title", [])
                if title_parts:
                    print(f"    - {title_parts[0].get('text',{}).get('content','')} ({p['id']})")
    return None


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
        print("    export NOTION_TOKEN=ntn_xxxx")
        sys.exit(1)

    r = requests.get(f"{API}/users/me", headers=H(tok))
    if r.status_code != 200:
        print(f"❌  인증 실패 ({r.status_code})")
        sys.exit(1)
    print(f"✅  인증 성공 — {r.json().get('name','?')}")

    print("\n🔍  nTIS 페이지 검색 중...")
    page_id = find_ntis_page(tok)

    if not page_id:
        page_id = input("\n페이지 ID를 직접 입력하세요 (32자리 UUID): ").strip().replace("-", "")
        if len(page_id) != 32:
            print("❌  유효하지 않은 페이지 ID")
            sys.exit(1)

    print(f"\n📝  3구역 분류 블록 추가 중 (페이지 ID: {page_id})...")
    blocks = inhibition_zone_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, page_id, blocks)

    print("\n✅  완료!")
    print(f"   GitHub Pages: {SITE_URL}")


if __name__ == "__main__":
    main()
