# Maven

## 仓库镜像

[阿里云](https://developer.aliyun.com/mvn/guide )


## Repository Manager

maven官网推荐的一些私服[组件](https://maven.apache.org/repository-management.html )

<ul>
<li><a href="https://archiva.apache.org/" target="_blank" class="externalLink">Apache Archiva</a> (open source)</li>
<li><a href="https://bytesafe.dev/" target="_blank" class="externalLink">Bytesafe</a> (commercial)</li>
<li><a href="https://www.cloudrepo.io" target="_blank" class="externalLink">CloudRepo</a> (commercial)</li>
<li><a href="https://www.cloudsmith.io" target="_blank" class="externalLink">Cloudsmith Package</a> (commercial)</li>
<li><a href="https://www.dist.cloud" target="_blank" class="externalLink">Dist</a> (commercial)</li>
<li><a href="https://docs.gitea.io/en-us/packages/maven/" target="_blank" class="externalLink">Gitea</a> (open source)</li>
<li><a href="https://inedo.com/proget" target="_blank" class="externalLink">Inedo ProGet</a> (commercial)</li>
<li><a href="https://www.jfrog.com/open-source" target="_blank" class="externalLink">JFrog Artifactory Open Source</a> (open source)</li>
<li><a href="https://www.jfrog.com/artifactory/" target="_blank" class="externalLink">JFrog Artifactory Pro</a> (commercial)</li>
<li><a href="https://www.myget.org" target="_blank" class="externalLink">MyGet</a> (commercial)</li>
<li><a href="https://www.sonatype.com/products/repository-oss-download" target="_blank" class="externalLink">Sonatype Nexus OSS</a> (open source)
<a href="https://help.sonatype.com/repomanager3">document</a>
</li>  
<li><a href="https://links.sonatype.com/products/nexus/pro/home" target="_blank" class="externalLink">Sonatype Nexus Pro</a> (commercial)</li>
<li><a href="https://packagecloud.io" target="_blank" class="externalLink">packagecloud.io</a> (commercial)</li>
<li><a href="https://reposilite.com" target="_blank" class="externalLink">Reposilite</a> (open source)</li>
</ul>


## Sonatype Nexus OSS


### 安装启动

1. 下载安装包
2. [修改Data Dir](https://help.sonatype.com/repomanager3/installation-and-upgrades/configuring-the-runtime-environment#ConfiguringtheRuntimeEnvironment-ConfiguringtheDataDirectory )
    文件`$install-dir/bin/nexus.vmoptions`
    ```
    -Dkaraf.data=/opt/sonatype-work/nexus3
    -Djava.io.tmpdir=/opt/sonatype-work/nexus3/tmp
    -XX:LogFile=/opt/sonatype-work/nexus3/log/jvm.log
    -Dkaraf.log=/opt/sonatype-work/nexus3/log
    ```
3. `./nexus run` 直接启动 没问题的话 `./nexus start` 后台启动
4. 访问 http://poul-pc:8081/#browse/browse 账号 admin 密码 admin@123

### 配置
仓库类型
- proxy
- hosted
- group

需要设置nexus允许匿名访问

nexus中创建角色`deployment`配置权限
> nx-repository-view-maven2-maven-releases-*
> nx-repository-view-maven2-maven-snapshots-*
> nx-repository-view-maven2-maven-third-*

nexus中创建用户`deployment`选择角色`deployment`

`settings.xml`文件中添加配置
```xml
<profiles>
	<profile>
		<id>nexus</id>
      	<repositories>
        		<repository>
          			<id>nexus</id>
          			<name>Nexus </name>
      	  		    <url>http://poul-pc:8081/repository/maven-public/</url>
          			<releases><enabled>true</enabled></releases>
          			<snapshots><enabled>true</enabled></snapshots>
        		</repository>
      	</repositories>
      	<pluginRepositories>
        		<pluginRepository>
          			<id>nexus</id>
          			<name>Nexus Plugin Repository</name>
      			    <url>http://poul-pc:8081/repository/maven-public/</url>
          			<releases><enabled>true</enabled></releases>
          			<snapshots><enabled>true</enabled></snapshots>
        		</pluginRepository>
      	</pluginRepositories>
	</profile>
</profiles>


<activeProfiles>
	<activeProfile>nexus</activeProfile>
</activeProfiles>


<servers>
	<server>
		<id>nexus-releases</id>
		<username>deployment</username>
		<password>deployment</password>
	</server>
	<server>
		<id>nexus-snapshots</id>
		<username>deployment</username>
		<password>deployment</password>
	</server>
	<server>
		<id>nexus-third</id>
		<username>deployment</username>
		<password>deployment</password>
	</server>
</servers>
<mirrors>
    <mirror>
            <id>poulmaven</id>
            <name>poul maven</name>
            <url>http://poul-pc:8081/repository/maven-public/</url>
            <mirrorOf>*</mirrorOf>
    </mirror>
</mirrors>
```

`pom.xml`文件中需要添加
```xml
<distributionManagement>
	<repository>
		<id>nexus-releases</id>
		<name> Nexus Release Repository</name>
		<url>http://poul-pc:8081/repository/maven-releases/</url>
	</repository>
	<snapshotRepository>
		<id>nexus-snapshots</id>
		<name> Nexus Snapshot Repository</name>
		<url>http://poul-pc:8081/repository/maven-snapshots/</url>
	</snapshotRepository>
</distributionManagement>
```

手动上传jar包到third仓库
```shell
mvn deploy:deploy-file -DgroupId=com.csource -DartifactId=fastdfs-client-java -Dversion=1.24 -Dpackaging=jar -Dfile=F:\DevelopmentKit\fastdfs_client_v1.24.jar -Durl=http://poul-pc:8081/repository/maven-third/ -DrepositoryId=nexus-third
```

