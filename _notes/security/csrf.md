# CSRF

Cross-site request forgery

[wiki](https://en.wikipedia.org/wiki/Cross-site_request_forgery )


## 博客
https://tech.meituan.com/2018/10/11/fe-security-csrf.html


## 解决方案

### Synchronizer token pattern （STP）

`<input type="hidden" name="csrfmiddlewaretoken" value="KbyUmhTLMpYj7CD2di7JKP1P3qmLlkPt" />`

### Cookie-to-header token


### Double Submit Cookie


### SameSite cookie attribute


### Client-side safeguards


### Other techniques

- Verifying that the request's headers contain X-Requested-With (used by Ruby on Rails before v2.0 and Django before v1.2.5), or checking the HTTP Referer header and/or HTTP Origin header. However, this is insecure – a combination of browser plugins and redirects can allow an attacker to provide custom HTTP headers on a request to any website, hence allowing a forged request.
- Checking the HTTP Referer header to see if the request is coming from an authorized page is commonly used for embedded network devices because it does not increase memory requirements. However, a request that omits the Referer header must be treated as unauthorized because an attacker can suppress the Referer header by issuing requests from FTP or HTTPS URLs. This strict Referer validation may cause issues with browsers or proxies that omit the Referer header for privacy reasons. Also, old versions of Flash (before 9.0.18) allow malicious Flash to generate GET or POST requests with arbitrary HTTP request headers using CRLF Injection. Similar CRLF injection vulnerabilities in a client can be used to spoof the referrer of an HTTP request.
- POST request method was for a while perceived as immune to trivial CSRF attacks using parameters in URL (using GET method). However, both POST and any other HTTP method can be now easily executed using XMLHttpRequest. Filtering out unexpected GET requests still prevents some particular attacks, such as cross-site attacks using malicious image URLs or link addresses and cross-site information leakage through `<script> `elements (JavaScript hijacking); it also prevents (non-security-related) problems with aggressive web crawlers and link prefetching.