# Agent 开发问题总结

> 底层逻辑：问题复盘是能力成长的抓手，形成闭环才能避免重复踩坑。

---

## 一、环境变量加载问题

### 问题现象
```python
KeyError: 'OPENAI_BASE_URL'
```

### 根因分析
- `os.environ["KEY"]` 只能读取进程启动时继承的系统环境变量
- 未配置系统环境变量 → Python 进程拿不到 → KeyError

### 解决方案

| 方案 | 适用场景 | 操作 |
|------|---------|------|
| dotenv 加载 | 推荐，代码内解决 | `from dotenv import load_dotenv; load_dotenv()` |
| 系统环境变量 | 永久生效 | PowerShell: `[Environment]::SetEnvironmentVariable("KEY", "VAL", "User")`，需重启终端 |
| 命令行注入 | 临时测试 | `OPENAI_KEY=xxx python script.py` |

### 顶层设计建议
- 项目统一使用 `dotenv` + `.env` 文件方案
- `.env.example` 作为模板，不含真实密钥
- `.gitignore` 排除 `.env` 和 `.env.local`

---

## 二、API 地址与模型名不匹配

### 问题现象
```
model `qwen-vl-max` is not supported
model `glm-5` is not supported
```

### 根因分析
- 阿里云 DashScope 地址配了智谱 GLM 模型名
- 或智谱地址配了阿里云模型名
- API 端点不认这个模型

### 正确配置对齐

| 平台 | base_url | 文本模型 | 多模态模型 |
|------|----------|---------|-----------|
| 阿里云 DashScope | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus`, `qwen3.6-plus` | `qwen-vl-max`, `qwen3-vl-plus` |
| 智谱 GLM | `https://open.bigmodel.cn/api/paas/v4/` | `glm-4-flash`, `glm-4-plus` | `glm-4v` |

---

## 三、多模态图片识别问题

### 问题现象
```
抱歉，我看不到您提到的图片
```

### 根因分析（多层问题）

| 层级 | 问题 | 解决方案 |
|------|------|---------|
| 路径层 | 相对路径找不到文件 | 用 `os.path.join(SCRIPT_DIR, "file.png")` |
| 模型层 | 文本模型不支持图片 | 用 `qwen-vl-max` 而非 `qwen-plus` |
| 格式层 | 消息格式不对 | OpenAI 格式：`{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}` |

### 正确的多模态消息格式
```python
{
    "role": "user",
    "content": [
        {"type": "text", "text": "描述这张图片"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
    ]
}
```

---

## 四、结构化输出问题

### 问题现象
```python
ValidationError: Field required [type=missing]
ModelBehaviorError: Input should be an object, input_type=list
```

### 根因分析

**核心问题：阿里云不支持 OpenAI 的 `json_schema` 格式**

| API | structured output 能力 | 效果 |
|-----|----------------------|------|
| OpenAI 官方 | `response_format={"type": "json_schema", ...}` | 强制按 schema 输出，字段名、类型都保证 |
| 阿里云 DashScope | `response_format={"type": "json_object"}` | 只保证输出合法 JSON，**不保证字段名匹配** |

### 解决方案

即使设置了 `output_type=MyModel`，也必须在 **instructions 中明确指定字段名和格式**：

```python
instructions="""必须输出JSON对象格式：
{"姓名": "张三", "年龄": 30, "性别": "男", "爱好": ["阅读"], "事迹": "..."}
不要输出数组格式。"""
```

### 额外要求
- prompt 中必须包含 "json" 关键词（阿里云 API 规则）
- 给出具体示例，避免模型自由发挥字段名

---

## 五、ReAct Agent 循环逻辑问题

### 问题现象
Agent 无法算出最终结果，中途退出循环

### 根因分析
```python
# 错误写法
if message["content"]:  # 工具调用时 content 为空 → False → 直接 break
    # 处理工具调用
else:
    break
```

当模型调用工具时，`content` 为空，条件为 False，直接 break，工具根本没执行！

### 正确写法
```python
if message.get("tool_calls"):  # 检查是否有工具调用
    # 执行工具
else:
    break  # 模型给出最终答案
```

---

## 六、通用经验总结

### 1. API 兼容性颗粒度
- OpenAI Agents SDK 设计针对 OpenAI官方 API
- 第三方 API（阿里云、智谱）可能有功能差异
- 用第三方 API 时，需要查文档确认具体支持哪些功能

### 2. 错误信息的底层逻辑
- `KeyError` → 环境变量没加载
- `BadRequestError: model not supported` → 地址和模型不匹配
- `ValidationError: Field required` → 字段名不对齐
- `Input should be an object` → 输出格式不对（数组 vs 对象）

### 3. 验证闭环
- 先跑最小测试代码验证环境
- 再跑业务代码验证逻辑
- 出错时看完整 traceback，定位到具体行

---

> 因为信任所以简单，但因为简单所以需要更严谨的底层逻辑支撑。