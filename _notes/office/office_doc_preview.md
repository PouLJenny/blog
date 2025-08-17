# Office 文件Web操作解决方案

## 一些产品
- https://products.conholdate.app/viewer/docx
- 

## MS / Google 官方预览借口
- `https://view.officeapps.live.com/op/view.aspx?src=[OFFICE_FILE_URL]`
- `https://docs.google.com/a/[DOMINIO]/viewer?url=[FILE_URL]`

## onlyoffice
[official website](https://www.onlyoffice.com/ )
[api document](https://api.onlyoffice.com/ )
[github](https://github.com/ONLYOFFICE/DocumentServer )


### docker安装
onlyoffice有三个版本的服务端
- community
  - `docker pull onlyoffice/documentserver`
- developer
  - `docker pull onlyoffice/documentserver-de` 
- enterprise 
  - `docker pull onlyoffice/documentserver-ee`

docker安装
`docker pull onlyoffice/documentserver-de:9.0.4.1`
`docker run -it  --name onlyoffice -p 30000:80 -d -e ALLOW_PRIVATE_IP_ADDRESS=true -e USE_UNAUTHORIZED_STORAGE=true -e NODE_TLS_REJECT_UNAUTHORIZED=0 -e JWT_ENABLED=false onlyoffice/documentserver-de:9.0.4.1`


**访问的时候需要使用本机的ip地址+端口号，不然编辑文档的时候会报错**
