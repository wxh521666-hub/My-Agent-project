
"""
Agent 运行时。

职责：
1. 维护对话消息和 Agent 循环。
2. 解析 LLM 返回的工具调用请求。
3. 调度并执行工具。
4. 管理 Task State 和 Step State。
5. 将工具结果回填给 LLM。
"""

import json
import uuid

from tools import TOOLS
from llm import chat


# True：显示详细调试信息
# False：只显示必要信息
DEBUG = False


# 1. 工具 Schema
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行基础数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                    "operator": {
                        "type": "string",
                        "enum": ["+", "-", "*", "/"]
                    }
                },
                "required": ["a", "b", "operator"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的模拟天气数据，不代表实时天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]


# 2. 调试输出
def debug_print(message):
    if DEBUG:
        print(message)


# 3. 执行工具
def execute_tool(tool_name, arguments):

    if tool_name not in TOOLS:
        return {"error": f"工具不存在：{tool_name}"}

    try:
        result = TOOLS[tool_name](**arguments)

        # 将工具返回的业务错误统一为外层 error
        if isinstance(result, dict) and "error" in result:
            return {"error": result["error"]}

        return {"result": result}

    except Exception as e:
        return {"error": str(e)}


# 4. Agent 主循环
def agent_runtime(user_input):

    # 初始化对话上下文
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个智能助手。"
                "当用户需要计算时，使用 calculator 工具。"
                "当用户询问天气时，使用 get_weather 工具。"
                "根据工具执行结果回答用户。"
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # 初始化 Agent State
    agent_state = {
        "task_id": str(uuid.uuid4()),
        "status": "running",
        "current_step": 0,
        "max_steps": 5,
        "steps": [],
        "results": {},
        "error": None
    }

    debug_print(f"任务 ID：{agent_state['task_id']}")
    debug_print(f"任务状态：{agent_state['status']}")

    # Agent Loop
    for step in range(agent_state["max_steps"]):

        agent_state["current_step"] = step + 1

        debug_print(f"\n--- Agent 第 {step + 1} 轮 ---")

        # 调用 LLM
        try:
            response = chat(messages, TOOL_SCHEMAS)

        except Exception as e:
            agent_state["status"] = "failed"
            agent_state["error"] = str(e)

            print("任务状态：failed")
            debug_print(f"LLM 请求异常：{e}")

            return f"Agent 请求失败：{e}"

        # 模型没有请求工具，进入最终回答阶段
        if not response.tool_calls:

            final_answer = response.content

            if final_answer and final_answer.strip():
                agent_state["status"] = "completed"
                agent_state["error"] = None
            else:
                agent_state["status"] = "failed"
                agent_state["error"] = "模型未返回有效回答"

            print(f"任务状态：{agent_state['status']}")

            debug_print(
                f"执行轮数：{agent_state['current_step']}"
            )
            debug_print(
                f"步骤记录：{agent_state['steps']}"
            )
            debug_print(
                f"错误信息：{agent_state['error']}"
            )

            return final_answer or "模型没有返回有效回答"

        # 保存 assistant 工具调用消息
        messages.append(
            response.model_dump(exclude_none=True)
        )

        # 逐个执行工具调用
        for tool_call in response.tool_calls:

            tool_name = tool_call.function.name

            print(f"调用工具：{tool_name}")

            # 先创建 Step State，保证解析失败也能记录
            step_record = {
                "step_id": str(uuid.uuid4()),
                "step_number": len(agent_state["steps"]) + 1,
                "tool_call_id": tool_call.id,
                "tool_name": tool_name,
                "status": "running",
                "arguments": None,
                "result": None,
                "error": None
            }

            agent_state["steps"].append(step_record)

            # 解析工具参数
            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

                if not isinstance(arguments, dict):
                    raise ValueError("工具参数必须是 JSON 对象")

                step_record["arguments"] = arguments

                debug_print(f"工具参数：{arguments}")

                # 执行工具
                result = execute_tool(tool_name, arguments)

            except (json.JSONDecodeError, ValueError) as e:
                result = {
                    "error": f"工具参数解析失败：{e}"
                }

            debug_print(f"工具结果：{result}")

            # 更新 Step State
            if "error" in result:
                step_record["status"] = "failed"
                step_record["error"] = result["error"]
            else:
                step_record["status"] = "completed"
                step_record["result"] = result

            # 保存工具结果
            agent_state["results"][step_record["step_id"]] = result

            # 回填工具结果，使用原始 tool_call_id
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    result,
                    ensure_ascii=False
                )
            })

        debug_print(f"当前步骤状态：{agent_state['steps']}")
        debug_print(f"当前步骤结果：{agent_state['results']}")

    # 超过最大执行轮数
    agent_state["status"] = "max_steps_exceeded"
    agent_state["error"] = "Agent 达到最大执行轮数，任务未完成"

    print(f"任务状态：{agent_state['status']}")

    debug_print(f"执行轮数：{agent_state['current_step']}")
    debug_print(f"步骤记录：{agent_state['steps']}")
    debug_print(f"错误信息：{agent_state['error']}")

    return agent_state["error"]
