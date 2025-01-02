# Neo4j

[官网](https://neo4j.com/)
[github](https://github.com/neo4j/neo4j)


[neo4j-browser github](https://github.com/neo4j/neo4j-browser)


[最新的neo4j-browser](https://browser-canary.graphapp.io/)


## 安装

1. clone代码 `https://github.com/neo4j/neo4j`
2. `mvn clean package -Dmaven.test.skip=true`
3. `packaging/standalone/target/neo4j-community-xxx` 目录下面,执行 `./bin/neo4j start`
4. 由于默认无法外网访问，需要修改配置文件`neo4j.conf`
```conf
server.default_listen_address=0.0.0.0
```
5. 访问http://browser-canary.graphapp.io/，这里注意使用http而不是https
6. 配置 连接url neo4j://10.0.1.3:7687 初始账号密码： neo4j neo4j, 修改后的密码： neo4j&neo4j
7. 也可以使用neo4j-browser项目自己打包运行
   1. 使用nvm下载`package.json`文件中指定的node版本
   2. `npm install -g yarn`
   3. `yarn install`
   4. `yarn start`
   5. 访问`localhost:8080`即可

