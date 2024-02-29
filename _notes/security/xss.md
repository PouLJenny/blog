# XSS

Cross-site scripting，XSS

[wiki](https://en.wikipedia.org/wiki/Cross-site_scripting )

## 博客/文章
https://tech.meituan.com/2018/09/27/fe-security.html


## 分类
There is no single, standardized classification of cross-site scripting flaws, but most experts distinguish between at least two primary flavors of XSS flaws: non-persistent and persistent. Some sources further divide these two groups into traditional (caused by server-side code flaws) and DOM-based (in client-side code).


### Non-persistent (reflected)
一般是url的参数上带有注入的代码，点击的时候浏览器就会自动执行

### Persistent (or stored)
一般是注入的代码会被server端持久化，这样的话每次被查询到都会执行注入的代码，危险性较第一种更大

这种方式变种很多，比如通过IM聊天方式，邮件的方式、系统日志的方式等

#### 例子
Suppose that Mallory, an attacker, joins the site and wants to figure out the real names of the people she sees on the site. To do so, she writes a script designed to run from other users' browsers when they visit her profile. The script then sends a quick message to her own server, which collects this information.

To do this, for the question "Describe your Ideal First Date", Mallory gives a short answer (to appear normal), but the text at the end of her answer is her script to steal names and emails. If the script is enclosed inside a `<script>` element, it won't be shown on the screen. Then suppose that Bob, a member of the dating site, reaches Mallory's profile, which has her answer to the First Date question. Her script is run automatically by the browser and steals a copy of Bob's real name and email directly from his own machine.



### Server-side versus DOM-based vulnerabilities
xss攻击最开始被发现是在存储在后端的项目里

As the JavaScript code was also processing user input and rendering it in the web page content, a new sub-class of reflected XSS attacks started to appear that was called DOM-based cross-site scripting. In a DOM-based XSS attack, the malicious data does not touch the web server. Rather, it is being reflected by the JavaScript code, fully on the client side.


### Self-XSS

### Mutated XSS (mXSS)



