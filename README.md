# My Agent Project

Python AI Agent 学习项目，按学习阶段分别组织。两个项目各自包含代码、配置示例、依赖和使用说明。

| 项目 | 内容 | 使用说明 |
| --- | --- | --- |
| 第二周：原生 Agent | 手写模型与工具调用循环，计算器、模拟天气和运行时测试 | [week2-native-agent](week2-native-agent/README.md) |
| 第四周：LangChain Agent | 模拟商品查价、小计与合计工具、工具异常中间件、连续对话 | [week4-langchain-agent](week4-langchain-agent/README.md) |

```text
My-Agent-project/
├── README.md
├── .gitignore
├── week2-native-agent/
│   ├── main.py
│   ├── runtime.py
│   ├── tools/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
└── week4-langchain-agent/
    ├── main.py
    ├── agent.py
    ├── tools.py
    ├── middleware.py
    ├── .env.example
    ├── requirements.txt
    └── README.md
```

## 运行方式

先进入对应项目目录，按该目录的 README 配置 Python 环境和 `.env`，然后运行：

```powershell
# 第二周项目
cd week2-native-agent
python main.py
```

或者从仓库根目录进入第四周项目：

```powershell
cd week4-langchain-agent
python main.py
```

每个项目分别配置 `.env`；真实密钥不提交到仓库。天气和商品价格均为模拟数据，适合学习演示。
