from agent import build_agent


def main():
    agent = build_agent()
    session_number = 1

    while True:
        question = input("请输入购物问题（输入“退出”结束）：").strip()

        if question == "退出":
            print("退出程序")
            break

        if question == "新对话":
            session_number += 1
            print(f"已开始新对话 {session_number}。")
            continue


        if not question:
            continue

        config = {
            "configurable": {
                "thread_id": f"shopping-{session_number}",
            }
        }
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": question}
            ]
        },
            config=config
        )

        print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
