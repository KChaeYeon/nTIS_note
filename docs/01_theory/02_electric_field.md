# Electric Field Model

## 1. Maxwell's Equations in Tissue

생물학적 조직 내 준정적(quasi-static) 조건에서:

$$\nabla \cdot (\sigma \nabla \phi) = 0$$

여기서 $\sigma$는 전도도 텐서, $\phi$는 전기 포텐셜.

전기장: $\mathbf{E} = -\nabla \phi$

## 2. Superposition

TI stimulation에서 두 주파수 성분의 전기장은 선형 중첩:

$$\mathbf{E}_{total}(\mathbf{r}, t) = \mathbf{E}_1(\mathbf{r})\cos(2\pi f_1 t) + \mathbf{E}_2(\mathbf{r})\cos(2\pi f_2 t + \phi_0)$$

## 3. Envelope Calculation

진폭 envelope (벡터 형태):

$$E_{env}(\mathbf{r}) = \left| |\mathbf{E}_1(\mathbf{r})| - |\mathbf{E}_2(\mathbf{r})| \right|
\text{ to } |\mathbf{E}_1(\mathbf{r})| + |\mathbf{E}_2(\mathbf{r})|$$

최대 envelope은 $\mathbf{E}_1 \parallel \mathbf{E}_2$ 조건에서 달성된다.

## 4. Numerical Methods

- FEM (Finite Element Method): SimNIBS, ROAST
- 구형 도체 모델 (해석적 해)

---

*Last updated: 2026-06-04*
