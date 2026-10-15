"""Stack-based expression evaluator (DCOMP320 - Stacks Implementation).

Reads expressions from input.txt, evaluates each one using stacks
(infix -> postfix with an operator stack, then postfix evaluation with a
value stack) and writes the results to output.txt, keeping separator lines.
"""
import re
import sys


class Stack:
    """Simple stack built on a Python list (end of list = top)."""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if not self.items:
            raise IndexError("peek at empty stack")
        return self.items[-1]

    def is_empty(self):
        return not self.items


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "u-": 3}  # u- = unary minus
TOKEN_RE = re.compile(r"\s*(\d+\.\d*|\.\d+|\d+|[-+*/()])")


def is_separator(line):
    s = line.strip()
    return len(s) >= 3 and set(s) == {"-"}


def tokenize(expr):
    """Split an expression into numbers, operators and parentheses.
    A '-' at the start, after an operator or after '(' is unary minus."""
    tokens, pos, prev = [], 0, None
    expr = expr.rstrip()
    while pos < len(expr):
        m = TOKEN_RE.match(expr, pos)
        if not m:
            raise ValueError("Invalid expression")
        tok = m.group(1)
        pos = m.end()
        if tok == "-" and (prev is None or prev in PRECEDENCE or prev == "("):
            tok = "u-"
        if tok[0].isdigit() or tok[0] == ".":
            tok = float(tok)
        tokens.append(tok)
        prev = tok if not isinstance(tok, float) else "num"
    if not tokens:
        raise ValueError("Invalid expression")
    return tokens


def to_postfix(tokens):
    """Convert infix tokens to postfix using an operator stack."""
    output, ops = [], Stack()
    for tok in tokens:
        if isinstance(tok, float):
            output.append(tok)
        elif tok == "u-":
            ops.push(tok)  # right-associative: never pops equal precedence
        elif tok in PRECEDENCE:
            while (not ops.is_empty() and ops.peek() != "("
                   and PRECEDENCE[ops.peek()] >= PRECEDENCE[tok]):
                output.append(ops.pop())
            ops.push(tok)
        elif tok == "(":
            ops.push(tok)
        else:  # ")"
            while not ops.is_empty() and ops.peek() != "(":
                output.append(ops.pop())
            if ops.is_empty():
                raise ValueError("Mismatched parentheses")
            ops.pop()
    while not ops.is_empty():
        top = ops.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses")
        output.append(top)
    return output


def evaluate_postfix(postfix):
    """Evaluate a postfix token list using a value stack."""
    values = Stack()
    try:
        for tok in postfix:
            if isinstance(tok, float):
                values.push(tok)
            elif tok == "u-":
                values.push(-values.pop())
            else:
                right, left = values.pop(), values.pop()
                if tok == "+":
                    values.push(left + right)
                elif tok == "-":
                    values.push(left - right)
                elif tok == "*":
                    values.push(left * right)
                else:
                    if right == 0:
                        raise ZeroDivisionError
                    values.push(left / right)
    except IndexError:
        raise ValueError("Invalid expression")
    result = values.pop()
    if not values.is_empty():
        raise ValueError("Invalid expression")
    return result


def format_result(x):
    x = round(x, 10)
    return str(int(x)) if x == int(x) else str(x)


def evaluate(expr):
    try:
        return format_result(evaluate_postfix(to_postfix(tokenize(expr))))
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as e:
        return f"Error: {e}"


def process_file(in_path="input.txt", out_path="output.txt"):
    with open(in_path) as fin, open(out_path, "w") as fout:
        for line in fin:
            line = line.rstrip("\n")
            if is_separator(line) or not line.strip():
                fout.write(line + "\n")
            else:
                fout.write(evaluate(line) + "\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    process_file(*args[:2])
    print("Done. Results written to", args[1] if len(args) > 1 else "output.txt")
