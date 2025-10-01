# Probability & Statistics Lecture Notes  
**TL;DR** – The class covered quiz logistics, a hands‑on blackjack expectation example, the mechanics of calculating **variance** and **standard deviation**, and a deep dive into the **binomial distribution** (definition, combinatorics, expectation, variance, and practical survey examples). The professor highlighted that questions about *“probability of two or fewer successes”* will appear on the exam.

---

## Key Concepts
- **Quiz schedule**: 1 quiz per week, due Monday evening, ~4 hrs total.
- **Blackjack expectation**: Use a table of outcomes → compute \(E[X] = \sum x\,p(x)\).
- **Variance**: \( \operatorname{Var}(X) = \sum (x-\mu)^2 p(x) \).
- **Standard deviation**: \( \sigma = \sqrt{\operatorname{Var}(X)} \).
- **Binomial distribution**: Discrete experiment with *n* independent trials, success probability *p*.
- **Combinatorics**: \( \binom{n}{k} = \frac{n!}{k!(n-k)!} \).
- **Binomial formulas**:
  - \( P(X=k) = \binom{n}{k}p^k(1-p)^{n-k} \)
  - \( E[X] = np \)
  - \( \operatorname{Var}(X) = np(1-p) \)
- **Survey example**: Treating a large population as effectively infinite → binomial model.
- **Factorial facts**: \(0! = 1\); powers of zero and one behave specially.

---

## Important Definitions
- **Expectation (Mean)** – The weighted average of all possible outcomes.
- **Variance** – The expected squared deviation from the mean.
- **Standard Deviation** – The square root of variance; measures spread.
- **Binomial Experiment** – A sequence of *n* independent trials, each with two outcomes (success/failure).
- **Success Probability** – The probability of a success in a single trial, denoted *p*.
- **Combinatorial Coefficient** – Number of ways to choose *k* successes from *n* trials.

---

## Step‑by‑Step Explanations

### 1. Calculating Expectation & Variance (Blackjack Example)
1. **List outcomes** \(x\) and their probabilities \(p(x)\) in a table.
2. **Expectation**:  
   \[
   \mu = E[X] = \sum_{i} x_i\,p(x_i)
   \]
3. **Deviation**: compute \(x_i - \mu\) for each outcome.
4. **Squared deviation**: \((x_i - \mu)^2\).
5. **Variance**:  
   \[
   \operatorname{Var}(X) = \sum_{i} (x_i - \mu)^2\,p(x_i)
   \]
6. **Standard deviation**: \(\sigma = \sqrt{\operatorname{Var}(X)}\).

> *Note*: No division by *n* is needed because the probabilities already sum to 1.

### 2. Binomial Distribution Basics
1. **Define** *n* (trials) and *p* (success probability).
2. **Compute** probability of exactly *k* successes:  
   \[
   P(X=k) = \binom{n}{k}p^k(1-p)^{n-k}
   \]
3. **Expectation**: \(E[X] = np\).
4. **Variance**: \(\operatorname{Var}(X) = np(1-p)\).
5. **Standard Deviation**: \(\sigma = \sqrt{np(1-p)}\).

### 3. Survey Example (10 people, 20% under‑employed)
- *n* = 10, *p* = 0.20.
- **Probability exactly 2 under‑employed**:  
  \[
  P(X=2) = \binom{10}{2}(0.20)^2(0.80)^8
  \]
- **Probability 2 or fewer**:  
  \[
  P(X\le 2) = P(0)+P(1)+P(2)
  \]
  where each term uses the binomial formula.

---

## Equations / Formulas

```math
E[X] = \sum_{i} x_i\,p(x_i)
```

```math
\operatorname{Var}(X) = \sum_{i} (x_i - \mu)^2\,p(x_i)
```

```math
\sigma = \sqrt{\operatorname{Var}(X)}
```

```math
P(X=k) = \binom{n}{k}p^k(1-p)^{n-k}
```

```math
\binom{n}{k} = \frac{n!}{k!(n-k)!}
```

```math
E[X]_{\text{binomial}} = np
```

```math
\operatorname{Var}(X)_{\text{binomial}} = np(1-p)
```

---

## Code Examples / Snippets

*No explicit code was provided in the lecture. The professor discussed Python list operations informally but did not present runnable code.*

---

## Examples (with timestamps if mentioned)

| Time | Example | Key Point |
|------|---------|-----------|
| 0:00 | Blackjack expectation table | Demonstrates \(E[X]\) calculation |
| 0:15 | Variance calculation for blackjack | Shows \((x-\mu)^2 p(x)\) method |
| 0:30 | Binomial survey (10 people, 20% under‑employed) | Computes \(P(X=2)\) and \(P(X\le2)\) |
| 0:45 | Factorial discussion (0! = 1) | Clarifies combinatorial calculations |

*(Exact timestamps were not provided; times are approximate.)*

---

## Potential Exam Questions

1. **Expectation & Variance**  
   - *Compute the expectation and variance of the blackjack payoff given the outcome table.*  
   - *Explain why we do not divide by *n* when computing variance from a probability table.*

2. **Binomial Distribution**  
   - *Given \(n=10\) and \(p=0.2\), calculate the probability that exactly 2 people are under‑employed.*  
   - *Find the probability that at most 2 people are under‑employed.*  
   - *Derive the expectation and variance formulas for a binomial distribution.*

3. **Combinatorics**  
   - *Show how to compute \(\binom{10}{2}\) using factorials.*  
   - *Explain why \(0! = 1\) and how it affects binomial coefficients.*

4. **Survey Approximation**  
   - *Justify treating a large population survey as a binomial experiment.*

> *Professor explicitly stated that at least one question about “probability of two or fewer successes” will appear on the exam.*

---

**End of Notes**