import json
from 基础教学.baseLLM import send_message
from 基础教学.tools import get_weather

message = send_message({
    "role": "user",
    "content": "今天合肥的天气如何？"
})

print("模型响应：", message) # LLM 的完整响应内容


func_call_id = message['tool_calls'][0].id  # 获取工具调用的 ID
func_call_args = json.loads(message['tool_calls'][0].function.arguments) # 获取工具调用的 arguments
func_result = get_weather(**func_call_args)  # 调用工具函数获取结果

message = send_message({
    "role": "tool",
    "content": str(func_result),
    "tool_call_id": func_call_id
})

print("模型响应：", message) # LLM 的完整响应内容