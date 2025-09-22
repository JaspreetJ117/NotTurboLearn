# Probability & Statistics – Lecture Notes (Exam‑Ready)

**TL;DR**  
The lecture covered the basics of probability: how to define a sample space, elementary and aggregation events, and the key operations (union, intersection, complement). It also introduced **classical**, **relative‑frequency**, and **subjective** probability, and explained the difference between **independent** and **dependent** events (with the gambler’s fallacy as a caution). Finally, the **coefficient of variation (CV)** was presented as a unit‑free risk metric.

---

## Key Concepts
- **Sample Space (S)** – the set of all possible outcomes of an experiment.  
- **Elementary Event** – the smallest indivisible outcome.  
- **Aggregation Event** – a collection of elementary events (e.g., “draw a heart”).  
- **Complement (A′)** – everything in the sample space that is *not* in event A.  
- **Union (A ∪ B)** – outcomes in A or B (or both).  
- **Intersection (A ∩ B)** – outcomes common to both A and B.  
- **Mutually Exclusive** – A ∩ B = ∅ (cannot happen together).  
- **Independent Events** – the occurrence of one does not affect the probability of the other.  
- **Dependent Events** – the occurrence of one changes the probability of the other.  
- **Classical Probability** – assumes all outcomes are equally likely.  
- **Relative‑Frequency Probability** – based on long‑run frequencies of events.  
- **Subjective Probability** – personal belief or expert judgment when data are lacking.  
- **Coefficient of Variation (CV)** – a dimensionless measure of relative variability:  
  \[
  \text{CV} = \frac{\sigma}{\mu}\times 100\%
  \]
- **Gambler’s Fallacy** – the mistaken belief that past outcomes influence future independent events.

---

## Important Definitions
| Term | Definition |
|------|------------|
| **Sample Space (S)** | Set of all possible outcomes of an experiment. |
| **Elementary Event** | A single, indivisible outcome. |
| **Aggregation Event** | A set of elementary events (e.g., “draw a heart”). |
| **Complement (A′)** | All outcomes not in event A. |
| **Union (A ∪ B)** | Outcomes in A or B (or both). |
| **Intersection (A ∩ B)** | Outcomes common to both A and B. |
| **Mutually Exclusive** | Two events that cannot occur simultaneously. |
| **Independent Events** | \(P(A \cap B) = P(A)P(B)\). |
| **Dependent Events** | \(P(A \cap B) \neq P(A)P(B)\). |
| **Classical Probability** | All outcomes equally likely. |
| **Relative‑Frequency Probability** | Probability estimated from observed frequencies. |
| **Subjective Probability** | Probability based on personal belief or expert opinion. |
| **Coefficient of Variation (CV)** | \(\displaystyle \frac{\sigma}{\mu}\times 100\%\) – a unit‑free risk metric. |

---

## Step‑by‑Step Explanations

### 1. Calculating the Coefficient of Variation
1. Compute the **standard deviation** (σ) of the data set.  
2. Compute the **mean** (μ).  
3. Divide σ by μ.  
4. Multiply by 100 to express as a percentage.  
   *Example:*  
   \[
   \text{CV} = \frac{5.36}{9.7}\times 100\% \approx 55.23\%
   \]
5. Interpret:  
   - **CV > 100 %** → highly variable/volatile.  
   - **CV < 100 %** → relatively stable.

### 2. Determining Probabilities in a 52‑Card Deck
1. **Total outcomes** = 52.  
2. **Probability of a specific card** = \(1/52\).  
3. **Probability of a rank (e.g., Ace)** = \(4/52 = 1/13\).  
4. **Probability of a suit (e.g., hearts)** = \(13/52 = 1/4\).  
5. **Probability of a red card** = \(26/52 = 1/2\).  
6. **Union of two events** (e.g., heart or Ace):  
   \[
   P(\text{heart or Ace}) = P(\text{heart}) + P(\text{Ace}) - P(\text{heart and Ace}) = \frac{13}{52} + \frac{4}{52} - \frac{1}{52} = \frac{16}{52} = \frac{4}{13}
   \]
7. **Complement**:  
   \[
   P(\text{not a heart}) = 1 - P(\text{heart}) = 1 - \frac{13}{52} = \frac{39}{52}
   \]

### 3. Sample Space for Two‑Card Draw (Order Matters)
1. First card: 52 possibilities.  
2. Second card (without replacement): 51 possibilities.  
3. Total outcomes: \(52 \times 51 = 2652\).  
4. If order did **not** matter, divide by 2 (but the lecture emphasized order matters).

### 4. Independent vs. Dependent Events
- **Independent**: Shuffle after each draw → probability of second draw unchanged.  
- **Dependent**: Draw two cards without shuffling → probability of second draw changes based on first card.

### 5. Classical vs. Relative‑Frequency vs. Subjective Probability
- **Classical**: All outcomes equally likely (e.g., fair coin, fair die).  
- **Relative‑Frequency**: Use long‑run frequencies (e.g., coin flips over many trials).  
- **Subjective**: Personal belief or expert judgment (e.g., predicting stock market moves).

---

## Equations / Formulas

```math
\text{Coefficient of Variation (CV)} = \frac{\sigma}{\mu}\times 100\%
```

```math
P(A') = 1 - P(A)
```

```math
P(A \cup B) = P(A) + P(B) - P(A \cap B)
```

```math
P(A \cap B) = 
\begin{cases}
0 & \text{if } A \text{ and } B \text{ are mutually exclusive} \\
P(A)P(B) & \text{if } A \text{ and } B \text{ are independent}
\end{cases}
```

---

## Examples (with timestamps if mentioned)

| Timestamp | Example | Key Point |
|-----------|---------|-----------|
| 00:00 | **Coefficient of Variation**: 5.36 ÷ 9.7 = 0.5523 → 55.23 % | Demonstrates CV calculation and interpretation. |
| 00:00 | **Card Probability**: Probability of drawing an Ace = 4/52 = 1/13 | Basic probability in a deck. |
| 00:00 | **Two‑Card Sample Space**: 52 × 51 = 2652 outcomes (order matters) | Illustrates combinatorial counting. |
| 00:00 | **Independent vs Dependent**: Drawing a card, shuffling, drawing again vs. drawing two cards without shuffling | Shows effect on probabilities. |
| 00:00 | **Gambler’s Fallacy**: Belief that a red ball is “due” after many reds | Common misconception in probability. |

---

## Potential Exam Questions

1. **Coefficient of Variation**  
   - *Compute the CV for a data set with σ = 5.36 and μ = 9.7. Interpret the result.*  
   - *When is a CV considered high or low?*

2. **Basic Card Probabilities**  
   - *What is the probability of drawing a heart or an Ace from a standard deck?*  
   - *What is the probability of drawing a card that is neither a heart nor an Ace?*

3. **Sample Space & Counting**  
   - *How many ordered two‑card draws are possible from a 52‑card deck?*  
   - *If order did not matter, how many distinct two‑card combinations would there be?*

4. **Independent vs Dependent Events**  
   - *Explain why drawing two cards without replacement results in dependent events.*  
   - *Give an example of an independent event in a card‑drawing scenario.*

5. **Probability Types**  
   - *Define classical, relative‑frequency, and subjective probability. Provide an example for each.*  
   - *Why is relative‑frequency probability often used in business and science?*

6. **Set Operations in Probability**  
   - *Write the formula for \(P(A \cup B)\) and explain each term.*  
   - *If A and B are mutually exclusive, simplify the formula for \(P(A \cup B)\).*

7. **Gambler’s Fallacy**  
   - *Describe the gambler’s fallacy and give an example involving a roulette wheel.*  
   - *Why is this fallacy incorrect from a probability standpoint?*

8. **Complement Rule**  
   - *If \(P(A) = 0.3\), what is \(P(A')\)?*  
   - *Explain the complement rule in your own words.*

These questions reflect the professor’s emphasis on probability fundamentals, set operations, and real‑world applications such as gambling and risk measurement. Good luck studying!