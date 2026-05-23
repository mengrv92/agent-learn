from agents import Agent, Runner
import local_setting
import asyncio

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，用中文帮助用户解答问题和提供信息。",
    model=local_setting.openai_provider.DEFAULT_MODEL  # 使用配置的模型
    ) 



async def main():
    result = await Runner.run(agent, "1+1=？")
    
    history = result.to_input_list()  # 获取对话历史，包含用户输入和 AI 回答
    print(history)  # 打印对话历史，查看之前的交互内容
    history.append({"role": "user", "content": "再+1=？"})  # 在历史中添加新的用户输入
    result = await Runner.run(agent, history)  # 使用更新后的历史继续对话
    print(result.final_output)
    
    print("AI助手的回答：", result.to_input_list())  # 打印最终的对话历史，包含所有交互内容
    
    
if __name__ == "__main__":
    asyncio.run(main())