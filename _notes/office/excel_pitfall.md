# Excel 实战过程中遇到的坑

## Excel打开csv文件乱码

微软为了识别文件的编码信息搞了一个BOM的机制
相关[wiki](https://en.wikipedia.org/wiki/Byte_order_mark )

使用vi做二进制文件编辑
https://www.zhihu.com/question/22281280

GBK文件没有BOM的规定，excel打开GBK的文件是走默认的编码配置

## 结论
- [修改excel的默认编码](https://answers.microsoft.com/zh-hans/msoffice/forum/all/excel%E6%89%93%E5%BC%80gbk%E6%A0%BC%E5%BC%8Fcsv/90a920d7-548e-468a-b2fb-d68c3c28168e )
- 推荐导出CSV的时候使用UTF8 with bom的格式，实测bom只对unicode编码生效，GB18030编码不起作用

