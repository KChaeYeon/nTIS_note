#!/usr/bin/env python3
"""
nTIS_Tibial nerve Notion 페이지에 EM Physics Study Guide 섹션 추가
Usage:
  export NOTION_TOKEN=secret_xxxx
  python3 scripts/add_study_guide_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
SITE_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/08_EM_physics_TIS_study_guide/"

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

def toggle(title, children=None):
    return {"object": "block", "type": "toggle",
            "toggle": {"rich_text": [rt(title, bold=True)],
                       "children": children or []}}

def eq(expr):
    return {"object": "block", "type": "equation",
            "equation": {"expression": expr}}

def para(*rts):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": list(rts)}}


def find_ntis_page(tok):
    """nTIS_Tibial nerve 페이지 검색"""
    r = requests.post(f"{API}/search", headers=H(tok),
                      json={"query": "nTIS", "filter": {"value": "page", "property": "object"}})
    if r.status_code != 200:
        print(f"❌ 검색 실패: {r.status_code} {r.text[:300]}")
        return None
    results = r.json().get("results", [])
    for page in results:
        title = ""
        props = page.get("properties", {})
        for pname, pval in props.items():
            if pval.get("type") == "title":
                title_parts = pval.get("title", [])
                if title_parts:
                    title = title_parts[0].get("text", {}).get("content", "")
        if "TIS" in title or "nTIS" in title or "Tibial" in title:
            print(f"  찾음: '{title}' (ID: {page['id']})")
            return page["id"]
    print("  자동 검색 실패 — 수동으로 PID를 지정하세요")
    for p in results[:5]:
        props = p.get("properties", {})
        for pname, pval in props.items():
            if pval.get("type") == "title":
                title_parts = pval.get("title", [])
                if title_parts:
                    print(f"    - {title_parts[0].get('text',{}).get('content','')} ({p['id']})")
    return None


def study_guide_blocks():
    """8장 학습 가이드 요약 블록"""
    blocks = []

    blocks.append(divider())
    blocks.append(h2("📚 EM 물리 학습 가이드 — TIS 전기자극 완전 이해"))
    blocks.append(callout(
        "전기공학/생체의학공학 입문 (고등학생 수준) 학습 문서. "
        "8개 장으로 TIS 이론의 전기장 물리학 기초부터 TENS vs TIS 비교까지 정리.",
        "📖", "yellow_background"
    ))
    blocks.append(para(rt("🔗 GitHub Pages 배포: ", bold=True),
                       rt(SITE_URL, link=SITE_URL)))
    blocks.append(para(rt("📄 로컬 파일: ", bold=True),
                       rt("docs/01_theory/08_EM_physics_TIS_study_guide.md", code=True)))
    blocks.append(para(rt("📑 참고 논문: ", bold=True),
                       rt("Lee et al. 2021 (IEEE TBME) · Kim et al. 2023 (Appl. Sci.)")))

    # Chapter overview table
    blocks.append(h3("목차 (8장 구성)"))
    blocks.append(make_table(
        ["장", "제목", "핵심 개념"],
        [
            ["1장", "전기장 vs 자기장", "E-field, B-field, 2kHz에서 자기장 무시 이유, λ=150km"],
            ["2장", "Electroquasistatic 가정", "맥스웰 단순화, λ≫인체, E=-∇φ 유도"],
            ["3장", "φ·E·I 관계", "등고선 비유, E=-∇φ, 시뮬레이션↔실험 입력 차이"],
            ["4장", "Conductivity·Permittivity", "조직별 σ 표, 세포막 커패시터, 주파수 의존성"],
            ["5장", "Laplace 방정식", "∇·[(σ+jωε)∇φ]=0 유도, FEM 개념"],
            ["6장", "3D E-field 벡터", "Ex/Ey/Ez 성분, tibial nerve 해부학, Ez 선택 이유"],
            ["7장", "TIS 포락선 계산", "삼각함수 합차, 2·min(|Ez1|,|Ez2|) 증명, 숫자 예시"],
            ["8장", "TENS vs TIS 비교", "E-field 1.56배, 역치 1.67배, aBCF -17%, aVV +7%"],
        ]
    ))

    # Key equations
    blocks.append(h3("핵심 수식 (Lee et al. 2021 기준)"))
    blocks.append(eq(r"\mathbf{E} = -\nabla\phi \quad \text{(Electroquasistatic)}"))
    blocks.append(eq(r"\nabla \cdot \left[(\sigma + j\omega\varepsilon)\nabla\phi\right] = 0 \quad \text{(Laplace)}"))
    blocks.append(eq(r"Ez_{env} = 2\min(|Ez_1|, |Ez_2|) = \big||Ez_1+Ez_2| - |Ez_1-Ez_2|\big|"))

    # Key numerical results
    blocks.append(h3("핵심 수치 결과 (실험 근거)"))
    blocks.append(make_table(
        ["지표", "TENS", "TIS (ICT)", "배율/변화"],
        [
            ["Tibial nerve E-field", "0.62 V/m", "0.97 V/m", "1.56배↑"],
            ["자극 역치 (Rat, n=18)", "10.7±3.80 V", "6.4±1.5 V", "1.67배 낮음 (p<0.001)"],
            ["피부→신경 침투율", "20%", ">80%", "4배↑"],
            ["aBCF (방광 수축 빈도)", "기준", "−16.8%", "p<0.001 (n=19)"],
            ["aVV (배뇨량)", "기준", "+7.38%", "p<0.01 (n=15)"],
        ]
    ))

    blocks.append(callout(
        "이 문서는 연구팀 내 교육용·세미나용으로 제작되었으며, "
        "MkDocs 사이트에 배포되어 GitHub에서 최신 버전 확인 가능합니다.",
        "ℹ️", "gray_background"
    ))

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
        print("    ! export NOTION_TOKEN=secret_xxxx")
        sys.exit(1)

    # Auth check
    r = requests.get(f"{API}/users/me", headers=H(tok))
    if r.status_code != 200:
        print(f"❌  인증 실패 ({r.status_code})")
        sys.exit(1)
    print(f"✅  인증 성공 — {r.json().get('name','?')}")

    # Find target page
    print("\n🔍  nTIS_Tibial nerve 페이지 검색 중...")
    page_id = find_ntis_page(tok)

    if not page_id:
        # Try with manual PID from existing script
        page_id = input("\n페이지 ID를 직접 입력하세요 (32자리 UUID): ").strip().replace("-", "")
        if len(page_id) != 32:
            print("❌  유효하지 않은 페이지 ID")
            sys.exit(1)

    print(f"\n📝  학습 가이드 블록 추가 중 (페이지 ID: {page_id})...")
    blocks = study_guide_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, page_id, blocks)

    print("\n✅  완료!")
    print(f"   Notion 페이지를 열어 확인하세요.")
    print(f"   GitHub Pages: {SITE_URL}")


if __name__ == "__main__":
    main()
