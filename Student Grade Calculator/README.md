# Student Grade Calculator

**Developers Arena — Week 2 Assignment**
A simple Python program that takes a student's mark and returns a letter grade with an encouraging message.

---

## What the Program Does

1. Shows a welcome message
2. Asks for the student's name
3. Asks for the student's mark (must be between 0 and 100)
4. If the mark is invalid, it keeps asking until a valid one is entered
5. Shows the letter grade and an encouraging message
6. Asks if you want to check another student

---

## Grading Scale

| Mark         | Grade |
|:------------:|:-----:|
| 90 to 100    |   A   |
| 80 to 89     |   B   |
| 70 to 79     |   C   |
| 60 to 69     |   D   |
| 0 to 59      |   F   |

---

## Encouraging Messages

| Grade | Message |
|:-----:|---------|
| A | Excellent work! You are outstanding! Keep it up! |
| B | Great job! You are doing really well! Keep pushing! |
| C | Good effort! You are on the right track. Keep going! |
| D | Don't give up! A little more effort will make a big difference! |
| F | Don't be discouraged! Every expert was once a beginner. Try again! |

---

## Project Files

```
week 2 Student Grade Calculator/
│
├── grade_calculator.py   ← The main Python program
├── README.md             ← This file
├── test_cases.txt        ← All test cases
└── screenshots/          ← Screenshots of the program running
```

---

## How to Run

Make sure you have Python installed, then open a terminal and run:

```
python grade_calculator.py
```

---

## Sample Output

```
====================================
   Student Grade Calculator
   Developers Arena - Week 2
====================================

Enter student name: Anuj
Enter mark (0 to 100): 95

------------------------------------
Result for: Anuj
Mark      : 95.0
Grade     : A
Message   : Excellent work! You are outstanding! Keep it up!
------------------------------------

Check another student? (yes or no): no

Thank you !
Keep learning and growing!
```

### What happens with invalid input:

```
Enter mark (0 to 100): abc
Invalid! Please enter a number.

Enter mark (0 to 100): 150
Invalid! Mark must be between 0 and 100.

Enter mark (0 to 100): 85
```

---

## Functions Explained

### `get_grade(mark)`
Takes the student's mark and returns a letter grade using `if/elif/else`.

### `get_message(grade)`
Takes the letter grade and returns an encouraging message using `if/elif/else`.

### `get_valid_mark()`
Uses a `while` loop to keep asking the user for a mark until they enter a valid number between 0 and 100.

---

## Requirements

- Python 3 (no extra libraries needed)
- Works on Windows, Mac, and Linux

---

*Built with love as part of the Developers Arena Python learning journey.*



