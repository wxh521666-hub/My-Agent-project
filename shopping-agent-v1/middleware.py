from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage


@wrap_tool_call
def handle_tool_errors(request, handler):
    try:
        return handler(request)

    except ValueError as e:
        return ToolMessage(
            content=f"工具调用失败：{e}",
            tool_call_id=request.tool_call["id"],
            status="error",
        )