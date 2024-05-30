import os
from openai import OpenAI

os.environ['http_proxy'] = 'socks5://localhost:1080'
os.environ['https_proxy'] = 'socks5://localhost:1080'

with open('/Users/poul/.openai/api_key', 'r') as file:
    api_key_1= file.read().lstrip().rstrip()

client = OpenAI(
  api_key=api_key_1
)


out = client.files.create(
  file=open("/Users/poul/tmp/translate_gpt/split_batch/v2-json1/batch-translate-v2-004.json1", "rb"),
  purpose="batch"
).to_json()


print(out)
