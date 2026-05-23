from agents import Agent, Runner, function_tool
import local_setting
import asyncio
import httpx
import os
from agents.mcp import MCPServerStdio

# 获取脚本所在目录，用于定位相对路径的资源文件
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

@function_tool
def get_weather(latitude, longitude):
    """一个示例工具函数，获取指定经纬度的当前天气信息。"""
    response = httpx.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    data = response.json()
    return f"{data['current_weather']['temperature']}°C, 风速 {data['current_weather']['windspeed']} km/h"
 




async def main():
    # 1. 启动MCPServer
    # 2. 获取MCPServer中的tools
    # 3. 将tools添加到Agent中
    
    async with MCPServerStdio(
        name="mcp demo",
        params= {
            "command": "python",  # 启动工具的命令
            "args": ["-u", os.path.join(SCRIPT_DIR, "mcp_server.py")],  # 使用绝对路径启动 MCP server
        }
    ) as mcp_server:
        agent = Agent(
            name="AI助手",
            instructions="你是一个友好的AI助手，用中文帮助用户解答问题和提供信息。",
            model=local_setting.openai_provider.DEFAULT_MODEL,  # 使用配置的模型
            tools=[get_weather],  # 添加工具函数到 Agent 中
            mcp_servers=[mcp_server],  # 将 MCPServer 实例传递给 Agent
        ) 
        result = await Runner.run(agent, "当前目录有多少个文件？")
        print("AI助手的回答：", result.final_output)
        
        
   
    
    
if __name__ == "__main__":
    asyncio.run(main())