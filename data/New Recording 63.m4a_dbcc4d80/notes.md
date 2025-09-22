# Logic Gates & Boolean Algebra – Lecture Notes  

**TL;DR**  
The lecture covered the fundamentals of digital logic: the basic gates (NOT, AND, OR, NAND, NOR), their truth tables, timing diagrams, and Boolean algebra rules (including De Morgan’s theorem). It also highlighted how to build more complex circuits (alarm, seat‑belt detector, window/door sensor) using only NAND gates, and gave hints on the types of questions that may appear on exams.

---

## Key Concepts
- **Logic Gates** – elementary building blocks that implement Boolean functions.  
- **Truth Tables & Timing Diagrams** – tools to describe gate behavior.  
- **Boolean Algebra** – algebraic manipulation of logical expressions.  
- **De Morgan’s Theorem** – key identities for converting between AND/OR and NAND/NOR.  
- **Universal Gates** – NAND (and NOR) can implement any other gate.  
- **Circuit Design** – constructing functional systems (alarm, seat‑belt detector, sensor network) with minimal gates.  
- **Exam Strategy** – focus on simple, “easy” questions first; avoid careless mistakes.

---

## Important Definitions
- **NOT (Inverter)** – outputs the opposite of the input.  
  - Symbol: `¬` or a bar over the variable.  
- **AND Gate** – outputs 1 only if all inputs are 1.  
  - Symbol: `∧` or multiplication (`·`).  
- **OR Gate** – outputs 1 if at least one input is 1.  
  - Symbol: `∨` or addition (`+`).  
- **NAND Gate** – NOT of AND: `¬(A·B)` or `A·B̅`.  
- **NOR Gate** – NOT of OR: `¬(A∨B)` or `A̅+B̅`.  
- **De Morgan’s Theorem** –  
  ```math
  ¬(A·B) = ¬A + ¬B
  ¬(A + B) = ¬A · ¬B
  ```  
- **Truth Table** – exhaustive list of input combinations and corresponding outputs.  
- **Timing Diagram** – visual representation of signal changes over time.

---

## Step‑by‑Step Explanations

### 1. Inverter (NOT Gate)
1. **Input**: `A` (0 or 1).  
2. **Output**: `¬A` (1 if `A`=0, 0 if `A`=1).  
3. **Truth Table**  
   | A | ¬A |
   |---|----|
   | 0 | 1  |
   | 1 | 0  |

### 2. AND Gate
1. **Inputs**: `A`, `B`.  
2. **Output**: `A·B`.  
3. **Truth Table**  
   | A | B | A·B |
   |---|---|-----|
   | 0 | 0 | 0   |
   | 0 | 1 | 0   |
   | 1 | 0 | 0   |
   | 1 | 1 | 1   |

### 3. OR Gate
1. **Inputs**: `A`, `B`.  
2. **Output**: `A + B`.  
3. **Truth Table**  
   | A | B | A+B |
   |---|---|-----|
   | 0 | 0 | 0   |
   | 0 | 1 | 1   |
   | 1 | 0 | 1   |
   | 1 | 1 | 1   |

### 4. NAND Gate (Universal Gate)
1. **Inputs**: `A`, `B`.  
2. **Output**: `¬(A·B)` (or `A·B̅`).  
3. **Truth Table**  
   | A | B | ¬(A·B) |
   |---|---|--------|
   | 0 | 0 | 1      |
   | 0 | 1 | 1      |
   | 1 | 0 | 1      |
   | 1 | 1 | 0      |

### 5. Building Other Gates with NAND
- **NOT**: connect both inputs of a NAND to the same signal.  
- **AND**: NAND followed by NOT (i.e., NAND + inverter).  
- **OR**: use De Morgan: `A + B = ¬(¬A·¬B)` → two NANDs for `¬A` and `¬B`, then a NAND of those outputs.

### 6. De Morgan’s Theorem (Proof Sketch)
1. Start with `¬(A·B)`.  
2. Apply Boolean identities:  
   ```math
   ¬(A·B) = ¬A + ¬B
   ```  
3. Similarly, `¬(A + B) = ¬A · ¬B`.  
4. These identities are used to simplify expressions and design circuits.

### 7. Example Circuit: Seat‑Belt Alarm
- **Inputs**: `CarOn` (1 if car started), `SeatBelt` (1 if belt fastened).  
- **Logic**: Alarm = `CarOn · ¬SeatBelt`.  
- **Implementation**: AND gate + inverter (or NAND + inverter).  
- **Behavior**: Alarm lights when car is on **and** seat belt is not fastened.

### 8. Example Circuit: Window/Door Sensor
- **Inputs**: `Win1`, `Win2`, `Door`.  
- **Logic**: Alarm = `¬(¬Win1 · ¬Win2 · ¬Door)` (i.e., any open).  
- **Implementation**: NAND of the inverted inputs (or OR of the inputs).  
- **Behavior**: Alarm lights if **any** of the three is open.

---

## Equations / Formulas

```math
\text{NOT: } \overline{A}
\text{AND: } A \cdot B
\text{OR: } A + B
\text{NAND: } \overline{A \cdot B}
\text{NOR: } \overline{A + B}
```

De Morgan’s Theorem:

```math
\overline{A \cdot B} = \overline{A} + \overline{B}
\overline{A + B} = \overline{A} \cdot \overline{B}
```

---

## Code Examples / Snippets
*None provided in the lecture.*

---

## Examples (with timestamps if mentioned)

| Time | Example | Description |
|------|---------|-------------|
| 0:00 | Inverter truth table | Shows `0 → 1`, `1 → 0`. |
| 0:15 | AND gate truth table | Demonstrates `1·1 = 1`, others 0. |
| 0:30 | OR gate truth table | Demonstrates `0+0 = 0`, others 1. |
| 0:45 | NAND gate truth table | Shows `1·1` inverted to 0. |
| 1:00 | Seat‑belt alarm circuit | `CarOn · ¬SeatBelt`. |
| 1:15 | Window/door sensor circuit | `¬(¬Win1 · ¬Win2 · ¬Door)`. |

*(Exact timestamps are approximate; the transcript did not provide explicit times.)*

---

## Potential Exam Questions

1. **Truth Table Construction**  
   - *“Draw the truth table for a 3‑input AND gate.”*  
   - *“What is the output of a NAND gate when inputs are 1 and 0?”*

2. **Boolean Simplification**  
   - *“Simplify the expression `¬(A·B) + A` using Boolean algebra.”*  
   - *“Apply De Morgan’s theorem to `¬(A + B)`.”*

3. **Circuit Design**  
   - *“Design a circuit that outputs 1 only when exactly two of three inputs are 1.”*  
   - *“Show how to implement an OR gate using only NAND gates.”*

4. **Timing Diagram Interpretation**  
   - *“Given the timing diagram for an AND gate, identify the output when inputs change from 0→1 at time t=5.”*

5. **Universal Gate Implementation**  
   - *“Using only NAND gates, construct a NOT gate, an AND gate, and an OR gate.”*  
   - *“Explain why NAND is considered a universal gate.”*

6. **Practical Application**  
   - *“Describe how you would build a seat‑belt alarm using logic gates.”*  
   - *“Explain the logic behind the window/door sensor alarm circuit.”*

> **Professor’s Hint:** “I will give you the input and four possible outputs; choose the correct one. These easy questions are worth a lot of marks, so double‑check your answer.”

---

**End of Notes**