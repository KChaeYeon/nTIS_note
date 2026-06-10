---
name: paper-draft
description: "nTIS 논문 초안 작성 스킬. Introduction·Methods·Results·Discussion·Abstract 섹션별 작성, IEEE TBME/JNE/Brain Stimulation 포맷 적용, 상관관계 언어 보장, AI 과잉 표현 제거. '논문 써줘', '초안 작성', 'Introduction 작성', 'Discussion 써줘', 'Abstract 써줘', '섹션 초안', 'paper draft', 'cover letter' 시 반드시 사용."
---

# Paper Draft — nTIS 논문작성 스킬

## 언어 품질 원칙 (모든 섹션 공통)

### 상관관계 언어 (필수 준수)

**허용 표현:**
```
- "was associated with"
- "correlated with" (Pearson/Spearman r 있을 때)
- "predicted" (회귀 모델 맥락)
- "co-occurred with"
- "paralleled"
- "was accompanied by"
```

**금지 표현 (인과관계 함의):**
```
- caused, led to, resulted in, produced
- due to (기전 미확인 시)
- demonstrated that X affects Y
- X improves/reduces Y (RCT 아닌 경우)
```

**통계 보고 형식:**
```
❌ p = 0.03
✅ t(28) = 2.41, p = 0.023, d = 0.87, 95%CI [0.23, 1.51]
```

**AI 전형 표현 블랙리스트:**
delve, underscore, it is worth noting, pivotal, transformative,
groundbreaking, landmark, robust (남용), noteworthy, crucially,
importantly (남용), significantly (통계적 의미 없는 맥락)

---

## 섹션별 작성 가이드

### Introduction

구조 (역 피라미드):
1. **Broad context** (2–3문장): 분야의 임상적 중요성
2. **Narrowing** (3–4문장): 현재 한계와 기존 접근법
3. **Gap statement** (1–2문장): "However, [갭 명시]"
4. **This study** (2–3문장): 무엇을 했고, 왜 이 접근이 갭을 채우는가

길이: IEEE TBME ≤ 600단어, JNE ≤ 500단어, Brain Stimulation ≤ 400단어

### Methods

필수 포함 항목:
```
- 연구 설계 (crossover, within-subject, ...)
- 피험자/동물 정보 (n, 종, 선정/제외 기준, 윤리 승인 번호)
- 자극 파라미터 (f1, f2, Δf, 강도, 지속시간, 전극 배치)
- FEM 검증 방법 (소프트웨어, 헤드 모델, 도전율)
- 데이터 수집 (장비 모델명, 샘플링 레이트)
- 분석 방법 (소프트웨어 버전, 통계 검정, 다중비교 보정)
- 검정력 분석 (효과크기 가정, 표본 수 근거)
```

### Results

구조:
1. **피험자 정보** (Table 1 형태)
2. **주요 결과** (가설 순서로, 수치 + 효과크기 + CI)
3. **부가 결과** (사전분석 명시)
4. **안전성/이상반응** (없어도 명시)

플레이스홀더 형식:
```markdown
The nTIS condition was associated with greater RMSSD compared to sham
[STAT: mean±SD, t(df)=X, p=X, d=X, 95%CI[lo, hi]].
[FIG 2: Boxplot of RMSSD by condition, with individual data points overlaid]
```

### Discussion

구조:
1. **핵심 발견 요약** (1문장, 수치 없이)
2. **선행연구와 비교** (일치·불일치 모두 설명)
3. **기전 해석** (correlational 언어로)
4. **한계점** (솔직하게, 최소 3개)
5. **임상·연구 함의**
6. **결론** (1–2문장)

### Abstract (Structured)

Brain Stimulation 형식:
```
Background: [왜 중요한가]
Objective: [무엇을 했는가]
Methods: [어떻게 했는가, 핵심 파라미터]
Results: [핵심 수치]
Conclusion: [함의, correlational 언어]
```

---

## 저널별 포맷 가이드

### IEEE TBME
- Full paper: ≤ 10페이지 (2단 컬럼)
- Letter: ≤ 6페이지
- Figure: ≤ 10개 (full), ≤ 5개 (letter)
- 참고문헌: IEEE 형식 (번호)

### Journal of Neural Engineering (JNE)
- Research article: ≤ 8,000단어
- Methods section 상세 기술 중요
- 참고문헌: 저자-연도 형식

### Brain Stimulation
- Research article: ≤ 4,000단어 (본문)
- Structured abstract 필수 (250단어)
- Clinical relevance statement 필수
- 참고문헌: 번호 형식

---

## Figure 계획 원칙

```
컬러: colorblind-safe palette (viridis, cividis, 또는 Wong 8-color)
해상도: 300 dpi (인쇄), 72 dpi (웹 초안)
폰트: Arial 또는 Helvetica, ≥ 8pt
통계 표시: * p<0.05, ** p<0.01, *** p<0.001, ns
오차막대: SEM 또는 95%CI (SD 금지 — 분포 가변성과 정밀도 혼동)
데이터 포인트: Boxplot에 개별 데이터 오버레이 권장
```

---

## 파일 명명 규칙

```
docs/05_Exp/draft_[JOURNAL]_[SECTION]_v[N].md

예시:
draft_TBME_introduction_v1.md
draft_JNE_methods_v2.md
draft_BrainStim_full_v1.md
```

최종 제출 파일은 `docs/05_Exp/submission/`으로 이동.
