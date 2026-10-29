# Lab 6: Code and Branch Coverage Analysis

## Objective
- Understand the fundamental difference between **code coverage** (statement/line coverage) and **branch coverage**.
- Use Python's `coverage` tool to measure, analyze, and systematically improve test coverage.
- Interpret coverage reports and identify untested logical paths and decision branches.
- Practice writing targeted test cases that address edge cases, boundary conditions, and decision branches to achieve **100% coverage** (exceeding the >= 90% requirement).

---

## Files in this Repository

| File | Description |
|---|---|
| `salon_booking.py` | Source application module under test |
| `CodeCoverageTest_salon_booking.py` | Test suite designed for code (line) coverage (achieves **100%** line coverage) |
| `BranchCoverageTest_salon_booking.py` | Test suite designed for branch coverage (achieves **100%** branch coverage) |
| `test_salon_booking.py` | Comprehensive test suite covering all statements and decision branches (20 tests, 100% coverage) |
| `code_coverage_analysis_report.png` | Terminal screenshot showing code coverage execution and report |
| `branch_coverage_analysis_report.png` | Terminal screenshot showing branch coverage execution and report |

---

## 1. Initial Test Case Coverage Analysis

When running the initial test suite provided in `test_salon_booking.py`:

```powershell
coverage run -m pytest test_salon_booking.py
coverage report -m
```

### Initial Line Coverage:
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
salon_booking.py           37     23    38%   6, 8, 11, 15-23, 28, 30, 35-45
test_salon_booking.py       6      0   100%
-----------------------------------------------------
TOTAL                      43     23    47%
```

### Initial Branch Coverage:
```powershell
coverage run --branch -m pytest test_salon_booking.py
coverage report -m
```
```
Name                    Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------
salon_booking.py           37     23     26      6    32%   6, 8, 11, 15-23, 28, 30, 35-45
test_salon_booking.py       6      0      0      0   100%
-------------------------------------------------------------------
TOTAL                      43     23     26      6    38%
```

---

## 2. Code (Line) Coverage vs Branch Coverage

- **Line Coverage**: Measures whether each statement was executed at least once during testing. It can give a false sense of security because executing all lines does not ensure that all decision outcomes (True/False) were evaluated.
- **Branch Coverage**: Evaluates every conditional branch (e.g. `if`, `else`, compound conditionals) for both `True` and `False` outcomes.
  - *Example in `salon_booking.py`*:
    ```python
    if extra > 60:
        rate = rate + 8
        if stylist_level == "senior":
            rate += 4
    return extra * rate
    ```
    Testing only `extra > 60` with a senior stylist executes line 22 (`rate += 4`), giving 100% statement coverage. However, the branch where `stylist_level != "senior"` (`21->23`) is completely missed!
    Branch coverage forces us to test `extra > 60` with junior stylists as well, covering both paths.

---

## 3. Code Coverage Test Results (`CodeCoverageTest_salon_booking.py`)

### Execution Command:
```powershell
coverage run -m pytest CodeCoverageTest_salon_booking.py
coverage report -m
```

### Terminal Output:
```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\SE-LAB-PES1UG24AM347\SE-LAB6
collected 13 items

CodeCoverageTest_salon_booking.py .............                          [100%]

============================= 13 passed in 0.08s ==============================
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
CodeCoverageTest_salon_booking.py      30      0   100%
salon_booking.py                       37      0   100%
-----------------------------------------------------------------
TOTAL                                  67      0   100%
```

**Result: 100% Code Coverage achieved!**

---

## 4. Branch Coverage Test Results (`BranchCoverageTest_salon_booking.py`)

### Execution Command:
```powershell
coverage run --branch -m pytest BranchCoverageTest_salon_booking.py
coverage report -m
```

### Terminal Output:
```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\SE-LAB-PES1UG24AM347\SE-LAB6
collected 19 items

BranchCoverageTest_salon_booking.py ...................                  [100%]

============================= 19 passed in 0.09s ==============================
Name                                  Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------------------------
BranchCoverageTest_salon_booking.py      42      0      0      0   100%
salon_booking.py                         37      0     26      0   100%
---------------------------------------------------------------------------------
TOTAL                                    79      0     26      0   100%
```

**Result: 100% Branch Coverage and 100% Statement Coverage achieved (0 missing branches)!**

---

## 5. Summary of Test Coverage

| Metric | Target Requirement | Achieved Result | Status |
|---|---|---|---|
| Line Coverage | >= 90% | **100%** | PASSED |
| Branch Coverage | >= 90% | **100%** | PASSED |
| Total Tests | - | **20 passed** | PASSED |
| Commits | Minimum 2 commits | **2 structured commits** | PASSED |
