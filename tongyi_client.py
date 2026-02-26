import os
from qwen_agent.agents import Assistant
from config import tongyi_config, server_config
# LLM 配置
llm_cfg = {
    "model": tongyi_config["model"],
    "model_server": tongyi_config["base_url"],
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    "api_key": tongyi_config["api_key"],
}

# 系统消息
system = "你是会天气查询、生成随机倍数和获取股票行情的助手"

# 工具列表
tools = [
    {
        "mcpServers": {
            "get_current_weather": {
                "type": "sse",
                "url": server_config["mcp_server"]
            },
            "get_num_rand": {
                "type": "sse",
                "url": server_config["mcp_server"]
            },
            "get_stock_quote": {
                "type": "sse",
                "url": server_config["mcp_server"]
            }
        }
    }
]

# 创建助手实例
bot = Assistant(
    llm=llm_cfg,
    name="助手",
    description="一个MCP demo，用于天气查询、生成随机倍数和获取股票行情",
    system_message=system,
    function_list=tools,
)

messages = []

while True:
    query = input("\nuser question: ")
    if not query.strip():
        print("user question cannot be empty！")
        continue
    messages.append({"role": "user", "content": query})
    bot_response = ""
    is_tool_call = False
    tool_call_info = {}
    for response_chunk in bot.run(messages):
        new_response = response_chunk[-1]
        if "function_call" in new_response:
            is_tool_call = True
            tool_call_info = new_response["function_call"]
        elif "function_call" not in new_response and is_tool_call:
            is_tool_call = False
            print("\n" + "=" * 20)
            print("工具调用信息：", tool_call_info)
            print("工具调用结果：", new_response)
            print("=" * 20)
        elif new_response.get("role") == "assistant" and "content" in new_response:
            incremental_content = new_response["content"][len(bot_response):]
            print(incremental_content, end="", flush=True)
            bot_response += incremental_content
    # response_chunk 是消息列表，追加到历史消息中用于多轮对话
    messages.extend(response_chunk)