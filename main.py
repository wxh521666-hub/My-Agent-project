"""程序入口。

职责：接收用户输入，启动 Agent 运行循环，输出最终回答。
"""

from runtime import agent_runtime


if __name__ == "__main__":

    print("=== 我的第一个 AI Agent ===")

    while True:

        user_input = input("\n请输入任务（输入 exit 退出）：")

        if user_input.lower() == "exit":
            break

        answer = agent_runtime(user_input)

        print("\nAgent 回答：")
        print(answer)