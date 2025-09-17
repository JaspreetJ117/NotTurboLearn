# VBA & Excel Fundamentals – Chapter 3 & 4 Review  
**TL;DR** – This lecture covers the basics of VBA programming in Excel: how to use **IntelliSense** for quick code completion, create and rename **modules**, record simple macros, and understand the limits of recorded code. It also reviews Excel fundamentals: cell references (relative vs. absolute, A1 vs. R1C1), common functions (SUM, VLOOKUP, PMT, etc.), error types, chart creation, sheet protection, and basic UI manipulation (hide/unhide, copy sheets, insert text boxes).  

---

## Key Concepts
- **IntelliSense** – auto‑completion, syntax highlighting, and error detection in the VBA editor.  
- **Modules** – containers for VBA code; each module can hold multiple **subroutines** (`Sub … End Sub`).  
- **Macro recording** – records user actions into VBA code; useful for repetitive tasks but cannot handle loops, controls, or advanced DB operations.  
- **Cell references** –  
  - *Relative* (e.g., `A1`) – changes when copied.  
  - *Absolute* (e.g., `$A$1`) – stays fixed.  
  - *A1 notation* vs. *R1C1 notation* (e.g., `R2C4`).  
- **Common Excel functions** – `SUM`, `VLOOKUP`, `PMT`, `SQRT`, `SIN`, `COS`, `TAN`, `ABS`, `LOG`, `EXP`, `SUMIF`, `AVERAGEIF`.  
- **Error types** – `#N/A`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#NUM!`, `#REF!`, `#NULL!`.  
- **Chart creation** – insert chart, use Design tab to add axis titles, legend, etc.  
- **Sheet protection** – lock cells, hide sheets, insert text boxes, and format cells.  

---

## Important Definitions
- **IntelliSense** – a feature in the VBA editor that provides code completion, parameter info, and syntax highlighting.  
- **Module** – a file in the VBA project that stores code; can contain multiple subroutines and functions.  
- **Subroutine** (`Sub … End Sub`) – a block of code that performs a task but does not return a value.  
- **Macro** – a recorded or written sequence of actions that can be executed with a single command.  
- **Relative reference** – a cell address that changes when the formula is copied.  
- **Absolute reference** – a cell address that remains constant when copied (denoted by `$`).  
- **A1 notation** – the standard Excel cell reference format (e.g., `B3`).  
- **R1C1 notation** – an alternative reference format where rows and columns are numbered (e.g., `R2C4`).  
- **VLOOKUP** – a function that looks up a value in the first column of a table and returns a value in the same row from a specified column.  

---

## Step‑by‑Step Explanations

### 1. Using IntelliSense in VBA
1. Open the **Developer** tab → **Visual Basic**.  
2. In the code window, start typing a keyword (e.g., `Sub`).  
3. IntelliSense shows a list of completions; press **Tab** or **Enter** to insert.  
4. While typing, IntelliSense highlights syntax errors (e.g., missing `=`).  

### 2. Creating a Module and a Subroutine
```vba
Sub pest()
    ' Your code here
End Sub
```
- Place the cursor inside the `Sub … End Sub` block.  
- Use **Ctrl+Space** to trigger IntelliSense for variables, functions, etc.  

### 3. Renaming a Module
1. In the **Project Explorer**, right‑click the module name.  
2. Choose **Rename** → type the new name (e.g., `Module1`).  

### 4. Recording a Macro
1. Developer → **Record Macro**.  
2. Perform the actions you want to automate (e.g., fill cells, calculate formulas).  
3. Click **Stop Recording**.  
4. The generated code appears in the module.  

### 5. Working with Cell References
- **Relative**: `A1` → changes when copied.  
- **Absolute**: `$A$1` → stays fixed.  
- **Mixed**: `$A1` or `A$1`.  
- **R1C1**: `R2C4` refers to the cell in row 2, column 4.  

### 6. Using Common Functions
- `=SQRT(A3^2 + E3^2)` – calculate the hypotenuse.  
- `=SIN(Radians)` – convert degrees to radians first (`=PI()/180*Degrees`).  
- `=VLOOKUP(205, A1:B10, 2, FALSE)` – lookup value 205 in column A.  
- `=PMT(rate, nper, pv)` – calculate mortgage payment.  

### 7. Handling Errors
| Error | Meaning | Example |
|-------|---------|---------|
| `#N/A` | Value not available | `=VLOOKUP(999, A1:B10, 2, FALSE)` |
| `#DIV/0!` | Division by zero | `=A1/B1` when `B1=0` |
| `#VALUE!` | Wrong data type | `=A1+"text"` |
| `#NAME?` | Unrecognized name | `=SINE(30)` |
| `#NUM!` | Invalid numeric value | `=SQRT(-1)` |
| `#REF!` | Invalid reference | `=A1+Z1` after deleting column Z |
| `#NULL!` | Space between references | `=A1 B1` |

### 8. Creating a Chart
1. Select data range.  
2. Insert → **Chart** → choose type.  
3. Use the **Design** tab to add axis titles, legend, etc.  

### 9. Protecting a Sheet
1. Review → **Protect Sheet**.  
2. Set a password if desired.  
3. Choose what actions are allowed (e.g., formatting cells).  

### 10. Adding a Button to Run a Macro
1. Developer → **Insert** → **Button (Form Control)**.  
2. Draw the button on the sheet.  
3. Assign the macro (e.g., `Module1`).  

---

## Equations / Formulas

```math
\text{Radians} = \frac{\pi}{180} \times \text{Degrees}
```

```vba
' Example formula in VBA
Range("B3").Formula = "=SQRT(A3^2 + E3^2)"
```

---

## Code Examples / Snippets

```vba
' Example Subroutine
Sub pest()
    MsgBox "Hello, world!"
    Range("B3").Value = 0
    Range("C3").Value = 5
    ' ... additional code ...
End Sub
```

```vba
' Example of using absolute reference
Range("$A$1").Value = 10
```

```vba
' Example of VLOOKUP
Dim result As Variant
result = Application.WorksheetFunction.VLookup(205, Range("A1:B10"), 2, False)
```

---

## Examples (with timestamps if mentioned)

| Time | Example | Description |
|------|---------|-------------|
| 0:00 | `Sub pest()` | Starting a subroutine. |
| 0:15 | `MsgBox "Hello"` | Displaying a message box. |
| 0:30 | `Range("A1")` | Referencing a cell. |
| 1:00 | `=SQRT(A3^2 + E3^2)` | Calculating a hypotenuse. |
| 1:45 | `VLOOKUP(205, A1:B10, 2, FALSE)` | Looking up a value. |
| 2:30 | `PMT(0.05/12, 60, 10000)` | Mortgage payment calculation. |

*(Exact timestamps are approximate; the transcript did not provide precise times.)*

---

## Potential Exam Questions

1. **IntelliSense**  
   - *What features does IntelliSense provide in the VBA editor?*  
   - *How does IntelliSense help prevent syntax errors?*

2. **Modules & Subroutines**  
   - *Explain the difference between a module and a subroutine.*  
   - *How do you rename a module in the VBA project?*

3. **Macro Recording**  
   - *What are the limitations of recorded macros?*  
   - *Describe the steps to record a macro that fills a range of cells.*

4. **Cell References**  
   - *Differentiate between relative, absolute, and mixed references.*  
   - *Convert the reference `R2C4` to A1 notation.*

5. **Common Functions**  
   - *Write a formula that uses `VLOOKUP` to find a name given an ID.*  
   - *Explain how to calculate the mortgage payment using the `PMT` function.*

6. **Error Types**  
   - *Match each Excel error (`#N/A`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#NUM!`, `#REF!`, `#NULL!`) with its meaning.*  

7. **Chart Creation**  
   - *Outline the steps to insert a chart and add axis titles using the Design tab.*

8. **Sheet Protection**  
   - *What actions can be restricted when a sheet is protected?*  

These questions reflect the topics the professor explicitly mentioned as likely to appear on the exam.  

---