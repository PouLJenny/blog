import requests
import re

# 设置请求头，模拟浏览器请求
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',
    'device-memory': '8',
    'downlink': '1.55',
    'dpr': '2',
    'ect': '3g',
    'rtt': '400',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '2',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"13.0.0"',
    'sec-ch-viewport-width': '1920',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'viewport-width': '1920',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'cookie': 'session-id=356-2519580-3741617; session-id-time=2082787201l; i18n-prefs=JPY; ubid-acbjp=358-8605154-6257824; lc-acbjp=ja_JP; skin=noskin; session-token="rsnvOcB0HUBm0HOb+k8UeD44Yz6xglzv3/pJA9CMDJt6LJIMMWuUlVkGvxghc4/Vw6pelJ/hdgtho1gQ2A0dYhkQcx8IjVUjnmIHb8jXsA1BAbH8ti1DtbQkzxF+IMOmz4JoFhgEmWJ/xzAwBmgbnOdfsLXfcEefi7+X9EW4pZc0lqqwcCx90u9bySqzd7WtTv/Ph7eXhWLir3refh2UL5rzBsBT4eFb9ouUcjRJ58jOcW0na/kFvppn/5kA+AWOYQFYLU6aZFSqjgETEcD3EwFWfftGAvm2XhKW/8WEK5l+Qe55Zc1cNjEELu2ZEo1F8PIrpkuzHbwuvxiU1dHFgJmtHMlTvdxielAQbDXgcZE="; csm-hit=tb:BH6Z5D12S30GSB4AA1MK+sa-M21WFEENDPVRT654RSR2-9VRG3JWHYAXPRR91H9VA|1712488244306&t:1712488244306&adb:adblk_no'
}

# 注意：referrer要根据实际情况使用，这里是示例
referrer = "https://www.amazon.co.jp/"


proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
    

# 要爬取的亚马逊页面的URL
# url = 'https://www.amazon.com/s?k=gaming+chair&page=1'
url = 'https://www.amazon.co.jp/s?k=goto&page=2&crid=2ML53FWCOQFQ3&qid=1712488111&sprefix=%2Caps%2C720&ref=sr_pg_2' 

# 发送HTTP GET请求
response = requests.get(url, headers=headers,proxies=proxies,verify=False)
# response = requests.get(url, headers=headers)
# 检查响应状态码
if response.status_code == 200:
    # 输出响应内容
    compressed_html = response.text
    # compressed_html = re.sub(r'\s+', ' ', compressed_html)
    print(compressed_html)
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
