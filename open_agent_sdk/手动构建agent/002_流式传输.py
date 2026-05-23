from agents import Agent, Runner
import local_setting
import asyncio

# 用于处理流式响应中的文本增量事件
from openai.types.responses import ResponseTextDeltaEvent

# 创建 AI Agent 实例
agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，用中文帮助用户解答问题和提供信息。",
    model=local_setting.openai_provider.DEFAULT_MODEL  # 使用配置的模型
)


async def main():
    """
    流式传输示例：
    使用 Runner.run_streamed() 获取流式响应，实时输出文本内容
    """
    # 启动流式响应，传入 agent 和用户问题
    result = Runner.run_streamed(agent, "讲一个关于小松鼠的故事。至少三百字。")

    # 遍历流式响应事件
    async for event in result.stream_events():
        # 筛选原始响应事件中的文本增量事件
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # 实时输出每个增量文本片段（不换行，连续输出）
            print(event.data.delta, end="", flush=True)  # flush=True 确保立即显示


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())