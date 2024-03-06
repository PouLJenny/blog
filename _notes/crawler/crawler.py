import requests

# 设置请求头，模拟浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 要爬取的亚马逊页面的URL
url = 'https://www.amazon.com/'

# 发送HTTP GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 输出响应内容
    print(response.text)
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
