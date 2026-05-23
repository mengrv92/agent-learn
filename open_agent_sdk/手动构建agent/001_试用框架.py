from agents import Agent, Runner
import local_setting
import asyncio

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，用中文帮助用户解答问题和提供信息。",
    model=local_setting.openai_provider.DEFAULT_MODEL  # 使用配置的模型
    ) 



async def main():
    result = await Runner.run(agent, "请介绍一下你自己。")
    print("AI助手的回答：", result.final_output)
    
    
if __name__ == "__main__":
    asyncio.run(main())