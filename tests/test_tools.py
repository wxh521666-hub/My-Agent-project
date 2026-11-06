import os

# 使用离线配置初始化客户端，Runtime 请求由 Mock 接管。
os.environ["API_KEY"] = "offline-test-placeholder"
os.environ["BASE_URL"] = "http://127.0.0.1:1"
os.environ["MODEL"] = "offline-test"
from tools import TOOLS


def test_calculator_success():
    result = TOOLS["calculator"](
        a=10,
        b=5,
        operator="+"
    )

    assert result == 15


def test_weather_success():
    result = TOOLS["get_weather"](
        city="北京"
    )

    assert result["city"] == "北京"
    assert result["weather"] == "sunny"
    assert result["temperature"] == 25
    assert "模拟天气数据" in result["notice"]


def test_calculator_zero_division():
    try:
        TOOLS["calculator"](
            a=10,
            b=0,
            operator="/"
        )

    except ValueError as e:
        assert str(e) == "除数不能为 0"

    else:
        raise AssertionError(
            "除零时应该抛出 ValueError"
        )



from runtime import execute_tool


def test_runtime_tool_success():
    result = execute_tool(
        "calculator",
        {"a": 10, "b": 5, "operator": "+"}
    )

    assert result == {"result": 15}


def test_runtime_tool_failure():
    result = execute_tool(
        "calculator",
        {"a": 10, "b": 0, "operator": "/"}
    )

    assert result == {
        "error": "除数不能为 0"
    }


def test_runtime_unknown_tool():
    result = execute_tool(
        "unknown_tool",
        {}
    )

    assert "error" in result

if __name__ == "__main__":
    test_calculator_success()
    test_weather_success()
    test_calculator_zero_division()

    test_runtime_tool_success()
    test_runtime_tool_failure()
    test_runtime_unknown_tool()

    print("所有工具单元测试通过！")
