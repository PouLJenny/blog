import tiktoken

# To get the tokeniser corresponding to a specific model in the OpenAI API:
# enc = tiktoken.encoding_for_model("gpt-4")
enc = tiktoken.encoding_for_model("gpt-4o")
text = """Translate each line above into Chinese, and only return Chinese in order.Please ensure that the number of input lines matches the number of output lines."""
out = enc.encode(text)

print(out)
print(enc.decode(out))
print("tokens数量:",len(out))


