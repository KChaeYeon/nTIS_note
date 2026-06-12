#!/usr/bin/env python3
"""
Notion Page Creator — nTIS Research
Creates:
  1. 📚 Background  : Theory, Tibial Nerve, Phrenic Nerve, all stim tech
  2. 📄 Paper DB    : Notion database with all 19 key papers

Usage:
  export NOTION_TOKEN=secret_xxxx
  python3 create_notion_pages.py
"""
import os, sys, time, json, requests

API   = "https://api.notion.com/v1"
VER   = "2022-06-28"
PID   = "37d6191a-4fdc-8035-acb1-d31b767ac08a"   # parent page


# ─────────────────────── helpers ───────────────────────

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

def para(*rts):
    return {"object":"block","type":"paragraph",
            "paragraph":{"rich_text":list(rts)}}

def h1(text):
    return {"object":"block","type":"heading_1",
            "heading_1":{"rich_text":[rt(text)],"is_toggleable":False}}

def h2(text):
    return {"object":"block","type":"heading_2",
            "heading_2":{"rich_text":[rt(text)],"is_toggleable":False}}

def h3(text):
    return {"object":"block","type":"heading_3",
            "heading_3":{"rich_text":[rt(text)],"is_toggleable":False}}

def bullet(*rts):
    return {"object":"block","type":"bulleted_list_item",
            "bulleted_list_item":{"rich_text":list(rts)}}

def callout(text, emoji="💡", color="blue_background"):
    return {"object":"block","type":"callout",
            "callout":{"rich_text":[rt(text)],
                       "icon":{"type":"emoji","emoji":emoji},
                       "color":color}}

def divider():
    return {"object":"block","type":"divider","divider":{}}

def eq(expr):
    return {"object":"block","type":"equation",
            "equation":{"expression":expr}}

def toggle(title_rts, children=None):
    return {"object":"block","type":"toggle",
            "toggle":{"rich_text": title_rts if isinstance(title_rts, list)
                       else [rt(title_rts, bold=True)],
                      "children": children or []}}

def make_table(headers, rows):
    n = len(headers)
    def cell(txt_):
        return [rt(str(txt_))]
    hr = {"object":"block","type":"table_row",
          "table_row":{"cells":[[rt(h, bold=True)] for h in headers]}}
    drs = [{"object":"block","type":"table_row",
            "table_row":{"cells":[cell(c) for c in row]}} for row in rows]
    return {"object":"block","type":"table",
            "table":{"table_width":n,"has_column_header":True,
                     "has_row_header":False,"children":[hr]+drs}}

def numbered(*rts):
    return {"object":"block","type":"numbered_list_item",
            "numbered_list_item":{"rich_text":list(rts)}}


# ─────────────────────── API calls ───────────────────────

def create_page(tok, parent_id, title, emoji="📚"):
    body = {"parent":{"type":"page_id","page_id":parent_id},
            "icon":{"type":"emoji","emoji":emoji},
            "properties":{"title":{"title":[{"text":{"content":title}}]}}}
    r = requests.post(f"{API}/pages", headers=H(tok), json=body)
    if r.status_code not in (200,201):
        print(f"  ❌ create_page: {r.status_code} {r.text[:400]}")
        sys.exit(1)
    return r.json()["id"]

def append_blocks(tok, page_id, blocks, chunk=90):
    for i in range(0, len(blocks), chunk):
        c = blocks[i:i+chunk]
        r = requests.patch(f"{API}/blocks/{page_id}/children",
                           headers=H(tok), json={"children":c})
        if r.status_code not in (200,201):
            print(f"  ⚠️  append chunk {i}: {r.status_code} {r.text[:300]}")
        else:
            print(f"  ✅ blocks {i+1}–{i+len(c)}")
        time.sleep(0.35)

def create_database(tok, parent_id, title, emoji="📄"):
    body = {
        "parent":{"type":"page_id","page_id":parent_id},
        "icon":{"type":"emoji","emoji":emoji},
        "title":[{"type":"text","text":{"content":title}}],
        "properties":{
            "Title":{"title":{}},
            "Authors":{"rich_text":{}},
            "Year":{"number":{"format":"number"}},
            "Journal":{"select":{"options":[]}},
            "DOI":{"url":{}},
            "Stars":{"select":{"options":[
                {"name":"⭐⭐⭐⭐⭐","color":"yellow"},
                {"name":"⭐⭐⭐⭐","color":"orange"},
                {"name":"⭐⭐⭐","color":"gray"},
            ]}},
            "Category":{"multi_select":{"options":[
                {"name":"TIS","color":"blue"},
                {"name":"TNS","color":"green"},
                {"name":"Phrenic","color":"purple"},
                {"name":"FEM","color":"orange"},
                {"name":"Clinical","color":"red"},
                {"name":"OAB","color":"yellow"},
                {"name":"Mechanism","color":"pink"},
                {"name":"Meta-analysis","color":"gray"},
                {"name":"Anatomy","color":"brown"},
                {"name":"Glymphatic","color":"default"},
            ]}},
            "Summary":{"rich_text":{}},
            "Gap":{"rich_text":{}},
        }
    }
    r = requests.post(f"{API}/databases", headers=H(tok), json=body)
    if r.status_code not in (200,201):
        print(f"  ❌ create_database: {r.status_code} {r.text[:400]}")
        sys.exit(1)
    return r.json()["id"]

def add_paper(tok, db_id, p):
    doi_val = p["doi"]
    if doi_val and not doi_val.startswith("http"):
        doi_val = f"https://doi.org/{doi_val}"
    props = {
        "Title":   {"title":[{"text":{"content":p["title"]}}]},
        "Authors": {"rich_text":[{"text":{"content":p["authors"]}}]},
        "Year":    {"number": p["year"]},
        "Journal": {"select":{"name": p["journal"]}},
        "Stars":   {"select":{"name": p["stars"]}},
        "Summary": {"rich_text":[{"text":{"content":p["summary"]}}]},
        "Gap":     {"rich_text":[{"text":{"content":p["gap"]}}]},
        "Category":{"multi_select":[{"name":c} for c in p["cats"]]},
    }
    if doi_val:
        props["DOI"] = {"url": doi_val}
    r = requests.post(f"{API}/pages", headers=H(tok),
                      json={"parent":{"database_id":db_id},"properties":props})
    ok = r.status_code in (200,201)
    print(f"  {'✅' if ok else '⚠️ '} {p['title'][:65]}")
    if not ok:
        print(f"     → {r.status_code} {r.text[:200]}")
    time.sleep(0.25)


# ─────────────────────── Background page content ───────────────────────

def bg_blocks():
    B = []

    # ── intro callout ──
    B.append(callout(
        "nTIS 연구 배경 지식 완전 정리 | 전기 자극 기술 전반 → 경골신경 → 횡격막신경 → TIS 응용까지. "
        "최종 업데이트: 2026-06-12 (4-에이전트 통합)",
        "📌", "yellow_background"))
    B.append(divider())

    # ══════════════════════════════════════════════
    # SECTION 1: Technology comparison table
    # ══════════════════════════════════════════════
    B.append(h1("⚡  전기 자극 기술 전체 비교"))
    B.append(make_table(
        ["기술", "침습성", "심부 도달", "선택성", "FDA 현황", "주요 적응증"],
        [
            ["tDCS",       "비침습",        "낮음 (~1 cm)", "낮음",  "연구용",       "인지·우울·재활"],
            ["TENS",       "비침습",        "중간",         "낮음",  "✅ 다수",       "통증 관리"],
            ["PTNS",       "최소침습 (바늘)","높음 (~1.5 cm)","높음 (Aβ)","✅ 2000", "OAB (3차치료)"],
            ["TTNS",       "비침습",        "중간",         "중간",  "일부",         "OAB (PTNS 대안)"],
            ["TIS",        "비침습",        "높음 (이론)",  "높음 (이론)","❌ 연구중", "심부 신경 자극"],
            ["n-phase TIS","비침습",        "높음+",        "더 높음","❌ 연구중",    "초점성·방향 제어"],
            ["SNM",        "침습 (수술)",   "최고",         "최고",  "✅ 1997",      "OAB / FI / 요폐"],
            ["eCoin",      "이식 (피하)",   "최고",         "최고",  "✅ PMA 2022",  "OAB (이식형 TNS)"],
            ["Revi (RENOVA)","이식 (피하)", "최고",         "최고",  "✅ De Novo 2023","OAB (무배터리)"],
            ["Altaviva",   "이식 (충전식)", "최고",         "최고",  "✅ 2025.09",   "OAB (Medtronic)"],
        ]
    ))
    B.append(divider())

    # ══════════════════════════════════════════════
    # SECTION 2: Each technology details (toggles)
    # ══════════════════════════════════════════════
    B.append(h1("🔬  각 기술 상세 설명"))

    # ── tDCS ──
    B.append(toggle("🧠  tDCS — 경두개 직류 자극 (Transcranial Direct Current Stimulation)", [
        callout("비침습 뇌 자극. 두 전극 사이 0.5~2 mA 직류 → 피질 흥분성 미세 조절.", "🔑","blue_background"),
        bullet(rt("원리: Anodal (+) → 막전위 소폭 상승 → 흥분성↑  /  Cathodal (−) → 흥분성↓")),
        bullet(rt("전극: 5~35 cm² 스폰지 패드, 두피 배치")),
        bullet(rt("주파수: 0 Hz (직류)")),
        bullet(rt("세션: 20~30분, 1~2 mA")),
        bullet(rt("장점: 매우 안전, 간편, 저비용")),
        bullet(rt("단점: 효과 재현성 낮음, 개인 간 변동 큼, 심부 도달 불가 (~1 cm)")),
        bullet(rt("임상 근거: 우울증 RCT 다수, 운동 재활, 인지 기능 향상 연구")),
    ]))

    # ── TENS ──
    B.append(toggle("⚡  TENS — 경피신경전기자극 (Transcutaneous Electrical Nerve Stimulation)", [
        bullet(rt("원리: Gate Control Theory — Aβ 활성화로 척수 후각에서 통증 신호 차단")),
        bullet(rt("고주파 TENS (80~150 Hz): 통증 관문 제어, 빠른 효과")),
        bullet(rt("저주파 TENS (1~10 Hz): 내인성 아편유사물질(엔돌핀) 유리")),
        bullet(rt("FDA: 다수의 510(k) 허가 기기 (1970년대부터)")),
        bullet(rt("한계: 심부 도달 제한, 전신 통증 조절에는 효과 제한적")),
    ]))

    # ── PTNS ──
    B.append(toggle("🦵  PTNS — 경피적 경골신경 자극 (Percutaneous TNS)", [
        callout("OAB 3차 치료 금표준. FDA 510(k) K001576 (2000). AUA 2024 Grade A Evidence.", "⭐","yellow_background"),
        h3("표준 파라미터"),
        make_table(
            ["파라미터","값","근거"],
            [
                ["주파수","20 Hz","표준 — 단, 2025 메타분석에서 10 Hz 우월 시사"],
                ["펄스폭","200 μs","Aβ chronaxie(~100 μs) × 2 → 선택적 자극"],
                ["강도","0~9 mA","운동 역치 기준 개인화 (발가락 굴곡 반응)"],
                ["세션","30분/회",""],
                ["빈도","주 1회 × 12주","유도기"],
                ["유지","월 1회 × 무기한","STEP 3년: 77% 반응 유지"],
            ]
        ),
        h3("핵심 임상 데이터"),
        bullet(rt("SUmiT 2010: PTNS 54.5% vs sham 20.9% (p<0.001)", bold=True)),
        bullet(rt("OrBIT 2010: PTNS 80% vs Tolterodine 55% (12주, p<0.01)")),
        bullet(rt("STEP 2013: 3년 77% 반응 유지 (월 1회 유지치료)")),
        bullet(rt("기기: Urgent-PC (Laborie Medical Technologies)")),
        bullet(rt("바늘: 34G, 내과 상방 5 cm, 60° 상향, 2~4 cm 삽입")),
    ]))

    # ── TTNS ──
    B.append(toggle("🩹  TTNS — 경피적 경골신경 자극 (비침습, Transcutaneous TNS)", [
        bullet(rt("표면 전극 내과 상방 5 cm (PTNS와 동일 위치) + 발꿈치 기준 전극")),
        bullet(rt("파라미터: 20 Hz / 200~300 μs / 10~30 mA / 운동 역치 기준")),
        bullet(rt("Bertolo 2021 메타분석(142명): TTNS = PTNS — 4개 OAB 지표 모두 유의 차이 없음")),
        bullet(rt("⚠️  2025 메타분석(972명, 13 RCTs): 10 Hz > 20 Hz 유의 (MD=−1.24, p<0.05)", bold=True)),
        bullet(rt("Booth 2018 (629명): TTNS vs sham ICIQ-UI SF −3.79 (p=0.0003)")),
        bullet(rt("장점: 바늘 없음, 합병증 0건")),
        bullet(rt("한계: 전극 위치 재현성 낮음, 피부 임피던스 장벽, 비선택적 자극")),
        bullet(rt("FDA 승인 웨어러블: Vivally System (Avation Medical)")),
    ]))

    # ── TIS ──
    B.append(toggle("🌊  TIS — 시간 간섭 전기 자극 (Temporal Interference Stimulation)", [
        callout("Grossman et al. 2017 (Cell) 제안. 두 고주파 전류 교차 → 심부 선택적 저주파 envelope 생성.", "🔑","blue_background"),
        h3("작동 원리 — AM 라디오 비유"),
        bullet(rt("두 전극 쌍에 각각 f₁, f₂ (Hz) 고주파 전류 인가 (예: f₁=2000 Hz, f₂=2020 Hz)")),
        bullet(rt("조직 내 교차점: 맥놀이(beat) 형성 → Δf = |f₁−f₂| = 20 Hz")),
        bullet(rt("표면: 2000 Hz 고주파만 → 뉴런 무반응 (빠름)")),
        bullet(rt("심부 교차점: 20 Hz envelope → 뉴런 반응 → 선택적 심부 자극")),
        h3("수식"),
        eq(r"I_{\text{total}} = I_1 + I_2 = 2A \cdot \underbrace{\cos(\pi \Delta f \cdot t)}_{\text{envelope (뉴런 반응)}} \cdot \underbrace{\cos(2\pi f_{\text{avg}} \cdot t)}_{\text{carrier (뉴런 무반응)}}"),
        h3("뇌 TIS vs. 말초신경 TIS — 패러다임 차이 (Budde 2023)"),
        make_table(
            ["구분","뇌 TIS","말초신경 TIS"],
            [
                ["막 시간 상수 τ","10~100 ms","0.05~0.2 ms"],
                ["캐리어(2 kHz) 반응","평균화 → 무반응","직접 활성화 가능"],
                ["활성화 기전","Envelope extraction","Instantaneous peak amplitude"],
                ["비선형 기여","주 메커니즘","<6% (무시 가능)"],
                ["설계 원칙","Δf 제어","합산 파형 피크 전기장 제어"],
                ["근거","Grossman 2017 (Cell)","Budde 2023 (JNE) / Opancar 2025 (Nature Comm)"],
            ]
        ),
        h3("현재 상태"),
        bullet(rt("FDA/CE 승인 TIS 의료기기: 전무")),
        bullet(rt("연구용 기기: TI Solutions AG (TIBS-R, CHF 500/월 임대), Soterix Medical (HD-IFS PRO)")),
        bullet(rt("현재 TIS 임상 6건 (2025-2026): 전부 뇌 표적 (파킨슨, 진전, 의식장애)")),
        bullet(rt("TIS + 경골신경 + OAB 인체 임상: 전 세계 0건 ← 세계 최초 기회", bold=True)),
    ]))

    # ── n-phase TIS ──
    B.append(toggle("🔀  n-phase TIS — 다전극 확장형 TIS", [
        para(rt("표준 TIS(2쌍, 4전극)를 n쌍으로 확장. 초점성과 방향성 제어를 크게 향상.")),
        h3("수식"),
        eq(r"I_{\text{total}}(\mathbf{r},t) = \sum_{k=1}^{n} A_k(\mathbf{r}) \cos\!\bigl(2\pi f_k t + \phi_k\bigr)"),
        bullet(rt("n=2: 표준 TIS (4전극, f₁≠f₂)")),
        bullet(rt("n=3: 3쌍 6전극, 120° 위상차 → 3차원 초점성 향상")),
        bullet(rt("Kim 2023 (Applied Sciences): FEM에서 n-phase 전극 최적화 → focality ratio 2~3배 향상")),
        bullet(rt("전기장 벡터 방향: 표적에서 두 쌍이 평행·동방향 → envelope 변조 깊이 최대")),
        bullet(rt("직교 배치 → 변조 없음 → 전극 배치 설계가 매우 중요")),
        bullet(rt("하드웨어: 전류 채널 증가, 정밀 동기화 필요 → 복잡도 증가")),
    ]))

    B.append(divider())

    # ══════════════════════════════════════════════
    # SECTION 3: Tibial Nerve
    # ══════════════════════════════════════════════
    B.append(h1("🦵  경골신경 (Tibial Nerve)"))

    B.append(toggle("📐  해부학 — 기원, 경로, Tarsal Tunnel", [
        h3("신경 기원 및 하행 경로"),
        para(rt("L4 / L5 / S1 / S2 / S3 → 요천추 신경총 → 좌골신경 → 슬와부 분기 → 경골신경")),
        make_table(
            ["구간","해부학적 위치","중요도"],
            [
                ["슬와부","슬와혈관 가장 표층(후방)","분기점"],
                ["하퇴 근위","가자미근 아치 통과",""],
                ["하퇴 중하부","심부후방구획 하행, 후경골동맥과 동행",""],
                ["발목 Tarsal Tunnel","내과(medial malleolus) 후방 통과","⭐ PTNS/TIS 자극 포인트"],
                ["족저부","내측·외측 족저신경으로 분지",""],
            ]
        ),
        h3("Tarsal Tunnel 내 구조 — Tom, Dick, And Very Nervous Harry"),
        make_table(
            ["약자","구조물","TIS/PTNS 관련성"],
            [
                ["T","후경골근건 (Tibialis Posterior)","전방 경계"],
                ["D","장지굴근건 (flexor Digitorum longus)","인접"],
                ["A","후경골동맥 (tibial Artery)","신경 0.3~0.8 mm 인접 → 바늘 위험"],
                ["V","후경골정맥 (Vein ×2)","인접"],
                ["N","경골신경 (tibial Nerve)","⭐ TIS/PTNS 표적"],
                ["H","장무지굴근건 (flexor Hallucis longus)","후방 경계"],
            ]
        ),
        bullet(rt("분기 패턴: 88% 족근관 내에서 내측/외측 족저신경으로 분기")),
        bullet(rt("신경 섬유: Aβ(8~12 μm, 방광 억제) / Aδ / C fiber")),
        bullet(rt("방광 억제 관련 Aβ: 족저 감각 fascicle에 집중 (i²CS 2025)")),
    ]))

    B.append(toggle("📍  PTNS 표준 자극 포인트 (정밀 해부)", [
        bullet(rt("위치: 내과(medial malleolus) 상방 5 cm, 경골 후연 내측 2 cm")),
        bullet(rt("바늘 각도: 60° 상향 / 삽입 깊이: 2~4 cm")),
        make_table(
            ["측정 항목","평균","범위","비고"],
            [
                ["피부 → 신경 깊이","1.35 cm","0.8~2.3 cm","체형 따라 큰 변동"],
                ["신경 단면적(CSA)","15 mm²","10~22 mm²","굵기 개인차 큼"],
                ["신경 → 동맥 거리","0.5 mm","0.3~0.8 mm","혈관 손상 주의"],
                ["여성 평균 깊이","0.86 cm","—","더 표층"],
                ["남성 평균 깊이","2.42 cm","—","더 심층"],
            ]
        ),
        bullet(rt("초음파 가이드: 신경 인접 성공률 OR 3.8배 향상 (p<0.01)")),
        bullet(rt("표준 촉진 기반: 바늘-신경 거리 평균 2.1 cm → 실제로 신경에서 멀리 삽입되는 경우 多")),
    ]))

    B.append(toggle("🧠  방광 조절 기전 — 경골신경 → OAB 억제 경로", [
        h3("신경 경로"),
        bullet(rt("경골신경 Aβ 활성화 → 천수 후각(S2-S4) GABAergic 억제 인터뉴런")),
        bullet(rt("→ 천수 부교감핵(SPN) 억제 → 배뇨근 과활성 억제 → OAB 증상 개선")),
        h3("핵심 기전 연구"),
        bullet(rt("McGee 2018: S2 척수 제V~VII층. 방광 발화 40~50% 억제. GABA-A 수용체 관여 직접 증명")),
        bullet(rt("Lyon 2016 역설: PMC 직접 유발 방광 수축은 억제 못함 → 척수 수준 비정상 감작만 억제")),
        bullet(rt("핵심 표적: C-fiber 과감작 억제 + GABAergic 척수 억제 인터뉴런 활성화")),
        h3("OAB 역학"),
        make_table(
            ["항목","수치"],
            [
                ["전 세계 유병률","11.8% (EpiLUTS 2011)"],
                ["전 세계 환자","약 5억 명"],
                ["OAB 시장 규모","$4.1B (2025) → $6.45B (2032)"],
                ["약물 중단 비율","89% 경험 (효능·부작용·비용)"],
                ["1년 약물 순응률","최저 35%"],
                ["AUA 2024 PTNS 등급","Grade A (기존 C에서 상향)"],
            ]
        ),
    ]))

    B.append(toggle("🔭  TIS를 이용한 경골신경 자극 — 현황 및 기회", [
        callout("세계 최초 기회: TIS + 경골신경 + OAB 인체 임상시험 전 세계 0건!", "⚡","red_background"),
        h3("선행 연구"),
        bullet(rt("Kim et al. 2023 (Applied Sciences 13(4):2430): 유일한 경골신경 TIS FEM 연구")),
        bullet(rt("  → 인체 발목 MRI 7-조직 모델 + 전극 최적화 → focality ratio 2~3배 향상")),
        bullet(rt("  → In vivo 검증 전무 → 가장 큰 한계이자 연구 기회")),
        h3("Budde 2023 패러다임이 경골신경 TIS 설계에 미치는 영향"),
        bullet(rt("말초신경 TIS 활성화 = envelope extraction이 아닌 instantaneous peak amplitude")),
        bullet(rt("→ FEM 설계 시 envelope 전기장뿐만 아니라 캐리어 피크 전기장도 계산 필요")),
        bullet(rt("→ 전도 차단(conduction block) 위험: TIS 교차 영역 외 단일 캐리어 강도 모니터링 필수")),
        h3("Rat vs. 인체 스케일"),
        make_table(
            ["항목","Rat 발목","인체 발목","시사점"],
            [
                ["발목 직경","~35 mm","~70 mm","2배 차이"],
                ["전극-신경 거리","5~8 mm","10~15 mm","2배 차이"],
                ["동등 효과 전류","기준","3~4배 증가","인체 적용 시 스케일업 필요"],
            ]
        ),
        bullet(rt("Gate condition: TI-ratio(신경 전기장 / 비표적) > 2.0 권장")),
    ]))

    B.append(toggle("🏭  FDA 승인 이식형 경골신경 자극 기기 (2026 기준)", [
        make_table(
            ["기기","회사","FDA","특징","최신 임상 결과"],
            [
                ["Urgent-PC","Laborie","510(k) 2000","PTNS 바늘 원조","SUmiT: 54.5% 반응"],
                ["eCoin","Valencia Tech","PMA 2022.03","동전형 자동 피하","2년: 78% (>50% UUI 감소)"],
                ["Revi (RENOVA)","BlueWind","De Novo 2023.08","배터리 없는 피하 리드","12개월: 82%, 완전건조 49.6%"],
                ["Altaviva","Medtronic","FDA 2025.09.19","충전식 15년 배터리","TITAN 2 RCT 근거"],
            ]
        ),
        bullet(rt("OAB 이식형 TNS 시장: $50~55M (2025) → $87~104M (2033)")),
        bullet(rt("Medtronic CEO: Altaviva = 'billion-dollar market opportunity' (JPM 2026.01)")),
    ]))

    B.append(divider())

    # ══════════════════════════════════════════════
    # SECTION 4: Phrenic Nerve
    # ══════════════════════════════════════════════
    B.append(h1("💨  횡격막신경 (Phrenic Nerve)"))

    B.append(toggle("📐  해부학 — 기원, 경로, 임상 접근", [
        para(rt("C3, C4, C5 → 경추 신경총 → 흉강 내 하행 → 횡격막 운동 지배")),
        make_table(
            ["구간","경로","임상 접근성"],
            [
                ["경부","흉쇄유돌근 아래, 전사각근 표면","피부 → 신경 ~1~2 cm (표층)"],
                ["흉강 상부","SVC·심낭 사이 하행","이식 페이싱 접근 위치"],
                ["횡격막","횡격막 중심건 부근 분지","운동 종판"],
            ]
        ),
        bullet(rt("직경: 약 2~3 mm (경골신경 ~6 mm 대비 얇음)")),
        bullet(rt("기능: 횡격막 수축 → 흡기 → 호흡의 약 70% 담당")),
        bullet(rt("자율신경 연결: C-fiber → 호흡 리듬 조절, HRV 관련")),
        bullet(rt("이식형 페이싱: 척수 손상(C5 이상) 환자 인공호흡 대체 — 수십 년 임상 역사")),
    ]))

    B.append(toggle("🌊  TIS 적용 및 글림프 시스템 연관성", [
        callout("현재 어떤 연구팀도 횡격막신경 TIS로 글림프 순환을 조절하려 시도하지 않음 — 세계 최초 기회", "🌟","green_background"),
        h3("횡격막 → 글림프 연결 근거"),
        bullet(rt("Dreha-Kulaczewski 2017 (Sci Rep): 호흡이 척수 CSF 흐름의 주 구동력")),
        bullet(rt("Sunshine 2021 (Nature Comm Bio): 흡기 시 림프 흐름 최대 → 호흡 주도 글림프 순환")),
        bullet(rt("→ TIS로 횡격막신경 자극 → 호흡 패턴/강도 조절 → CSF 및 글림프 순환 영향 가능")),
        h3("Lab 내 시너지 (Student A)"),
        bullet(rt("Student A: 침습적 횡격막 cuff + ICG 림프 측정 진행 중")),
        bullet(rt("→ 비침습 TIS 자극 vs. 침습적 cuff 직접 자극 직접 비교 가능")),
        bullet(rt("→ ICG로 글림프 순환 변화 정량 측정 가능 → 최고 수준 검증 플랫폼")),
        h3("FINES 평가 결과"),
        make_table(
            ["후보","FINES 점수","잠재 저널","상태"],
            [
                ["비침습 횡격막 TIS → Glymphatic","4.85","Nature BME","최우선 후보"],
                ["ECG/RSP closed-loop 횡격막 TIS","4.35","JNE","2위"],
                ["경골신경 TIS Rat OAB","4.35","Brain Stimulation","3위"],
            ]
        ),
    ]))

    B.append(divider())

    # ══════════════════════════════════════════════
    # SECTION 5: Prior Research — TIS + peripheral
    # ══════════════════════════════════════════════
    B.append(h1("📑  선행 논문 — TIS × 경골/횡격막신경"))

    B.append(toggle("🦵  TIS × 경골신경 (Tibial Nerve)", [
        h3("Kim et al. 2023 — 유일한 직접 연구"),
        bullet(rt("제목: FEM-based Electrode Optimization for Tibial Nerve TIS")),
        bullet(rt("저널: Applied Sciences (MDPI) 13(4):2430")),
        bullet(rt("DOI: 10.3390/app13042430")),
        bullet(rt("내용: 인체 MRI 기반 발목 7-조직 FEM 모델. 전극 위치 최적화. Focality ratio 2~3배 향상")),
        bullet(rt("한계: In silico만 — in vivo 검증 전무")),
        bullet(rt("의의: 경골신경 TIS 연구의 유일한 선행 FEM 근거 → 우리 연구의 직접 출발점", bold=True)),
        h3("Botzanowski et al. 2022 — 말초신경 TIS 타당성"),
        bullet(rt("저널: Advanced Healthcare Materials 11(17):2200075")),
        bullet(rt("DOI: 10.1002/adhm.202200075")),
        bullet(rt("내용: 쥐 in vivo TIS 역치 350 μA (TTNS 대비 매우 낮음). 전기장 집중 깊이 ~7 mm")),
        bullet(rt("의의: 말초신경 TIS 비침습 타당성 최초 직접 증명 → 경골신경 적용 근거")),
        h3("Budde et al. 2023 — 패러다임 전환"),
        bullet(rt("저널: Journal of Neural Engineering 20(2):026041")),
        bullet(rt("DOI: 10.1088/1741-2552/acc6f1")),
        bullet(rt("내용: 쥐 좌골신경 30마리. envelope extraction이 아닌 instantaneous peak amplitude")),
        bullet(rt("의의: 말초신경 TIS 메커니즘 근본 재정의 → 경골신경 TIS 설계 원칙 변경 필요", bold=True)),
    ]))

    B.append(toggle("💨  TIS × 횡격막신경 / 호흡 관련", [
        callout("현재 TIS + 횡격막신경 직접 연구 전무. 아래는 배경 근거 논문들.", "ℹ️","gray_background"),
        h3("Dreha-Kulaczewski et al. 2017"),
        bullet(rt("저널: Scientific Reports")),
        bullet(rt("DOI: 10.1038/s41598-017-01813-3")),
        bullet(rt("내용: fMRI 기반 척수 CSF 흐름 측정. 흡기 시 CSF 흐름 증가 → 호흡이 CSF 흐름 주 구동력")),
        h3("Sunshine et al. 2021"),
        bullet(rt("저널: Nature Communications Biology")),
        bullet(rt("DOI: 10.1038/s42003-021-01813-0")),
        bullet(rt("내용: 횡격막 이식 전극 + ICG. 흡기 위상에서 림프 흐름 최대 → 호흡 주도 글림프 근거")),
        h3("i²CS 2025 — First-in-Human 경골신경 fascicle 선택성"),
        bullet(rt("저널: Nature Communications 2025")),
        bullet(rt("내용: 경골신경 fascicle 선택적 자극으로 방광 억제 효과 차별화 → 방광 관련 Aβ = 족저 감각 fascicle")),
        bullet(rt("의의: 방향 TIS로 특정 fascicle 활성화 가능성 → n-phase TIS의 핵심 동기")),
    ]))

    B.append(divider())

    # ══════════════════════════════════════════════
    # SECTION 6: Research Gaps
    # ══════════════════════════════════════════════
    B.append(h1("🔭  연구 갭 및 기회"))
    B.append(make_table(
        ["갭 ID","내용","중요도","해결 방법","관련 논문"],
        [
            ["G-TN1","TIS + 경골신경 in vivo 검증 전무","★★★★★","Rat OAB 모델 실험","Kim 2023, Botzanowski 2022"],
            ["G-TN2","TIS vs. PTNS 직접 비교 없음","★★★★★","동물 모델 head-to-head","—"],
            ["G-TN3","Budde 2023 경골신경 특화 검증 없음","★★★★★","경골신경 in vivo 기전","Budde 2023, Opancar 2025"],
            ["G-PH1","횡격막신경 TIS 비침습 검증 없음","★★★★★","경부 4전극 TIS 프로토콜","Grossman 2017"],
            ["G-PH2","횡격막 TIS → 글림프 순환 연구 없음","★★★★★","ICG + CSF 측정","Sunshine 2021"],
            ["CG-4","말초신경 TIS 기전 논쟁 미해결","★★★★★","독립 재현 + 경골신경 적용","Budde 2023, Opancar 2025"],
        ]
    ))

    return B


# ─────────────────────── Paper DB entries ───────────────────────

PAPERS = [
    dict(title="Noninvasive Deep Brain Stimulation via Temporally Interfering Electric Fields",
         authors="Grossman N, Bono D, Dobbins C, et al. (MIT)",
         year=2017, journal="Cell",
         doi="10.1016/j.cell.2017.05.024",
         cats=["TIS"], stars="⭐⭐⭐⭐⭐",
         summary="TIS 기반 논문. 2 kHz 캐리어 + Δf=10 Hz로 마우스 해마 심부 자극 성공. 중간 조직 활성화 없음 확인.",
         gap="모든 TIS 연구의 출발점"),

    dict(title="FEM Optimization of Electrode Placement for Tibial Nerve TIS",
         authors="Kim E, Ye E, Lee J, et al.",
         year=2023, journal="Applied Sciences",
         doi="10.3390/app13042430",
         cats=["TIS","FEM","TNS"], stars="⭐⭐⭐⭐⭐",
         summary="유일한 경골신경 TIS FEM 연구. 인체 발목 MRI 7-조직 모델. 전극 최적화로 focality ratio 2~3배 향상. In vivo 검증 없음.",
         gap="G-TN1, G-TN2"),

    dict(title="Peripheral Nerve Activation by TIS is Not Envelope Extraction",
         authors="Budde RB, Williams MT, Irazoqui PP (Johns Hopkins)",
         year=2023, journal="Journal of Neural Engineering",
         doi="10.1088/1741-2552/acc6f1",
         cats=["TIS","Mechanism"], stars="⭐⭐⭐⭐⭐",
         summary="패러다임 전환. Rat 좌골신경 30마리. 말초신경은 instantaneous peak amplitude로 반응. 비선형 기여 <6%. τ_m=0.05~0.2 ms.",
         gap="CG-4, G-TN3"),

    dict(title="Reconfirmation: Peripheral Nerve TIS ≠ Envelope Extraction",
         authors="Opancar et al.",
         year=2025, journal="Nature Communications",
         doi="",
         cats=["TIS","Mechanism"], stars="⭐⭐⭐⭐⭐",
         summary="Budde 2023 독립 재현. 포유류 말초신경 in vivo. TIS ≠ envelope extraction 확정.",
         gap="CG-4"),

    dict(title="Noninvasive Peripheral Nerve Activation via TIS (350 μA threshold)",
         authors="Botzanowski B, et al.",
         year=2022, journal="Advanced Healthcare Materials",
         doi="10.1002/adhm.202200075",
         cats=["TIS","Mechanism"], stars="⭐⭐⭐⭐⭐",
         summary="In vivo TIS 역치 350 μA. 전기장 집중 깊이 ~7 mm. 말초신경 TIS 비침습 타당성 최초 직접 증명.",
         gap="G-TN1"),

    dict(title="Analytical Model of TIS: Conduction Block Risk",
         authors="Mirzakhalili E, et al.",
         year=2020, journal="Cell Systems",
         doi="10.1016/j.cels.2020.10.001",
         cats=["TIS","Mechanism","FEM"], stars="⭐⭐⭐⭐",
         summary="교차 영역 외 단일 캐리어에 의한 전도 차단 위험 수학적 분석. 전기장 벡터 방향 = envelope 변조 깊이 결정.",
         gap="안전성 고려"),

    dict(title="SUmiT Trial: RCT of PTNS for OAB (54.5% vs 20.9%)",
         authors="Peters KM, Macdiarmid SA, Wooldridge LS, et al.",
         year=2010, journal="Journal of Urology",
         doi="10.1016/j.juro.2009.12.036",
         cats=["TNS","Clinical","OAB"], stars="⭐⭐⭐⭐⭐",
         summary="Level 1 근거. PTNS 54.5% vs sham 20.9% (p<0.001). 이중맹검 RCT 220명. 중대 부작용 없음.",
         gap="임상 근거 기반"),

    dict(title="STEP Study: 3-year Long-term Outcomes of PTNS",
         authors="Peters KM, Carrico DJ, MacDiarmid SA, et al.",
         year=2013, journal="Journal of Urology",
         doi="10.1016/j.juro.2012.11.175",
         cats=["TNS","Clinical","OAB"], stars="⭐⭐⭐⭐⭐",
         summary="3년 추적. 월 1회 유지치료로 77% 반응 유지. 배뇨 12.0→8.7회/일, 요실금 3.3→0.3회/일.",
         gap="임상 장기 데이터"),

    dict(title="OrBIT Trial: PTNS vs Tolterodine for OAB",
         authors="MacDiarmid SA, Peters KM, Shobeiri SA, et al.",
         year=2010, journal="Journal of Urology",
         doi="10.1016/j.juro.2009.09.093",
         cats=["TNS","Clinical","OAB"], stars="⭐⭐⭐⭐⭐",
         summary="PTNS 80% vs Tolterodine ER 55% (12주, p<0.01). 12개월 96% 반응자 유지. PTNS > 1차 항콜린제.",
         gap="약물 비교 근거"),

    dict(title="CONFIDeNT: PTNS for Fecal Incontinence (negative RCT)",
         authors="Knowles CH, Horrocks EJ, Bremner SA, et al.",
         year=2015, journal="Health Technology Assessment",
         doi="10.3310/hta19770",
         cats=["TNS","Clinical"], stars="⭐⭐⭐⭐",
         summary="변실금 RCT 227명. 1차 결과 38% vs sham 31% (p=0.396) 유의 차이 없음. PTNS 변실금 효과 불명확.",
         gap="적응증 한계"),

    dict(title="Cochrane: Non-implanted Electrical Stimulation for OAB",
         authors="Stewart F, Berghmans B, Bø K, et al.",
         year=2016, journal="Cochrane Database of Systematic Reviews",
         doi="10.1002/14651858.CD010098.pub3",
         cats=["TNS","Clinical","Meta-analysis","OAB"], stars="⭐⭐⭐⭐⭐",
         summary="비침습 전기자극 Cochrane 리뷰. 전반적 근거 수준 낮음. ⚠️ Wibisono 2019 Cochrane은 존재하지 않음 — Stewart 2016이 정확.",
         gap="임상 근거 수준"),

    dict(title="TTNS Meta-analysis: 629 patients (ICIQ-UI SF -3.79)",
         authors="Booth J, Connelly L, Dickson S, et al.",
         year=2018, journal="Neurourology and Urodynamics",
         doi="10.1002/nau.23351",
         cats=["TNS","Clinical","Meta-analysis","OAB"], stars="⭐⭐⭐⭐⭐",
         summary="RCT 10편 629명. TTNS vs sham ICIQ-UI SF -3.79 (p=0.0003, I²=25%). OAB 48~93% 호전. 이상반응 없음.",
         gap="TTNS 임상 근거"),

    dict(title="TTNS vs PTNS Direct Comparison (142 patients, no difference)",
         authors="Bertolo R, et al.",
         year=2021, journal="Medicine",
         doi="10.1097/MD.0000000000025993",
         cats=["TNS","Clinical","Meta-analysis","OAB"], stars="⭐⭐⭐⭐",
         summary="4편 142명. 4개 OAB 지표 모두 유의 차이 없음. TTNS 합병증 0건 vs PTNS 2.1%. TTNS ≈ PTNS 효능.",
         gap="TTNS 타당성"),

    dict(title="Optimal TTNS Parameters: 10 Hz > 20 Hz (RCT 13, n=972)",
         authors="PMC12291541 meta-analysis",
         year=2025, journal="—",
         doi="PMC12291541",
         cats=["TNS","Clinical","Meta-analysis","OAB"], stars="⭐⭐⭐⭐⭐",
         summary="13 RCTs 972명. 10 Hz > 20 Hz (MD=-1.24, p<0.05). 운동 역치 > 감각 역치. 현재 표준 프로토콜 재고 필요.",
         gap="파라미터 최적화"),

    dict(title="TNS Does Not Inhibit PMC-evoked Contractions (Lyon Paradox)",
         authors="Lyon TD, et al.",
         year=2016, journal="Journal of Urology",
         doi="",
         cats=["TNS","Mechanism","OAB"], stars="⭐⭐⭐⭐⭐",
         summary="마취 고양이. PTNS는 PMC 직접 유발 방광 수축 억제 못함. β-adrenergic 경로 촉진. 척수 수준 비정상 감작만 억제.",
         gap="기전 Lyon 역설"),

    dict(title="GABAergic Interneurons Mediate TNS-induced Bladder Inhibition at S2",
         authors="McGee MJ, et al.",
         year=2018, journal="—",
         doi="",
         cats=["TNS","Mechanism","OAB"], stars="⭐⭐⭐⭐⭐",
         summary="S2 척수 제V~VII층 방광 관련 인터뉴런. 발화 40~50% 억제. GABA-A 수용체 차단 → 효과 소실. GABAergic 기전 직접 증명.",
         gap="G-TN3 기전 근거"),

    dict(title="Breathing Drives Pulsatile Spinal CSF Flow",
         authors="Dreha-Kulaczewski S, et al.",
         year=2017, journal="Scientific Reports",
         doi="10.1038/s41598-017-01813-3",
         cats=["Phrenic","Glymphatic"], stars="⭐⭐⭐⭐",
         summary="fMRI 기반. 호흡이 척수 CSF 흐름의 주 구동력. 흡기 시 두개내 CSF 흐름 증가.",
         gap="G-GL1, G-PH2"),

    dict(title="Inspiration Drives Upper Extremity Lymphatic Flow (ICG)",
         authors="Sunshine MD, et al.",
         year=2021, journal="Nature Communications Biology",
         doi="10.1038/s42003-021-01813-0",
         cats=["Phrenic","Glymphatic"], stars="⭐⭐⭐⭐",
         summary="횡격막 이식 전극 + ICG 림프 측정. 흡기 시 림프 흐름 최대. 호흡 주도 글림프 순환 기전 지지.",
         gap="G-PH2"),

    dict(title="i²CS First-in-Human: Intrafascicular Tibial Nerve Selectivity",
         authors="i²CS study group",
         year=2025, journal="Nature Communications",
         doi="",
         cats=["TNS","Anatomy"], stars="⭐⭐⭐⭐⭐",
         summary="First-in-Human fascicle 선택적 자극. 방광 억제 Aβ = 족저 감각 fascicle. Fascicle 선택에 따라 방광 억제 효과 차별화.",
         gap="G-TN3, KG-4"),
]


# ─────────────────────── main ───────────────────────

def main():
    tok = os.environ.get("NOTION_TOKEN")
    if not tok:
        print("❌  NOTION_TOKEN 환경변수를 설정하세요")
        print()
        print("  발급 방법:")
        print("  1. https://www.notion.so/my-integrations 접속")
        print("  2. '+ New integration' → 이름: nTIS Research → Submit")
        print("  3. 토큰(secret_...) 복사")
        print("  4. Notion 페이지 'TIS_Tibal-Nerve' → 우상단 '...' → Connections → 방금 만든 integration 추가")
        print("  5. 터미널에서: export NOTION_TOKEN=secret_xxxx")
        sys.exit(1)

    # verify
    r = requests.get(f"{API}/users/me", headers=H(tok))
    if r.status_code != 200:
        print(f"❌  인증 실패 ({r.status_code}): {r.text[:300]}")
        sys.exit(1)
    user = r.json().get("name","?")
    print(f"✅  인증 성공 — {user}")

    # ── Background page ──
    print("\n📚  Background 페이지 생성 중...")
    bg_id = create_page(tok, PID, "Background", "📚")
    print(f"    ID: {bg_id}")
    blocks = bg_blocks()
    print(f"    총 {len(blocks)}개 블록 추가...")
    append_blocks(tok, bg_id, blocks)

    # ── Paper DB ──
    print("\n📄  Paper DB 생성 중...")
    db_id = create_database(tok, PID, "Paper DB", "📄")
    print(f"    ID: {db_id}")
    print(f"    {len(PAPERS)}개 논문 추가...")
    for p in PAPERS:
        add_paper(tok, db_id, p)

    print("\n" + "─"*60)
    print("✅  완료!")
    print(f"  Background : https://notion.so/{bg_id.replace('-','')}")
    print(f"  Paper DB   : https://notion.so/{db_id.replace('-','')}")


if __name__ == "__main__":
    main()
