import os
import re
import requests
from tavily import TavilyClient
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# ==========================================
# 1. 配置项 (从 .env 文件读取)
# ==========================================
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ==========================================
# 2. 指令模板 (从 prompts.py 导入)
# ==========================================
from Prompts import AGENT_SYSTEM_PROMPT

# ==========================================
# 3. 工具函数 (智能体的手脚)
# ==========================================
def get_weather(city: str) -> str:
    """通过调用 wttr.in API 查询真实的天气信息"""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        current_condition = data['current_condition'][0]  # current_condition 是一个列表
        weather_desc = current_condition['weatherDesc'][0]['value']  # weatherDesc 也是一个列表
        temp_c = current_condition['temp_C']
        return f"{city}当前天气:{weather_desc}，气温{temp_c}摄氏度"
    except requests.exceptions.RequestException as e:
        return f"错误:查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"

def get_attraction(city: str, weather: str) -> str:
    """根据城市和天气，使用Tavily Search API搜索并返回优化后的景点推荐"""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key or api_key == "YOUR_TAVILY_API_KEY":
        return "错误:未配置有效的TAVILY_API_KEY，无法搜索景点。"
    
    tavily = TavilyClient(api_key=api_key)
    query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"
    
    try:
        response = tavily.search(query=query, search_depth="basic", include_answer=True)
        if response.get("answer"):
            return response["answer"]
        
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")
        
        if not formatted_results:
            return "抱歉，没有找到相关的旅游景点推荐。"
        return "根据搜索，为您找到以下信息:\n" + "\n".join(formatted_results)
    except Exception as e:
        return f"错误:执行Tavily搜索时出现问题 - {e}"

# 将工具注册到字典中，方便主循环动态调用
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

# ==========================================
# 4. 接入大语言模型 (兼容OpenAI接口的客户端)
# ==========================================
class OpenAICompatibleClient:
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用LLM API来生成回应"""
        print("⏳ 正在调用大语言模型...")
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            
            # 兼容不同的API响应格式
            if isinstance(response, str):
                # 响应直接是字符串
                answer = response
            elif hasattr(response, 'choices') and response.choices:
                # 标准OpenAI格式
                answer = response.choices[0].message.content
            elif isinstance(response, dict) and 'choices' in response and response['choices']:
                # 字典格式响应
                answer = response['choices'][0]['message']['content']
            else:
                # 其他格式，尝试直接转换为字符串
                answer = str(response)
            
            print("✅ 大语言模型响应成功。")
            return answer
        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return "错误:调用语言模型服务时出错。"

# ==========================================
# 5. 主循环 (执行 Thought-Action-Observation 循环)
# ==========================================
def run_agent():
    llm = OpenAICompatibleClient(
        model=MODEL_ID,
        api_key=API_KEY,
        base_url=BASE_URL
    )

    user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
    prompt_history = [f"用户请求: {user_prompt}"]

    print(f"🗣️ 用户输入: {user_prompt}\n" + "="*50)

    for i in range(5):  # 设置最大循环次数防止死循环
        print(f"\n--- 🔄 循环 {i+1} ---")
        
        # 1. 构建 Prompt
        full_prompt = "\n".join(prompt_history)
        
        # 2. 调用 LLM 思考
        llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
        
        # 清理多余输出：模型可能会输出多余的Thought-Action，需要截断
        match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                print("⚠️ 已截断多余的 Thought-Action 对")
        
        print(f"🤖 模型输出:\n{llm_output}")
        prompt_history.append(llm_output)
        
        # 3. 解析 Action
        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
            observation_str = f"Observation: {observation}"
            print(f"👀 {observation_str}\n" + "="*50)
            prompt_history.append(observation_str)
            continue
            
        action_str = action_match.group(1).strip()

        # 如果是结束指令，直接打印结果并退出
        if action_str.startswith("Finish"):
            final_answer_match = re.match(r"Finish\[(.*)\]", action_str, re.DOTALL)
            final_answer = final_answer_match.group(1) if final_answer_match else action_str
            print(f"\n🎉 任务完成！最终答案: {final_answer}")
            break
        
        # 4. 执行工具调用
        tool_name_match = re.search(r"(\w+)\(", action_str)
        args_match = re.search(r"\((.*)\)", action_str)
        
        if not tool_name_match or not args_match:
            observation = f"错误: 无法解析动作格式 '{action_str}'"
        else:
            tool_name = tool_name_match.group(1)
            args_str = args_match.group(1)
            # 解析参数，仅支持双引号包裹的字符串参数
            kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

            if tool_name in available_tools:
                try:
                    observation = available_tools[tool_name](**kwargs)
                except TypeError as e:
                    observation = f"错误: 工具参数调用不匹配 - {e}"
            else:
                observation = f"错误: 未定义的工具 '{tool_name}'"

        observation_str = f"Observation: {observation}"
        print(f"👀 {observation_str}\n" + "="*50)
        prompt_history.append(observation_str)

if __name__ == "__main__":
    run_agent()