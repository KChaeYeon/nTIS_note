#!/usr/bin/env python3
"""
STEP 3: SNM / PTNS / TTNS 기존 기술 분석 — Notion 페이지에 추가
Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/add_step3_SNM_PTNS_TTNS_to_notion.py
"""
import os, sys, time, requests

API = "https://api.notion.com/v1"
VER = "2022-06-28"
NOTION_PAGE_ID = "37d6191a4fdc8035acb1d31b767ac08a"
GITHUB_URL = "https://kchaeyeon.github.io/nTIS_note/01_theory/11_PTNS_TTNS_SNM_technology_analysis/"

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


def step3_blocks():
    blocks = []

    # 헤더
    blocks.append(divider())
    blocks.append(h2("🏥 STEP 3: SNM / PTNS / TTNS 기존 기술 분석"))
    blocks.append(callout(
        "커리큘럼 3/13단계. OAB 신경조절 치료 3가지의 기전·임상 근거·한계를 선행논문 기반으로 분석하고 TIS 연구의 필요성 도출.",
        "📊", "yellow_background"
    ))
    blocks.append(para(rt("🔗 GitHub Pages: ", bold=True), rt(GITHUB_URL, link=GITHUB_URL)))
    blocks.append(para(rt("📄 로컬 파일: ", bold=True),
                       rt("docs/01_theory/11_PTNS_TTNS_SNM_technology_analysis.md", code=True)))

    # 전체 그림
    blocks.append(h3("전체 그림"))
    blocks.append(make_table(
        ["기술", "자극 방식", "침습도", "특징"],
        [
            ["SNM", "S3 신경근 직접 이식 자극", "높음 (수술)", "효과 강 / 침습·비용 문제"],
            ["PTNS", "발목 바늘 → 경골신경 → S2-S4", "중간 (바늘)", "안전 / 병원 의존 문제"],
            ["TTNS", "발목 전극 → 경골신경 → S2-S4", "없음", "비침습 / 깊이·선택성 문제"],
        ]
    ))
    blocks.append(callout(
        "공통 한계: 침습 or 자극 깊이 부족 or 수술 비용·합병증 → TIS: 비침습 + 깊은 표적화 + 선택성",
        "🎯", "green_background"
    ))

    # ── SNM ──
    blocks.append(h3("1. SNM (Sacral Neuromodulation) — 천수 신경 조절"))
    blocks.append(callout(
        "수술로 척수 S3 신경근 옆에 전극 이식 → 피하 배터리 → 지속적 전기 자극 (InterStim, Medtronic — FDA 승인 1997)",
        "🔧", "gray_background"
    ))
    blocks.append(bullet(rt("수술 Step 1: 시험 자극 1~2주 → 50% 이상 개선 확인")))
    blocks.append(bullet(rt("수술 Step 2: 영구 이식 (전신마취)")))
    blocks.append(bullet(rt("PTNS/TTNS 차이: 경골신경 간접 억제 vs S3 신경근 직접·지속 자극 → 효과 더 강")))

    blocks.append(para(rt("📄 핵심 근거: Bycroft et al. 2020 (Toxins) — 네트워크 메타분석", bold=True)))
    blocks.append(make_table(
        ["치료", "효능 순위", "부작용"],
        [
            ["BoNT-A (보툭스)", "1위 (최강)", "요폐 20~30%"],
            ["SNM", "2위", "수술 합병증"],
            ["PTNS", "3위", "최소 (안전성 1위)"],
            ["Sham", "최하", "-"],
        ]
    ))
    blocks.append(callout(
        "AUA 가이드라인: 3치료 모두 3차 치료 동등 권고. PTNS 안전성 최강 → TIS가 PTNS 안전성 + 더 나은 효능 = 판도 변화 가능성",
        "💡", "blue_background"
    ))

    blocks.append(toggle("SNM 한계 (4가지)", [
        bullet(rt("수술 필요: 전신마취·감염·이식 실패 위험")),
        bullet(rt("비용: ~3만 달러 (미국), 한국 보험 제한적")),
        bullet(rt("배터리 교체: 5~7년마다 재수술")),
        bullet(rt("장기 실패율: ~20~40% 효과 소실")),
    ]))

    # ── PTNS ──
    blocks.append(h3("2. PTNS (Percutaneous Tibial Nerve Stimulation)"))
    blocks.append(callout(
        "장비: Urgent PC (FDA 승인 2000년) / 34 gauge 침 → 내과 5 cm 위 삽입 → 경골신경 자극 / 20 Hz, 200 μs, 0.5~9 mA / 30분 × 주 1회 × 12주",
        "💉", "gray_background"
    ))

    blocks.append(para(rt("작용 기전 — 3단계 모델 (Al-Danakh et al. 2022)", bold=True)))
    blocks.append(make_table(
        ["단계", "경로", "기전"],
        [
            ["1단계 (말초→척수)", "경골신경 Aβ → S2-S4 후각", "방광 구심성 신호 억제 (Gate control 유사)"],
            ["2단계 (척수)", "GABAergic interneuron 활성화", "배뇨 척수 반사 억제 → DO 감소"],
            ["3단계 (중추)", "척수 → PMC → 대뇌 피질", "방광 과민성 하향 조절"],
        ]
    ))
    blocks.append(callout(
        "신경섬유 선택성: 10~20 Hz → Aβ 섬유 우선 활성화 (무통 억제) / >50 Hz → C섬유 활성화 위험",
        "⚡", "purple_background"
    ))

    blocks.append(para(rt("핵심 임상 근거 3대 RCT", bold=True)))
    blocks.append(toggle("① SUmiT Trial (Peters 2010, J Urol) — FDA 승인 근거", [
        bullet(rt("설계: PTNS vs Sham, n=220, 12주")),
        bullet(rt("치료 반응률: PTNS 54.5% vs Sham 20.9% (p<0.001)")),
        bullet(rt("빈뇨 감소: -2.4회/day")),
        bullet(rt("→ PTNS 효과의 핵심 근거 RCT")),
    ]))
    blocks.append(toggle("② OrBIT Trial (Finazzi-Agrò 2010)", [
        bullet(rt("설계: PTNS vs Tolterodine (항무스카린제) 비교")),
        bullet(rt("결과: 12주 후 반응률 차이 없음 → 동등 효능")),
        bullet(rt("부작용: PTNS 훨씬 적음 → 안전성 우위")),
    ]))
    blocks.append(toggle("③ STEP Study (MacDiarmid 2010) — 3년 추적", [
        bullet(rt("12주 치료 후 3년 장기 추적")),
        bullet(rt("월 1회 유지 치료 시 효과 유지율: 77%")),
        bullet(rt("→ 장기 유지 치료의 필요성 + 가능성 확인")),
    ]))
    blocks.append(bullet(rt("임상 반응률 범위: 60~71% (Al-Danakh 2022 종합)")))

    blocks.append(toggle("PTNS 한계 (4가지)", [
        bullet(rt("침습성: 바늘 삽입 → 감염·출혈·통증 / 항응고제 환자 불가")),
        bullet(rt("병원 의존: 주 1회 × 12주 + 유지 월 1회 내원")),
        bullet(rt("반응률 한계: ~45%는 효과 없음")),
        bullet(rt("파라미터 비표준화: 최적 주파수·전류 불명확 (Al-Danakh 2022 한계)")),
    ]))

    # ── TTNS ──
    blocks.append(h3("3. TTNS (Transcutaneous Tibial Nerve Stimulation)"))
    blocks.append(callout(
        "피부 표면 전극만으로 경골신경 자극 — 비침습, 자가 사용 가능 / 단점: 전류 손실, 선택성 낮음, FDA 미승인",
        "🩹", "gray_background"
    ))

    blocks.append(para(rt("핵심 임상 근거 4편", bold=True)))
    blocks.append(toggle("① PTNS vs TTNS RCT (2024, Basic and Clinical Neuroscience, n=44)", [
        bullet(rt("두 군 모두 OABSS, I-QOL 유의미 개선")),
        bullet(rt("군 간 차이: p>0.05 → 동등 효능")),
        bullet(rt("→ 비침습화 추세의 직접 근거")),
    ]))
    blocks.append(toggle("② TTNS + Mirabegron 병용 (2024, Scientific Reports, n=40)", [
        bullet(rt("병용군 > 단독군 (OAB-q bother, QoL 모두 유의미 우수, p<0.05)")),
        bullet(rt("이유: TTNS(중추 신경 회로) + Mirabegron(방광 근육 β3) 다른 기전 동시 타겟")),
        bullet(rt("추가 부작용 없음 → TIS + 약물 병용 연구 설계 근거")),
    ]))
    blocks.append(toggle("③ TTNS 자율신경 효과 (Muñoz et al. 2026, Neurourology and Urodynamics, n=20)", [
        bullet(rt("건강인 TTNS 10분 중 부교감 지표 증가: RMSSD↑, pNN50↑")),
        bullet(rt("→ 단순 방광 억제 넘어 자율신경계 전반 조절")),
        bullet(rt("→ 연구팀 ECG/HRV 장비로 Rat TIS 실험에 바로 적용 가능")),
        bullet(rt("→ 방광 효과 + 자율신경 효과 동시 측정 → 논문 contribution 확장")),
    ]))
    blocks.append(toggle("④ 최적 파라미터 메타분석 (13개 RCT, n=972)", [
        bullet(rt("10 Hz > 20 Hz 더 효과적")),
        bullet(rt("표준 펄스폭: 200 μs")),
        bullet(rt("→ Al-Danakh 2022 Aβ 섬유 선택 기전과 일치")),
    ]))

    blocks.append(toggle("TTNS 한계 (4가지)", [
        bullet(rt("자극 깊이: 피부/지방층 통과 → 전류 손실 → 재현성 낮음")),
        bullet(rt("선택성 부족: 주변 근육·피부 동시 자극 → 불쾌감")),
        bullet(rt("FDA 미승인: 대규모 표준화 RCT 부족")),
        bullet(rt("파라미터 비표준화: 연구 간 직접 비교 어려움")),
    ]))

    # 종합 비교
    blocks.append(h3("4. 세 기술 종합 비교"))
    blocks.append(make_table(
        ["", "SNM", "PTNS", "TTNS"],
        [
            ["침습도", "높음 (수술)", "중간 (바늘)", "없음"],
            ["자극 위치", "S3 신경근 (직접)", "경골신경 (간접)", "경골신경 (간접)"],
            ["효능 (NMA)", "높음 (2위)", "중간 (3위)", "중간~"],
            ["지속성", "지속 자극", "월 1회 유지", "월 1회 유지"],
            ["자가 사용", "가능 (리모컨)", "불가", "가능"],
            ["비용", "매우 높음", "중간", "낮음"],
            ["부작용", "높음 (수술)", "낮음", "최소"],
            ["FDA 승인", "✅ 1997", "✅ 2000", "❌"],
            ["자율신경 효과", "있음", "간접적", "✅ 확인 (2026)"],
        ]
    ))

    # 논문 요약
    blocks.append(h3("5. 논문 근거 요약"))
    blocks.append(make_table(
        ["논문", "설계", "핵심 결과", "우리 연구 연관성"],
        [
            ["Bycroft 2020 (NMA)", "NMA", "BoNT-A>SNM>PTNS / PTNS 안전 1위", "TIS 임상 위치 설정"],
            ["Peters 2010 (SUmiT)", "RCT n=220", "PTNS 54.5% vs Sham 20.9%", "PTNS 대조군 근거"],
            ["Finazzi-Agrò 2010 (OrBIT)", "RCT", "PTNS = Tolterodine", "신경조절이 약물 대안"],
            ["MacDiarmid 2010 (STEP)", "3년 추적", "유지율 77%", "장기 효과 기전"],
            ["Al-Danakh 2022", "리뷰", "Aβ→S2-S4→GABA 3단계", "TIS 동일 기전 적용"],
            ["2024 PTNS vs TTNS", "RCT n=44", "PTNS = TTNS (동등)", "비침습화 추세 근거"],
            ["2024 TTNS+Mirabegron", "RCT n=40", "병용 > 단독", "TIS+약물 병용 설계"],
            ["Muñoz 2026", "탐색 n=20", "TTNS → 부교감↑ (HRV)", "ECG/HRV 측정 근거"],
        ]
    ))

    # TIS 필요성
    blocks.append(h3("6. 공통 한계 → TIS의 필요성"))
    blocks.append(make_table(
        ["기술", "핵심 한계"],
        [
            ["SNM", "수술 + 비용 + 합병증"],
            ["PTNS", "침습(바늘) + 병원 의존"],
            ["TTNS", "자극 깊이 부족 + 선택성 낮음 + FDA 미승인"],
        ]
    ))
    blocks.append(callout(
        "TIS 해결책: 고주파 2쌍 간섭 → 피부 표면 안전 + 경골신경 깊이에서 저주파 envelope → 비침습 + 깊이 + 선택성 동시 달성",
        "🚀", "green_background"
    ))

    # 자기평가
    blocks.append(h3("자기평가 문항"))
    for q in [
        "SNM의 자극 위치가 PTNS/TTNS와 다른 점은? 왜 더 강한 효과를 내나?",
        "SUmiT Trial의 핵심 결과는? PTNS FDA 승인에서 이 연구의 의의는?",
        "PTNS와 TTNS 효과가 동등하다면 임상적으로 어떤 의미인가? (2024 RCT 기반)",
        "Bycroft 2020 NMA에서 3치료 효능·안전성 순위는? TIS가 노려야 할 위치는?",
        "TTNS가 자율신경계에 영향을 준다는 근거는? 우리 실험에 어떻게 적용하나?",
        "세 기술의 공통 한계와 TIS가 이론적으로 극복하는 방식을 설명하라.",
    ]:
        blocks.append(numbered(q))

    blocks.append(divider())
    blocks.append(para(rt("작성: 2026-06-21 | 커리큘럼 STEP 3/13 | 다음: STEP 4 — Temporal Interference Stimulation (TIS) 원리", color="gray")))

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

    print(f"\n📝  STEP 3 SNM/PTNS/TTNS 블록 추가 중...")
    blocks = step3_blocks()
    print(f"    총 {len(blocks)}개 블록")
    append_blocks(tok, NOTION_PAGE_ID, blocks)

    print("\n✅  완료!")
    print(f"   GitHub Pages: {GITHUB_URL}")


if __name__ == "__main__":
    main()
