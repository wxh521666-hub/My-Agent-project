import os

# 使用离线配置初始化客户端，Runtime 请求由 Mock 接管。
os.environ["API_KEY"] = "offline-test-placeholder"
os.environ["BASE_URL"] = "http://127.0.0.1:1"
os.environ["MODEL"] = "offline-test"
from unittest.mock import patch
from types import SimpleNamespace

from runtime import agent_runtime


def test_agent_direct_answer():

    # 模拟一个不需要调用工具的 LLM 响应
    fake_response = SimpleNamespace(
        tool_calls=None,
        content="你好，我是 Mini Agent"
    )

    # 临时替换 runtime.py 中的 chat 函数
    with patch(
        "runtime.chat",
        return_value=fake_response
    ) as mock_chat:

        answer = agent_runtime("你好")

    # 验证 Agent 返回结果
    assert answer == "你好，我是 Mini Agent"

    # 验证 LLM 只被调用了一次
    assert mock_chat.call_count == 1


import json
from types import SimpleNamespace
from unittest.mock import patch

from runtime import agent_runtime


def test_agent_tool_call():

    # 1. 模拟工具调用对象
    fake_tool_call = SimpleNamespace(
        id="call_test_001",
        function=SimpleNamespace(
            name="calculator",
            arguments=json.dumps({
                "a": 10,
                "b": 5,
                "operator": "+"
            })
        )
    )

    # 2. 模拟第一轮 LLM 响应
    response1 = SimpleNamespace(
        tool_calls=[fake_tool_call],
        content=None
    )

    # Runtime 需要使用 model_dump()
    response1.model_dump = lambda exclude_none=True: {
        "role": "assistant",
        "tool_calls": [
            {
                "id": fake_tool_call.id,
                "type": "function",
                "function": {
                    "name": "calculator",
                    "arguments": fake_tool_call.function.arguments
                }
            }
        ]
    }

    # 3. 模拟第二轮 LLM 响应
    response2 = SimpleNamespace(
        tool_calls=None,
        content="10 + 5 = 15"
    )

    # 4. 按顺序返回两次 LLM 响应
    with patch(
        "runtime.chat",
        side_effect=[response1, response2]
    ) as mock_chat:

        answer = agent_runtime("计算 10 + 5")

        # 检查第二轮传入 LLM 的消息
        second_messages = mock_chat.call_args_list[1].args[0]

        tool_messages = [
            msg for msg in second_messages
            if msg["role"] == "tool"
        ]

        # 5. 验证工具消息
        assert len(tool_messages) == 1

        assert (
            tool_messages[0]["tool_call_id"]
            == "call_test_001"
        )

        tool_result = json.loads(
            tool_messages[0]["content"]
        )

        assert tool_result == {"result": 15}

    # 6. 验证最终回答和调用次数
    assert answer == "10 + 5 = 15"
    assert mock_chat.call_count == 2

    print("两轮工具调用 Mock 测试通过！")


def test_agent_tool_failure():

    # 第一轮：模拟 LLM 请求计算 10 / 0
    fake_tool_call = SimpleNamespace(
        id="call_error_001",
        function=SimpleNamespace(
            name="calculator",
            arguments=json.dumps({
                "a": 10,
                "b": 0,
                "operator": "/"
            })
        )
    )

    response1 = SimpleNamespace(
        tool_calls=[fake_tool_call],
        content=None
    )

    response1.model_dump = lambda exclude_none=True: {
        "role": "assistant",
        "tool_calls": [
            {
                "id": fake_tool_call.id,
                "type": "function",
                "function": {
                    "name": "calculator",
                    "arguments": fake_tool_call.function.arguments
                }
            }
        ]
    }

    # 第二轮：模拟 LLM 根据错误生成解释
    response2 = SimpleNamespace(
        tool_calls=None,
        content="除数不能为 0，因此 10 / 0 无法计算。"
    )

    with patch(
        "runtime.chat",
        side_effect=[response1, response2]
    ) as mock_chat:

        answer = agent_runtime("计算 10 / 0")

        # 检查工具反馈
        messages = mock_chat.call_args_list[1].args[0]

        tool_messages = [
            msg for msg in messages
            if msg["role"] == "tool"
        ]

        assert len(tool_messages) == 1

        result = json.loads(
            tool_messages[0]["content"]
        )

        assert result == {
            "error": "除数不能为 0"
        }

        assert (
            tool_messages[0]["tool_call_id"]
            == "call_error_001"
        )

    # 验证任务正常返回
    assert "除数不能为 0" in answer
    assert mock_chat.call_count == 2


if __name__ == "__main__":
    test_agent_direct_answer()
    test_agent_tool_call()
    test_agent_tool_failure()

    print("所有 Runtime Mock 测试通过！")
