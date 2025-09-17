# Variability, Variance & Standard Deviation  
**TL;DR** – In this lecture we covered the *population* vs *sample* distinction, how to compute the **mean**, **variance**, **standard deviation**, and **mean absolute deviation**. We also learned the *computational formula* for variance, the reason for using *\(n-1\)* in the sample variance (Venn’s correction), and how these concepts relate to the **normal distribution**, the **empirical rule**, and **Z‑scores**.  

---

## Key Concepts
- **Population vs Sample** – A population contains *all* units of interest; a sample is a subset.  
- **Mean (\(\mu\) or \(\bar{x}\))** – Average of a set of numbers.  
- **Variance** – Average of squared deviations from the mean.  
- **Standard Deviation** – Square root of variance; restores original units.  
- **Mean Absolute Deviation (MAD)** – Average of absolute deviations from the mean.  
- **Computational Formula** – A shortcut for variance that avoids a separate mean calculation.  
- **Venn’s Correction** – Divide by \(n-1\) for sample variance to obtain an unbiased estimator.  
- **Normal Distribution** – Symmetric, bell‑shaped curve; many natural phenomena follow it.  
- **Empirical Rule** – Roughly 68 % within 1σ, 95 % within 2σ, 99.7 % within 3σ.  
- **Z‑score** – Number of standard deviations a value is from the mean.

---

## Important Definitions
| Term | Definition |
|------|------------|
| **Population Mean (\(\mu\))** | \(\displaystyle \mu = \frac{1}{N}\sum_{i=1}^{N}x_i\) |
| **Sample Mean (\(\bar{x}\))** | \(\displaystyle \bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i\) |
| **Population Variance (\(\sigma^2\))** | \(\displaystyle \sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2\) |
| **Sample Variance (\(s^2\))** | \(\displaystyle s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2\) |
| **Population Standard Deviation (\(\sigma\))** | \(\displaystyle \sigma = \sqrt{\sigma^2}\) |
| **Sample Standard Deviation (\(s\))** | \(\displaystyle s = \sqrt{s^2}\) |
| **Mean Absolute Deviation (MAD)** | \(\displaystyle \text{MAD} = \frac{1}{n}\sum_{i=1}^{n}|x_i-\bar{x}|\) |
| **Z‑score** | \(\displaystyle z_i = \frac{x_i-\bar{x}}{s}\) (sample) or \(\displaystyle z_i = \frac{x_i-\mu}{\sigma}\) (population) |

---

## Step‑by‑Step Explanations

### 1. Calculating the Mean
1. **Sum** all observations \(x_i\).  
2. **Divide** by the number of observations \(n\) (sample) or \(N\) (population).  

### 2. Computing Variance
- **Table Method**  
  1. Compute each deviation \(d_i = x_i - \bar{x}\).  
  2. Square each deviation \(d_i^2\).  
  3. Sum the squared deviations.  
  4. Divide by \(n-1\) for a sample, \(N\) for a population.  

- **Computational Formula**  
  \[
  s^2 = \frac{\sum x_i^2 - \frac{(\sum x_i)^2}{n}}{n-1}
  \]
  (use \(N\) instead of \(n-1\) for population).

### 3. Deriving Standard Deviation
- Take the square root of the variance:
  \[
  s = \sqrt{s^2}, \qquad \sigma = \sqrt{\sigma^2}
  \]

### 4. Mean Absolute Deviation
1. Compute deviations \(d_i = x_i - \bar{x}\).  
2. Take absolute values \(|d_i|\).  
3. Average the absolute deviations.

### 5. Z‑score Calculation
\[
z_i = \frac{x_i - \bar{x}}{s}
\]
(Use \(\sigma\) if the population mean/variance is known.)

---

## Equations / Formulas

```math
\mu = \frac{1}{N}\sum_{i=1}^{N}x_i
```

```math
\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i
```

```math
\sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2
```

```math
s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2
```

```math
\sigma = \sqrt{\sigma^2}
```

```math
s = \sqrt{s^2}
```

```math
\text{MAD} = \frac{1}{n}\sum_{i=1}^{n}|x_i-\bar{x}|
```

```math
z_i = \frac{x_i-\bar{x}}{s}
```

**Computational Formula (sample)**  
```math
s^2 = \frac{\sum x_i^2 - \frac{(\sum x_i)^2}{n}}{n-1}
```

**Computational Formula (population)**  
```math
\sigma^2 = \frac{\sum x_i^2 - \frac{(\sum x_i)^2}{N}}{N}
```

---

## Examples (with timestamps)

| Time | Example | Key Takeaway |
|------|---------|--------------|
| **~12:15** | *Variance of a six‑sided die* | Population mean \(\mu = 3.5\). Squared deviations sum to 35. \(\sigma^2 = 35/6 \approx 2.91\). \(\sigma \approx 1.71\). |
| **~12:30** | *Sample variance of 10 COVID symptom‑day data* | Sample mean \(\bar{x} = 9.7\). Squared deviations sum to 114.8. \(s^2 = 114.8/(10-1) \approx 12.76\). \(s \approx 3.57\). |
| **~12:45** | *Mean Absolute Deviation of same data* | MAD ≈ 4.3 days. |
| **~13:00** | *Empirical rule check* | 68 % of 20 data points lie within \(\bar{x} \pm s\). |
| **~13:15** | *Z‑score for a value* | For \(x=12\), \(z = (12-9.7)/3.57 \approx 0.64\). |

---

## Potential Exam Questions  
*(Professor explicitly mentioned that some of these will appear on the quiz.)*

1. **Compute the sample mean and sample variance** for a given data set.  
2. **Explain why the sample variance uses \(n-1\)** instead of \(n\).  
3. **Derive the computational formula** for variance and apply it to a data set.  
4. **Calculate the mean absolute deviation** for a small sample.  
5. **Compare and contrast** MAD, variance, and standard deviation.  
6. **Plot a normal distribution** with a given mean and standard deviation; identify the 68‑95‑99.7 rule.  
7. **Compute a Z‑score** for a specific observation and interpret its meaning.  
8. **Explain the difference** between a population and a sample in the context of mean and variance.  
9. **Show how to convert** a population variance to a population standard deviation.  
10. **Discuss the empirical rule** and verify it with a provided data set.

---

## Quick Quiz & Practice Resources  
- **Quiz 1**: Covers material up to the end of this lecture (including variance, standard deviation, MAD, normal distribution, empirical rule, Z‑scores).  
- **Practice Sites**:  
  - *Khan Academy* – Statistics & probability practice.  
  - *Stat Trek* – Variance & standard deviation calculators.  
  - *OpenStax* – Interactive statistics problems.  
- **Video Textbook Program**: Available for review; watch the relevant sections on variability.

---

**End of notes.** Happy studying!