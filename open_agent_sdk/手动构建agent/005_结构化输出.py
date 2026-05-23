from pydantic import BaseModel
from agents import Agent, Runner
import local_setting
import asyncio

class MyModel(BaseModel):
    姓名: str
    年龄: int
    性别: str
    爱好: list[str]
    事迹: str

agent = Agent(
    name="AI助手",
    instructions="""你是一个友好的AI助手。输出时必须严格使用以下JSON字段名：
- 姓名（字符串）
- 年龄（整数）
- 性别（字符串）
- 爱好（字符串数组）
- 事迹（字符串）

不要使用其他字段名，必须精确匹配上述字段。""",
    model=local_setting.openai_provider.DEFAULT_MODEL,  # 使用配置的模型
    output_type=MyModel
    ) 


    

async def main():
    result = await Runner.run(agent, "介绍一位值得记住的人物")
    
    obj: MyModel = result.final_output  # 直接获取解析后的对象
    print("AI助手的回答：", obj)
    print("姓名：", obj.姓名)
    print("年龄：", obj.年龄)
    print("性别：", obj.性别)
    print("爱好：", obj.爱好)
    print("事迹：", obj.事迹)
    
    
if __name__ == "__main__":
    asyncio.run(main())

