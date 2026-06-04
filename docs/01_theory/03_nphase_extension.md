# n-Phase TI Extension

## 1. Motivation

고전적 TI (2전극 쌍)의 한계:
- 전기장 초점 제어가 제한적
- Steerability(방향성 제어) 부재

n-phase TI는 $n$개의 전극 쌍을 사용하여 이를 극복한다.

## 2. General Formulation

$n$개의 전극 쌍 각각에 carrier frequency $f_k$와 위상 $\phi_k$를 적용:

$$\mathbf{E}_{total}(\mathbf{r}, t) = \sum_{k=1}^{n} \mathbf{E}_k(\mathbf{r}) \cos(2\pi f_k t + \phi_k)$$

모든 $f_k$가 동일하고 위상만 다를 때 (n-phase 간섭):

$$\mathbf{E}_{total}(\mathbf{r}, t) = \text{Re}\left[\left(\sum_{k=1}^{n} \mathbf{E}_k(\mathbf{r}) e^{j\phi_k}\right) e^{j 2\pi f t}\right]$$

## 3. Open Questions

- [ ] 최적 $n$은 얼마인가?
- [ ] 위상 최적화 알고리즘
- [ ] n-phase에서 envelope 정의의 일반화

---

*Last updated: 2026-06-04*
