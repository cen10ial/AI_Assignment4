# AI_Assignment4

# CSP Programming Assignment – README

## Overview

This file (`csp_assignment.py`) implements all **4 questions** of the CSP Programming Assignment using **Constraint Satisfaction Problem (CSP)** techniques in Python. No external libraries are required — it runs on standard Python 3.

---

## How to Run

```bash
python csp_assignment.py
```

All 4 problems will execute sequentially and print results to the terminal.

---

## File Structure

```
csp_assignment.py
│
├── class CSP                  # Generic reusable CSP solver
│   ├── is_consistent()        # Checks if a value assignment is valid
│   ├── select_unassigned_variable()  # MRV heuristic
│   ├── forward_check()        # Prunes domains after each assignment
│   ├── backtrack()            # Recursive backtracking search
│   └── solve()                # Entry point
│
├── solve_australia()          # Q1 – Australia Map Coloring
├── solve_telangana()          # Q2 – Telangana 33-District Map Coloring
├── solve_sudoku()             # Q3 – Sudoku Puzzle
└── solve_cryptarithmetic()    # Q4 – SEND + MORE = MONEY
```

---

## Question-by-Question Breakdown

### Q1 – Map Coloring: Australia

**Problem:** Color the 7 regions of Australia (WA, NT, SA, Q, NSW, V, T) such that no two adjacent regions share the same color.

**Approach:**
- Variables: 7 regions
- Domain: `[Red, Green, Blue]` (3 colors)
- Constraints: Adjacent regions must have different colors

**Result:**
```
WA → Red     NT → Green    SA → Blue
Q  → Red     NSW → Green   V  → Red
T  → Red
```
✓ All constraints satisfied with just 3 colors.

---

### Q2 – Map Coloring: Telangana (33 Districts)

**Problem:** Color all 33 districts of Telangana such that no two bordering districts share the same color.

**Approach:**
- Variables: 33 districts
- Domain: `[Crimson, SteelBlue, ForestGreen, Gold]` (4 colors)
- Constraints: Bordering districts must have different colors
- Adjacency defined based on actual Telangana district borders

**Result:** All 33 districts colored successfully with 4 colors.
✓ Guaranteed possible by the **4-Color Theorem** (any planar map needs at most 4 colors).

---

### Q3 – Sudoku Puzzle

**Problem:** Solve a standard 9×9 Sudoku puzzle using CSP.

**Approach:**
- Variables: 81 cells `(row, col)`
- Domain: Digits `1–9` (pre-filled cells have domain of size 1)
- Constraints: Each cell's **peers** (same row, same column, same 3×3 box) must all have different values

**Puzzle Input:**
```
┌───────┬───────┬───────┐
│ 5 3 . │ . 7 . │ . . . │
│ 6 . . │ 1 9 5 │ . . . │
│ . 9 8 │ . . . │ . 6 . │
├───────┼───────┼───────┤
│ 8 . . │ . 6 . │ . . 3 │
│ 4 . . │ 8 . 3 │ . . 1 │
│ 7 . . │ . 2 . │ . . 6 │
├───────┼───────┼───────┤
│ . 6 . │ . . . │ 2 8 . │
│ . . . │ 4 1 9 │ . . 5 │
│ . . . │ . 8 . │ . 7 9 │
└───────┴───────┴───────┘
```

**Solution:**
```
┌───────┬───────┬───────┐
│ 5 3 4 │ 6 7 8 │ 9 1 2 │
│ 6 7 2 │ 1 9 5 │ 3 4 8 │
│ 1 9 8 │ 3 4 2 │ 5 6 7 │
├───────┼───────┼───────┤
│ 8 5 9 │ 7 6 1 │ 4 2 3 │
│ 4 2 6 │ 8 5 3 │ 7 9 1 │
│ 7 1 3 │ 9 2 4 │ 8 5 6 │
├───────┼───────┼───────┤
│ 9 6 1 │ 5 3 7 │ 2 8 4 │
│ 2 8 7 │ 4 1 9 │ 6 3 5 │
│ 3 4 5 │ 2 8 6 │ 1 7 9 │
└───────┴───────┴───────┘
```
✓ All rows, columns, and 3×3 boxes verified.

---

### Q4 – Cryptarithmetic: SEND + MORE = MONEY

**Problem:** Assign a unique digit (0–9) to each letter so that the equation holds. Leading letters S and M cannot be 0.

**Approach:**
- Variables: `S, E, N, D, M, O, R, Y`
- Domain: Digits `0–9` (all unique)
- Constraint: `SEND + MORE = MONEY`, S ≠ 0, M ≠ 0
- Method: Permutation-based brute-force over 8 chosen digits from 10

**Solution:**
```
S=9, E=5, N=6, D=7, M=1, O=0, R=8, Y=2

  9567
+ 1085
──────
 10652
```
✓ 9567 + 1085 = 10652

---

## CSP Techniques Used

| Technique | Description |
|---|---|
| **Backtracking Search** | Tries values one by one; undoes assignment on failure |
| **MRV Heuristic** | Picks the variable with the fewest remaining legal values next |
| **Forward Checking** | After each assignment, removes invalid values from neighbors' domains |
| **Constraint Propagation** | Domain wipe-out detection to fail early |

---

## Requirements

- Python 3.6+
- No external libraries needed (`itertools` is from the standard library)
