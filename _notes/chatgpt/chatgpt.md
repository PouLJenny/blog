# 做一个ChatGPT的小App

## gpt开户升级教程
https://www.vpsdawanjia.com/8223.html
https://www.vvacard.com/index/Index/signIn.html

## 盈利模式

普通用户限制返回1000字

这样的话你就得付费，开会员，才能返回大于1000的文字

## 技术调研

### OpenAI API

[官方API文档](https://platform.openai.com/docs/api-reference/introduction)

#### 计算token的小工具
https://platform.openai.com/tokenizer

或者直接使用当前目录的小程序`caltoken.py`

#### 各个模型的api价格

https://openai.com/api/pricing/

#### api-keys
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

所有的请求都要带上这个参数：
```
Authorization: Bearer OPENAI_API_KEY
```

#### 关键概念

- Text generatiion models
- Assistants
- Embeddings
- Tokens

#### 限流策略

- RPM requests per minute
- RPD requests per day
- TPM tokens per minute
- TPD tokens per day
- IPM images per minute

batch api的限流策略(下面是chatgpt给我的回答):
The batch queue limits for the GPT-4o model in the OpenAI API are as follows:

Per-Batch Limits: A single batch may include up to 50,000 requests, and a batch input file can be up to 100 MB in size.
Rate Limits: GPT-4o supports up to 10 million tokens per minute for high-usage developers​




### Android

### 支付宝/微信的支付接口


## 资源准备

- 域名
- 服务器
- 支付账号