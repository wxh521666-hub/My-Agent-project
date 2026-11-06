"""大模型调用层。

职责：封装对 LLM API 的请求，把消息列表发给模型并返回模型回复。
不负责执行工具，也不负责 Agent 循环。
"""
from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL

# 创建模型客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


def chat(messages, tools):
    """
    调用真实 LLM，并返回模型的消息对象
    """
    #create 就是发请求
    '''
    技术栈	发送模型请求的方式
OpenAI Python SDK	client.chat.completions.create()
LangChain	llm.invoke() 或 model.invoke()
    '''
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    return response.choices[0].message