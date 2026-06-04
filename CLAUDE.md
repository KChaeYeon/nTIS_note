# Project: nTIS Research Notebook

## Research Topic

**n-phase Temporal Interference Electrical Stimulation (nTIS)**

비침습적 심부 전기자극 기법. 두 개 이상의 고주파 전류 간섭을 이용해 조직 내부에 저주파 자극 envelope을 생성. n-phase 확장은 전극 쌍을 n개로 늘려 초점성(focality)과 방향성 제어를 개선.

## Research Stage

A → B → C 순서로 진행:
- **A. Theory**: 원리, 수식, 전기장 모델 정리 (현재)
- **B. Research Gaps**: 선행연구 체계적 정리 → 미해결 문제 목록
- **C. Proposal**: 구체적 연구 질문, 방법론, 기여점

## Site & Repo

- GitHub: https://github.com/KChaeYeon/nTIS_note
- Pages: https://kchaeyeon.github.io/nTIS_note/
- 로컬: `/mnt/d/00_Project/nTIS_note/`

## Folder Structure

```
docs/
├── index.md           ← 홈 (진행 현황 업데이트)
├── 01_theory/         ← 이론 정리
├── 02_papers/         ← 논문별 요약 (YYYY_Author_Keyword.md)
├── 03_gaps/           ← 연구 갭 분석
├── 04_proposal/       ← 연구 제안서
├── 05_Exp/            ← 실험 데이터·분석 결과
└── 06_Meeting/        ← 회의록·발표 자료
```

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
- `index.md` Progress Tracker는 단계 변경 시 업데이트
- git push 전 확인 요청

## Registered Skills

| Trigger | Use when |
|---------|----------|
| "논문 요약해줘" | 02_papers/에 새 논문 요약 파일 추가 |
| "갭 추가해줘" | 03_gaps/gap_analysis.md에 새 갭 항목 추가 |
| "회의록 작성" | 06_Meeting/에 YYYYMMDD_*.md 파일 생성 |
| "실험 기록" | 05_Exp/에 YYYYMMDD_*.md 파일 생성 |
