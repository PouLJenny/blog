import os
from openai import OpenAI

os.environ['http_proxy'] = 'socks5://localhost:1080'
os.environ['https_proxy'] = 'socks5://localhost:1080'

# 打开文件并读取api_key
with open('/Users/poul/.openai/api_key', 'r') as file:
    api_key_1= file.read().lstrip().rstrip()

client = OpenAI(
  api_key=api_key_1
)

content= """#1 dad cup
adventskalender 2023
 bissell spot clean pro heat
 kids buch
 koffer
 tresor
 vital baby nourish perfectly simple plates - toddler feeding plates - bright colours - bpa, phthala
 把上面每行翻译成中文，并按照一行原文一行翻译的格式返回"""

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "user", "content": content}
  ],
  temperature=0.1
)

print(completion.choices[0].message.content)
