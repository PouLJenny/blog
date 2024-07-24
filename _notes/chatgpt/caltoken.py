import tiktoken

# To get the tokeniser corresponding to a specific model in the OpenAI API:
# enc = tiktoken.encoding_for_model("gpt-4")
enc = tiktoken.encoding_for_model("gpt-4o")
text = """移动电源；充电宝"""
out = enc.encode(text)

print(out)
print(enc.decode(out))
print("tokens数量:",len(out))


