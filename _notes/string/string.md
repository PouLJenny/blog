


## 表情字符转8进制，给html使用

```js
function to8(str){
//把utf16的emoji表情字符进行转码成八进制的字符function utf16toEntities(str) {   // 检测utf16字符正则,只要落在0xD800到0xDBFF的区间，就要连同后面2个字节一起读取。
   // 类似的问题存在于所有的JavaScript字符操作函数
   var patt = /[\ud800-\udbff][\udc00-\udfff]/g;
    return str.replace(patt, function (char) {
        var H, L, code;        
        if (char.length === 2) {
            H = char.charCodeAt(0); // 取出高位  
            L = char.charCodeAt(1); // 取出低位  
            code = (H - 0xD800) * 0x400 + 0x10000 + L - 0xDC00; // 转换算法,知道这回事就行了~
            return "&#" + code + ";"; // HTML实体符
        } else {
            return char;
        }
    });
}
```
