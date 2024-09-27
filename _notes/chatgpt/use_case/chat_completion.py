# pip install openai
# pip install httpx[socks]
import os
from openai import OpenAI

os.environ['http_proxy'] = 'socks5://localhost:1080'
os.environ['https_proxy'] = 'socks5://localhost:1080'

# 打开文件并读取api_key
with open('/home/poul/.openai/api_key', 'r') as file:
    api_key_1= file.read().lstrip().rstrip()

client = OpenAI(
  api_key=api_key_1
)

content= """有一些数组，需要实现以下功能：
        1. 根据数组的子集分组，子集作为分组键，子集的基大于等于2，子集中的元素不重复
        2. 原始数组分配到对应的分组中，且一个原始数组只分配到一个分组中
        3. 如果分组键是另一个分组键的子集，则合并两个分组，分组键使用基最小的
        4. 分组键中子集元素的顺序使用大部分原始数组中出现的顺序
        5. 取分组数量最少的可能
     数组用List<T>表示,T表示范型， 方法入口签名为 `public <T> Map<List<T>, List<List<T>>> groupBySubList(List<List<T>> arrays)`"""

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "user", "content": content}
  ],
  temperature=0.1
)

print(completion.choices[0].message.content)
