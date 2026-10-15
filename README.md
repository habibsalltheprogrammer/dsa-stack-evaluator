# Stack-Based Expression Evaluator (DCOMP320 - Stacks Implementation)

A Python program that reads arithmetic expressions from `input.txt`, evaluates
them using stacks, and writes the results to `output.txt`.

## How to run
Requires Python 3 (no extra libraries). Put `stack_evaluator.py` and
`input.txt` in the same folder, then run:

    python stack_evaluator.py

Optional: `python stack_evaluator.py my_input.txt my_output.txt`

## File format
- **input.txt**: one expression per line; separator lines (three or more `-`,
  e.g. `-----`) divide the expressions.
- **output.txt**: one result per line, in the same order; separator lines are
  copied unchanged.

## How it works
1. `Stack` class: `push`, `pop`, `peek` (plus `is_empty`), built on a list.
2. `tokenize`: splits numbers, operators and parentheses.
3. `to_postfix`: infix to postfix using an operator stack (precedence + brackets).
4. `evaluate_postfix`: evaluates using a value stack.
5. `process_file`: reads input, handles separators, writes results.

## Assumptions and limitations
- Supports `+ - * /`, parentheses, decimals and negative numbers.
- Whole-number results print without decimals (e.g. `4`, not `4.0`).
- Errors are written to the output line: `Error: Division by zero`,
  `Error: Mismatched parentheses`, `Error: Invalid expression`.
- Blank lines are kept as blank lines. No exponents, variables or functions.
- Note: the assignment brief's sample output shows 17 for `(8 / 4) + 7 * 2`;
  standard arithmetic gives 16, which this program outputs.
