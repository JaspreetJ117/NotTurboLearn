# Random Variables & Probability Distributions  
**TL;DR** – A *random variable* (RV) is a numeric description of an experiment’s outcome.  
Its *distribution* lists all possible values and their probabilities.  
Discrete RVs are shown with bar graphs; continuous RVs with curves.  
Key rules: probabilities ∈ [0, 1] and sum to 1.  
The *expectation* \(E[X]\) is the weighted average of the RV’s values.

---

## Key Concepts
- **Random Variable (RV)** – a variable that can take on different values in an experiment (often denoted \(X\)).  
- **Distribution** – a table, graph, or other description of the RV’s possible values and their probabilities.  
- **Discrete vs. Continuous** – discrete RVs use bar graphs; continuous RVs use smooth curves (PDFs).  
- **Probability Density Function (PDF)** – the graph of a distribution; for discrete RVs, a bar chart; for continuous RVs, a curve.  
- **Properties of a Probability Distribution**  
  - Each probability \(P(X=x)\) satisfies \(0 \le P(X=x) \le 1\).  
  - The probabilities over all possible \(x\) sum to 1.  
  - The set of possible \(x\) values is **exhaustive** (covers all outcomes).  
  - The outcomes are **mutually exclusive** (no overlap).  
- **Expectation / Mean** – denoted \(E[X]\); the average value of the RV.  

---

## Important Definitions
- **Random Variable (RV)** – a variable that can take on different values in an experiment.  
- **Distribution** – a description (table, graph, etc.) of the RV’s possible values and their probabilities.  
- **Probability Density Function (PDF)** – the graph that shows how likely each result is.  
- **Expectation \(E[X]\)** – the weighted average of the RV’s values:  
  \[
  E[X] = \sum_{x} x \cdot P(X=x)
  \]  
- **Classical Probability** – probability calculated by counting favorable outcomes over total outcomes.  

---

## Step‑by‑Step Explanations

### 1. Example: Coin Tosses
1. **Experiment** – Flip a fair coin 3 times.  
2. **RV** – Let \(X\) = number of heads.  
3. **Possible outcomes** – 0, 1, 2, 3 heads.  
4. **Count favorable outcomes**  
   - 0 heads: 1 way (TTT)  
   - 1 head: 3 ways (HTT, THT, TTH)  
   - 2 heads: 3 ways (HHT, HTH, THH)  
   - 3 heads: 1 way (HHH)  
5. **Total outcomes** – \(2^3 = 8\).  
6. **Probability distribution**  
   \[
   \begin{array}{c|c}
   x & P(X=x) \\ \hline
   0 & 1/8 \\
   1 & 3/8 \\
   2 & 3/8 \\
   3 & 1/8
   \end{array}
   \]  
7. **Check properties** – All probabilities ∈ [0, 1] and sum to 1.  

### 2. Plotting the Distribution
- **Discrete case** – draw a bar for each \(x\) with height \(P(X=x)\).  
- **Continuous case** – draw a smooth curve (PDF).  

### 3. Calculating Expectation
1. Multiply each value \(x\) by its probability.  
2. Sum the products.  
   \[
   E[X] = 0\cdot\frac{1}{8} + 1\cdot\frac{3}{8} + 2\cdot\frac{3}{8} + 3\cdot\frac{1}{8}
        = \frac{6}{8} = 0.75
   \]  

---

## Equations / Formulas

```math
P(X=x) \in [0,1] \quad \text{and} \quad \sum_{x} P(X=x) = 1
```

```math
E[X] = \sum_{x} x \cdot P(X=x)
```

---

## Examples

| Experiment | RV | Possible Values | Probabilities |
|------------|----|-----------------|---------------|
| Flip a coin 3 times | \(X\) = #heads | 0, 1, 2, 3 | 1/8, 3/8, 3/8, 1/8 |

*(No timestamps were provided in the transcript.)*

---

## Potential Exam Questions

1. **Define a random variable and give an example.**  
2. **Explain the difference between a discrete and a continuous probability distribution.**  
3. **State the two key properties that a probability distribution must satisfy.**  
4. **Given a probability table, verify whether it represents a valid distribution.**  
5. **Compute the expectation \(E[X]\) for a given discrete distribution.**  
6. **Sketch the probability density function for a discrete RV with values 0, 1, 2 and probabilities 0.2, 0.5, 0.3.**  
7. **Describe the classical method for calculating probability.**  

*(The professor explicitly mentioned that questions on these topics will appear on the exam.)*