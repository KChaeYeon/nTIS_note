---
name: literature-search
description: "nTIS 및 전기자극 분야 문헌검색 스킬. PubMed/bioRxiv/Semantic Scholar 검색 → 02_papers/ 요약 작성 → gap_analysis.md 갱신. '논문 찾아줘', '최신 TIS 논문', 'PubMed 검색', '갭 업데이트', '논문 요약해줘', 'paper summary', '선행연구 조사' 시 반드시 사용. 중요 논문은 GPT+Gemini 다관점 분석 포함."
---

# Literature Search — nTIS 문헌검색 스킬

## 검색 전략

### 핵심 검색 쿼리 세트

**기본 TIS 쿼리:**
```
"temporal interference stimulation" OR "temporal interference" AND (brain OR nerve OR neural)
"TIS" AND ("non-invasive" OR "noninvasive") AND (stimulation OR neuromodulation)
"n-phase TIS" OR "multi-electrode TIS" OR "nTIS"
```

**표적별 확장 쿼리:**
```
# 미주신경
"temporal interference" AND ("vagus nerve" OR "vagal")
"non-invasive vagus nerve stimulation" AND (interferential OR interference)

# 수면
"temporal interference" AND (sleep OR "slow oscillation" OR "sleep spindle")
"closed-loop" AND "temporal interference" AND EEG

# 말초신경
"temporal interference" AND ("peripheral nerve" OR sciatic OR tibial)
"temporal interference" AND (autonomic OR HRV OR "heart rate variability")
```

### 검색 소스 및 우선순위

1. **PubMed** (pubmed.ncbi.nlm.nih.gov): 동료심사 논문 최우선
2. **bioRxiv/medRxiv** (biorxiv.org): 최신 프리프린트
3. **Semantic Scholar API**: 인용 검증 + 관련 논문 추천
4. **Google Scholar**: 위 3곳에서 못 찾은 경우 보조

### 필터 기준

- **연도**: 2020년 이후 우선; 핵심 선행연구(2017 Grossman Cell 등)는 예외
- **언어**: 영어
- **유형**: Original research > Review > Case report

---

## 다관점 분석 (중요 논문)

임팩트 높은 논문(IF ≥ 4 저널 or 핵심 갭 관련)은 CCG 분석 의무 실행:

```
oh-my-claudecode:ccg 활용:
- Claude: 신경공학·의공학 관점 분석
- GPT: 임상 번역 가능성, 규제 관점
- Gemini: 방법론 비판, 재현성 평가
```

세 관점을 통합하여 "다관점 요약" 섹션을 논문 요약 파일에 추가.

---

## 논문 요약 작성 형식

파일 위치: `docs/02_papers/YYYY_FirstAuthor_Keyword.md`

```markdown
# YYYY_Author_Keyword

## 서지 정보
- **저자:** Full author list
- **저널:** Journal Name (IF: X.X)
- **연도:** YYYY
- **DOI:** 10.XXXX/...
- **Semantic Scholar 확인:** ✅/❌
- **검색일:** YYYY-MM-DD

## 연구 질문
[논문이 답하려는 핵심 질문 1–2문장]

## 방법
- **설계:** [실험 설계 유형]
- **표본:** [동물/인체, n=X]
- **자극:** [캐리어 주파수, Δf, 전극, 세기]
- **결과 변수:** [측정한 것들]

## 주요 결과
[핵심 수치 + 효과크기 포함]

## 한계점
[저자가 인정한 한계 + 리뷰어 관점 추가]

## 다관점 요약 (CCG)
- **Claude (신경공학):** ...
- **GPT (임상):** ...
- **Gemini (방법론):** ...

## 관련 갭
- [G-XX]: [어떤 갭과 연결되는지]

## nTIS 연구와의 연관성
[현재 연구 후보 주제와의 관련성]
```

---

## 갭 분석 업데이트 규칙

`docs/03_gaps/gap_analysis.md` 수정 시:

1. 기존 갭 행의 "관련 논문" 열에 `YYYY_Author` 추가
2. 새 논문이 갭을 부분적으로 채웠으면 🔴→🟡 격하 검토
3. 완전히 채워진 갭은 🟢로 변경 + 날짜 표기
4. 새 갭 발견 시 테이블에 새 행 추가 (ID: G-[분야코드][번호])

---

## 인용 무결성 체크

```
검증 절차:
1. DOI → Semantic Scholar API 조회
2. 저자명·연도·저널 3개 모두 일치 확인
3. 불일치 또는 조회 실패 → [UNVERIFIED] 표기
4. [UNVERIFIED] 논문은 02_papers/ 파일에 포함하되 연구 논문 인용에서 제외
```

---

## 경쟁 위험 스캔

연구 주제 확정 전 반드시 실행:

```
검색: "[연구 주제 핵심 키워드]" in last 12 months
→ 동일 갭을 다룬 논문 존재 여부 확인
→ bioRxiv 프리프린트 포함 (공개되지 않은 경쟁 연구 위험)
```

결과: "경쟁 없음" / "유사 연구 존재: [논문]" / "동일 연구 진행 중: [팀명]"
