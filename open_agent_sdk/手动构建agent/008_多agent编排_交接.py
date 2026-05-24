from agents import Agent, Runner
import local_setting
import asyncio



agent_a = Agent(
    name="assistant_a",
    instructions="只用中文回答",
    model=local_setting.openai_provider.DEFAULT_MODEL  # 使用配置的模型
    ) 

agent_b = Agent(
    name="assistant_b",
    instructions="只用英文回答",
    model=local_setting.openai_provider.DEFAULT_MODEL  # 使用配置的模型
    ) 

agent_c = Agent(
    name="assistant_c",
    instructions="只用韩文回答",
    model=local_setting.openai_provider.DEFAULT_MODEL  # 使用配置的模型
    ) 

agent = Agent(
    name="AI助手",
    model=local_setting.openai_provider.DEFAULT_MODEL,  # 使用配置的模型
    instructions="你是调度者，只负责分析用户提问的语言，并把问题转发给对应语言的子Agent处理：中文转给assistant_a，英文转给assistant_b，韩文转给assistant_c。",
    handoffs= [agent_a, agent_b, agent_c]
    ) 



async def main():
    result = await Runner.run(agent, "안녕하세요, 요즘 어떻게 지내세요?")  # 韩文问题会被转发给 agent_c 处理
    print("AI助手的回答：", result.final_output)  # 打印完整对象的字典形式
    
    result = await Runner.run(agent, "Hello, how are you doing?")  # 英文问题会被转发给 agent_b 处理
    print("AI助手的回答：", result.final_output)  # 打印完整对象
    
    result = await Runner.run(agent, "你好，最近怎么样？")  # 中文问题会被转发给 agent_a 处理
    print("AI助手的回答：", result.final_output)  # 打印完整对象
    
    
if __name__ == "__main__":
    asyncio.run(main())