# Research Gaps

선행연구 정리 후 발견된 미해결 문제들을 기록합니다.

## 분류 기준

- 🔴 Major gap — 아무도 다루지 않은 문제
- 🟡 Partial gap — 일부 연구됐지만 불충분
- 🟢 Addressed — 충분히 연구됨 (참고용)

---

## TIS 전반 갭

| ID | Gap | 분류 | 관련 논문 |
|----|-----|------|----------|
| G-T1 | 인간 TIS 연구 절대 부족 (20편, 820명, 2026 기준) | 🔴 | Vassiliadis 2026 (Nat BME) |
| G-T2 | 최적 캐리어 주파수 미결정 (1 kHz vs. 9 kHz 등) | 🔴 | 뇌전증 논문(2025 Brain Stim): 9 kHz > 1 kHz 시사, 체계적 비교 없음 |
| G-T3 | 최적 Δf 선택 기준 없음 ("목표 뇌 리듬 = Δf" 가설, 미검증) | 🔴 | Violante 2023 (5 Hz theta), Lamoš 2025 (130 Hz) |
| G-T4 | 다중 세션 장기 효과 미연구 (단일 세션 연구 16/20편) | 🟡 | AD 연구(2025): 10일 세션, n=21 |
| G-T5 | Non-responder 예측 인자 전무 | 🔴 | — |
| G-T6 | 개인 간 해부학 변동성 → 표준 몽타주 부정확 (최대 4.4 cm 오차) | 🟡 | Lanzone 2025 (Brain Stim) |
| G-T7 | 장기 안전성 데이터 없음 (FDA 미승인, 28개 시험 진행 중) | 🟡 | Cassarà 2025 (Bioelectromag) |

---

## 분야별 갭

### A. 수면 신경생리

| ID | Gap | 분류 | 관련 논문 |
|----|-----|------|----------|
| G-S1 | 피질 서파(SWA) TIS: 건강 성인 단일 세션만 존재 | 🟡 | SWA TIS 2025 (medRxiv), n=21 |
| G-S2 | 시상 방추파 TIS: 건강 성인 단일 낮잠만 존재 | 🟡 | Spindle TIS 2026 (medRxiv), n=24 |
| G-S3 | MCI/치매 환자 수면 TIS 전무 | 🔴 | — |
| G-S4 | SO 위상 잠금 TIS (phase-locked stimulation) 전무 | 🔴 | Helfrich 2018: 청각 자극으로 SO 위상 잠금 효과 증명 |
| G-S5 | SO–Spindle–Ripple 동시 조율 TIS 전무 (단독 표적만 존재) | 🔴 | Staresina 2015 (Nat Neuro): 세 리듬 coupling이 기억 강화의 핵심 |
| G-S6 | 개인 방추파 피크 주파수 = 개인화 Δf 전략 미검증 | 🟡 | Spindle TIS 2026: 개인 피크 > 고정 10 Hz 경향 확인, 통계 불충분 |

### B. 폐쇄형 TIS

| ID | Gap | 분류 | 관련 논문 |
|----|-----|------|----------|
| G-C1 | EEG 기반 실시간 폐쇄형 TIS 전무 | 🔴 | EEG-TMS 폐쇄형은 존재; TIS는 0건 |
| G-C2 | 발작 전조 감지 → TIS 자동 트리거링 전무 | 🔴 | IED 억제 TIS (2025 Brain Stim): open-loop 고정 자극만 |
| G-C3 | 수면 서파 위상 감지 → TIS 트리거링 전무 | 🔴 | SO 위상 잠금 청각 자극(Helfrich 2018)의 TIS 버전 없음 |
| G-C4 | 폐쇄형 TIS 하드웨어/소프트웨어 프레임워크 없음 | 🔴 | ECAP CL-SCS는 선례 (통증 분야) |

### C. 파킨슨병 / 운동 장애

| ID | Gap | 분류 | 관련 논문 |
|----|-----|------|----------|
| G-P1 | 단일 표적(STN 또는 GPi)만 검증, 동시 자극 없음 | 🔴 | Lamoš 2025 (STN), Yang 2025 (GPi) |
| G-P2 | 다중 세션 TIS 효과 미검증 (단일 세션만) | 🟡 | Yang 2025: 20분 1회; 임상적 충분성 미달 |
| G-P3 | 보행 장애·자세 불안정 개선 미검증 (서동증·진전만) | 🟡 | Agrawal 2025: 다중 표적 DBS가 보행 추가 개선 |

### D. 신경정신 질환

| ID | Gap | 분류 | 관련 논문 |
|----|-----|------|----------|
| G-N1 | 알츠하이머 TIS: n=21 pilot만, 기전 biomarker 미확립 | 🟡 | PMC12739658 (2025): 기억 향상 확인, PET/p-tau 변화 없음 |
| G-N2 | 우울증 TIS: 임상시험 진행 중, 결과 미발표 | 🟡 | 표적(DLPFC? sgACC?) 미확정 |
| G-N3 | 의식 장애(DOC) TIS: case report 1건 | 🔴 | Frontiers 2026: 시상 TIS 후 EEG 각성 증가, n=1 |
| G-N4 | PTSD 편도체 TIS 전무 | 🔴 | — |

### E. 말초 / 자율신경계

| ID | Gap | 분류 | 관련 논문 |
|----|-----|------|----------|
| G-A1 | 경부 미주신경 **비침습** TIS 전무 (taVNS와 비교 없음) | 🔴 | i²CS 2025 (Nat Comm): interferential이나 **삽입형 epineural cuff** — 비침습 TIS 아님 |
| G-A2 | 방광 제어 경골신경 TIS: in silico만 존재, in vivo 전무 | 🔴 | Optimization Framework for TI Tibial Nerve Stimulation (MDPI Appl Sci, 2023): FEM만 |
| G-A3 | 설하신경 TIS: 단일 야간(1회) 연구만 존재 | 🟡 | Missey 2023: 반응률 50%, 장기 프로토콜 없음 |
| G-A4 | 척수/횡격막신경 TIS: rat in vivo 검증됨, 비침습 인체 적용 미완 | 🟡 | Sunshine 2021 (Nat Comm Bio): opioid/SCI 쥐 모델 검증; 인체 case series 3례(2024) |
| G-A5 | 말초신경 **n-phase TIS** 전무 (좌골신경 포함) | 🔴 | Botzanowski 2022/2025: 2-pair TIS만; n-phase 확장 없음 |

### F. nTIS 고유 갭

| ID | Gap | 분류 | 관련 논문 |
|----|-----|------|----------|
| G-N1 | 다중 심부 표적 동시 비침습 자극 전무 | 🔴 | Agrawal 2025: 침습 다중 표적만 존재 |
| G-N2 | n-phase에서 위상(φ) 최적화 알고리즘 없음 | 🔴 | RL focality opt. 2025: 2-pair TIS만; 위상 자유도 미포함 |
| G-N3 | n-phase 기전 시뮬레이션 전무 | 🔴 | Mirzakhalili 2020: 2-pair 분석; n-phase 확장 없음 |
| G-N4 | TI-Toolbox: 2-pair만 지원, nTIS 미지원 | 🟡 | TI-Toolbox 2025 (ScienceDirect) |

---

## 연구 주제 후보 — 우선순위

> 연구자 배경: ECG·RSP 신호처리 / MRI·CT 영상 / ML·DL (PyTorch)  
> 실험 인프라: TIS 자극기, ECG/HRV, Rat 동물실험 (**EEG 없음**)  
> 팀 진행 중: 설하신경 nTIS FEM + LED 팬텀 검증 + 논문 작성

| 우선순위 | 주제 | 관련 갭 | 실현 가능성 | 비고 |
|---------|------|---------|-----------|------|
| ⭐⭐⭐ | **경부 미주신경 비침습 nTIS** (rat HRV + 인체 taVNS 비교) | G-A1, G-A5 | 높 (ECG/HRV + Rat) | **최우선 추천** |
| ⭐⭐ | 말초신경 n-phase TIS 선택성 (rat 좌골신경) | G-A5 | 높 (Rat) | EMG 장비 확인 필요 |
| ⭐⭐ | 경골신경 TIS in vivo (rat 방광 조절) | G-A2 | 중 (Rat, cystometry 필요) | 방광압 측정 장비 필요 |
| ⭐ | SO 위상 잠금 폐쇄형 TIS × 수면 기억 | G-S4, G-C3 | 낮 (**EEG 필요**) | 장비 미보유 |
| ⭐ | TIS 반응 예측 모델 (EEG + ML) | G-T5, G-T6 | 낮 (**EEG 필요**) | 장비 미보유 |

---

## Research Gap 5분류 (2026-06-11 추가)

> 학술적 갭 유형별 체계화 — 논문 Introduction/Discussion 작성 기반

### Knowledge Gap — 이론적 이해 부재

| ID | Gap 내용 | 중요도 |
|----|---------|-------|
| KG-1 | TIS 심부 선택성 메커니즘: envelope detection이 심부에서만 일어나는지, 아니면 캐리어 자체 효과가 지배적인지 미규명 | ★★★★★ |
| KG-2 | 최적 Δf 선택 원리: "Δf = 목표 뇌 리듬" 가설의 신경생물학적 근거 부재 | ★★★★ |
| KG-3 | n-phase TIS에서 위상 φ 조작이 뉴런 방향성 반응에 미치는 원리 미규명 | ★★★★ |
| KG-4 | 말초신경 TIS에서 신경 섬유 선택성(A-β vs. A-δ vs. C fiber) 원리 미규명 | ★★★ |
| KG-5 | TIS와 단순 경피 전기 자극(TENS) 간 기전적 차이 불명확 | ★★★★ |

### Methodological Gap — 방법론 부재

| ID | Gap 내용 | 중요도 |
|----|---------|-------|
| MG-1 | 생체신호(ECG/EEG) 실시간 피드백 기반 폐쇄형(closed-loop) TIS 시스템 프레임워크 없음 | ★★★★★ |
| MG-2 | n-phase TIS 다중 표적 동시 최적화 알고리즘 없음 (위상 자유도 미활용) | ★★★★★ |
| MG-3 | TIS 연구에서 진정한 sham 조건 설계 방법 없음 (캐리어 효과 때문) | ★★★★ |
| MG-4 | 개인화 FEM 기반 TIS 파라미터 개인 맞춤화 방법론 없음 | ★★★★ |
| MG-5 | 말초신경 n-phase TIS 전극 배치 최적화 방법론 없음 | ★★★ |

### Evidence Gap — 임상적 증거 부재

| ID | Gap 내용 | 중요도 |
|----|---------|-------|
| EG-1 | 전체 인체 TIS 연구 20편, 820명 (Vassiliadis 2026) — 분야 전반 증거 극히 부족 | ★★★★★ |
| EG-2 | 경부 미주신경 비침습 TIS 인체/동물 임상 근거 전무 | ★★★★★ |
| EG-3 | 다중 세션 장기 효과 데이터 없음 (16/20편이 단일 세션) | ★★★★ |
| EG-4 | 3-phase TIS in vivo 효과 근거 전무 | ★★★★★ |
| EG-5 | 말초신경 n-phase TIS 기능적 결과(방광, 호흡, HRV) 근거 전무 | ★★★★ |
| EG-6 | 장기 안전성 데이터 없음 (FDA 미승인) | ★★★ |

### Contradictory Gap — 상충하는 증거

| ID | 상충 내용 | 시사점 |
|----|---------|-------|
| CG-1 | **캐리어 주파수**: 뇌전증 연구(2025 Brain Stim)에서 9 kHz > 1 kHz 시사, 표준 2 kHz 연구들과 충돌 | 최적 캐리어 주파수 체계적 비교 연구 기회 |
| CG-2 | **심부 선택성 실재 여부**: Rampersad 2019 등 계산 연구에서 표피 전기장이 여전히 큼, 실험 연구들은 심부 효과 주장 | 표피 vs. 심부 분리 실험 필요 |
| CG-3 | **Δf 공명 가설**: Violante 2023에서 지지, 다른 연구들에서 Δf-리듬 매핑 불일치 보고 | Δf 선택 체계적 비교 기회 |
| CG-4 | **말초신경 envelope extraction**: Wang 2023(JNE) — "peripheral nerve TIS is NOT driven by envelope extraction" → 뇌 TIS와 기전이 다를 수 있음 | 말초신경 TIS 메커니즘 독립적 규명 필요 |

### Application Gap — 응용 부재

| ID | Gap 내용 | 시장/임상 잠재력 |
|----|---------|--------------|
| AG-1 | **경부 미주신경 비침습 TIS** — taVNS 대비 더 선택적 미주신경 자극 | 자율신경 조절, 염증, 심장 리듬, 수면 |
| AG-2 | **경골신경 TIS 방광 조절** — OAB, SCI 환자 비침습 PTNS 대체 | OAB 치료기기 ~$5B 시장 |
| AG-3 | **n-phase TIS 말초신경 선택성** — 2-pair 대비 향상된 신경 분지 선택 | neuroprosthetics, FES |
| AG-4 | **설하신경 TIS 만성 프로토콜** — OSA 장기 치료 | OSA 치료기기 시장 |
| AG-5 | **3-phase TIS 다중 표적 in vivo** — DBS 대체 가능성 (PD, 뇌전증, 통증) | 신경조절 ~$8B 시장 |
| AG-6 | **생체신호 동기화 폐쇄형 TIS** — ECG/RSP 실시간 자율신경 조절 | 웨어러블 자율신경 치료기기 |

---

---

## 횡격막신경 / Glymphatic / 경골신경 TIS 특화 갭 (2026-06-11 추가)

> phrenic nerve TIS + tibial nerve TIS + glymphatic 활성화 문헌 분석 기반

### G-PH: 횡격막신경(Phrenic Nerve) TIS

| ID | Gap 내용 | 중요도 |
|----|---------|-------|
| G-PH1 | 경부 phrenic nerve **직접** 비침습 TIS 전무 (Sunshine 2021은 척수 C4-C5 경유 자극) | ★★★★★ |
| G-PH2 | 비침습 phrenic TIS 다중 세션 만성 반복 프로토콜 전무 | ★★★★ |
| G-PH3 | 3-phase TIS의 좌/우 phrenic nerve **독립** 제어 가능성 미탐색 | ★★★★★ |
| G-PH4 | C3/C4 SCI rat에서 경부 비침습 phrenic TIS 만성 호흡 회복 검증 전무 | ★★★★ |

### G-TN: 경골신경(Tibial Nerve) TIS

| ID | Gap 내용 | 중요도 |
|----|---------|-------|
| G-TN1 | 경골신경 TIS in vivo 전무 (Kim 2023 FEM만 존재, G-A2와 동일) | ★★★★★ |
| G-TN2 | TIS vs. 침습 PTNS 직접 비교 임상/동물 연구 전무 | ★★★★★ |
| G-TN3 | n-phase TIS tibial nerve vs. 인접 신경 선택성 검증 전무 | ★★★★ |

### G-GL: Glymphatic System × 신경 자극

| ID | Gap 내용 | 중요도 |
|----|---------|-------|
| G-GL1 | **비침습** 신경 자극으로 glymphatic system 직접 활성화 시도 전무 (세계 최초 영역) | ★★★★★ |
| G-GL2 | 호흡 패턴 최적화 × 비침습 phrenic TIS → CSF/glymphatic flux 연결 전무 | ★★★★★ |
| G-GL3 | TIS + ICG 방법론 결합 — glymphatic/lymphatic 흐름 직접 측정 전무 | ★★★★★ |
| G-GL4 | AD/수면 장애 환자에서 phrenic TIS 기반 glymphatic 치료 전무 | ★★★★ |

> **근거 논문:**
> - Sunshine et al. 2021 (Nat Comm Bio): TIS → phrenic motor neuron 활성화 가능성 증명 (척수 경유)
> - Dreha-Kulaczewski et al. 2015, 2017 (JNeurosci): 심호흡 시 CSF 흐름 3~5배 증가 실증
> - Fultz et al. 2019 (Science): 수면 서파-혈류-CSF 3-way coupling
> - Rasmussen et al. 2021 (Cell Reports): 피질 서파 → ISF 흐름 파동 직접 구동
> - 2026 최신 발견: 각성 상태 controlled breathing으로도 glymphatic 활성화 가능

---

## 신규 발견 논문 (2026-06-11)

| 논문 | 갭 연결 | 비고 |
|------|---------|------|
| Wang et al. 2023 (JNE) — "TIS in peripheral nerves NOT driven by envelope extraction" | CG-4, KG-4 | ⚠️ 요약 작성 필요 — 말초신경 TIS 메커니즘 반박 |
| Multi-channel TIS for PD (ScienceDirect 2025) — "Enhanced focality, deep brain" | G-N2, EG-4 | 요약 작성 필요 — 다채널 초점성 in silico |
| bioRxiv 2026 — "Feasibility of TIS of human brains using two arrays" | MG-4, EG-1 | 요약 작성 필요 |
| i²CS 2025 (Nat Comm Bio) — 미주신경 장기 선택적 interferential (cuff) | G-A1 | 비침습 아님 → G-A1 갭 유지 확인 |
| Frontiers 2025 — "Advances in TIS: a scoping review" | G-T1 | 분야 현황 종합 — 요약 작성 필요 |
| Sunshine et al. 2021 (Nat Comm Bio) — Phrenic nerve TIS for respiration (척수 경유) | G-PH1, G-A4 | ⭐ Phrenic TIS 분야 창시 논문 |
| Dreha-Kulaczewski et al. 2015/2017 (JNeurosci) — 심호흡 → CSF 흐름 3~5배 증가 | G-GL1, G-GL2 | ⭐ Glymphatic × 호흡 핵심 근거 |
| Kim et al. 2023 (MDPI Appl Sci) — TIS tibial nerve FEM 최적화 | G-TN1, G-A2 | 요약 작성 필요 — in vivo 없음 |

---

*Last updated: 2026-06-11*
