import os
from openai import OpenAI

os.environ['http_proxy'] = 'socks5://localhost:1080'
os.environ['https_proxy'] = 'socks5://localhost:1080'

with open('/Users/poul/.openai/api_key', 'r') as file:
    api_key_1= file.read().lstrip().rstrip()

client = OpenAI(
  api_key=api_key_1
)
outfile = "/Users/poul/tmp/translate_gpt/split_batch/batch_gpt_result/batch-translate-v2-001-test.json1.res.file.json1"
out = client.files.content("file-hnMbY6882jaGzxNPMsLsrWoQ")
out.write_to_file(outfile)
print("done,file is",outfile)