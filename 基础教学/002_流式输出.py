from openai import OpenAI

# 阿里云百炼 Coding Plan 配置（sk-sp- 格式是套餐专属 Key）
api_key = ""
base_url = ""  # Coding Plan 专属 Base URL

client = OpenAI(api_key=api_key, base_url=base_url)

t=0.9  # 温度参数的测试


completion = client.chat.completions.create(
    model="qwen3-coder-plus",  # Coding Plan 支持的模型：qwen3-coder-plus, glm-5, kimi-k2.5 等
    messages=[
        {"role": "user", "content": "你是谁"}
    ],
    temperature=t,
    stream=True  # 开启流式输出
)

# 逐步打印流式输出的内容
for chunk in completion:
    print(f"{chunk.choices[0].delta.content}", end='') 

    

