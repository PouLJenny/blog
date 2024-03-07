import requests
import re

# 设置请求头，模拟浏览器请求
headers = {
    'authority':'www.amazon.com',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language':'en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    'cache-control':'max-age=0',
    'cookie':'session-id=130-0116487-9762450; ubid-main=132-4629721-2028445; ubid-acbus=132-4629721-2028445; kndctr_7742037254C95E840A4C98A6_AdobeOrg_identity=CiYzNjM4NTY5Mjc0NzQwMzk0NjYzMDY4NzIxNTc4NzY3MjYwNDQ1MlITCN3b0oC5MRABGAEqBFNHUDMwAPABoNCWlrox; _mkto_trk=id:365-EFI-026&token:_mch-amazon.com-1700106828925-32500; AMCV_4A8581745834114C0A495E2B%40AdobeOrg=179643557%7CMCIDTS%7C19678%7CMCMID%7C36675581045416916600653717722173454991%7CMCAAMLH-1700711629%7C11%7CMCAAMB-1700711629%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1700114029s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1700106873897-374719.42_0; mbox=session#648cec39c72e44c4ba81e97d1db51b68#1700108753|PC#648cec39c72e44c4ba81e97d1db51b68.32_0#1763351693; s_lv=1700106896473; i18n-prefs=USD; s_vnum=2133661639847%26vn%3D3; s_nr=1705390494559-Repeat; s_dslv=1705390494560; x-main=R0kztEgob68AqTHCGhKv3uh5jANvsFu3aPccNQrW2zAaFtTKbJ5rJQUbMQ87Gx21; at-main=Atza|IwEBIE_PJ5MW6uwa5HXaNa1JplhLVpVwVmlTy-EhzxX0XNo9m8mqqfaDs0YYqLgsBzaH-BDNS1LuiF65gzFE6YMPAUQbLQ0JsihXSUZ1aaqSI2of7wkm_pBSHSzu_sObQTa5f9HwDxdtkd9-pWnQBo39FGV93iNgaqEX9Mcm7sAlGFX9gq18hEoCjNFYspytlDcBAOYLTjTeMac8oVpp-GsyR9H8k8uDnTa8k6ZVyron5xvh0w; sess-at-main="yv5cSujFLjpHwWFFNN3GESkjrkUlQ4+9arS40E/FnNs="; sst-main=Sst1|PQGxyOxuM4iqETIoQKxLJleFCQxmArNYpVXCG3xt8-bXNnlMG3srkzejcZf1NbB2mFIdv6-Ti1ml6gdzQASXrtRvwFm07d1rkVJOD9JqayFRMZdMCJIpFMA4vZBYy7O5dKE49DJpcJID-3nRU9_ZYyEJHK-zWoRgWnQARaZ2aLHl3gmb7nW0a2LVMmH9T2VTu5n8swz7broo5BLs0JbJvrLsvivCbCSuJXeDsSgmJW6iqjsZI9CaA_wuIhjywFxCHbC9p9-TvJaqdiJbi1RUbYQygFq-AXYjO8kQtibEiR9d-wo; session-id-time=2082787201l; lc-main=en_US; s_pers=%20s_fid%3D238EF3C32E405588-04DC7BD118839FAF%7C1863346295973%3B%20s_dl%3D1%7C1705495295973%3B%20gpv_page%3DUS%253AAZ%253ASOA-overview-sell%7C1705495295974%3B%20s_ev15%3D%255B%255B%2527NSGoogle%2527%252C%25271705464236256%2527%255D%252C%255B%2527AZUSSOA-sell%2527%252C%25271705493495974%2527%255D%255D%7C1863346295974%3B; aws-ubid-main=352-6102067-4184836; noflush_locale=zh-CN; regStatus=registered; awsc-uh-opt-in=""; awsc-color-theme=light; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCMID%7C36385692747403946630687215787672604452%7CMCIDTS%7C19782%7CMCAAMLH-1705384791%7C11%7CMCAAMB-1709086182%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCOPTOUT-1709205792s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6ImRmMDYyMjgyLTE4OGUtNDdmYi1hNjc1LThiYjllYWNhMzc3NCJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoid2ZkdkhXNUtsSUZZM1Q4WmZRcWNOd256cm10ZCtCcFhuT21uY0t6aW0wND0iLCJhcm4iOiJhcm46YXdzOmlhbTo6MDU4MjY0NDA5NDg1OnJvb3QiLCJ1c2VybmFtZSI6IlhYZ2FtZSJ9.ssa0h1bc0bBaaHVjvHI-w6sf3niD12sfOGEKKepUHwmD1X2XOt6Tb942QJ_VqD5Vtwl0RkDeoDIhU5s2vI6gqGcyKkfrd5KpUuzwJerYOn9ghG183a5JUGUTMQpcm-f-; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A058264409485%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22XXgame%22%2C%22keybase%22%3A%22wfdvHW5KlIFY3T8ZfQqcNwnzrmtd%2BBpXnOmncKzim04%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; noflush_awsccs_sid=2e845b5eaa3ba59083fb796024c4bab365a00ffcd86ed4cb098da57dd8904aa4; JSESSIONID=410523478FCB61823FD18C613B7CECE1; session-token=+jS54FpVMUwDWq7QUW+AE0fK+KmnRf4rSEaj9eh5B4TTQovDaUqRh6N9NQmyvabfn3YLWlCP8n/RxNFuS+D/R8yYMFDHPfj8CYgt3WZwmXwwKvgPxhrgTLA1FARbqd3D0uxqklh45F4y58cRiP2hoRzbbSKh2XoxXo8r6JM2jn5+IL0LiWBJ/LvOzHLsU1EuhVAY281gC7zZKrb4pSh5eJT4s+ToDT9uBuwKT2wZoQp94rCpqCP8Y2k+RS83hjOnZc6qJMiDHBgwH0kL90QMgHz1Hek9AE5l9f7Xfh/DABwA8SiJj1XxjqYffvoy/IINNeETCHe+k4aDFxbpwdJYxuE9II5KPWSM0IeGeWdX2M+KejnVR7l+SxZXXjL+yOaZ; skin=noskin; csm-hit=tb:1297CPB9VC9PXAWPFQKT+s-6WPXV5HTS67ZCC9JJ8MA|1709778619236&t:1709778619236&adb:adblk_no',
    'device-memory':'8',
    'downlink':'10',
    'dpr':'2',
    'ect':'4g',
    'rtt':'250',
    'sec-ch-device-memory':'8',
    'sec-ch-dpr':'2',
    'sec-ch-ua':'"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"macOS"',
    'sec-ch-viewport-width':'1680',
    'sec-fetch-dest':'document',
    'sec-fetch-mode':'navigate',
    'sec-fetch-site':'same-origin',
    'sec-fetch-user':'?1',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'viewport-width':'1680'
    }
    

# 要爬取的亚马逊页面的URL
url = 'https://www.amazon.com/s?k=gaming+chair&page=3'

# 发送HTTP GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 输出响应内容
    compressed_html = response.text
    # compressed_html = re.sub(r'\s+', ' ', compressed_html)
    print(compressed_html)
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
