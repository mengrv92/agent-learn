import os

from openai import AsyncOpenAI
from agents.models import openai_provider

from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

# 创建异步 OpenAI 客户端
# 使用环境变量配置 base_url 和 api_key，支持对接第三方 API（如智谱 GLM）
client = AsyncOpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],  # API 服务地址，如 "https://open.bigmodel.cn/api/paas/v4/"
    api_key=os.environ["OPENAI_API_KEY"],    # API 密钥，从环境变量获取
)

# 设置默认 OpenAI 客户端，use_tracing=False 表示不使用内置追踪
set_default_openai_client(client, False)

# 设置 API 类型为 chat_completions（聊天补全模式）
set_default_openai_api("chat_completions")

# 禁用追踪功能，避免日志输出干扰
set_tracing_disabled(True)

# 设置默认模型名称，从环境变量读取（如 "glm-4-flash"）
openai_provider.DEFAULT_MODEL = os.environ["OPENAI_MODEL_NAME"]