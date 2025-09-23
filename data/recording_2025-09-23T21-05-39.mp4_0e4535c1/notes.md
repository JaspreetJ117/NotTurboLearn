# Boolean Logic & Digital Design – Lecture Notes  
**TL;DR** – The lecture covered the **NOR gate** as a universal gate, De Morgan’s theorem, building NOT/AND/OR from NOR, XOR/XNOR basics, 2’s‑complement arithmetic, overflow, and binary/hex/BCD conversions.  The professor also explained the exam format (take‑home midterm, multiple‑choice final) and how grades are weighted.

---

## Key Concepts
- **NOR gate** – OR followed by NOT; truth table:  
  | X | Y | X + Y | (X + Y)’ | NOR |
  |---|---|-------|----------|-----|
  | 0 | 0 | 0     | 1        | 1   |
  | 0 | 1 | 1     | 0        | 0   |
  | 1 | 0 | 1     | 0        | 0   |
  | 1 | 1 | 1     | 0        | 0   |
- **Universal gate** – a gate that can implement any Boolean function (NOR and NAND are universal).
- **De Morgan’s theorem** –  
  \[
  (X\cdot Y)' = X' + Y', \qquad (X+Y)' = X' \cdot Y'
  \]
- **Constructing basic gates from NOR**  
  - NOT: `X NOR X`  
  - AND: ` (X NOR Y) NOR (X NOR Y)`  
  - OR: ` (X NOR X) NOR (Y NOR Y)`
- **XOR (exclusive OR)** – outputs 1 only when inputs differ.  
  | X | Y | XOR |
  |---|---|-----|
  | 0 | 0 | 0   |
  | 0 | 1 | 1   |
  | 1 | 0 | 1   |
  | 1 | 1 | 0   |
- **XNOR (exclusive NOR)** – outputs 1 only when inputs are equal.  
  | X | Y | XNOR |
  |---|---|------|
  | 0 | 0 | 1    |
  | 0 | 1 | 0    |
  | 1 | 0 | 0    |
  | 1 | 1 | 1    |
- **2’s complement** – to negate a binary number: invert all bits (1’s complement) and add 1.
- **Overflow in 2’s complement addition** – occurs when adding two numbers of the same sign yields a result of opposite sign.
- **Binary/Hex/Octal/BCD conversions** – standard positional systems; BCD uses 4 bits per decimal digit.
- **Programmable logic & VHDL** – describing hardware in software; ROM, EPROM, EEPROM concepts briefly mentioned.

---

## Important Definitions
- **NOR gate** – a logic gate that outputs the negation of the OR of its inputs.  
- **Universal gate** – a gate that can be used to implement any other gate.  
- **De Morgan’s theorem** – a pair of duality rules for negating AND/OR expressions.  
- **XOR** – exclusive OR; true when inputs differ.  
- **XNOR** – exclusive NOR; true when inputs are equal.  
- **2’s complement** – binary representation of negative numbers; obtained by inverting bits and adding 1.  
- **Overflow** – error when the result of an addition exceeds the representable range.  
- **BCD (Binary‑Coded Decimal)** – 4‑bit binary representation of each decimal digit.  
- **VHDL** – hardware description language used to model digital circuits.

---

## Step‑by‑Step Explanations

### 1. Proving De Morgan’s Theorem with a Truth Table
1. List all input combinations for X and Y.  
2. Compute `X·Y` and its complement `(X·Y)'`.  
3. Compute `X'` and `Y'`, then `X' + Y'`.  
4. Verify that `(X·Y)'` equals `X' + Y'` for all rows.

### 2. Building Gates from NOR
- **NOT**: `X NOR X` → outputs `X'`.  
- **AND**: ` (X NOR Y) NOR (X NOR Y)` → outputs `X·Y`.  
- **OR**: ` (X NOR X) NOR (Y NOR Y)` → outputs `X + Y`.

### 3. Constructing XOR from Basic Gates
1. XOR truth table shown above.  
2. Realize XOR using AND, OR, and NOT (or directly with NOR if desired).  
3. Verify with a truth table.

### 4. 2’s Complement Arithmetic
1. Write the binary number.  
2. Invert all bits → 1’s complement.  
3. Add 1 → 2’s complement.  
4. Check for overflow: if the sign bit changes unexpectedly, overflow occurred.

### 5. Binary ↔ Hex/Octal ↔ Decimal ↔ BCD
- **Hex to Binary**: each hex digit → 4 binary bits.  
- **Binary to Decimal**: sum of powers of 2.  
- **Decimal to BCD**: split decimal digits, encode each with 4 bits.  
- **BCD to Binary**: convert each 4‑bit group to its decimal value, then to binary.

---

## Equations / Formulas

```math
(X \cdot Y)' = X' + Y'
(X + Y)' = X' \cdot Y'
\text{2’s complement of } N: \; \overline{N} + 1
\text{Overflow condition: } \text{sign}(a) = \text{sign}(b) \land \text{sign}(a+b) \neq \text{sign}(a)
```

---

## Code Examples / Snippets

```python
# 2's complement of an 8‑bit number
def twos_complement(n):
    return (~n + 1) & 0xFF

print(twos_complement(0b00101101))  # example
```

---

## Examples (from lecture)

- **NOR truth table** (already shown above).  
- **XOR truth table** (already shown above).  
- **XNOR truth table** (already shown above).  
- **2’s complement of 0b011010** → `0b100110`.  
- **Hex F → Binary 1111**; Hex 3 → Binary 0011.  
- **Decimal 42.56 → BCD**: `0100 0010 . 0101 0110`.

---

## Potential Exam Questions

1. **Truth tables**  
   - Draw the truth table for a NOR gate.  
   - Draw the truth table for XOR and XNOR gates.

2. **De Morgan’s theorem**  
   - Prove `(X·Y)' = X' + Y'` using a truth table.  
   - Use De Morgan to simplify `¬(A + B)`.

3. **Universal gate construction**  
   - Show how to build an AND gate using only NOR gates.  
   - Show how to build a NOT gate using a NOR gate.

4. **2’s complement & overflow**  
   - Find the 2’s complement of `1011 0101`.  
   - Determine if adding `0110 0011` and `0101 1100` causes overflow.

5. **Conversions**  
   - Convert hex `2A` to binary and decimal.  
   - Convert decimal `123` to BCD.  
   - Convert binary `1101 0110` to octal.

6. **Exam policy**  
   - Explain the difference between the take‑home midterm and the final exam.  
   - How does missing the midterm affect the final grade weighting?

---

**End of notes.**