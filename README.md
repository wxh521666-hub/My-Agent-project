# Mini Agent V0.1

基于 Python 和 DeepSeek API 实现的最小 AI Agent，支持通过 Function Calling 自主选择并调用工具。

## 1. 项目功能

- 自然语言交互
- DeepSeek LLM API 调用
- Calculator 数学计算工具
- Weather 模拟天气查询工具
- Function Calling 工具选择与执行
- Agent Loop 多轮执行
- Task State 与 Step State 状态管理
- Max Steps 执行轮数限制
- 基础异常处理
- DEBUG 调试模式

## 2. 项目结构

```text
my_first_agent_turn_end/
├── main.py
├── config.py
├── llm.py
├── runtime.py
├── tools/
│   ├── __init__.py
│   ├── calculator.py
│   └── weather.py
├── tests/
│   ├── __init__.py
│   ├── test_tools.py
│   └── test_runtime.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 3. 安装依赖

建议使用 Python 虚拟环境。

```bash
pip install -r requirements.txt
```

## 4. 环境变量配置

复制 `.env.example` 为 `.env`，并填写自己的 API Key。

```dotenv
API_KEY=your_api_key_here
BASE_URL=https://api.deepseek.com
MODEL=deepseek-flash
```

实际变量名称以 `config.py` 为准。

不要将包含真实 API Key 的 `.env` 提交到 Git。

## 5. 启动 Agent

在项目根目录执行：

```bash
python main.py
```

示例输入：

```text
查询北京天气
计算 10 + 5
计算 10 / 0
```

注意：天气工具目前使用本地模拟数据，不代表实时天气。

## 6. 运行测试

在项目根目录执行：

```bash
python -m tests.test_tools
python -m tests.test_runtime
```

## 7. Agent 执行流程

```text
User Input
    ↓
Agent Runtime
    ↓
LLM
    ↓
Tool Calling?
    ├── No → Final Answer
    └── Yes
          ↓
      Execute Tool
          ↓
      Update Step State
          ↓
      Return Tool Result
          ↓
      LLM (Next Round)
```

## 8. 当前版本限制

Mini Agent V0.1 是学习项目，暂未实现：

- Pydantic 参数校验
- 完整的超时与重试机制
- 工具权限及敏感操作审批
- 状态持久化与断点恢复
- 严格的任务完成条件验证
- 生产级日志与监控

这些能力将在后续课程逐步完善。

## 9. 后续规划

- V0.2：Function Calling 与 Tools 工程化
- V0.3：Prompt Engineering
- V1.0：使用 LangChain 重构个人智能助手
