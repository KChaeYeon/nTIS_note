# Budde et al. 2023 — TIS in Peripheral Nerves: NOT Envelope Extraction

**Citation:** Budde RB, Blankenship KA, Wang B, Grill WM. Temporal interference current stimulation in peripheral nerves is not driven by envelope extraction. *Journal of Neural Engineering* 2023;20(2):026041. DOI: [10.1088/1741-2552/acbf8f](https://doi.org/10.1088/1741-2552/acbf8f)

---

## 핵심 요약

**TIS 말초신경 자극 메커니즘 논쟁 촉발 논문.** 포락선 추출(envelope extraction)이 TIS의 신경 활성화 원인이 **아님**을 전기생리학·계산모델로 실증. 대신 **peak-to-peak 진폭**이 결정적 인자.

---

## 연구 설계

| 항목 | 세부 사항 |
|------|----------|
| 모델 | in vitro 신경 (frog sciatic nerve, rat sciatic nerve) |
| 방법 | 세포외 기록 (compound action potential), RC 회로 분석 |
| 비교 | TIS vs 단순 kHz 자극, 포락선 주파수 변조 |

---

## 주요 주장 및 근거

### 기존 TIS 이론 (Grossman 2017)
$$E_{TI} = ||E_1 + E_2| - |E_1 - E_2||$$
→ 저주파 포락선이 신경세포막 RC 필터를 통과하여 발화 유도

### Budde 2023 반론

| 실험 | 결과 | 해석 |
|------|------|------|
| TIS vs AM 자극 비교 | 동일 발화 패턴 | 포락선 추출 아님 |
| kHz 자극 단독 | 신경 반응 있음 | kHz 자체가 원인 |
| RC 모델 분석 | 막 시정수(τ_m) >> 1/f_carrier | 막이 고주파 필터링 → 포락선만 통과 주장 반박 |
| peak-to-peak 진폭 | 임계값 결정 | 실제 활성화 결정인자 |

---

## 핵심 주장

> **"TIS에서 신경 발화는 포락선(Δf) 추출이 아닌, 합성파의 peak-to-peak 진폭에 의존한다."**

- 임상적 함의: Δf ≠ 자극 주파수 → TIS 주파수 선택성 재검토 필요
- 말초신경과 중추신경 메커니즘 차이 가능성 제기

---

## 관련 논쟁 타임라인

| 연도 | 논문 | 주장 |
|------|------|------|
| 2017 | Grossman et al. (*Cell*) | 포락선 추출로 심부 선택 자극 |
| 2021 | Sunshine et al. (*Comm Biol*) | 말초신경 TIS 비침습 실증 |
| 2022 | Botzanowski et al. (*Adv HM*) | 완전 경피 TINS 검증 |
| 2023 | **Budde et al. (*JNE*)** | **말초신경에서 포락선 추출 아님** |
| 2025 | Opančar et al. (*Nat Commun*) | TIS와 kHz 동일 메커니즘 확인 |

---

## nTIS 연구와의 연관성

- 경골신경 TIS 설계 시 **Δf를 자극 주파수로 직접 해석하면 안 됨**을 시사
- in vivo 검증에서 신경 발화 측정 방법 → compound action potential 기록 필요
- Rat 모델에서도 동일 논쟁 적용 → 실험 해석 시 peak-to-peak 진폭 우선 보고

---

*PMID: 36958037 | PMC10158317*
