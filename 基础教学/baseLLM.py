from openai import OpenAI
from 基础教学.tools import tools  # 导入工具函数列表

# 阿里云百炼 Coding Plan 配置（sk-sp- 格式是套餐专属 Key）
api_key = ""
base_url = ""  # Coding Plan 专属 Base URL

client = OpenAI(api_key=api_key, base_url=base_url)


system_prompt = """
你运行在一个思考、行动、观察和回答的循环中，在循环结束时，你输出最终答案。
用“思考”来描述你对被问问题的想法。
用“行动”来描述你将要采取的行动，例如调用一个函数、查询一个数据库等。
用“观察”来描述你从行动中得到的结果。
用“答案”来描述你最终的答案。
"""

# 使用变量保存历史记录
message_history = []

message_history.append({"role": "system", "content": system_prompt})  # 将系统提示添加到历史记录中


# 发送消息给大模型，并保存历史记录
def send_message(message):
    message_history.append(message)  # 将用户消息添加到历史记录中
    
    completion = client.chat.completions.create(
        model="glm-5",  # Coding Plan 支持的模型：qwen3-coder-plus, glm-5, kimi-k2.5 等
        messages=message_history,
        tools=tools  # 传入工具函数列表
    )
    
    response_dict = dict(completion.choices[0].message)  # 将响应转换为字典格式
    message_history.append(response_dict)  # 将模型响应添加到历史记录中
    
    return response_dict # 返回模型响应的字典格式





    

