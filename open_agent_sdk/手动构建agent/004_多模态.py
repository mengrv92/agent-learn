import os
from agents import Agent, Runner
import local_setting
import asyncio
import base64

# 获取脚本所在目录，用于定位相对路径的资源文件
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，用中文帮助用户解答问题和提供信息。",
    model=local_setting.openai_provider.DEFAULT_MODEL  # 使用配置的模型
    ) 


def image_to_base64(path: str) -> str:
    """将本地图片文件转换为 base64 字符串。"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")







async def main():
    # 使用绝对路径加载图片，避免工作目录问题
    image_path = os.path.join(SCRIPT_DIR, "helloWorld.png")
    image_b64 = image_to_base64(image_path)
    
    print(image_b64)  # 打印 base64 字符串，验证图片是否正确加载

    # OpenAI Responses API 多模态消息格式：
    # 一个消息的 content 是一个列表，包含文本和图片
    result = await Runner.run(agent, [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
                {"type": "text", "text": "请描述一下这张图片的内容。"},
            ]
        }
    ])
    print("AI助手的回答：", result.final_output)
    
    
if __name__ == "__main__":
    asyncio.run(main())