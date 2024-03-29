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
    'viewport-width': '1920'
}

# 注意：referrer要根据实际情况使用，这里是示例
referrer = "https://www.amazon.co.jp/s?k=prime&language=en_US&refresh=1&ref=glow_cls"


proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
    

# 要爬取的亚马逊页面的URL
# url = 'https://www.amazon.com/s?k=gaming+chair&page=1'
url = 'https://www.amazon.co.jp/s?k=%E3%82%B4%E3%83%AB%E3%83%95%E3%83%9C%E3%83%BC%E3%83%AB&crid=2ESXJDPVS2PLI&sprefix=go%2Caps%2C657&ref=nb_sb_ss_ts-doa-p_5_2' 

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
