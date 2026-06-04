# Basic Principles of Temporal Interference Stimulation

## 1. Background

Conventional transcranial electrical stimulation (tES) 방법들은 두피와 두개골의 낮은
전도도로 인해 심부 뇌 구조에 충분한 전류를 전달하기 어렵다.

TI stimulation은 이 문제를 우회하기 위해 두 개의 고주파 전류의 **간섭(interference)**을
이용한다.

## 2. Core Principle

두 전극 쌍에서 각각 주파수 $f_1$과 $f_2 = f_1 + \Delta f$의 사인파 전류를 인가하면,
두 전류가 겹치는 조직 내 깊은 부위에서 envelope 주파수 $\Delta f$를 가진 진폭 변조
신호가 생성된다.

$$
E(t) = E_1 \cos(2\pi f_1 t) + E_2 \cos(2\pi f_2 t)
$$

Envelope amplitude:

$$
|E_{env}(t)| \approx 2E_1 \cos\left(\pi \Delta f \cdot t\right) \quad \text{(when } E_1 = E_2\text{)}
$$

## 3. Key Reference

> Grossman, N., et al. (2017). Noninvasive deep brain stimulation via temporally interfering
> electric fields. *Cell*, 169(6), 1029–1041.

---

*Last updated: 2026-06-04*
