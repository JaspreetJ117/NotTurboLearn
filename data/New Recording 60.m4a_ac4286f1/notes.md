# Excel & VBA Basics – Lecture Notes

**TL;DR**  
This lecture covered how to calculate mortgage payments in Excel (PMT function and manual formula), the structure of a two‑part assignment (manual vs. VBA‑automated), and the fundamentals of VBA: modules, variable declaration, constants, object variables, worksheet handling, message/input boxes, formatting, and string manipulation.  

---

## Key Concepts
- **PMT Function** – Built‑in Excel function for loan payments.  
- **Manual PMT Calculation** – Using the formula `PMT = (rate * pv) / (1 - (1 + rate)^-nper)`.  
- **Assignment Structure** – Part A: manual Excel work; Part B: VBA automation.  
- **VBA Modules & Code Windows** – Separate modules for each part, use of the Project Explorer, Properties, Immediate, and Debug windows.  
- **Variable Declaration** – `Option Explicit`, `Dim`, `Const`, `Set`.  
- **Object Variables** – `Range`, `Worksheet`, `Workbook`, `Chart`, `PivotTable`.  
- **Message & Input Boxes** – `MsgBox`, `InputBox` with prompts, buttons, titles, and return values.  
- **Formatting & String Functions** – `Format`, `Left`, `Right`, `Mid`, `Len`, `UCase`, `LCase`, `Replace`, `InStr`.  

---

## Important Definitions
- **PMT** – Excel function that returns the payment for a loan based on constant payments and a constant interest rate.  
- **PV** – Present value of a loan or investment.  
- **FV** – Future value (optional in PMT).  
- **Option Explicit** – VBA directive that forces explicit variable declaration.  
- **Object Variable** – A variable that holds a reference to an object (e.g., `Range`, `Worksheet`).  
- **Set** – Keyword used to assign an object reference to an object variable.  
- **MsgBox** – Function that displays a dialog box with a message and optional buttons.  
- **InputBox** – Function that prompts the user for input and returns the entered value.  
- **Format** – Function that returns a string representation of a value in a specified format.  

---

## Step‑by‑Step Explanations

### 1. Calculating Mortgage Payments
1. **Using Excel PMT**  
   ```excel
   =PMT(rate, nper, pv, [fv], [type])
   ```
   - `rate`: monthly interest rate  
   - `nper`: total number of payments  
   - `pv`: present value (loan amount)  
   - `fv`: future value (usually 0)  
   - `type`: 0 = end of period, 1 = beginning  

2. **Manual Calculation**  
   ```excel
   = (rate * pv) / (1 - (1 + rate)^-nper)
   ```
   - Same parameters as above; useful when Excel’s PMT is not available.

### 2. Assignment Parts
- **Part A (Manual)**  
  1. Enter loan data in Excel.  
  2. Use PMT or manual formula to compute monthly payment.  
  3. Create a graph of payment schedule.  
  4. Follow the step‑by‑step rubric (steps 1‑5).  

- **Part B (VBA Automation)**  
  1. Create a new module for Part A code.  
  2. Create a second module for Part B code.  
  3. Write VBA to perform the same calculations automatically.  
  4. Record a macro, then edit the code.  
  5. Add a control button that runs the macro.  
  6. Submit a macro‑enabled workbook (`.xlsm`).  

### 3. VBA Basics
1. **Enable Developer Tab** – `File → Options → Customize Ribbon → Developer`.  
2. **Insert Module** – `Developer → Visual Basic → Insert → Module`.  
3. **Variable Declaration**  
   ```vba
   Option Explicit
   Dim i As Integer
   Dim rng As Range
   Const PI As Double = 3.14159
   ```
4. **Object Variables & Set**  
   ```vba
   Set rng = Worksheets("Sheet1").Range("A1")
   ```
5. **Worksheet & Code Names**  
   - Tab name: `Sheet1`  
   - Code name (VBA property): `Sheet1` (can be changed in Properties window).  

6. **Message Box**  
   ```vba
   Dim result As Integer
   result = MsgBox("Continue?", vbYesNo + vbQuestion, "Confirm")
   If result = vbYes Then
       ' do something
   End If
   ```
7. **Input Box**  
   ```vba
   Dim name As String
   name = InputBox("Enter your name:", "Name Prompt", "Default")
   ```
8. **Formatting**  
   ```vba
   Dim formatted As String
   formatted = Format(1234.567, "0.00")
   ```
9. **String Functions**  
   ```vba
   Dim s As String
   s = "Hello World"
   Left(s, 5)      ' "Hello"
   Right(s, 5)     ' "World"
   Mid(s, 7, 5)    ' "World"
   Len(s)          ' 11
   UCase(s)        ' "HELLO WORLD"
   LCase(s)        ' "hello world"
   Replace(s, "World", "VBA")  ' "Hello VBA"
   InStr(s, "lo")  ' 4
   ```

10. **Debugging**  
    - `Debug.Print` writes to the Immediate window.  
    - Use the Immediate window (`Ctrl+G`) to test expressions.  

---

## Equations / Formulas

```math
\text{PMT} = \frac{r \cdot PV}{1 - (1 + r)^{-n}}
```

where  
- \( r \) = periodic interest rate  
- \( PV \) = present value (loan amount)  
- \( n \) = total number of periods  

---

## Code Examples / Snippets

```vba
Option Explicit

' Part A: Manual calculation
Sub CalculateMortgage()
    Dim rate As Double, nper As Integer, pv As Double
    rate = 0.05 / 12
    nper = 30 * 12
    pv = 200000
    MsgBox "Monthly payment: " & Format(PMT(rate, nper, pv), "0.00")
End Sub

' Part B: Automated calculation with button
Sub AutoMortgage()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Sheet1")
    ws.Range("B1").Value = PMT(0.05 / 12, 30 * 12, 200000)
End Sub
```

```vba
' Message box example
Dim userChoice As Integer
userChoice = MsgBox("Do you want to continue?", vbYesNo + vbQuestion, "Continue?")
If userChoice = vbYes Then
    ' proceed
End If
```

```vba
' Input box example
Dim userName As String
userName = InputBox("Enter your name:", "Name Prompt", "John Doe")
```

```vba
' String manipulation example
Dim txt As String
txt = "Excel VBA Tutorial"
Debug.Print Left(txt, 5)          ' Excel
Debug.Print Right(txt, 7)         ' Tutorial
Debug.Print Mid(txt, 7, 3)        ' VBA
Debug.Print Len(txt)              ' 20
Debug.Print UCase(txt)            ' EXCEL VBA TUTORIAL
Debug.Print Replace(txt, "VBA", "Macro")  ' Excel Macro Tutorial
```

---

## Examples (from lecture)

- **Mortgage payment calculation** using both Excel PMT and manual formula.  
- **Assignment rubric**: steps 1‑5 for Part A, points distribution (12 for Part A, 8 for Part B).  
- **Worksheet naming**: default `Sheet1`, `Sheet2`; custom names like `EDA` or `Macro`.  
- **Code name change** via Properties window.  
- **Message box** with `vbYesNo` buttons and return value handling.  
- **Input box** with default value `"Default"`.  
- **Format function** example: `Format(1234.567, "0.00")`.  

---

## Potential Exam Questions

1. **Explain the difference between using Excel’s PMT function and writing the PMT formula manually.**  
2. **Write VBA code that calculates the monthly mortgage payment for a loan of $250,000 at 4.5% annual interest over 30 years.**  
3. **Describe the purpose of `Option Explicit` and the `Set` keyword in VBA.**  
4. **What are the advantages of using object variables (e.g., `Range`, `Worksheet`) over simple variables?**  
5. **Show how to create a message box that asks the user to confirm an action and handles the user's response.**  
6. **Demonstrate how to use the `InputBox` function to collect a numeric value and store it in a variable of the appropriate type.**  
7. **List and explain at least five string manipulation functions available in VBA.**  
8. **Explain how to add a control button to a worksheet that runs a macro.**  
9. **What is the difference between the `Sheets` and `Worksheets` collections?**  
10. **Describe how to use the Immediate window for debugging purposes.**  

---