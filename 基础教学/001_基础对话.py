from openai import OpenAI

# 阿里云百炼 Coding Plan 配置（sk-sp- 格式是套餐专属 Key）
api_key = ""
base_url = ""  # Coding Plan 专属 Base URL

client = OpenAI(api_key=api_key, base_url=base_url)

for t in [0, 0.3, 0.7, 1.0, 1.2, 1.5]:  # 不同温度参数的测试
    completion = client.chat.completions.create(
        model="qwen3-coder-plus",  # Coding Plan 支持的模型：qwen3-coder-plus, glm-5, kimi-k2.5 等
        messages=[
            {"role": "system", "content": "回复等于十个字"},
            {"role": "user", "content": "你是谁"}
        ],
        temperature=t
    )
    
    print(f"Temperature: {t}, Response: {completion.choices[0].message.content}")
    
    

