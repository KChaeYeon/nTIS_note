# Lee 2021 — An Efficient Noninvasive Neuromodulation Modality for Overactive Bladder Using Time Interfering Current Method

**Citation:** Lee J, Park E, Kang W, Kim Y, Lee K-S, Park S-M. An Efficient Noninvasive Neuromodulation Modality for Overactive Bladder Using Time Interfering Current Method. *IEEE Transactions on Biomedical Engineering* 2021;68(1):214–224. DOI: [10.1109/TBME.2020.2995841](https://doi.org/10.1109/TBME.2020.2995841)

> 경골신경 TIS(ICT)를 OAB에 적용해 **동물 in vivo 효과**를 보고한 핵심 선행연구. nTIS의 직접 근거 논문.

---

## 초록 (Abstract)

*(Zotero에 abstract 미등록 — 아래 요약은 원문 및 이론 노트 [전자기 물리·FEM](../01_theory/05_EM_physics_FEM.md) 기반으로 작성)*

Interfering current(TIS)를 경골신경 자극(TNS)에 적용해 OAB를 조절하는 비침습 신경조절 기법을 제안하고, Rat in vivo 실험과 FEM 시뮬레이션으로 기존 경피 자극(TENS) 대비 효율·안전성을 정량 비교한다.

---

## 연구 질문

경골신경 OAB 치료에서, 고주파 간섭 전류(ICT/TIS)가 기존 경피 자극(TENS)보다 **더 낮은 표면 부담으로 더 강한 심부 신경 자극**을 낼 수 있는가?

## 방법

- **FEM 시뮬레이션**: Rat·인체 발목 모델에서 조직별 전도도(주파수 의존 $\sigma+j\omega\varepsilon$)로 $E_z$(경골신경 주행축 평행 성분) 분포 계산
- **포락선 정의**: $E_{z,env} = 2\min(|E_{z1}|, |E_{z2}|)$
- 자극 파라미터: $f_1 \approx 2$ kHz, $f_2 = f_1 + \Delta f$, $\Delta f = 10$ Hz
- **Rat in vivo** cystometry: 자극 역치, 방광 수축 빈도(aBCF), 배뇨량(aVV)을 ICT vs TENS 비교

## 주요 결과

- 신경 위치 $E_z$: **ICT가 TENS 대비 약 1.56배** (심부 도달 효율↑, 표면 전기장은 더 낮음 → 안전)
- 자극 역치: ICT **6.4 ± 1.5 V** vs TENS **10.7 ± 3.80 V** → ICT가 약 **1.67배 낮음** (p < 0.001)
- 방광 생리: aBCF **−16.8%** (p < 0.001), aVV **+7.38%** (p < 0.01) — 방광 과활성 완화와 상관
- 해석: 고주파 캐리어가 피부 임피던스를 낮춰 심부 침투를 높이고, 간섭으로 심부에서만 저주파 envelope 생성

## 한계점

- 급성 urethane 마취 Rat 모델 — 만성·각성 조건 및 장기 효과 미검증
- **envelope 추출** 전제에 기반한 해석 — 말초신경 기전 반박([2023_Budde_TIS_Not_Envelope_JNE](2023_Budde_TIS_Not_Envelope_JNE.md)) 고려 필요
- 경골신경 특화 전극·전류 최적화는 후속([2023_Kim_OptimizationFrameworkTemporal](2023_Kim_OptimizationFrameworkTemporal.md))에서 다룸
- 인과관계가 아닌 상관적 근거(자극–방광지표 변화)

## 관련 연구 갭 (nTIS)

경골신경 TIS의 초기 in vivo 근거이나, **최적 전극 배치·파라미터·만성 효과·PTNS 직접 비교**는 미해결 → `01_theory/13_research_gaps.md`의 G-TN1(in vivo 검증), G-TN2(vs PTNS)로 직접 연결. 본 연구(경골신경 nTIS)가 확장·검증하려는 baseline이다.
