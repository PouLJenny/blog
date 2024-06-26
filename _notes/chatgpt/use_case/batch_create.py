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

batch_input_file_id = "file-XQH1H7z7y1oClBhcPqE89OqN"

out = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "batch-translate-v2-004.json1"
    }
).to_json()


print(out)
