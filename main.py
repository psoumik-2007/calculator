from pathlib import Path
import ast
import math
import operator

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Python Calculator")

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
}


def calculate(expression: str):
    if len(expression) > 200:
        raise ValueError("Expression is too long")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Invalid number")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in OPERATORS:
                raise ValueError("Unsupported operator")

            left = evaluate(node.left)
            right = evaluate(node.right)
            if op_type is ast.Div and right == 0:
                raise ZeroDivisionError("Cannot divide by zero")

            result = OPERATORS[op_type](left, right)
            if abs(result) > 1e100:
                raise ValueError("Result is too large")
            return result

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in OPERATORS:
                raise ValueError("Unsupported operator")
            return OPERATORS[op_type](evaluate(node.operand))

        raise ValueError("Invalid expression")

    return evaluate(ast.parse(expression, mode="eval"))


class CalculationRequest(BaseModel):
    expression: str


@app.post("/calculate")
def calculate_api(request: CalculationRequest):
    try:
        result = calculate(request.expression)
        if isinstance(result, float) and not math.isfinite(result):
            raise ValueError("Result is not finite")
        return {"result": result}
    except ZeroDivisionError:
        raise HTTPException(400, "Cannot divide by zero")
    except (ValueError, SyntaxError, TypeError, OverflowError):
        raise HTTPException(400, "Invalid calculation")


@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/contact")
def contact():
    return {"data": "Welcome to the calculator app!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)
