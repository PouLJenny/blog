import os
from openai import OpenAI

os.environ['http_proxy'] = 'socks5://localhost:1080'
os.environ['https_proxy'] = 'socks5://localhost:1080'

with open('/Users/poul/.openai/api_key', 'r') as file:
    api_key_1= file.read().lstrip().rstrip()

client = OpenAI(
  api_key=api_key_1
)
outfile = "/Users/poul/tmp/translate_gpt/split_batch/batch_gpt_result/batch-translate-v2-037.json1.error.json1"
out = client.files.content("file-QiuirDrBTHYNm3U4ZsUtyQlm")
out.write_to_file(outfile)
print("done,file is",outfile)