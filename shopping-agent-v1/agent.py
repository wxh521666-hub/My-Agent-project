from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek

from config import API_KEY, BASE_URL, MODEL
from tools import get_price, calculate_total, sum_totals


from middleware import handle_tool_errors
from langgraph.checkpoint.memory import InMemorySaver
def build_agent():
    # 1. 复制之前的 ChatDeepSeek 初始化代码
    model = ChatDeepSeek(
        model=MODEL,
        api_key=API_KEY,
        api_base=BASE_URL,
        temperature=0,
        timeout=20,
        max_retries=2,
        extra_body={"thinking": {"type": "disabled"}},
    )

    # 2. 使用 create_agent 组装
    agent = create_agent(
        model=model,
        tools=[get_price, calculate_total, sum_totals],
        system_prompt= (
        "你是购物助手，使用 get_price 查询商品单价。"
        "使用 calculate_total 计算小计，使用 sum_totals 计算合计。"
        "所有价格都是模拟数据，回答时必须注明。"
        "商品或数量不明确时，先向用户确认。"
        "工具失败时如实说明，不编造结果，不擅自修改商品或数量。"
        "数量不合法时，只说明原因并请用户提供合法数量，不自行假设或计算替代数量。"
        ),
        middleware=[handle_tool_errors],
        checkpointer=InMemorySaver(),
    )

    # 3. 把创建好的 Agent 返回出去
    return agent