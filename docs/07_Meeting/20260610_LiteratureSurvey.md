# 2026-06-10 말초·자율신경 TIS 문헌 조사 세션

**목적:** nTIS 팀 합류 시 맡을 수 있는 연구 주제 선정을 위한 체계적 문헌 조사  
**방법:** WebSearch 기반 deep-research (lit-review 모드)  
**결과:** 갭 지도 업데이트 + 최우선 주제 도출

---

## 세션 맥락

- 기존 팀 진행 중: **설하신경 nTIS** — FEM 시뮬(human head), 3D cubic 모델, LED 팬텀 검증, 논문 작성 중
- 사용자 합류 후 맡을 주제 탐색
- 실험 가능 대상: **건강 성인 + Rat** (임상군 불가)
- 보유 장비: TIS 자극기, ECG/HRV, Rat 동물실험 인프라 (**EEG 없음**)

---

## 핵심 발견: 갭 지도 업데이트

### 기존 기록과 달라진 점

| 항목 | 기존 기록 | 오늘 확인 |
|------|---------|---------|
| G-A4 척수 TIS | "시뮬레이션만, 생체 실험 없음" | **수정**: Sunshine 2021 (Nat Comm Bio)에서 rat in vivo 이미 완료 → 🟡 Partial |
| G-A1 경부 미주신경 TIS | "전무" | **유지**: i²CS (Nat Comm 2025)는 삽입형 cuff → 비침습 TIS는 여전히 전무 |
| G-A2 경골신경 TIS | "전무" | **보완**: MDPI 2023에 in silico 최적화 연구 존재 → 생체 검증은 여전히 없음 |
| 좌골신경 TIS | 갭에 없음 | **신규**: Botzanowski 2022/2025로 2-pair in vivo 완료, **n-phase는 전무** → G-A5 추가 |

### 말초·자율신경 TIS 현황 지도 (2026년 6월)

| 신경 표적 | 2-pair TIS | n-phase TIS | Rat in vivo | 비침습 인체 |
|---------|-----------|-------------|-------------|-----------|
| 좌골신경 | ✅ 2022, 2025 | ❌ | ✅ | ❌ |
| 횡격막/척수 | ✅ 2021 | ❌ | ✅ | case 3례 |
| 경골신경(방광) | in silico만 | ❌ | ❌ | ❌ |
| 경부 미주신경 | ❌ (i²CS는 삽입형) | ❌ | ❌ | ❌ |
| 설하신경 | 1편(2023) | **팀 진행** | ❌ | **팀 진행** |

---

## 새로 파악한 핵심 논문 (02_papers/ 추가 필요)

| 논문 | 저널 | 중요도 | 핵심 내용 |
|------|------|--------|---------|
| Botzanowski et al. 2022 | Adv Healthcare Mat | 🔴 필수 | 좌골신경 TIS rat in vivo 최초 검증; 2-pair |
| Botzanowski et al. 2025 | J NeuroEng Rehab | 🔴 필수 | 64채널 cuff + TIS; biphasic 대비 1.75× 선택성 |
| Sunshine et al. 2021 | Nat Comm Bio | 🔴 필수 | 횡격막신경/척수 TIS rat; opioid·SCI 호흡 회복 |
| i²CS 2025 | Nature Comm | 🔴 필수 | 돼지 미주신경 삽입형 interferential → 장기 선택 자극 |
| MDPI TI-Tibial 2023 | Appl Sci (MDPI) | 🟡 필요 | 경골신경 TIS 최적화 in silico; 생체 검증 없음 |
| Frontiers Scoping 2025 | Front Hum Neurosci | 🟡 필요 | TIS 전체 적용 범위 scoping review |

---

## 연구 주제 추천

### ⭐⭐⭐ 1순위: 경부 미주신경 비침습 nTIS

**연구 질문:**
> n-phase temporal interference stimulation이 경부 미주신경을 비침습적으로 표적화하여, 기존 taVNS(귀 분지 자극) 대비 HRV 및 자율신경 반응에서 차별화된 효과를 보이는가?

**논문 시리즈 (학위논문 구성안):**
1. (팀) 설하신경 nTIS: FEM + 팬텀 검증
2. **(사용자 Paper 1)** 경부 vagus nTIS FEM feasibility + Rat HRV/심장 in vivo 검증
3. **(사용자 Paper 2)** 비침습 경부 nTIS vs. taVNS (인체, ECG/HRV)

**선택 근거:**
- 세계 최초 비침습 TIS 적용 경부 미주신경 (🔴 Major gap G-A1)
- ECG/HRV = 결과변수로 완벽 부합 (보유 장비)
- Rat 경부 미주신경 수술 프로토콜 확립 (VNS 연구 선례 풍부)
- i²CS 2025 (Nature Comm)이 분야 관심 확인 → 비침습 TIS 버전 타이밍 좋음
- 팀의 FEM 인프라(설하신경 모델 → 경부 vagus 적용)와 협업 가능
- 설하신경(OSA)과 미주신경(자율신경·항염)이 같은 경부 영역 → 스토리 연결

### ⭐⭐ 2순위: 말초신경 n-phase TIS 선택성 (rat 좌골신경)

**연구 질문:**
> n-phase TIS가 2-pair TIS 대비 rat 좌골신경에서 더 높은 fascicle 선택성을 달성하는가?

- 기준선: Botzanowski 2022/2025 (2-pair 선택성 데이터)
- **필요 장비 확인 필요: EMG 기록 시스템**

---

## 다음 할 일

- [ ] 위 6편 논문 02_papers/에 요약 추가
- [ ] **팀 확인**: FEM 프레임워크 경부 vagus 확장 가능 여부, EMG 장비 보유 여부
- [ ] 경부 미주신경 nTIS 연구 질문 → 04_proposal/ 에 구체화
- [ ] G-A5 추가, G-A4 수정 반영된 gap_analysis.md 확인

---

*Last updated: 2026-06-10*
