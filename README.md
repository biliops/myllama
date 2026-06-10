# 智能旅行助手项目 - 小白入门指南

## 📁 项目结构

```
演示项目/
├── AgentDemo.py     # 主程序（核心代码）
├── Prompts.py       # 提示词模板（告诉AI该怎么做）
├── .env            # 配置文件（存放密钥和地址）
├── Debug.json      # 运行过程日志（记录3次请示详情）
└── README.md       # 项目说明文档
```

---

## 🔧 运行方式（按需执行）

```bash
. ~/conda.env # 激活 conda 环境
conda activate ClaudeTap # 进入虚拟环境
python ./AgentDemo.py # 执行程序
```

---

## 🚀 项目工作流程（像讲故事一样）

```
用户提问 → AI思考 → 执行工具 → 获取结果 → 总结回答
```

### 第一步：用户提问
```python
user_prompt = "帮我查询北京天气并推荐景点"
```

### 第二步：AI思考（调用大语言模型）
程序把问题发给 AI（如 Qwen3.6），AI 分析后决定下一步要做什么。

### 第三步：执行工具
根据 AI 的指令，程序会自动调用工具：
- `get_weather("北京")` - 查询天气
- `get_attraction("北京", "Sunny")` - 根据天气推荐景点

### 第四步：总结回答
AI 把所有信息整理成友好的回答。

---

## 📖 核心代码逐行解释

### 1. 导入工具（像借工具一样）

```python
import os                    # 操作系统工具（读取文件、环境变量）
import re                    # 正则表达式工具（查找文本）
import requests              # 网络请求工具（访问网站API）
from tavily import TavilyClient  # 搜索引擎工具
from openai import OpenAI      # AI大模型客户端
from dotenv import load_dotenv # 读取配置文件工具
```

### 2. 读取配置（从 .env 文件拿钥匙）

```python
load_dotenv()                    # 打开 .env 文件
API_KEY = os.getenv("API_KEY")   # 读取 API 密钥
BASE_URL = os.getenv("BASE_URL") # 读取服务地址
```

### 3. 定义工具函数（智能体的手脚）

```python
# 查天气工具
def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)  # 访问天气网站
    data = response.json()        # 解析返回的数据
    return f"{city}天气:{weather_desc}，气温{temp_c}度"

# 查景点工具
def get_attraction(city, weather):
    tavily = TavilyClient(api_key=api_key)
    response = tavily.search(query=f"{city} {weather}景点推荐")
    return response["answer"]
```

### 4. 调用 AI（让 AI 思考）

```python
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
response = client.chat.completions.create(
    model="Qwen3.6:MTP",
    messages=[
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},  # 告诉AI它的身份
        {"role": "user", "content": user_prompt}             # 用户的问题
    ]
)
```

---

## 🧩 常用工具说明

| 工具 | 作用 | 例子 |
|------|------|------|
| `requests` | 访问网站API | `requests.get("https://wttr.in/北京")` |
| `openai` | 调用大语言模型 | 让 AI 帮我们思考和决策 |
| `tavily` | 搜索互联网 | 搜索旅游景点信息 |
| `dotenv` | 读取配置文件 | 从 `.env` 获取密钥 |

---

## 📝 关键语法讲解

### 1. 字符串格式化（f-string）

```python
name = "北京"
print(f"我想去{name}旅游")  # 输出: 我想去北京旅游
```

### 2. 函数定义

```python
def 函数名(参数1, 参数2):
    # 函数体（要做的事情）
    return 返回值
```

### 3. 列表和字典

```python
# 列表（有序的容器）
fruits = ["苹果", "香蕉", "橙子"]
print(fruits[0])  # 输出: 苹果

# 字典（键值对容器）
person = {"name": "小明", "age": 18}
print(person["name"])  # 输出: 小明
```

### 4. JSON 数据

API 返回的数据通常是 JSON 格式，像字典一样读取：

```python
data = response.json()  # 把 JSON 变成 Python 字典
print(data["current_condition"])
```

---

## 🎯 练习建议

1. **修改城市**：把代码中的 `"北京"` 改成 `"上海"`，看看结果
2. **修改提示词**：编辑 `prompts.py`，让 AI 用不同的风格回答
3. **添加新工具**：尝试添加一个 `get_news(city)` 工具来获取城市新闻

---

## 📊 Debug.json - 运行过程日志

这个文件记录了智能体一次完整对话的**3次请示详情**，非常有助于理解智能体的工作流程。

### 🚦 三次请示的流程

| 次数 | 目的 | AI输出 | 工具调用 |
|------|------|--------|----------|
| **第一次** | 分析用户请求 | "我需要调用 get_weather 获取北京天气" | `get_weather(city="北京")` |
| **第二次** | 根据天气推荐景点 | "已获取天气，现在调用 get_attraction" | `get_attraction(city="北京", weather="Sunny")` |
| **第三次** | 总结回答用户 | "已收集足够信息，现在结束任务" | `Finish[最终答案]` |

### 📝 日志文件字段说明

**请求部分（request）：**
- `method`: HTTP 方法（POST）
- `path`: API 路径（`/v1/chat/completions`）
- `body.messages`: 发送给 AI 的消息列表
  - `role="system"`: 系统提示词（告诉 AI 它的身份和规则）
  - `role="user"`: 用户的问题 + 历史对话记录

**响应部分（response）：**
- `status`: HTTP 状态码（200 表示成功）
- `body.choices[0].message.content`: AI 的回复内容
  - `Thought`: AI 的思考过程
  - `Action`: AI 要执行的操作

**使用信息（usage）：**
- `prompt_tokens`: 输入的 token 数
- `completion_tokens`: AI 生成的 token 数
- `total_tokens`: 总 token 数

### 🔍 查看日志

打开 `Debug.json` 文件，可以看到每次请示的完整数据：

```json
{
"turn": 7,  // 第7次请示（第一次对话）
"request": {
    "body": {
    "messages": [
        {"role": "system", "content": "你是一个智能旅行助手..."},
        {"role": "user", "content": "用户请求: 你好，请帮我查询一下今天北京的天气..."}
    ],
    "model": "Qwen3.6:MTP"
    }
},
"response": {
    "body": {
    "choices": [{
        "message": {
        "content": "Thought: 用户想要查询北京的天气...\nAction: get_weather(city=\"北京\")"
        }
    }]
    }
}
}
```

---

## ❓ 常见问题

**Q: 为什么要配置 API_KEY？**
A: API 密钥相当于你的"身份证"，服务提供商需要验证你的身份才能让你使用。

**Q: 什么是环境变量？**
A: 就像一个全局的小黑板，程序可以从上面读取配置信息，不用写死在代码里。

**Q: 为什么要分多个文件？**
A: 这样更清晰，修改配置不用动代码，修改提示词也不用动核心逻辑。

---

## 📚 学习资源

- Python 基础：https://www.runoob.com/python/python-tutorial.html
- requests 库：https://docs.python-requests.org/
- OpenAI API：https://platform.openai.com/docs/introduction
