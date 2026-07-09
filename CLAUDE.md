# Project: nTIS Research Notebook

## Research Topic

**n-phase Temporal Interference Electrical Stimulation (nTIS)**

비침습적 심부 전기자극 기법. 두 개 이상의 고주파 전류 간섭을 이용해 조직 내부에 저주파 자극 envelope을 생성. n-phase 확장은 전극 쌍을 n개로 늘려 초점성(focality)과 방향성 제어를 개선.

## Research Stage

A → B → C → D 순서로 진행:
- **A. Theory**: 원리, 수식, 전기장 모델 정리 ✅
- **B. Research Gaps**: 선행연구 체계적 정리 → 미해결 문제 목록 ✅
- **C. Proposal**: 연구 주제 선정 → 경골신경 TIS in vivo Rat OAB 확정 ✅ (2026-06-16)
- **D. Execution**: 실험 설계·수행·논문 작성 (진행 중)

> A~C 산출물(이론·갭·제안)은 **Background 탭(`01_theory/`)의 STEP 1~4**로 통합되어 하나의 연속된 연구 배경으로 관리한다.

## Site & Repo

- GitHub: https://github.com/KChaeYeon/nTIS_note
- Pages: https://kchaeyeon.github.io/nTIS_note/
- 로컬: `/mnt/d/00_Project/nTIS/`

## Folder Structure

사이트는 5개 탭으로 구성된다 (탭 순서: Background · Simulation · Experiment · Meeting · Reference).
탭명·순서는 각 폴더의 `.pages`(title)와 최상위 `docs/.pages`(nav)로 제어한다.

```
docs/
├── index.md           ← 홈 (5개 탭 구성 개요)
├── 01_theory/         ← [Background] 연구 배경 = 이론 + 연구 갭(13) + 제안(14~16)
├── 02_papers/         ← [Reference]  논문별 요약 (YYYY_Author_Keyword.md)
├── 05_Code/           ← 분석 코드 (사이트 nav 미노출)
├── 06_Exp/            ← [Experiment] 실험 데이터·분석 결과
├── 07_Meeting/        ← [Meeting]    회의록·발표 자료
└── 07_Simulation/     ← [Simulation] COMSOL FEM 시뮬레이션 (사용법·변수체계·데이터)
```

> 구 `03_gaps/`·`04_proposal/`는 Background(`01_theory/13~16_*.md`)로 통합·이동되었다.

## Workflow

1. 마크다운 파일 작성·수정
2. `git add . && git commit -m "note: ..." && git push`
3. GitHub Actions 자동 빌드 (~1~2분) → 사이트 자동 업데이트

## Content Rules

- 논문 파일명: `YYYY_FirstAuthor_Keyword.md` (예: `2017_Grossman_TI_Cell.md`)
- 실험 파일명: `YYYYMMDD_ExperimentName.md`
- 회의 파일명: `YYYYMMDD_MeetingType.md`
- 수식: 인라인 `$...$`, 블록 `$$...$$` (MathJax 렌더링)
- 상관관계 언어만 사용 — 인과관계 표현 금지 (논문 작성 원칙 준수)
- 통계: 효과크기 + CI를 p-value와 함께 보고

## Claude Instructions

- 노트 추가 시 해당 섹션 폴더의 파일 명명 규칙을 따를 것
- 논문 요약 작성 시: 연구 질문, 방법, 주요 결과, 한계점, 관련 갭 순서로 정리
- 새 이론 내용 추가 시 MathJax 문법으로 수식 작성
- 홈 `index.md`는 5개 탭 구성 개요를 유지 (Progress Tracker 방식 폐지)
- 탭 추가·이름·순서 변경 시 해당 폴더의 `.pages`(title)와 `docs/.pages`(nav)를 함께 수정
- git push 전 확인 요청

## 응답 워크플로우 (모든 세션 적용)

모든 사실적 주장·수식·연구 방법론이 포함된 답변은 **3단계 프로세스**로 처리한다:

1. **에이전트/스킬 선택 & 실행** — 요청 의도에 맞는 최적 에이전트 또는 스킬 활용
2. **Gemini 검증** — `mcp__gemini__ask-gemini`로 사실성·논리성 크로스체크
3. **최종 답변** — 검증 결과 반영 후 사용자에게 전달

> 단순 조작(파일 작성, git 명령, 포맷 변환 등)은 검증 생략 가능.

---

## 하네스: nTIS Research

**목표:** 1~1.5년 내 박사 졸업 논문 + IEEE TBME/JNE/Brain Stimulation 급 저널 제출

**트리거:** nTIS 연구 관련 작업(주제 선정, 문헌조사, 실험 설계, 논문 작성) 요청 시 `.claude/skills/nTIS-research/SKILL.md` (오케스트레이터) 스킬을 사용하라. 단순 질문은 직접 응답 가능.

**에이전트:** `.claude/agents/` — literature-scout, research-designer, paper-writer, theory-mentor

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-06-10 | 초기 하네스 구성 | 전체 | nTIS 연구 주제 선정 세션 시작 |
| 2026-07-07 | theory-mentor 에이전트 + ti-efield-theory 스킬 추가 | agents/theory-mentor.md, skills/ti-efield-theory/ | TI 전기장 이론 학습(연구교수 페르소나) 요청 |
| 2026-07-07 | 세션 간 이어쓰기 로그(study_log.md) + 터미널 수식 표기 원칙 추가 (신규 스킬 생성 없이 기존 스킬 보강) | docs/01_theory/study_log.md, skills/ti-efield-theory/SKILL.md | 여러 세션에 걸친 TI 전기장 이론 공부 지속성 확보 |

---

## Agent & Skill Selection

키워드 매칭이 아닌 **질문의 의도와 맥락**을 파악해 가장 적합한 에이전트/스킬을 자동 선택한다.
모든 응답은 관련 에이전트/스킬을 최대한 활용해 사실 기반의 풍성한 답변을 제공한다.

### 에이전트 (`.claude/agents/`)

| 에이전트 | 활용 상황 |
|---------|---------|
| `literature-scout` | 선행 논문 검색·요약, 특정 논문 내용 파악, 연구 동향 파악, 논문 PDF 정리가 필요할 때 |
| `research-designer` | 실험 프로토콜 설계, FEM 모델링, FINES 평가, 연구 주제·방법론 선정이 필요할 때 |
| `paper-writer` | 논문 초안·섹션(Introduction~Discussion) 작성, 저널 포맷 적용이 필요할 때 |
| `theory-mentor` | TI 전기장 이론 심층 수식 유도·표기법 교차검증·오류 진단이 필요할 때 (`ti-efield-theory` 스킬에서 위임) |

### nTIS 전용 스킬 (`.claude/skills/` — 이 프로젝트 로컬)

| 스킬 | 활용 상황 |
|------|---------|
| `nTIS-research` | nTIS 연구 전반 오케스트레이션 (주제 선정→문헌→설계→집필 전 과정) |
| `literature-search` | TIS/nTIS 논문 검색, PubMed/Semantic Scholar 조회, 갭 분석 |
| `research-design` | 실험 프로토콜·FEM 모델링·FINES 평가·타임라인 설계 |
| `paper-draft` | nTIS 논문 섹션 초안 작성, 저널 포맷(TBME/JNE) 적용 |
| `ti-efield-theory` | TI 전기장 이론 학습, 연구교수 페르소나 소크라테스식 문답, envelope/n-phase 수식 이해 |

### 상위 프로젝트 스킬 (`/mnt/d/00_Project/.claude/skills/academic-research-skills/`)

| 스킬 | 활용 상황 |
|------|---------|
| `research-topic-selection` | 연구 주제 고민, FINES 다기준 평가, 연구 방향성 조언이 필요할 때 |
| `deep-research` | 특정 주제의 깊은 문헌 조사, PRISMA 리뷰, 사실 확인이 필요할 때 |
| `academic-paper` | 논문 초안 작성, 수정, LaTeX 포맷 작업이 필요할 때 |
| `academic-paper-reviewer` | 제출 전 peer review 시뮬레이션이 필요할 때 |
| `academic-pipeline` | 처음부터 끝까지 논문 작성 전 과정이 필요할 때 |

### OMC 글로벌 스킬 (Skill 도구로 호출)

| 스킬 | 활용 상황 |
|------|---------|
| `superpowers:brainstorming` | 새 기능·접근법·연구 방향 탐색 전 |
| `superpowers:systematic-debugging` | 코드·분석 파이프라인 오류 추적 |
| `superpowers:verification-before-completion` | 작업 완료 전 결과 검증 |
| `oh-my-claudecode:deep-dive` | 요구사항 심층 인터뷰 + 인과 추적 |
| `oh-my-claudecode:autoresearch` | 자동 심층 조사 |

### MCP 도구 (검증·조사 보조)

| 도구 | 활용 상황 |
|------|---------|
| `mcp__gemini__ask-gemini` | **모든 사실적 답변의 Gemini 검증** (필수) |
| `mcp__gemini__brainstorm` | 연구 아이디어 브레인스토밍 |
| `mcp__notebooklm__ask_question` | NotebookLM 노트북 질문 |
| `mcp__plugin_context7_context7__query-docs` | 라이브러리·프레임워크 공식 문서 조회 |

### 파일 작업 (Claude 직접 처리 + 에이전트 보조)

| 작업 | 처리 방식 |
|------|---------|
| 논문 요약 파일 추가 | `02_papers/`에 파일 작성 (내용이 복잡하면 `literature-scout` 활용) |
| 갭 항목 추가 | `03_gaps/gap_analysis.md` 수정 (갭 분석이 필요하면 `research-designer` 활용) |
| 회의록 작성 | `06_Meeting/YYYYMMDD_*.md` 생성 |
| 실험 기록 | `05_Exp/YYYYMMDD_*.md` 생성 |

### 모든 질문 유형에 대한 처리 원칙

- **연구 이론·개념 학습**: 수식·이론 배경 포함, `deep-research` 또는 `mcp__gemini__ask-gemini` 사실 검증 병행
- **선행 논문 읽기·분석**: `literature-scout` 에이전트로 문헌 맥락 보강
- **논문 작성 전 과정**: `deep-research` → `academic-paper` → `academic-paper-reviewer` 체이닝
- **일상 궁금증·사실 확인**: `WebSearch` 또는 Context7 MCP로 최신 정보 기반 답변
- **불확실한 내용**: 추측하지 않고 검색·문헌 근거를 명시
