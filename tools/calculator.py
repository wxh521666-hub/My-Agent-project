"""数学计算工具。

职责：执行基础四则运算，供 Agent 在需要计算时调用。
"""
def calculator(a: float, b: float, operator: str):
    """执行基础数学计算"""

    if operator == "+":
        return a + b

    elif operator == "-":
        return a - b

    elif operator == "*":
        return a * b

    elif operator == "/":
        if b == 0:
            raise ValueError("除数不能为 0")

        return a / b

    else:
        raise ValueError("不支持的运算符")