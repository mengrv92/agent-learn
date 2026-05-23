import json
from 基础教学.baseLLM import send_message
from 基础教学.tools import get_game_info


def agent(query):
    max_turns = 5  # 设置最大循环次数，防止无限循环
    current_turn = 0 # 当前循环次数
    next_message = {"role": "user", "content": query} # 用户输入的消息
    while current_turn < max_turns:
        message = send_message(next_message) # 发送消息给模型
        print(message['content'])  # 打印模型的响应内容
        if message["tool_calls"]:  # 如果模型调用了工具函数
            func_call_id = message["tool_calls"][0].id  # 获取工具调用的 ID
            func_call_args = json.loads(message["tool_calls"][0].function.arguments)  # 获取工具调用的 arguments
            func_result = get_game_info(**func_call_args)  # 调用工具函数获取结果
            
            print(f"观察: {func_result}")  # 打印工具函数的结果
            next_message = {
                "role": "tool",
                "content": str(func_result),
                "tool_call_id": func_call_id
            }  # 准备下一轮循环的消息，包含工具函数的结果
        else:
            break 
if __name__ == "__main__":
    agent("比赛场上，篮球队的人数乘以足球队的人数是多少？")
    agent("再乘以橄榄球队的场上人数，结果是多少呢？")