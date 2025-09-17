# Lecture Notes – Binary Arithmetic, Floating‑Point, and Number Systems  

**TL;DR**  
The lecture covered how computers represent signed integers (two’s complement), floating‑point numbers (IEEE‑754 single precision), and various base conversions (binary ↔ octal ↔ hexadecimal ↔ decimal). It also explained overflow detection, BCD arithmetic, Gray code, and ASCII. Key take‑aways: use bias for exponents, add 6 for BCD correction, and remember that Gray code changes only one bit between successive values.

---

## Key Concepts
- **Two’s Complement** – representation of negative integers; obtained by inverting bits and adding 1.  
- **Floating‑Point (IEEE‑754 single)** – 1 sign bit, 8‑bit exponent (bias = 127), 23‑bit mantissa (implicit leading 1).  
- **Overflow** – occurs when the result of an addition/subtraction has a different sign than both operands.  
- **BCD (Binary‑Coded Decimal)** – 4 bits per decimal digit; correction by adding 6 when sum > 9.  
- **Gray Code** – binary sequence where successive values differ by only one bit.  
- **Base Conversions** – use grouping of bits (3 for octal, 4 for hex) or repeated division/multiplication.  

---

## Important Definitions
- **Sign Bit** – first bit of a signed number; 0 = positive, 1 = negative.  
- **Exponent Bias** – constant added to the true exponent to obtain the stored exponent field.  
- **Mantissa (Fraction)** – bits after the implicit leading 1 in IEEE‑754.  
- **Two’s Complement** – `~x + 1` (bitwise NOT plus one).  
- **One’s Complement** – `~x` (bitwise NOT).  
- **BCD Correction** – if BCD sum > 9, add binary `0110` (decimal 6).  
- **Gray Code Property** – only one bit changes between consecutive codes.  

---

## Step‑by‑Step Explanations

### 1. Two’s Complement of –11
1. Write +11 in binary: `00001011`.  
2. Invert bits → `11110100`.  
3. Add 1 → `11110101`.  
4. Result: `11110101` represents –11.

### 2. Floating‑Point Encoding (Example: 13 + (–11))
- **Sign**: 0 (positive).  
- **Exponent**: true exponent = 12 → stored exponent = 12 + 127 = **139** (`10001011`).  
- **Mantissa**: binary of 13 is `1101`; drop leading 1 → `101000…` (23 bits).  

### 3. Overflow Detection in Addition
- Add two 8‑bit numbers.  
- If the carry into the sign bit differs from the carry out of the sign bit → **overflow**.  

### 4. BCD Addition & Correction
1. Add two 4‑bit BCD digits.  
2. If result > 9 (`1001`), add `0110`.  
3. Example: `1001` (9) + `0100` (4) = `1101` (13) → add `0110` → `0011` (3) with carry 1.  

### 5. Gray ↔ Binary Conversion
- **Binary → Gray**: `G[i] = B[i] XOR B[i+1]` (MSB unchanged).  
- **Gray → Binary**: `B[MSB] = G[MSB]`; for each lower bit, `B[i] = B[i+1] XOR G[i]`.  

### 6. Base Conversions
- **Binary → Octal**: group bits in 3s from LSB.  
- **Binary → Hex**: group bits in 4s from LSB.  
- **Decimal → Binary**: repeated division by 2.  
- **Decimal → Octal/Hex**: repeated division by 8/16.  
- **Octal/Hex → Binary**: map each digit to 3/4 bits.  

---

## Equations / Formulas

```math
\text{Stored Exponent} = \text{True Exponent} + \text{Bias}
```

```math
\text{Two’s Complement of } x = \sim x + 1
```

```math
\text{BCD Correction} = \begin{cases}
\text{sum} + 6 & \text{if sum} > 9 \\
\text{sum} & \text{otherwise}
\end{cases}
```

---

## Code Examples / Snippets

```python
# Two's complement of -11 in 8 bits
x = 11
twos_complement = (~x + 1) & 0xFF
print(bin(twos_complement))  # 0b11110101
```

```python
# BCD addition with correction
a = 0b1001  # 9
b = 0b0100  # 4
sum_ = a + b
if sum_ > 0b1001:
    sum_ += 0b0110
print(bin(sum_))  # 0b0011 (3) with carry
```

---

## Examples (from lecture)

| Operation | Binary | Result |
|-----------|--------|--------|
| 13 – 11 | `1101` – `1011` | `0010` (2) |
| Two’s complement of –11 | `11110101` | –11 |
| Floating‑point of 13 | Sign = 0, Exp = 139 (`10001011`), Mantissa = `101000…` | 13.0 |
| BCD addition 9 + 4 | `1001` + `0100` → `1101` → +`0110` → `0011` (3) |
| Gray code for 3 | `011` | Binary `010` |
| Hex `1A` to binary | `0001 1010` | 26 |

---

## Potential Exam Questions

1. **Two’s Complement**  
   *“Convert –11 to two’s complement using 8 bits.”*  
   *Answer:* `11110101`.

2. **Floating‑Point Encoding**  
   *“Encode the decimal number 13.0 in IEEE‑754 single precision.”*  
   *Answer:* Sign = 0, Exponent = 139 (`10001011`), Mantissa = `101000…`.

3. **Overflow Detection**  
   *“Explain how to detect overflow in an 8‑bit signed addition.”*  
   *Answer:* Compare carry into and out of the sign bit; if they differ, overflow occurred.

4. **BCD Correction**  
   *“Why do we add 6 when a BCD sum exceeds 9?”*  
   *Answer:* Because BCD uses only 10 values (0–9) out of 16 possible 4‑bit patterns; adding 6 brings the result back into the 0–9 range.

5. **Gray Code Property**  
   *“What is the key property of Gray code and why is it useful?”*  
   *Answer:* Only one bit changes between successive values, reducing errors in digital communication.

6. **Base Conversion**  
   *“Convert decimal 547 to binary, octal, and hexadecimal.”*  
   *Answer:* Binary `1000100011`, Octal `1053`, Hex `223`.

7. **Two’s Complement Subtraction**  
   *“Show how to compute 16 – 24 using two’s complement.”*  
   *Answer:* 16 (`00010000`) + two’s complement of 24 (`11100100`) = `11100100` (–8).

8. **Floating‑Point Bias**  
   *“What is the bias for single‑precision IEEE‑754 and how is it used?”*  
   *Answer:* Bias = 127; stored exponent = true exponent + 127.

9. **BCD to Decimal**  
   *“Convert BCD `0011 0101` to decimal.”*  
   *Answer:* 35.

10. **ASCII Code**  
    *“What is the ASCII code for the character ‘A’?”*  
    *Answer:* `01000001` (decimal 65).

---

**End of notes.**