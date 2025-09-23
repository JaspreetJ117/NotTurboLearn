# Classical Probability & Conditional Probability – Exam‑Ready Notes  

**TL;DR**  
The lecture covered the fundamentals of classical probability, how to build and use frequency and probability tables, the addition and multiplication rules, and conditional probability (including Bayes’ theorem). A key real‑world example was the accuracy of rapid COVID tests, illustrating test sensitivity, specificity, false positives/negatives, and how prior probabilities affect posterior conclusions.  

---

## Key Concepts
- **Classical probability**: probability = favorable outcomes ÷ total outcomes when all outcomes are equally likely.  
- **Frequency table**: counts of outcomes for events and their intersections.  
- **Probability table**: frequency table divided by the total number of outcomes.  
- **Addition rule**:  
  \[
  P(A\cup B)=P(A)+P(B)-P(A\cap B)
  \]  
  *Mutually exclusive* case: \(P(A\cup B)=P(A)+P(B)\).  
- **Multiplication rule**:  
  \[
  P(A\cap B)=P(A)\,P(B|A)
  \]  
- **Conditional probability**: \(P(A|B)=\dfrac{P(A\cap B)}{P(B)}\).  
- **Bayes’ theorem** (rearranged multiplication rule):  
  \[
  P(A|B)=\frac{P(B|A)P(A)}{P(B)}
  \]  
- **Test sensitivity**: \(P(\text{Positive}\mid\text{Disease})\).  
- **Test specificity**: \(P(\text{Negative}\mid\text{No Disease})\).  
- **False positive**: \(P(\text{Positive}\mid\text{No Disease})\).  
- **False negative**: \(P(\text{Negative}\mid\text{Disease})\).  
- **Prior probability**: initial belief about the event before new evidence.  
- **Posterior probability**: updated belief after observing evidence.  

---

## Important Definitions
- **Event** – a subset of the sample space.  
- **Sample space** – all possible outcomes of an experiment.  
- **Mutually exclusive events** – events that cannot occur simultaneously.  
- **Independent events** – occurrence of one does not affect the probability of the other.  
- **Conditional probability** – probability of an event given that another event has occurred.  
- **Sensitivity** – true‑positive rate of a diagnostic test.  
- **Specificity** – true‑negative rate of a diagnostic test.  

---

## Step‑by‑Step Explanations

### 1. Building a Frequency Table (Card Deck Example)
1. **Identify events**:  
   - \(A\): card is an ace.  
   - \(B\): card is a spade.  
2. **Count outcomes**:  
   - Total cards = 52.  
   - Aces = 4.  
   - Spades = 13.  
   - Ace & spade (ace of spades) = 1.  
3. **Fill the table**  

|          | Spade | Not Spade | Total |
|----------|-------|-----------|-------|
| Ace      | 1     | 3         | 4     |
| Not Ace  | 12    | 36        | 48    |
| Total    | 13    | 39        | 52    |

4. **Convert to probability table** – divide each cell by 52.  

### 2. Using the Addition Rule
- Compute \(P(A\cup B)\) (ace or spade):  
  \[
  P(A)+P(B)-P(A\cap B)=\frac{4}{52}+\frac{13}{52}-\frac{1}{52}=\frac{16}{52}
  \]

### 3. Conditional Probability Example
- **Question**: What is \(P(\text{spade}\mid\text{ace})\)?  
  \[
  P(\text{spade}\mid\text{ace})=\frac{P(\text{ace}\cap\text{spade})}{P(\text{ace})}=\frac{1/52}{4/52}=\frac{1}{4}
  \]

### 4. Bayes’ Theorem (Rapid Test Example)
1. **Given**  
   - Prior \(P(\text{COVID})=0.40\).  
   - Sensitivity \(P(\text{Pos}\mid\text{COVID})=0.875\).  
   - Specificity \(P(\text{Neg}\mid\text{No COVID})=0.935\).  
2. **Compute false positives/negatives**  
   - \(P(\text{Pos}\mid\text{No COVID})=1-0.935=0.065\).  
   - \(P(\text{Neg}\mid\text{COVID})=1-0.875=0.125\).  
3. **Build joint probabilities** (multiply prior by conditional)  
   - \(P(\text{Neg}\cap\text{COVID})=0.40\times0.125=0.05\).  
   - \(P(\text{Neg}\cap\text{No COVID})=0.60\times0.935=0.561\).  
4. **Marginal probability of a negative test**  
   \[
   P(\text{Neg})=0.05+0.561=0.611
   \]  
5. **Posterior probability**  
   \[
   P(\text{COVID}\mid\text{Neg})=\frac{0.05}{0.611}\approx0.08
   \]  
   *Interpretation*: Even with a negative rapid test, there’s still an ~8 % chance of having COVID.  

---

## Equations / Formulas

```math
P(A\cup B)=P(A)+P(B)-P(A\cap B)
```

```math
P(A\cap B)=P(A)\,P(B|A)
```

```math
P(A|B)=\frac{P(A\cap B)}{P(B)}
```

```math
P(A|B)=\frac{P(B|A)P(A)}{P(B)}
```

---

## Code Examples / Snippets
*(None provided in the lecture transcript.)*

---

## Examples (with timestamps if mentioned)

| Time | Example | Key Point |
|------|---------|-----------|
| 0:00 | Deck of cards – frequency table | How to count and build tables |
| 0:15 | Ace or spade – addition rule | Demonstrates union probability |
| 0:30 | Conditional probability \(P(\text{spade}\mid\text{ace})\) | Shows how knowledge changes probability |
| 0:45 | Rapid COVID test – sensitivity & specificity | Real‑world application of Bayes’ theorem |

---

## Potential Exam Questions  
*(Professor explicitly mentioned that some of these will appear on the exam.)*

1. **Construct a frequency table** for a given set of events and compute the corresponding probability table.  
2. **Apply the addition rule** to find \(P(A\cup B)\) when \(P(A)=0.2\), \(P(B)=0.3\), and \(P(A\cap B)=0.05\).  
3. **Determine conditional probability** \(P(B|A)\) given a joint probability table.  
4. **Use Bayes’ theorem** to update the probability of having a disease after a positive test result, given sensitivity, specificity, and prior prevalence.  
5. **Explain the difference** between test sensitivity and specificity, and compute false‑positive and false‑negative rates.  
6. **Interpret a posterior probability** in a real‑world context (e.g., rapid test results).  

---

## Quiz & Homework Policy  
- **Two attempts per question**; questions remain the same between attempts.  
- Quizzes are treated as **homework** and study tools; they are not meant to be a quick way to score high.  
- Consistent weekly work leads to easier midterm performance.  

---