# 2023_Kim_TibialTIS_FEM_AppliedSci

## 서지 정보

- **저자:** Kim E, Ye E, Lee J, Kim T, Choi D, Lee K, Park S
- **저널:** Applied Sciences (MDPI), IF: 2.7
- **연도:** 2023
- **권호:** 13(4), 2430
- **DOI:** 10.3390/app13042430
- **Semantic Scholar 확인:** ⚠️ 확인 필요
- **검색일:** 2026-06-11

---

## 연구 질문

경골신경(tibial nerve)에 TIS(Temporal Interference Stimulation) 에너지를 선택적으로 집중시키기 위한 최적의 전극 배치 프레임워크를 FEM으로 개발할 수 있는가?

---

## 방법

- **설계:** In silico (FEM 시뮬레이션), 인체 MRI 기반
- **모델:** 인체 발목 내측 횡단면 MRI → 7개 조직 세그멘테이션
  - 조직: 피부, 피하지방, 근육, 힘줄, 경골신경 번들, 경골동맥, 경골/내과
- **소프트웨어:** COMSOL Multiphysics (AC/DC 모듈, Frequency Domain)
- **최적화:** 전극 위치 최적화(Electrode opt) vs. 병렬 배치(Parallel opt) 비교
- **목적 함수:** 초점성 지표 PR = E_envelope(tibial nerve) / E_envelope(non-target)
- **자극:** 2-pair TIS, 캐리어 주파수 1~5 kHz, Δf 10~100 Hz

---

## 주요 결과

- Electrode opt 그룹에서 PR (focality ratio) 유의하게 증가
- 개인 맞춤형 전극 배치가 표준 배치 대비 2~3배 향상된 경골신경 집중 달성
- 최적 전극 배치: 내측 복사뼈(medial malleolus) 전후방 대각선 배열
- 경골신경 TI envelope 강도: ~0.15~0.25 V/m/mA (1 mA 기준)
- TI-ratio (신경/표면): 표준 TTNS 대비 2~3배 향상

---

## 한계점

1. **In silico 연구만** — in vivo 검증 완전 부재 (가장 큰 한계)
2. 단일 해부학 모델 — 개인 간 해부학적 변동성 미반영
3. 뉴런 활성화 모델 미포함 (전기장 강도 ≠ 활성화 확률)
4. 조직 전도도 문헌 기반 단순화 (실제 측정값 아님)
5. 신경 내부 구조(perineurium, endoneurium) 세분화 미흡

---

## 관련 갭

- **G-TN1**: 이 논문의 in vivo 검증이 전무 — 최우선 연구 기회
- **G-A2**: FEM만 존재, in vivo 전무 — 동일 갭
- **G-TN3**: 개인 맞춤형 전극 배치의 임상 적용성

---

## nTIS 연구와의 연관성

**직접 연결**: 이 논문은 Tibial Nerve TIS in vivo 연구의 유일한 선행 FEM 근거.

- COMSOL 파이프라인: 팀이 보유한 FEM 파이프라인으로 Rat 스케일 모델 직접 재구성 가능
- 전극 배치 참고: 인체 모델 → Rat 스케일 다운 (발목 둘레 ~25 cm → ~30~40 mm)
- 최적화 결과가 실제 Rat 실험의 전극 배치 근거 제공

**연구 전략**: Kim 2023 FEM → Rat in vivo 검증 → 세계 최초 Tibial Nerve TIS in vivo 논문

*요약 작성: 2026-06-11*
