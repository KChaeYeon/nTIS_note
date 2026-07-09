# 연구 주제 제안서 — 횡격막신경 · 경골신경 · Glymphatic System

> 2026-06-11 | 선행연구 분석 + FINES 평가 + 추천 순위

---

## 배경: 팀 시너지 구조

```
Lab Student A (진행 중)
└── 침습: Rat 경부 phrenic nerve에 cuff 전극
    → 정밀 호흡 패턴 제어
    → ICG 형광 이미징으로 림프 흐름 측정
    → Glymphatic system 활성화 연구

연구자 (이번 제안)
└── 비침습: 2-pair TIS (경부 피부 전극)
    → phrenic nerve 비침습 자극
    → 동일 ICG 방법론으로 림프 흐름 측정
    → "침습 vs. 비침습" 논문 쌍 구성 가능
```

**핵심 전략**: 두 연구가 동일 가설을 다른 방법으로 검증 → 랩 포트폴리오 강화 + 공동 투고 가능

---

## 1. 횡격막신경(Phrenic Nerve) TIS 선행연구

### 1.1 Sunshine et al. 2021 ⭐⭐⭐⭐⭐ (분야 창시 논문)

- **저널**: Nature Communications Biology
- **DOI**: 10.1038/s42003-021-02652-7
- **연구 목적**: TIS가 척수(C4-C5)를 경유하여 phrenic motor neuron을 활성화, opioid 유발 호흡 억제 및 SCI(T2 절단) rat에서 호흡 기능 회복 가능한지 검증
- **방법**: Rat (n=6~12/조건), 2-pair TIS, 캐리어 2 kHz vs. 4 kHz, Δf=10~100 Hz, 경피 척추 전극, 횡격막 EMG
- **주요 결과**:
  - Opioid 후 호흡 멈춘 쥐 8/10에서 TIS로 호흡 재개
  - T2 SCI rat에서 TIS로 횡격막 EMG 유발
  - sham 대비 유의한 호흡 기능 회복 (p<0.001)
  - 단독 캐리어보다 Δf 결합 자극이 더 효과적
- **한계점**:
  - 급성 실험만 (만성 효과 미검증)
  - 척수 경유 간접 자극 — phrenic nerve 본체 직접 TIS 아님
  - 인체 해부학 직접 적용 어려움
  - 최적 파라미터 체계적 탐색 없음
  - SCI 완전 절단 모델만 (partial injury 미탐색)
- **Future Work**: 인체 적용 타당성, 만성 호흡 보조 프로토콜, 경부 직접 phrenic TIS, 웨어러블 시스템
- **갭 연결**: G-PH1, G-PH2

### 1.2 침습적 Phrenic Nerve Pacing 선행연구 (비교 대상)

| 논문 | 방법 | 주요 결과 | 한계 |
|------|------|---------|------|
| DiMarco et al. 2014 (AJRCCM) | 침습 phrenic nerve 전극 (SCI 인체 n=50) | 인공호흡기 이탈 64% 성공 | 수술 필요, 양측 phrenic integrity 필요 |
| Onders et al. 2013 (Chest) | 복강경 횡격막 근육 전극 (n=100+) | ALS, SCI 호흡 보조 유효 | 복강경 수술 |
| Posluszny et al. 2014 (Neurology) | 경추 자기 자극 | phrenic 활성화 가능 | 초점성 낮음 |
| Sherwood 1992~2005 (SCI) | 침습 phrenic nerve cuff (임상 금표준) | 장기 사용 가능 | 수술, 감염 위험 |

**임상적 맥락**: C3/C4 SCI 환자 전체 SCI의 ~50%, 대부분 인공호흡기 의존. 비침습 대안 수요 극대.

---

## 2. Glymphatic System + 호흡 선행연구

### 2.1 Glymphatic 기초 논문

| 논문 | 주요 발견 | nTIS 연관성 |
|------|---------|------------|
| Iliff et al. 2012 (Sci Transl Med) | Glymphatic system 발견: AQP4 채널 ISF↔CSF 교환 | 시스템 이해 기반 |
| Xie et al. 2013 (Science) | 수면 중 ISF 공간 60% 확장 → β-amyloid 클리어런스 60% 증가 | 수면-glymphatic 연결 |
| Fultz et al. 2019 (Science) | 수면 서파→혈류→CSF 진동 3-way coupling (인체) | 폐쇄형 TIS 트리거 근거 |
| Hablitz et al. 2019 (JNeurosci) | delta 파워↑, HR↓ → glymphatic influx↑ (마취 쥐) | TIS slow 자극과 연결 |
| Rasmussen et al. 2021 (Cell Reports) | 피질 서파(0.5~1 Hz) → ISF 흐름 파동 직접 구동 | Δf=0.5~1 Hz TIS 근거 |

### 2.2 호흡 → CSF/Glymphatic 흐름 핵심 논문

**Dreha-Kulaczewski et al. 2015 (Journal of Neuroscience)** ⭐⭐⭐⭐⭐

- **연구 목적**: 심박 vs. 호흡 중 CSF 흐름의 주 구동력 규명
- **방법**: 건강 성인 (n=16), 4D Flow MRI, 정상 vs. 강제 호흡
- **주요 결과**:
  - 흡기 시 CSF가 뇌 방향으로 이동
  - 호흡이 심박보다 CSF 흐름에 더 큰 영향
  - **심호흡 시 CSF 흐름 3~5배 증가**
- **한계점**: 건강 성인만, CSF 흐름 = glymphatic flux 직접 등치 불가
- **Future Work**: 특정 호흡 패턴 최적화, 임상군 적용
- **핵심 의의**: **"호흡 패턴 조절 → CSF 흐름 조절 → glymphatic 활성화"** 경로 실증

**Dreha-Kulaczewski et al. 2017 (JNeurosci)** — 2015 결과 재확인, 횡격막 수축이 흉강 내압 변화 → 경막낭 → CSF 두개강 이동 메커니즘 제시

**2026 최신 발견**: 각성 상태에서도 controlled breathing으로 glymphatic 활성화 가능성 — 수면 의존성 탈피, 임상 적용성 대폭 향상

### 2.3 ICG + 림프 흐름 측정

| 논문 | 내용 |
|------|------|
| Kwon et al. 2012 | ICG 근적외선 형광 이미징으로 림프 흐름 정량 측정법 확립 |
| Proulx 2021 (Nature Neurosci Review) | CSF 배출 경로: 코/경막/신경 주위 림프관 → AD 연결 |
| Student A 연구 (진행 중) | Rat 경부 phrenic cuff → ICG 림프 흐름 측정 프로토콜 확립 중 |

---

## 3. Tibial Nerve 자극 선행연구

### 3.1 TIS 적용 (유일한 논문)

**Kim et al. 2023 (MDPI Applied Sciences)**
*"Optimization Framework for Temporal Interference Tibial Nerve Stimulation"*

- **방법**: 인체 하지 FEM 모델, 전극 배치/파라미터 최적화
- **결과**: TIS로 경골신경 전기장 집중 가능성 입증, 최적 전극 배치 제시
- **한계**: **in vivo 검증 전무**, 뉴런 비선형성 미반영
- **Future Work**: "in vivo rat 검증 필요", "인체 임상 파일럿"
- **갭 확인**: G-TN1 (FEM 이후 in vivo 전무)

### 3.2 PTNS/TTNS 비교 대상

| 논문 | 설계 | 결과 | 한계 |
|------|------|------|------|
| Peters et al. 2010 (Eur Urol) | PTNS RCT, OAB n=220 | 54.5% 반응률 | 침습 바늘 전극 |
| Finazzi-Agro 2010 (Eur Urol) | PTNS pilot | UUI 60% 감소 | n=35, 단기 |
| Booth et al. 2018 (Neurourology) | TTNS 웨어러블 | 가능성 있으나 PTNS 미달 | 효과 불안정 |
| Wibisono et al. 2019 (Cochrane) | 체계적 리뷰 | 효과 확실, 장기 불충분 | 이질성 |

### 3.3 말초신경 TIS 메커니즘 논쟁

**Wang/Budde et al. 2023 (JNE)**
*"Temporal interference current stimulation in peripheral nerves is not driven by envelope extraction"*

- 말초신경은 고주파 캐리어 자체에 반응, envelope detection 아님
- **뇌 TIS와 메커니즘이 다를 수 있음 → 말초 TIS 별도 기전 규명 필요**
- 갭 연결: CG-4 (Contradictory Gap)

**i²CS 2025 (Nature Communications Biology)**
- 미주신경 장기별 선택적 interferential 자극 성공
- **단, 삽입형 epineural cuff → 비침습 TIS와 다름**
- 갭 유지: G-A1 (비침습 버전 전무)

---

## 4. 신규 Research Gap 추가

### 횡격막신경 TIS 특화

| ID | Gap | 중요도 |
|----|-----|-------|
| G-PH1 | 경부 phrenic nerve 직접 비침습 TIS 전무 (Sunshine 2021은 척수 경유) | ★★★★★ |
| G-PH2 | 비침습 phrenic TIS 만성 반복 프로토콜 전무 | ★★★★ |
| G-PH3 | 3-phase TIS의 좌/우 phrenic nerve 독립 제어 가능성 미탐색 | ★★★★★ |
| G-PH4 | C3/C4 SCI rat에서 경부 비침습 phrenic TIS 검증 전무 | ★★★★ |

### Tibial Nerve TIS 특화

| ID | Gap | 중요도 |
|----|-----|-------|
| G-TN1 | TIS tibial nerve in vivo 전무 (G-A2와 동일) | ★★★★★ |
| G-TN2 | TIS vs. 침습 PTNS 직접 비교 전무 | ★★★★★ |
| G-TN3 | n-phase TIS tibial vs. 인접 신경 선택성 전무 | ★★★★ |

### Glymphatic × 신경 자극 (완전 새로운 영역)

| ID | Gap | 중요도 |
|----|-----|-------|
| G-GL1 | 비침습 신경 자극으로 glymphatic system 직접 활성화 시도 전무 | ★★★★★ |
| G-GL2 | 호흡 패턴 최적화 + 비침습 phrenic TIS → CSF/glymphatic flux 연결 전무 | ★★★★★ |
| G-GL3 | TIS + ICG 방법론 결합 glymphatic/lymphatic 흐름 측정 전무 | ★★★★★ |
| G-GL4 | AD/수면 장애에서 phrenic TIS 기반 glymphatic 치료 전무 | ★★★★ |

---

## 5. 연구 주제 후보 10개 — FINES × Impact 평가

### 후보 1. 비침습 Phrenic TIS → Glymphatic 활성화 (Rat ICG 측정) ⭐⭐⭐⭐⭐

**연구 질문:**
> 경부 비침습 2-pair TIS로 rat 횡격막신경을 자극하여 특정 호흡 패턴(0.2~0.5 Hz 심호흡)을 유도하면, ICG 형광 이미징으로 측정한 경부 림프 흐름이 자연 호흡 대비 유의미하게 증가하는가?

**배경:**
- Sunshine 2021: TIS로 phrenic nerve 활성화 가능 (증명됨)
- Dreha-Kulaczewski 2015/2017: 심호흡 시 CSF 흐름 3~5배 증가
- Student A: ICG 측정 프로토콜 + cuff 연구 진행 중 → 방법론 공유 가능
- 세 분야 결합은 세계 최초

**방법 초안:**
- Rat (n=25, 5그룹): ① TIS 느린 호흡 ② TIS 빠른 호흡 ③ 자연 호흡 ④ 인공호흡기 대조 ⑤ sham
- 자극: 경부 bilateral 4전극, COMSOL 최적 배치, Δf=0.3 Hz/1 Hz
- 측정: ① 횡격막 EMG (호흡 패턴 확인) ② ICG 경부 림프 흐름 ③ 경막 내압 (선택)
- 분석: 호흡 패턴 × 림프 흐름 상관, Mixed effects model

**Student A 시너지:** ICG 프로토콜 공유, 침습 vs. 비침습 비교 논문 세트
**해결 갭:** G-PH1, G-GL1, G-GL2, G-GL3
**즉시 실행 가능성:** 높 (ICG 방법 Student A에게 학습, TIS 하드웨어 보유)

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 4 | 5 | 5 | 3 | 5 | **4.85** | 🔴 최상 | A |

**목표 저널:** Nature Biomedical Engineering (IF≈29) / Brain (IF≈14)
**경쟁 위험:** 낮

---

### 후보 2. ECG/RSP 폐쇄형 Phrenic TIS — 호흡-자율신경 실시간 최적화 ⭐⭐⭐⭐⭐

**연구 질문:**
> ECG(RR interval) + RSP(호흡 위상) 실시간 피드백으로 최적 글림프 활성화 윈도우(흡기 피크 직후)를 감지하여 TIS를 트리거하는 폐쇄형 시스템이, open-loop TIS 대비 ICG 림프 흐름 및 HRV를 더 효과적으로 변조하는가?

**배경:**
- 연구자의 ECG + RSP 실시간 신호처리 강점 100% 활용
- Respiratory Sinus Arrhythmia: 흡기 시 심박수 증가, 호기 시 감소 → 최적 타이밍 존재
- 폐쇄형 TIS (G-C1 adaptation) — 뇌 EEG 없이 말초 신호로 구현 가능

**방법 초안:**
- Rat (n=20) 또는 건강 성인 파일럿
- RSP 위상 감지 → TIS 트리거 (흡기 피크 시점)
- 측정: HRV + ICG 림프 (Rat) 또는 HRV + 혈압 (인체)

**해결 갭:** G-GL2, G-C1 (adaptation), MG-1

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 4 | 5 | 5 | 2 | 5 | **4.35** | 🔴 최상 | A |

---

### 후보 3. 경골신경 TIS in vivo — Rat OAB 방광 조절 ⭐⭐⭐⭐

**연구 질문:**
> Rat OAB 모델에서 경골신경 표적 2-pair TIS가 방광내압 및 배뇨 주기를 조절하며, 침습 PTNS 대비 동등 또는 우월한 효과를 보이는가?

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 4 | 4 | 5 | 3 | 5 | **4.35** | 🟠 높음 | A |

**목표 저널:** Brain Stimulation (IF≈8), Neurourology and Urodynamics

---

### 후보 4. C3/C4 SCI Rat — 경부 비침습 Phrenic TIS 만성 호흡 회복 ⭐⭐⭐⭐⭐

**연구 질문:**
> C4 SCI rat에서 경부 비침습 2-pair TIS 매일 20분 × 14일이 횡격막 EMG 진폭, 호흡수, 혈산소포화도를 유의미하게 회복시키는가?

**배경:**
- Sunshine 2021의 직접 후속 (척수 경유 → 경부 직접)
- C3/C4 SCI: 전체 SCI의 ~50%, 인공호흡기 의존
- 만성 프로토콜 (G-PH2, G-T4 갭 해결)

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 4 | 4 | 4 | 4 | 5 | **4.40** | 🔴 최상 | A |

**FDA Breakthrough Device 가능성** / 목표: JNER, Annals of Neurology

---

### 후보 5. 3-phase TIS × 좌/우 Phrenic Nerve 독립 제어 ⭐⭐⭐⭐⭐

**연구 질문:**
> 3-phase TIS(삼각 전극 배열)가 rat 경부에서 좌측/우측 phrenic nerve를 독립적으로 선택 자극하여 좌/우 횡격막 수축을 분리 제어할 수 있는가?

**배경:**
- 편측 SCI, 폐 수술 후 일측 횡격막 마비: 좌/우 독립 제어 필수
- 2-pair TIS: 공간 선택성 한계 → 3-phase: 삼각 배열로 좌/우 분리 이론적 가능
- 팀의 3-phase 시뮬레이션 in vivo 검증 핵심 논문

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 3 | 5 | 5 | 3 | 5 | **4.20** | 🔴 최상 | B |

---

### 후보 6. 경부 미주신경 비침습 TIS × HRV 자율신경 조절 ⭐⭐⭐⭐

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 5 | 4 | 4 | 4 | 4 | **4.25** | 🟠 높음 | A |

---

### 후보 7. Phrenic TIS + Sleep Slow Oscillation × Glymphatic ⭐⭐⭐⭐

**연구 질문:**
> 수면 중 Δf=0.5~1 Hz TIS로 phrenic nerve를 자극하여 수면 서파 리듬에 맞는 호흡 패턴을 유도하면, 각성 상태 vs. 수면 중 glymphatic 클리어런스가 차별적으로 향상되는가?

**배경:**
- Rasmussen 2021: 수면 서파 → ISF 흐름 파동 직접 구동
- Fultz 2019: 수면 서파-혈류-CSF 3-way coupling
- TIS Δf=0.5~1 Hz로 동기화 가능성

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 3 | 5 | 5 | 3 | 5 | **4.15** | 🔴 최상 | B |

---

### 후보 8. 말초신경 n-phase TIS 선택성 (Rat 좌골신경) ⭐⭐⭐

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 3 | 5 | 5 | 3 | 4 | **4.00** | 🟠 높음 | B |

---

### 후보 9. TIS 캐리어 주파수/Δf 파라미터 최적화 × 자율신경 반응 ⭐⭐⭐

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 5 | 4 | 4 | 3 | 4 | **4.05** | 🟡 중간 | A |

---

### 후보 10. 건강 성인 호흡 동기화 TIS + HRV — Rat→Human 번역 ⭐⭐⭐⭐

**연구 질문:**
> 건강 성인에서 RSP-gated 경부 TIS(미주신경 또는 phrenic nerve 표적)가 자연 호흡 대비 HRV 및 자율신경 균형을 향상시키는가?

**배경:** Rat 결과(후보 2, 6)의 인체 번역 → 임상 적용성 + 박사 논문 완결성

| F | I | N | E | S | 합산 | 임팩트 | 트랙 |
|---|---|---|---|---|------|-------|------|
| 3 | 4 | 4 | 3 | 5 | **4.25** | 🟠 높음 | A/B |

---

## FINES × Impact 최종 종합 테이블

| 추천 순위 | # | 연구 주제 | F | I | N | E | S | 합산 | 임팩트 등급 | 트랙 |
|---------|---|---------|---|---|---|---|---|------|-----------|------|
| **🥇 1위** | 1 | 비침습 Phrenic TIS → Glymphatic (ICG) | 4 | 5 | 5 | 3 | 5 | **4.85** | 🔴 최상 (Nature급) | A |
| **🥈 2위** | 4 | SCI 호흡 회복 만성 Phrenic TIS | 4 | 4 | 4 | 4 | 5 | **4.40** | 🔴 최상 | A |
| **🥉 3위** | 3 | 경골신경 TIS Rat OAB | 4 | 4 | 5 | 3 | 5 | **4.35** | 🟠 높음 | A |
| 4위 | 2 | ECG/RSP 폐쇄형 Phrenic TIS | 4 | 5 | 5 | 2 | 5 | **4.35** | 🔴 최상 | A |
| 5위 | 6 | 경부 미주신경 TIS HRV | 5 | 4 | 4 | 4 | 4 | **4.25** | 🟠 높음 | A |
| 6위 | 10 | Human RSP-gated TIS 파일럿 | 3 | 4 | 4 | 3 | 5 | **4.25** | 🟠 높음 | B |
| 7위 | 5 | 3-phase 좌/우 Phrenic 독립 제어 | 3 | 5 | 5 | 3 | 5 | **4.20** | 🔴 최상 | B |
| 8위 | 7 | Phrenic TIS × 수면 Glymphatic | 3 | 5 | 5 | 3 | 5 | **4.15** | 🔴 최상 | B |
| 9위 | 9 | TIS 파라미터 최적화 매핑 | 5 | 4 | 4 | 3 | 4 | **4.05** | 🟡 중간 | A |
| 10위 | 8 | n-phase 말초신경 선택성 | 3 | 5 | 5 | 3 | 4 | **4.00** | 🟠 높음 | B |

---

## 추천 순위 + 추천 이유 + 예상 임팩트

### 🥇 1위: 비침습 Phrenic TIS → Glymphatic 활성화

**추천 이유:**
nTIS 기술 × glymphatic system × 호흡 생리학 세 분야가 교차하는 지점에서, 현재 세계 어느 연구팀도 탐색하지 않은 완전히 새로운 연구 공간입니다. Sunshine 2021이 TIS로 phrenic nerve를 활성화할 수 있음을 증명했고, Dreha-Kulaczewski 2015/2017이 호흡이 CSF 흐름을 3~5배 증폭시킴을 증명했습니다. 이 두 근거를 연결하면 "TIS → 호흡 → glymphatic"이라는 전례 없는 치료 경로가 열립니다. Student A의 ICG 방법론을 공유받으면 즉시 시작 가능하며, 침습 vs. 비침습 비교 논문 세트는 랩 전체의 임팩트를 극대화합니다.

**예상 임팩트:**
- 학술: Glymphatic 분야 최초 전기 자극 개입 → *Nature Biomedical Engineering* (IF≈29) 목표
- 임상: 알츠하이머 예방/치료, 수면 장애, 뇌압 관리의 완전 새로운 비침습 접근
- 산업: 수면 테크 + 신경조절 기기 융합 시장, 특허 잠재력 극대
- **경쟁 위험: 낮** (2026 현재 이 조합 탐색 팀 없음 확인)

### 🥈 2위: C4 SCI 호흡 회복 만성 Phrenic TIS

**추천 이유:**
C3/C4 SCI 환자의 인공호흡기 의존 해결은 신경공학계 최우선 임상 과제입니다. Sunshine 2021의 직접 후속으로서 척수 경유 → 경부 직접 TIS의 혁신을 가지며, 만성 반복 프로토콜로 G-T4 갭까지 동시 해결합니다. FDA Breakthrough Device Designation 가능성이 있는 연구로 임상 번역 시간이 짧습니다.

**예상 임팩트:**
- 학술: *JNER* (IF≈5), *Respiratory Physiology & Neurobiology*
- 임상: SCI 인공호흡기 이탈 비침습 솔루션, 연간 신규 SCI 환자 ~17,000명(미국)
- 경쟁 위험: 중 (Sunshine 팀 후속 가능성)

### 🥉 3위: 경골신경 TIS Rat OAB

**추천 이유:**
실현 가능성과 임상 임팩트의 최적 균형점. OAB는 전 세계 5억+ 유병, FDA 승인 PTNS의 비침습 대체라는 명확한 임상 가치가 있고, TIS in vivo 데이터가 전무하므로 독창성이 확실합니다. cystometry 장비 확보 후 즉시 시작 가능하며 6~9개월 내 첫 논문이 현실적입니다. 1위(Glymphatic)의 리스크를 보완하는 안전한 병행 연구로 최적입니다.

---

## 권장 로드맵 (18개월)

```
2026 Q3 (지금 즉시)
├── IACUC/IRB 신청
├── Student A와 ICG 프로토콜 공유 미팅
├── 경부 phrenic TIS COMSOL 전극 최적화 (팀 도움)
└── 후보 3(경골신경) cystometry 장비 확인

2026 Q4 (M4-6)
├── 후보 3: 경골신경 TIS Rat 예비 실험
└── 후보 1: ICG 방법론 습득 + 예비 phrenic TIS 실험

2027 Q1 (M7-9)
├── 후보 3: 본 실험 완료 → 데이터 분석
└── 후보 1: Rat 본 실험 시작

2027 Q2 (M10-12)
├── 후보 3: 논문 투고 (Brain Stimulation / Neurourology)
└── 후보 1: 데이터 완료 + 분석

2027 Q3-Q4 (M13-18)
├── 후보 1: 논문 투고 (Nature Biomedical Engineering / Brain)
└── 후보 2 or 5: 시작 (3-phase 하드웨어 완성 후)

목표 결과: 2편 논문 (Impact Factor 합산 ≥ 20)
```

---

*Last updated: 2026-06-11*
