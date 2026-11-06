"""工具包。

后续在这里集中注册所有可被 Agent 调用的工具，
runtime 通过注册表按名称查找并执行。
"""
from .weather import get_weather
from .calculator import calculator


TOOLS = {
    "calculator": calculator,
    "get_weather": get_weather
}