---
name: nTIS-research
description: "nTIS 연구 오케스트레이터. 문헌조사(literature-scout) → 연구설계(research-designer) → 논문작성(paper-writer) 에이전트를 조율. '연구 주제 선정', '연구 단계 전환', '하네스 시작', '전체 연구 진행', '다음 단계', 'nTIS 연구 도와줘', 'stage 전환', '연구 업데이트' 시 반드시 이 스킬 사용. 후속 작업: '다시 실행', '재실행', '이전 결과 기반으로', '보완해줘' 포함."
metadata:
  version: "1.0.0"
  last_updated: "2026-06-10"
  domain: nTIS, neural-engineering, electrical-stimulation
---

# nTIS Research Orchestrator

**목표:** 1~1.5년 내 박사 졸업 논문 + IEEE TBME/JNE/Brain Stimulation 급 논문 제출  
**현재 단계:** A(Theory) ✅ → B(Gaps) ✅ → **C(Proposal)** 진행 중 → D(Execution)

---

## Phase 0: 컨텍스트 확인

실행 시작 시 기존 산출물 상태를 파악하여 실행 모드를 결정한다.

1. `docs/04_proposal/research_proposal.md` 존재 및 최신성 확인
2. `docs/03_gaps/gap_analysis.md` 마지막 업데이트 확인
3. `docs/02_papers/` 파일 수 확인
4. 실행 모드 분기:
   - **초기 실행**: proposal 미존재 → Phase 1부터 전체 실행
   - **단계 전환**: proposal 존재 + 사용자가 C→D 전환 요청 → Phase 3으로 직행
   - **부분 재실행**: 특정 에이전트 재호출 → 해당 에이전트만 실행

---

## Phase 1: 현재 상태 브리핑

오케스트레이터가 직접 실행:

```
연구 단계: [현재 단계 표시]
보유 논문 요약: [02_papers/ 파일 수]편
확인된 갭: [gap_analysis.md에서 Major 갭 수]개
후보 주제: [research_proposal.md에서 후보 수]개
마지막 업데이트: [날짜]
```

사용자 요청 유형 분류:
- **"주제 선정" / "FINES 평가"** → Phase 2A (연구설계 에이전트 주도)
- **"논문 찾아줘" / "갭 업데이트"** → Phase 2B (문헌조사 에이전트 주도)
- **"논문 써줘" / "섹션 작성"** → Phase 2C (논문작성 에이전트 주도)
- **"전체 진행"** → Phase 2A+B 병렬 실행

---

## Phase 2: 에이전트 실행 (Supervisor 패턴)

**실행 모드: 서브 에이전트** (독립적 산출물 → 오케스트레이터 종합)

### Phase 2A — 연구설계 (research-designer)

```
Agent(
  subagent_type: "general-purpose",
  agent_file: ".claude/agents/research-designer.md",
  model: "opus",
  task: "FINES 다기준 평가 실행",
  input: {
    candidates: [research_proposal.md의 후보 목록],
    constraints: {timeline: "1~1.5yr", equipment: ["TIS", "ECG/HRV", "Rat"]},
    require_multi_ai: true  // CCG로 GPT+Gemini 가설 수집 필수
  }
)
```

산출물: `docs/04_proposal/research_proposal.md` 업데이트 (FINES 표 + 최종 추천)

### Phase 2B — 문헌조사 (literature-scout)

```
Agent(
  subagent_type: "general-purpose",
  agent_file: ".claude/agents/literature-scout.md",
  model: "opus",
  task: "갭 보완 문헌 검색",
  input: {
    priority_gaps: ["G-A1", "G-S4", "G-C1", "G-A5"],
    pending_papers: [
      "Botzanowski 2022 (Adv Healthcare Mat)",
      "Sunshine 2021 (Nat Comm Bio)",
      "i²CS 2025 (Nature Comm)"
    ],
    depth: "standard"
  }
)
```

산출물: `docs/02_papers/` 새 파일들, `docs/03_gaps/gap_analysis.md` 업데이트

### Phase 2C — 논문작성 (paper-writer)

```
Agent(
  subagent_type: "general-purpose",
  agent_file: ".claude/agents/paper-writer.md",
  model: "opus",
  task: "지정 섹션 초안 작성",
  input: {
    section: [사용자 지정],
    target_journal: [사용자 지정],
    research_context: [research-designer 산출물 기반]
  }
)
```

산출물: `docs/05_Exp/draft_[journal]_[section]_v1.md`

---

## Phase 3: 연구 단계 전환 관리

### C → D 전환 체크리스트

단계 전환 전 반드시 확인:
- [ ] 최종 연구 주제 1개 확정 (FINES 가중 합산 ≥ 3.5)
- [ ] 지도교수 승인 확인 여부
- [ ] 목표 저널 확정
- [ ] 1차 실험 시작 날짜 설정
- [ ] 필요 추가 장비 목록 작성

체크리스트 미완료 항목이 있으면 D 단계 진입 전 사용자에게 경고.

### D단계 진입 시 실행

1. `docs/index.md` Progress Tracker 업데이트 (C → D)
2. `docs/06_Meeting/YYYYMMDD_StageTransition.md` 생성 (전환 결정 기록)
3. D단계 첫 마일스톤 설정: 실험 프로토콜 확정 → IRB/IACUC 제출

---

## Phase 4: 결과 종합 및 git 커밋

모든 에이전트 완료 후:

1. 변경된 파일 목록 요약
2. git 커밋 메시지 초안 제시 (사용자 승인 후 commit)
3. push 여부 사용자에게 확인

```
note([stage]): [변경 내용 한 줄 요약]

Agents: [실행된 에이전트 목록]
Files: [변경된 파일 목록]
Next: [다음 액션]

Confidence: high
Scope-risk: narrow
```

---

## 보유 장비 레퍼런스 (항상 참조)

| 장비 | 상태 | 비고 |
|------|------|------|
| TIS 자극기 | ✅ 보유 | 모델 확인 필요 |
| ECG/HRV | ✅ 보유 | |
| Rat 인프라 | ✅ 보유 | |
| EEG | ❌ 미보유 | 대여/공동사용 여부 확인 필요 |
| fMRI/MRI | ❓ 미확인 | |
| 인체 피험자 IRB | ❓ 미확인 | |

## 타임라인 제약

- **전체 기간**: 1~1.5년 (2026-06 ~ 2027-06/12)
- **Phase C 완료 목표**: 2026-07 (주제 확정 + 프로토콜)
- **Phase D 실험 완료**: 2027-03
- **논문 제출**: 2027-06~09

---

## 테스트 시나리오

**정상 흐름:**
1. 사용자: "연구 주제 선정 도와줘"
2. → Phase 0: 기존 proposal 확인
3. → Phase 1: 현황 브리핑
4. → Phase 2A: research-designer가 FINES 평가 실행
5. → Phase 4: 결과 요약 + git 커밋 제안

**에러 흐름:**
1. research-designer가 F≤1 Kill-switch 발동
2. → 탈락 사유 명시 + 남은 후보 재평가 자동 실행
3. → 모든 후보 탈락 시 사용자에게 새 후보 요청
