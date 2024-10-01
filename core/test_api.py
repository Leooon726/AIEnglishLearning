import os
from volcenginesdkarkruntime import Ark
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('ARK_API_KEY')

client = Ark(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="ep-20240930222858-7mzmx",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
print(completion.choices[0].message.content)

# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    model="ep-20240930222858-7mzmx",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    stream=True
)
for chunk in stream:
    if not chunk.choices:
        continue
    print(chunk.choices[0].delta.content, end="")
print()