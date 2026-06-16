# Research Proposal

> **상태:** ✅ **최종 결정 (2026-06-16)** — 경골신경(tibial nerve) TIS Rat OAB 조절 연구 (후보 3) 확정

---

## 팀 현황 요약 (2026-06-11 기준)

| 항목 | 내용 |
|------|------|
| 팀 진행 중 | 설하신경(hypoglossal nerve) nTIS 시뮬레이션 + 3D 정육면체/쥐 뇌 COMSOL + 2D LED 팬텀 → 논문 작성 중 |
| 3-phase TIS 시스템 | 수식 + COMSOL + 2D LED 팬텀 완료, **하드웨어 개발 중** |
| 즉시 사용 가능 | 2-pair TIS 하드웨어, ECG/HRV 측정, Rat 동물 인프라 |
| 미보유 | EEG (대여/공동연구 가능성 있으나 즉시 불가) |

---

## 연구 주제 후보 10개 (FINES 평가 완료)

### FINES 최종 요약 테이블

| # | 연구 주제 (압축) | F | I | N | E | S | 합산 | 트랙 | 추천 |
|---|---------------|---|---|---|---|---|------|------|------|
| 1 | 경부 미주신경 2-pair TIS Rat HRV | 5 | 4 | 4 | 4 | 4 | **4.25** | A | ⭐⭐⭐ |
| 2 | n-phase 말초신경 선택성 (rat 좌골신경) | 3 | 5 | 5 | 3 | 4 | 4.00 | B | ⭐⭐ |
| **3** | **경골신경 TIS Rat 방광 조절** | **4** | **5** | **5** | **3** | **5** | **4.45** | **A** | **✅ 최종 결정** |
| 4 | 캐리어 주파수 최적화 Rat ECG/HRV 매핑 | 5 | 4 | 4 | 3 | 4 | 4.05 | A | ⭐⭐ |
| 5 | SO 위상 잠금 폐쇄형 TIS × 수면 기억 | 2 | 5 | 5 | 4 | 5 | 4.05 | B | ⭐ |
| 6 | TIS 반응 예측 모델 (MRI + ML) | 3 | 4 | 4 | 3 | 4 | 3.65 | B | — |
| 7 | Δf 최적화 × 경부 TIS HRV 반응 | 5 | 4 | 4 | 3 | 4 | 4.05 | A | ⭐⭐ |
| 8 | 3-phase TIS 심부 초점성 c-Fos in vivo | 3 | 5 | 5 | 4 | 4 | **4.20** | B | ⭐⭐⭐ |
| 9 | RSP-gated TIS (호흡 동기화 폐쇄형) | 4 | 4 | 5 | 3 | 4 | 4.05 | A | ⭐⭐ |
| 10 | 장기 반복 TIS 안전성 (조직병리) | 5 | 3 | 3 | 4 | 4 | 3.75 | A | ⭐ |

> FINES = Feasibility / Innovation / Novelty / Evidence-base / Significance (각 1~5, 가중평균)

---

### Track A — 즉시 실행 가능 (2-pair TIS + ECG/HRV + Rat)

---

#### 후보 1. 경부 미주신경 비침습 2-pair TIS — Rat HRV 자율신경 반응 검증 ⭐⭐⭐

**연구 질문:**
> 경부 미주신경(cervical vagus nerve)을 표적으로 한 2-pair TIS가 Rat 모델에서 HRV 지표(RMSSD, LF/HF)를 통해 측정 가능한 자율신경 조절 효과를 유도하며, 이 효과는 sham 자극 대비 유의미한가?

**배경:**
- G-A1: 경부 미주신경 비침습 TIS 전무 (i²CS 2024/Nat Comm은 삽입형 cuff → 비침습 아님)
- taVNS는 귀 이갑개 분지만 자극 → TIS는 경부 미주신경 본체 직접 비침습 표적 가능
- 세계 최초 경부 비침습 TIS 자율신경 검증

**방법 초안:**
- 대상: Sprague-Dawley rat (n=20, 4그룹)
- 그룹: 2-pair TIS(경부), sham-TIS(Δf=0), 전신마취 대조, 각성 대조
- 자극: 캐리어 2/3 kHz, Δf=10 Hz, 20분
- 측정: ECG 연속 기록 → HRV (RMSSD, LF/HF, pNN50)
- 분석: Repeated measures ANOVA + effect size (Cohen's d) + 95% CI

**해결하는 갭:** G-A1, EG-2, AG-1
**즉시 실행 가능성:** 높 — 기존 TIS 하드웨어 + ECG/HRV + Rat 인프라 모두 보유
**팀 시너지:** hypoglossal nerve와 경부 해부학 공유, FEM 파이프라인 재활용
**목표 저널:** Journal of Neural Engineering, Brain Stimulation, Neuromodulation

---

#### ✅ 후보 3. 경골신경 TIS in vivo — Rat 과민성 방광 조절 【최종 결정 2026-06-16】

**연구 질문:**
> Rat 과민성 방광(OAB) 모델에서 경골신경 표적 2-pair TIS가 방광내압(cystometry) 및 배뇨 주기를 조절하며, 침습적 경골신경 자극(PTNS) 대비 유사한 억제 효과를 보이는가?

**배경:**
- G-A2: FEM 시뮬레이션만 존재(MDPI Appl Sci 2023), in vivo 전무
- PTNS(percutaneous tibial nerve stimulation): OAB FDA 1차 치료 승인 → TIS 비침습화 명확한 임상 가치
- 시장: OAB 치료기기 ~$5B (2025)

**방법 초안:**
- OAB 모델: Acetic acid(0.5%) 방광 주입
- 자극: 경골신경 주행 따라 발목 내측 4전극, Δf=20 Hz
- 측정: cystometry, 배뇨 빈도, 용적 임계점
- 대조군: PTNS(침습), sham TIS, 비처치

**해결하는 갭:** G-A2, AG-2, EG-5
**즉시 실행 가능성:** 높 (2-pair TIS + Rat), cystometry 장비 확인 필요
**팀 시너지:** 팀의 COMSOL FEM 파이프라인 → 경골신경 전기장 검증
**목표 저널:** Neurourology and Urodynamics, Brain Stimulation, JNE

---

#### 후보 4. TIS 캐리어 주파수 최적화 — Rat ECG/HRV 파라미터 매핑

**연구 질문:**
> TIS 캐리어 주파수(1, 2, 5, 10 kHz) 및 Δf(5, 10, 20, 40 Hz)의 조합이 경부 TIS Rat HRV 반응에 미치는 영향 차이와 최적 조합은?

**배경:** G-T2: 1 kHz 관습 vs. 9 kHz 우수성 논쟁 (뇌전증 2025) 미해결
**즉시 실행 가능성:** 높 — 후보 1과 인프라 동일, 결합 설계 가능
**해결하는 갭:** G-T2, G-T3

---

#### 후보 7. Δf 최적화 × 경부 TIS HRV 반응

**연구 질문:**
> Δf(5, 10, 20, 40 Hz)에 따라 경부 미주신경 TIS의 HRV 부교감 반응이 어떻게 다른가? (G-T3 체계적 검증)

**즉시 실행 가능성:** 높 — 후보 1과 결합 가능한 파라미터 탐색 실험
**해결하는 갭:** G-T3

> ⚡ **후보 1 + 4 + 7 통합 전략:** 단일 연구에서 "파라미터 최적화 → 최적 파라미터로 미주신경 효과 검증"으로 논문 완결성 극대화

---

#### 후보 9. RSP-gated TIS — 호흡 동기화 폐쇄형 TIS ⭐⭐

**연구 질문:**
> 호흡 주기(흡기 vs. 호기)에 동기화된 경부 TIS가 비동기(open-loop) TIS 대비 HRV 반응을 증폭시키는가?

**배경:**
- 호흡-미주신경 coupling (respiratory sinus arrhythmia): 흡기 시 심박 억제, 호기 시 심박 촉진
- tVNS 호흡 동기화 효과 일부 보고, TIS 버전 전무
- **연구자의 RSP 신호처리 강점과 완벽히 일치**

**방법 초안:**
- RSP 센서 → 실시간 호흡 위상 검출 → 흡기/호기에 TIS 트리거
- 측정: ECG → HRV 비교 (동기 vs. 비동기 vs. sham)

**해결하는 갭:** G-C1 (말초신경 버전 폐쇄형), MG-1
**즉시 실행 가능성:** 높 — RSP 센서 + ECG + TIS 하드웨어 트리거 인터페이스
**독자성:** 호흡-TIS 동기화 최초 연구, 연구자 신호처리 역량 핵심 활용

---

#### 후보 10. 장기 반복 TIS 안전성 — Rat 조직병리학적 평가

**연구 질문:**
> 2주간 일일 2-pair TIS가 rat 뇌·피부 조직에 조직병리학적 손상을 유발하는가?

**즉시 실행 가능성:** 높 — 팀 전체 임상 전환의 기반 데이터
**해결하는 갭:** G-T7 (장기 안전성)

---

### Track B — 3-phase TIS 하드웨어 완성 후

---

#### 후보 2. 말초신경 n-phase TIS 선택성 — Rat 좌골신경 분지 선택 ⭐⭐

**연구 질문:**
> 3-phase TIS가 rat 좌골신경의 특정 분지(tibial vs. peroneal)를 2-pair 대비 더 선택적으로 활성화하는가?

**방법 초안:**
- 전극: 3-phase 삼각 배열 vs. 2-pair 표준 배열
- 측정: 비복근 vs. 전경골근 EMG, Selectivity Index
**해결하는 갭:** G-A5, EG-4
**팀 시너지:** 팀의 3-phase TIS 시뮬레이션 → 연구자의 in vivo 검증

---

#### 후보 5. SO 위상 잠금 폐쇄형 TIS × 수면 기억 ⭐

**연구 질문:** SO up-state 동기화 TIS가 개방형 TIS 대비 수면 중 서술 기억 강화에 더 효과적인가?
**즉시 실행 가능성:** 낮 — EEG 장비 필요
**해결하는 갭:** G-S4, G-C1

---

#### 후보 6. TIS 반응 예측 모델 (MRI + ML)

**연구 질문:** 개인 해부학(두개골 두께, 전도도 등)이 TIS 전기장 및 생리 반응을 얼마나 예측하는가?
**즉시 실행 가능성:** 중 — 인체 IRB + MRI 접근 필요
**해결하는 갭:** G-T5, G-T6

---

#### 후보 8. 3-phase TIS 심부 초점성 — Rat c-Fos 조직학 검증 ⭐⭐⭐

**연구 질문:**
> 3-phase TIS가 2-pair TIS 대비 rat 해마에서 더 집중된 c-Fos 발현 패턴을 유도하는가?

**배경:** 팀의 3-phase TIS COMSOL 시뮬레이션의 직접 in vivo 검증 — 팀 논문 시리즈의 핵심 파트
**방법 초안:** 자극 2시간 후 뇌 적출 → c-Fos 면역조직화학 → 초점성 정량화
**해결하는 갭:** G-N2, G-N3 (nTIS 고유 갭)
**팀 시너지:** 팀 n-phase 논문의 in vivo 검증 파트로 공동저자 기여 or 독립 논문

---

## 지도교수 관점 최종 추천 전략

### 권장 투-트랙 로드맵

```
2026 Q3 (즉시 시작)
├── IACUC/IRB 신청
├── 전극 배치 FEM 최적화 (팀 도움)
└── 후보 3(경골신경-방광) 또는 후보 1(미주신경-HRV) 예비 실험

2026 Q4 ~ 2027 Q1
├── Track A 본 실험 완료 (후보 1~4, 7, 9 중 1개 선택)
├── 후보 4 + 7: 파라미터 탐색 (후보 1과 병행)
└── 논문 초고 시작

2027 Q1 (3-phase 하드웨어 완성 예상)
└── 후보 8 (c-Fos 검증) 착수 — 팀 n-phase 논문과 시너지

2027 Q2~Q3
├── Track A 논문 투고 (JNE / Neuromodulation / Brain Stimulation)
└── Track B 데이터 수집

2027 Q4
└── Track B 논문 투고 (팀 공동 or 독립)
```

### 최종 선택 전 확인 사항

- [ ] cystometry 장비 보유 여부 ← **확인 필요 (최우선)**
- [ ] IACUC/IRB 진행 가능한 동물 프로토콜 범위
- [ ] 3-phase 하드웨어 완성 예상 시점
- [x] 지도교수 관심: 경부 미주신경 vs. 경골신경 어느 쪽 우선? → **경골신경 결정**
- [ ] 목표 저널 수준 (단편 연구 vs. 학위논문 규모)

---

## 추가 발견 논문 (2026-06-11 업데이트, 요약 작업 예정)

| 논문 | 중요도 | 관련 갭 | 비고 |
|------|-------|---------|------|
| Wang et al. 2023 (JNE) — "TIS in peripheral nerves is NOT driven by envelope extraction" | ★★★★★ | CG-2, CG-4 | 말초신경 TIS 메커니즘 반박 논문 — 핵심 문헌 |
| Multi-channel TIS for PD (ScienceDirect 2025) — "Enhanced focality, deep brain targeting" | ★★★★ | G-N2, EG-4 | n-phase 초점성 in silico 선행 연구 |
| bioRxiv 2026 — "Feasibility of TIS of human brains using two arrays" | ★★★ | G-T1, MG-4 | 2-array TIS 인체 타당성 최신 계산 연구 |
| i²CS 2025 (Nat Comm Bio) — 미주신경 장기 선택적 interferential 자극 | ★★★★★ | G-A1 | 미주신경 fasicle selectivity — 비침습이 아닌 cuff이므로 G-A1 갭 유지 |
| Frontiers 2025 — "Advances in TIS: a scoping review" | ★★★ | G-T1 | 분야 현황 종합 리뷰 |
| Sunshine et al. 2021 (Nat Comm Bio) — Phrenic TIS for respiration (척수 경유) | ★★★★★ | G-PH1, G-A4 | ⭐ Phrenic TIS 분야 창시 논문 |
| Dreha-Kulaczewski et al. 2015/2017 (JNeurosci) — 심호흡 → CSF 흐름 3~5배 | ★★★★★ | G-GL1, G-GL2 | ⭐ Glymphatic × 호흡 핵심 근거 |

---

## 2라운드 분석 — 횡격막신경·경골신경·Glymphatic 주제 (2026-06-11 추가)

> 상세 분석: [proposal_phrenic_tibial_glymphatic.md](proposal_phrenic_tibial_glymphatic.md)

### 팀 시너지 구조

Lab Student A (진행 중): 침습 rat 경부 phrenic cuff → 정밀 호흡 제어 → ICG 림프 흐름 측정 → glymphatic 활성화  
**연구자 제안**: 비침습 경부 TIS → phrenic nerve → 동일 ICG 방법론 → "침습 vs. 비침습" 논문 쌍

### FINES 합산 최종 순위 (1라운드 + 2라운드 통합)

| 최종 순위 | 연구 주제 | FINES 합산 | 임팩트 | 트랙 | 결정 |
|---------|---------|-----------|-------|------|------|
| 🥇 1 | **비침습 Phrenic TIS → Glymphatic 활성화 (Rat ICG)** | **4.85** | 🔴 최상 (Nature급) | A | — |
| 🥈 2 | C4 SCI 만성 호흡 회복 Phrenic TIS | 4.40 | 🔴 최상 | A | — |
| 🥉 3 | **경골신경 TIS Rat OAB (= 1라운드 후보 3)** | **4.35** | 🟠 높음 | A | ✅ **최종 결정 (2026-06-16)** |
| 4 | ECG/RSP 폐쇄형 Phrenic TIS | 4.35 | 🔴 최상 | A | — |
| 5 | 경부 미주신경 TIS HRV (= 1라운드 후보 1) | 4.25 | 🟠 높음 | A | — |
| 6 | 3-phase 좌/우 Phrenic 독립 제어 | 4.20 | 🔴 최상 | B | — |

> 📄 10개 전체 후보 상세: [proposal_phrenic_tibial_glymphatic.md](proposal_phrenic_tibial_glymphatic.md)

### 업데이트된 확인 사항 (2026-06-16 경골신경 결정 후)

- [ ] cystometry 장비 보유 여부 ← **확인 필요 (최우선)**
- [x] 지도교수 방향성: glymphatic 고위험고보상 vs. 경골신경 안정적 고임팩트 → **경골신경 결정**
- [ ] IACUC/IRB 진행 가능한 동물 프로토콜 범위
- [ ] 3-phase 하드웨어 완성 예상 시점 (Track B 후보들)
- [ ] Rat 발목 COMSOL FEM 모델 착수 시점 확인 (팀 파이프라인 재활용)

---

*Last updated: 2026-06-16 — 경골신경 TIS (후보 3) 최종 결정*
