# Zookeeper

## 简介

[官网](https://zookeeper.apache.org/ '')

## 数据模型/Data Model

### Znode

- Persistent Nodes
- Ephemeral Nodes
- Sequence Nodes -- Unique Naming
- Container Nodes **Added in 3.6.0**
- TTL Nodes **Added in 3.6.0**
When creating PERSISTENT or PERSISTENT_SEQUENTIAL znodes, you can optionally set a TTL in milliseconds for the znode. If the znode is not modified within the TTL and has no children it will become a candidate to be deleted by the server at some point in the future.

Note: TTL Nodes must be enabled via System property as they are disabled by default

## ZooKeeper Stat Structure
The Stat structure for each znode in ZooKeeper is made up of the following fields:

`czxid` The zxid of the change that caused this znode to be created.
`mzxid` The zxid of the change that last modified this znode.
`pzxid` The zxid of the change that last modified children of this znode.
`ctime` The time in milliseconds from epoch when this znode was created.
`mtime` The time in milliseconds from epoch when this znode was last modified.
`version` The number of changes to the data of this znode.
`cversion` The number of changes to the children of this znode.
`aversion` The number of changes to the ACL of this znode.
`ephemeralOwner` The session id of the owner of this znode if the znode is an ephemeral node. If it is not an ephemeral node, it will be zero.
`dataLength` The length of the data field of this znode.
`numChildren` The number of children of this znode.


## 命令行

### ZooKeeper Commands: The Four Letter Words
ZooKeeper responds to a small set of commands. Each command is composed of four letters. You issue the commands to ZooKeeper via telnet or nc, at the client port.

Three of the more interesting commands: "stat" gives some general information about the server and connected clients, while "srvr" and "cons" give extended details on server and connections respectively.

**New in 3.5.3**: Four Letter Words need to be explicitly white listed before using. Please refer to 4lw.commands.whitelist described in cluster configuration section for details. Moving forward, Four Letter Words will be deprecated, please use AdminServer instead.

- `conf` : **New in 3.3.0**: Print details about serving configuration.
- `cons` : **New in 3.3.0**: List full connection/session details for all clients connected to this server. Includes information on numbers of packets received/sent, session id, operation latencies, last operation performed, etc...
- `crst` : **New in 3.3.0**: Reset connection/session statistics for all connections.
- `dump` : Lists the outstanding sessions and ephemeral nodes.
- `envi` : Print details about serving environment
- `ruok` : Tests if the server is running in a non-error state. When the whitelist enables ruok, the server will respond with imok if it is running, otherwise it will not respond at all. When ruok is disabled, the server responds with: "ruok is not executed because it is not in the whitelist." A response of "imok" does not necessarily indicate that the server has joined the quorum, just that the server process is active and bound to the specified client port. Use "stat" for details on state wrt quorum and client connection information.
- `srst` : Reset server statistics.
- `srvr` : **New in 3.3.0**: Lists full details for the server.
- `stat` : Lists brief details for the server and connected clients.
- `wchs` : **New in 3.3.0**: Lists brief information on watches for the server.
- `wchc` : **New in 3.3.0**: Lists detailed information on watches for the server, by session. This outputs a list of sessions(connections) with associated watches (paths). Note, depending on the number of watches this operation may be expensive (ie impact server performance), use it carefully.
- `dirs` : **New in 3.5.1**: Shows the total size of snapshot and log files in bytes
- `wchp` : **New in 3.3.0**: Lists detailed information on watches for the server, by path. This outputs a list of paths (znodes) with associated sessions. Note, depending on the number of watches this operation may be expensive (ie impact server performance), use it carefully.
- `mntr` : **New in 3.4.0**: Outputs a list of variables that could be used for monitoring the health of the cluster.

示例：
```shell
## 使用nc命令
## mac上安装nc命令 brew install netcat
echo mntr | nc 192.168.20.35 2181
## 使用telnet命令
telnet 192.168.20.35 2181
mntr
```

### AdminServer **New in 3.5.0**
The AdminServer is an embedded Jetty server that provides an HTTP interface to the four-letter word commands. By default, the server is started on port 8080, and commands are issued by going to the URL "/commands/[command name]", e.g., http://localhost:8080/commands/stat. The command response is returned as JSON. Unlike the original protocol, commands are not restricted to four-letter names, and commands can have multiple names; for instance, "stmk" can also be referred to as "set_trace_mask". To view a list of all available commands, point a browser to the URL /commands (e.g., http://localhost:8080/commands).

[详情见](https://zookeeper.apache.org/doc/r3.8.0/zookeeperAdmin.html#sc_4lw '')


