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
    instructions="""你是一个友好的AI助手。必须输出JSON对象格式，包含以下字段：

    {"姓名": "张三", "年龄": 30, "性别": "男", "爱好": ["阅读", "运动"], "事迹": "简要描述"}

    必须输出对象格式（带字段名），不要输出数组格式。""",
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
    print("完整对象：", result.to_input_list())  # 打印完整对象的字典形式
    
    
if __name__ == "__main__":
    asyncio.run(main())

