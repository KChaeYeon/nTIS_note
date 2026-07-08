# TI 자극 공간 3구역 분류

## 학습 목표

LED phantom 실험에서 관찰되는 "항상 켜짐 / 깜박임 / 항상 꺼짐"을 AM 포락선 수식으로 설명하고,  
각 구역의 신경생리학적 의미(Activation / Inhibition / Subthreshold)를 정의할 수 있다.

---

## 전체 그림

```
전극A ←————————————————→ 중심 ←————————————————→ 전극B

  [Inhibition Zone]   [Activation Zone]   [Subthreshold Zone]   [Inhibition Zone]
  E_min > E_th         E_min < E_th         E_max < E_th          E_min > E_th
                        E_max > E_th

  LED: 항상 ON          LED: 40Hz 깜박임      LED: 항상 OFF         LED: 항상 ON
  신경: HFB (억제)      신경: 40Hz 발화       신경: 무반응           신경: HFB (억제)
```

---

## 핵심 변수 정의

두 채널의 전기장 진폭을 $A_1(\mathbf{r}),\; A_2(\mathbf{r})$ 라 하면,  
AM 포락선의 최댓값과 최솟값은 위치 $\mathbf{r}$ 마다 결정된다:

$$
E_{\max}(\mathbf{r}) = A_1(\mathbf{r}) + A_2(\mathbf{r}) \quad \text{(보강 간섭)}
$$

$$
E_{\min}(\mathbf{r}) = \left|A_1(\mathbf{r}) - A_2(\mathbf{r})\right| \quad \text{(상쇄 간섭)}
$$

- **전극 근처**: $A_1 \gg A_2$ → $E_{\min} \approx A_1$ (높음), 포락선 변조 깊이 낮음  
- **중심부**: $A_1 \approx A_2$ → $E_{\min} \approx 0$, 포락선이 거의 0까지 내려감

신경 활성화 역치를 $E_{th}$ 라 할 때, 세 구역이 정의된다.

---

## 3구역 분류

| 구역 | 조건 | LED 상태 | 신경 반응 | 위치 |
|------|------|----------|-----------|------|
| **Activation Zone** | $E_{\min} < E_{th} < E_{\max}$ | 40Hz 깜박임 | 40Hz 발화 | 중심부 (표적) |
| **Inhibition Zone** | $E_{th} \leq E_{\min}$ | 항상 ON | HFB — 억제 | 전극 근처 |
| **Subthreshold Zone** | $E_{\max} < E_{th}$ | 항상 OFF | 무반응 | 외곽 |

---

## ① Activation Zone — 왜 40Hz 발화인가?

포락선이 매 beat마다 $E_{th}$를 아래-위로 교차한다:

$$
E_{\min} < E_{th} < E_{\max}
\implies \text{포락선 주기마다 역치 교차} \implies \Delta f \text{ 발화}
$$

신경막은 **저역통과 필터** ($\tau_\text{membrane} \approx 5\text{–}20\,\text{ms}$):

- 1 kHz 캐리어 주기 = 1 ms ≪ $\tau$ → **추적 불가 → 반응 없음**
- 40 Hz 포락선 주기 = 25 ms ≈ $\tau$ → **추적 가능 → 발화**

> 핵심 통찰: 신경은 캐리어(1 kHz)를 무시하고, 포락선(40 Hz)만 "본다".

---

## ② Inhibition Zone — 왜 "억제"인가?

조건: $E_{\min} = |A_1 - A_2| \geq E_{th}$  
→ 포락선 최솟값조차 역치 이상 → LED 항상 ON

이 상황에서 신경에 일어나는 기전:

### 2-1. High-Frequency Block (HFB)

~1 kHz 연속 자극 → 전압개폐형 $\text{Na}^+$ 채널이 **비활성화(inactivated) 상태에 갇힘**  
→ 채널이 열리지 못함 → 활동전위 발생 불가

```
정상:     -70 mV → AP threshold(-55 mV) → 발화 → 재분극
HFB:      -70 mV → kHz 연속 자극 → Na+ 채널 비활성화
                 → 재분극 기회 없음 → 발화 불가
```

### 2-2. Wedensky Inhibition

고주파 연속 자극에 의한 **탈분극 블록(depolarization block)**:  
지속적 탈분극 → 막전위가 발화 역치 근방에 갇힘 → AP 생성 기전 자체가 마비

> "LED는 항상 켜지지만, 신경은 발화하지 못한다" — 이것이 inhibition의 본질

### TIS의 설계 이점

표면(피질) 신경 → Inhibition Zone → 자극 없음  
심부 표적 신경 → Activation Zone → 40Hz 선택적 자극  
→ 두개골 절개 없이 심부 선택적 자극 가능

---

## ③ Subthreshold Zone — 단순 무반응

$$
E_{\max} = A_1 + A_2 < E_{th}
$$

보강 간섭 최대치조차 역치에 못 미침 → LED 꺼짐, 신경 무반응.  
특별한 생리 기전 없음. 전극·중심에서 멀리 떨어진 외곽 영역.

> Subthreshold Zone의 존재 여부는 $E_{th}$ 값과 전극 배치에 따라 달라짐.  
> 소형 phantom에서는 없을 수 있고, 실제 뇌·말초신경 볼륨에서는 외곽에 반드시 존재.

---

## 정리: Inhibition Zone 공식 정의

> **Inhibition Zone**: AM 포락선 최솟값 $E_{\min} = |A_1 - A_2|$ 가 신경 활성화 역치 $E_{th}$를 초과하는 공간 영역.  
> 이 영역의 신경은 ~kHz 연속 자극에 의한 전압개폐형 $\text{Na}^+$ 채널 비활성화(HFB / Wedensky inhibition)로 기능적으로 억제된다.

---

## 다음 단계

- COMSOL에서 $E_{\min}$, $E_{\max}$ 맵 계산 및 3구역 경계 시각화
- $E_{th}$ 결정 방법: Strength-Duration Curve 기반
- dual overlay map (activation + inhibition 동시 표시) Python 구현
