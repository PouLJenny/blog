# email/电子邮件

[Electronic mail](https://en.wikipedia.org/wiki/Email )



## email protocol

- **SMTP**
- **POP3**
- **IMAP**


## 历史

- 1960 Email entered limited use, but users could only send to users of the same computer,and some early email systems required the author and the recipient to both be online simultaneously, similar to instant messaging.
- 1971 Ray Tomlinson is credited as the inventor of email.
he developed the first system able to send mail between users on different hosts across the *ARPANET*, using the @ sign to link the user name with a destination server

## 标准


- [RFC524](https://tools.ietf.org/html/rfc524 '')
- [RFC561](https://tools.ietf.org/html/rfc561 '')
- [RFC733](https://tools.ietf.org/html/rfc733 '')
- [RFC821](https://tools.ietf.org/html/rfc821 '')
- [RFC822](https://tools.ietf.org/html/rfc822 '')
- [RFC2045](https://tools.ietf.org/html/rfc2045 '')
- [RFC2047](https://tools.ietf.org/html/rfc2047 '')
- [RFC2049](https://tools.ietf.org/html/rfc2049 '')
- [RFC2822](https://tools.ietf.org/html/rfc2822 '')
- [RFC5321](https://tools.ietf.org/html/rfc5321 '') SMTP RFC 标准 
- [SMPT STD标准](https://www.rfc-editor.org/info/std10 '')
- [RFC5322](https://tools.ietf.org/html/rfc5322 '')
- [RFC3864](https://tools.ietf.org/html/rfc3864 '')


## SMTP/SMTP SSL 协议
Simple Mail Transfer Protocol 

Simple Mail Transfer Protocol is used to send mails over the internet. SMTP uses TCP as the transport layer protocol. It handles the sending and receiving of messages between email servers over a TCP/IP network.

默认端口: 25 
SSL默认端口: 465/587/2525 尽量使用587，2525通常作为备用端口
465 端口的协议是 Message Submission over TLS protocol [RFC 8314](https://www.iana.org/go/rfc8314)
587	端口的协议是 Message Submission [RFC 6409](https://www.iana.org/go/rfc6409)

SMTP相关的端口有这几个，25/587/465 - 25：该端口在 RFC 821引入，但是该端口默认是不支持SSL并且不用身份认证，而且很多ISP会拦截该端口的请求，所以推荐用于relaying阶段。 - 587：该端口在 RFC 2476中定义，需要身份认证，推荐用于submitting阶段。 - 465：这个端口设计的初衷是用于SSL连接，但是最终未被IETF采纳。所以很多文章介绍这个端口时，都建议不使用它。但是其实它还是有使用场景的，很多邮件服务器在submitting阶段，可以通过25/587建立TCP明文连接，然后再通过starttls和服务器进行协商，把TCP明文连接升级为SSL/TLS连接。而如果希望在和服务器第一次建立连接就是一个SSL/TLS连接，则需要使用465端口。 总结一下，submitting阶段有三种和SMTP建立连接的方式，他们分别使用以下端口 - 使用25/587建立TCP明文连接，进行发信 - 使用25/587建立TCP明文连接，执行STARTTLS，升级为SSL/TLS连接，进行发信 - 使用465端口建立SSL/TLS连接，进行发信

## POP3/POP3 SSL 协议
Post Office Protocol Version 3
Post Office Protocol is used to retrieve email for a single client.POP3 version is the current version of POP used.

默认端口: 110
SSL默认端口: 995

## IMAP/IMAP SSL 协议
Internet Message Access Protocol is used to retrieve mails for multiple clients. There are several IMAP versions: IMAP, IMAP2, IMAP3, IMAP4, etc. 

默认端口: 143
SSL默认端口: 993


[邮件协议的默认端口](https://www.cloudflare.com/zh-cn/learning/email-security/smtp-port-25-587/#:~:text=SMTPS%20%E7%9A%84%E5%AE%98%E6%96%B9%E9%BB%98%E8%AE%A4%E7%AB%AF%E5%8F%A3%E4%B8%BA%E7%AB%AF%E5%8F%A3587%E3%80%82 )


## Telnet 163邮箱发邮件
https://www.cnblogs.com/05-hust/p/14707724.html

授权码
```shell
## 明文
UMJLXEIFUZXKOEXK
## base64编码
VU1KTFhFSUZVWlhLT0VYSw==
```


