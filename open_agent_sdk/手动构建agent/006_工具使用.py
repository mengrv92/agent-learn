from agents import Agent, Runner, function_tool
import local_setting
import asyncio
import httpx

@function_tool
def get_weather(latitude, longitude):
    """一个示例工具函数，获取指定经纬度的当前天气信息。"""
    response = httpx.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    data = response.json()
    return f"{data['current_weather']['temperature']}°C, 风速 {data['current_weather']['windspeed']} km/h"
 

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，用中文帮助用户解答问题和提供信息。",
    model=local_setting.openai_provider.DEFAULT_MODEL,  # 使用配置的模型
    tools=[get_weather]  # 添加工具函数到 Agent 中
    ) 



async def main():
    result = await Runner.run(agent, "合肥的天气如何？")
    print("AI助手的回答：", result.final_output)
    
    
if __name__ == "__main__":
    asyncio.run(main())