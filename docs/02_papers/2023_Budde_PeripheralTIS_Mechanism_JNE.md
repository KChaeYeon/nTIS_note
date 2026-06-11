# 2023_Budde_PeripheralTIS_Mechanism_JNE

## 서지 정보

- **저자:** Ryan B Budde, Michael T Williams, Pedro P Irazoqui (Johns Hopkins University)
- **저널:** Journal of Neural Engineering, IF: 5.5
- **연도:** 2023
- **권호:** 20(2), 026041
- **DOI:** 10.1088/1741-2552/acc6f1
- **Semantic Scholar 확인:** ✅
- **검색일:** 2026-06-11

---

## 연구 질문

뇌 TIS의 작동 원리인 "envelope extraction"이 말초신경에서도 동일하게 적용되는가? 아니라면 말초신경 TIS는 어떤 메커니즘으로 작동하는가?

---

## 방법

- **설계:** In vivo 동물 실험 (Rat)
- **표본:** Long Evans Rat 30마리 (수컷 16, 암컷 14)
- **신경:** 좌골신경(sciatic nerve) — 경골/비복/비골 분지 근위부
- **전극:** 12-접점 맞춤형 cuff 전극 (Pt-Ir 합금, 50 μm 직경, 2열 × 6접점)
- **자극:** 캐리어 1~20 kHz, envelope 1~1000 Hz, 다양한 진폭 조합
- **기록:** 족저근(plantaris) + 대퇴이두근(biceps femoris) EMG (100~500 Hz bandpass)

### 핵심 비교 실험 설계

```
실험 1: TIS (f1=1kHz, f2=1.02kHz, Δf=20Hz)
        → CAP 발화 타이밍 기록
        결과: 20Hz 주기 아닌 캐리어(1kHz) 주기에 CAP 동기화

실험 2: Δf=20Hz 정현파 직접 자극 (동일 진폭)
        → CAP 기록
        결과: 20Hz 주기에 CAP 발화

비교: 실험 1 ≠ 실험 2 → envelope extraction 반박

실험 3: Undermodulation — 동일 peak-to-peak, envelope 진폭만 변화
        결과: 역치는 총 신호 진폭과 상관 (R²=0.93), envelope 진폭과 무관

실험 4: Amplitude steering
        결과: 한 신호 진폭 증가 → 활성화 최대점이 해당 소스 쪽으로 이동
              (envelope 이론 예측과 반대 방향)
```

---

## 주요 결과

### 핵심 발견: **말초신경 TIS는 envelope extraction이 아니다**

1. **RC 적분기 모델**: 신경막은 20 kHz까지 "거의 이상적인 적분기(near-ideal integrator)"처럼 행동
2. **비선형 envelope extraction 기여: <6%** — 무시할 수 있는 수준
3. **공간적 중첩이 이온채널 역학 전에 발생**: 두 전류의 순간 합산이 신경 활성화 결정
4. **역치 결정 인자**: Peak-to-peak 총 진폭 (R²=0.93)이 핵심, Δf 아님

### 뇌 TIS vs. 말초신경 TIS 메커니즘 비교

| | 뇌 TIS | 말초신경 TIS |
|---|---|---|
| 활성화 기전 | Envelope extraction (비선형 이온채널) | Instantaneous peak amplitude |
| 캐리어 역할 | 통과용 (뉴런 무반응) | 자체도 신경 활성화 유발 |
| Δf 역할 | 자극 주파수 직접 결정 | 간접적, 부차적 |
| 공간 선택성 근거 | Envelope 교차 지점 | 두 전류 합산 진폭 최대 지점 |

---

## 한계점

1. 좌골신경 in vitro / in vivo — 경골신경 직접 검증 아님
2. 개구리 신경 준비물 결과와의 일치/불일치 미비교
3. 온전한 생체 조직에서의 검증 제한 (마취 상태, 신경 노출)
4. 인체 말초신경에서의 검증 부재

---

## 관련 갭

- **CG-4 (Contradictory Gap)**: 이 논문이 CG-4의 핵심 근거 — 말초신경 TIS 기전 규명 연구 기회
- **G-TN3**: 경골신경 특화 메커니즘 규명 전무
- **KG-4**: 말초신경 TIS 섬유 선택성(A-β vs. C fiber) 원리 미규명

---

## nTIS 연구와의 연관성

**중요도: ⭐⭐⭐⭐⭐ (패러다임 전환)**

이 논문은 Tibial Nerve TIS 연구 설계에 근본적 영향:

1. **파라미터 최적화 재고**: Δf=20 Hz 선택이 중요하지만, 캐리어 주파수(1~5 kHz)와 순간 최대 전류 강도도 동등하게 중요
2. **공간 선택성 재검토**: 뇌 TIS처럼 envelope 교차 지점이 아닌, 두 전류의 합산 진폭이 최대인 지점에서 활성화 → FEM에서 TI envelope 대신 instantaneous peak 전기장도 계산 필요
3. **TTNS와의 차별점**: 말초신경에서 TIS의 이점은 "envelope 선택성"이 아닌 "4전극 배치로 인한 공간적 전류 집중" — 여전히 TTNS보다 유리할 수 있음
4. **연구 기회**: Rat 경골신경에서 Budde 2023 결과 재현 + OAB 억제 효과 동시 검증 → 메커니즘과 기능 두 마리 토끼

**2025년 Nature Comm (Opancar 2025)에서 이 결과 재확인됨**

*요약 작성: 2026-06-11*
