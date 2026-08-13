# Kubernetes 专家养成手册

> 目标：从 Docker 基础出发，系统性掌握 K8s，深入源码层理解机制，最终能独立应对生产环境的架构设计、部署交付、故障排查与性能调优。
>
> 预估总周期：16-20 周（按每周 8-10 小时业余时间计）
>
> **本手册采用三线并行结构：**
> - **实操线**：从源码编译启动集群开始，每个阶段配套破坏性实验
> - **文档线**：官方文档系统性精读（★必读 / ☆推荐 / △进阶）
> - **源码线**：编译 → 目录结构 → 逐组件源码阅读，追到机制底层
>
> 三条线在每个阶段交叉推进。先编译跑起来，再读文档建立心智模型，再钻源码验证理解。

---

# 目录

- [第零阶段：环境准备 + 源码编译](#第零阶段)
- [第一阶段：心智模型 + API 类型 + 控制器源码](#第一阶段)
- [第二阶段：真实 Java 工作负载 + 控制器/kubelet 源码](#第二阶段)
- [第三阶段：生产级运维 + 调度器/proxy 源码](#第三阶段)
- [第四阶段：故障排查与高级运维](#第四阶段)
- [第五阶段：进阶专题](#第五阶段)
- [附录 A：官方文档完整阅读清单](#附录a)
- [附录 B：源码阅读路线全图](#附录b)
- [附录 C：学习资源汇总](#附录c)
- [附录 D：核心学习方法论](#附录d)

---

<a name="第零阶段"></a>
# 第零阶段：环境准备 + 源码编译（第 0-1 周）

本阶段目标：把 K8s 源码编译出来，用自己编译的二进制启动一个白盒集群。这是后续所有学习的基础设施。

## 0.1 Docker 基础自检

开始前确认你能独立完成以下操作（不能的先补）：

- [ ] 编写多阶段 Dockerfile（build stage + runtime stage）
- [ ] 理解 ENTRYPOINT vs CMD 的区别和组合
- [ ] docker build / tag / push 到 registry
- [ ] docker network 创建自定义网络，容器间通信
- [ ] docker volume 挂载持久化数据
- [ ] docker compose 编排多服务（你已有 sif-agent-infra 经验）

## 0.2 Go 语言最小必要知识

K8s 全部用 Go 编写。不需要成为 Go 专家，但需要能读懂源码。以你的 Java 背景，重点关注差异点。

| Go 概念 | Java 类比 | 差异要点 |
|---------|----------|---------|
| struct | class（无继承） | 没有类继承，用组合（embedding） |
| interface | interface | 隐式实现（无需 implements 声明），鸭子类型 |
| goroutine | 虚拟线程 | `go func()` 启动，比 Java 线程轻量得多 |
| channel | BlockingQueue | goroutine 间通信的核心机制 |
| select | — | 多 channel 多路复用，控制器大量使用 |
| context.Context | — | 取消传播、超时控制，几乎所有函数第一个参数 |
| defer | try-finally | 函数退出时执行清理 |
| package | package | 目录即 package，首字母大写 = public |
| error | Exception | 无异常机制，返回 error 值，`if err != nil` 模式 |
| pointer receiver | this | `func (s *Server) Run()` 中 `s` 类似 `this` |

**学习方式**：不要系统学 Go——直接用 K8s 源码当阅读材料，遇到不懂的语法再查。

| 资源 | URL | 用途 |
|------|-----|------|
| Go by Example | https://gobyexample.com/ | 语法速查，每概念一页带可运行示例 |
| Effective Go | https://go.dev/doc/effective_go | 惯用法参考 |

```bash
# Manjaro 安装 Go
sudo pacman -S go
go version    # 需要 1.22+（K8s master 分支当前要求）
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
source ~/.bashrc
```

## 0.3 克隆与编译源码

```bash
mkdir -p ~/code && cd ~/code
git clone https://github.com/kubernetes/kubernetes.git
cd kubernetes

# 切到最新稳定 release 分支，不要用 master（变化太快）
git branch -r | grep 'release-1\.' | tail -5
git checkout release-1.36

# 编译所有核心组件
make all

# 编译产物在 _output/bin/
ls _output/bin/
# kube-apiserver / kube-controller-manager / kube-scheduler
# kubelet / kube-proxy / kubectl / ...
```

仓库约 2GB，编译需要 Go 1.22+、make、gcc。你的 X670E + RTX 3090 大内存机器编译无压力。

**只编译单个组件（日常调试用）：**
```bash
make WHAT=cmd/kube-apiserver
make WHAT=cmd/kubectl
make WHAT=cmd/kubelet
```

## 0.4 两种集群环境：白盒与黑盒

### 白盒：从源码启动（理解机制用）

```bash
# 装 etcd
hack/install-etcd.sh
export PATH="${PWD}/third_party/etcd:${PATH}"

# 编译 + 启动所有组件（etcd → apiserver → controller-manager → scheduler → kubelet → kube-proxy）
hack/local-up-cluster.sh

# 另开终端操作
export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
kubectl get nodes
kubectl get pods -A
```

**为什么用 `local-up-cluster.sh` 而不是 kind？**
kind 是黑盒——看不到组件怎么启动、参数是什么、日志在哪。`local-up-cluster.sh` 是白盒——每个组件是独立进程，日志直接输出终端，可以：改源码 → 重编译单组件 → 替换二进制 → 重启；用 delve 断点调试某个组件。

### 黑盒：kind 多节点（练调度/高可用用）

源码集群是单节点，练习调度、反亲和性、Node drain 需要多节点。这时用 kind 补充：

```bash
sudo pacman -S kubectl helm k9s kubectx
go install sigs.k8s.io/kind@latest

cat <<EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
EOF
kind create cluster --name lab --config kind-config.yaml
```

### 必备工具链

| 工具 | 用途 | 安装 |
|------|------|------|
| kubectl | 核心 CLI | `pacman -S kubectl` |
| kind | 多节点本地集群 | `go install sigs.k8s.io/kind@latest` |
| helm | 包管理（第三阶段引入） | `pacman -S helm` |
| k9s | 终端 UI（强烈推荐） | `pacman -S k9s` |
| stern | 多 Pod 日志聚合 | `go install github.com/stern/stern@latest` |
| kubectx/kubens | 切换 context/namespace | `pacman -S kubectx` |
| delve | Go 调试器（断点调试源码） | `go install github.com/go-delve/delve/cmd/dlv@latest` |

## 0.5 源码目录结构全景（先建立地图）

```
kubernetes/
├── cmd/                        # ← 各组件 main() 入口
│   ├── kube-apiserver/         #   API Server
│   ├── kube-controller-manager/#   控制器管理器
│   ├── kube-scheduler/         #   调度器
│   ├── kubelet/                #   节点 Agent
│   ├── kube-proxy/             #   网络代理
│   ├── kubectl/                #   CLI 客户端
│   └── kubeadm/                #   集群引导工具
│
├── pkg/                        # ← 核心业务逻辑（被 cmd/ 导入）
│   ├── controller/             #   各种内置控制器
│   │   ├── deployment/         #     ★ Deployment 控制器（最值得精读）
│   │   ├── replicaset/         #     ReplicaSet 控制器
│   │   ├── statefulset/        #     StatefulSet 控制器
│   │   ├── job/                #     Job 控制器
│   │   ├── endpoint/           #     Endpoints 控制器
│   │   └── nodelifecycle/      #     Node 生命周期控制器
│   ├── kubelet/                #   kubelet 核心逻辑
│   ├── scheduler/              #   调度器核心逻辑
│   ├── proxy/                  #   kube-proxy 核心逻辑
│   └── volume/                 #   存储卷插件
│
├── staging/src/k8s.io/         # ← 拆分子项目（同步到独立 repo）
│   ├── api/                    #   API 类型定义
│   │   ├── core/v1/types.go    #     ★ Pod/Service/Node 等核心类型
│   │   └── apps/v1/types.go    #     ★ Deployment/StatefulSet/DaemonSet
│   ├── apimachinery/           #   API 基础设施（序列化/版本转换/Scheme）
│   ├── apiserver/              #   通用 API Server 框架
│   └── client-go/              #   Go 客户端库
│       ├── informers/          #     Informer 工厂
│       └── tools/cache/        #     ★ SharedInformer/DeltaFIFO/Reflector
│
├── hack/                       # 开发脚本
│   ├── local-up-cluster.sh     #   ★ 本地源码启动集群
│   ├── install-etcd.sh
│   └── verify-all.sh           #   提交 PR 前验证
├── build/                      # 构建脚本和 Dockerfile
└── test/                       # 测试（e2e / integration）
```

**关键认知：mono-repo + staging 同步机制**

K8s 用单一巨型仓库开发，但 `staging/src/k8s.io/` 下子项目被 `publishing-bot` 自动同步到独立 repo：

| staging 路径 | 独立 repo |
|-------------|----------|
| staging/src/k8s.io/api | github.com/kubernetes/api |
| staging/src/k8s.io/apimachinery | github.com/kubernetes/apimachinery |
| staging/src/k8s.io/client-go | github.com/kubernetes/client-go |
| staging/src/k8s.io/apiserver | github.com/kubernetes/apiserver |

外部项目（包括你若用 Go 写 Operator）导入的是独立 repo 的包。所以想找 Pod 定义不在 `pkg/api/pod`，而在 `staging/src/k8s.io/api/core/v1/types.go`。

## 0.6 阶段验收

- [ ] 成功编译出所有核心组件二进制
- [ ] 用 `hack/local-up-cluster.sh` 启动白盒集群并能 kubectl 操作
- [ ] kind 多节点集群可用
- [ ] 能在源码目录里快速定位任一组件的 main 入口

---

<a name="第一阶段"></a>
# 第一阶段：心智模型 + API 类型 + 控制器源码（第 2-4 周）

## 1.1 K8s 的本质

K8s 不是"容器编排工具"——这是市场部的说法。从工程视角看，它是**一个声明式、最终一致的分布式系统状态管理器**。核心循环只有一个：`Observe → Diff → Act`（控制器模式 / Reconciliation Loop）。你在 YAML 里写期望状态，控制器不断把实际状态往期望状态上靠。理解这一点，后面所有资源类型都是这个模式的具体实例。

## 1.2 文档线：建立全局视图

### 全局视角

| 优先级 | 页面 | URL | 时间 | 备注 |
|--------|------|-----|------|------|
| ★ | Overview | /docs/concepts/overview/ | 15min | 只读 "What K8s is/is not" 两段 |
| ★ | Kubernetes Components | /docs/concepts/overview/components/ | 20min | 画出 control-plane 和 node 各组件关系图 |
| ★ | The Kubernetes API | /docs/concepts/overview/kubernetes-api/ | 15min | 声明式 API 思想 |
| ★ | The kubectl tool | /docs/concepts/overview/kubectl/ | 10min | |

### 对象模型（理解"一切皆资源"）

| 优先级 | 页面 | URL | 时间 | 备注 |
|--------|------|-----|------|------|
| ★ | Object Management | /docs/concepts/overview/working-with-objects/object-management/ | 15min | 命令式 vs 声明式 |
| ★ | Labels and Selectors | /docs/concepts/overview/working-with-objects/labels/ | 15min | **松耦合核心机制，必须吃透** |
| ★ | Namespaces | /docs/concepts/overview/working-with-objects/namespaces/ | 10min | |
| ☆ | Finalizers | /docs/concepts/overview/working-with-objects/finalizers/ | 10min | 删除保护，排查资源删不掉时用 |
| ☆ | Owners and Dependents | /docs/concepts/overview/working-with-objects/owners-dependents/ | 10min | 级联删除基础 |

### 集群架构

| 优先级 | 页面 | URL | 时间 | 备注 |
|--------|------|-----|------|------|
| ★ | Cluster Architecture | /docs/concepts/architecture/ | 15min | |
| ★ | Nodes | /docs/concepts/architecture/nodes/ | 20min | Node 状态、心跳、条件 |
| ★ | Controllers | /docs/concepts/architecture/controller/ | 15min | **控制器模式是 K8s 的灵魂** |
| ☆ | Garbage Collection | /docs/concepts/architecture/garbage-collection/ | 10min | |
| ☆ | About cgroup v2 | /docs/concepts/architecture/cgroups/ | 10min | 容器资源隔离基础 |

## 1.3 源码线：API 类型定义

**配合文档"对象模型"，理解资源在代码里长什么样。**

```
staging/src/k8s.io/api/core/v1/types.go    （约 7000 行）
```

包含所有核心类型：Pod、Service、Node、Namespace、ConfigMap、Secret、PV、PVC。

```go
type Pod struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`
    Spec              PodSpec   `json:"spec,omitempty"`
    Status            PodStatus `json:"status,omitempty"`
}

type PodSpec struct {
    Containers         []Container       `json:"containers"`
    InitContainers     []Container       `json:"initContainers,omitempty"`
    Volumes            []Volume          `json:"volumes,omitempty"`
    NodeSelector       map[string]string `json:"nodeSelector,omitempty"`
    ServiceAccountName string            `json:"serviceAccountName,omitempty"`
    // ... 几十个字段
}
```

**要做的事：**
- 通读 Pod / PodSpec / PodStatus 字段定义，对照官方文档的 YAML 字段
- 看 Deployment 定义：`staging/src/k8s.io/api/apps/v1/types.go`
- 理解 `TypeMeta`（apiVersion + kind）和 `ObjectMeta`（name/namespace/labels/annotations/ownerReferences）是所有资源的公共头

## 1.4 源码线：控制器骨架（本阶段最有价值）

**配合文档"Controllers"概念。**

```
pkg/controller/deployment/deployment_controller.go
```

**所有控制器的统一骨架：Informer + WorkQueue + Reconcile**

```go
func (dc *DeploymentController) Run(workers int, stopCh <-chan struct{}) {
    // 1. 等待 Informer 缓存同步
    if !cache.WaitForCacheSync(stopCh, dc.dListerSynced, dc.rsListerSynced) {
        return
    }
    // 2. 启动 worker goroutine
    for i := 0; i < workers; i++ {
        go wait.Until(dc.worker, time.Second, stopCh)
    }
}

func (dc *DeploymentController) processNextWorkItem() bool {
    key, quit := dc.queue.Get()   // 从 WorkQueue 取 key
    if quit { return false }
    defer dc.queue.Done(key)
    err := dc.syncHandler(key)    // ← 这就是 Reconcile 逻辑
    dc.handleErr(err, key)
    return true
}
```

- **Informer**：watch etcd 变更，维护本地缓存
- **WorkQueue**：去重、限速、延迟重试
- **syncHandler（Reconcile）**：对比期望状态和实际状态，执行操作

读完 Deployment 控制器的 `syncDeployment()`，你就理解了滚动更新、扩缩容、回滚的所有细节。**读透这一个控制器，剩下所有控制器都是同一个骨架。**

## 1.5 源码线：kubectl（最简单的入口）

```
cmd/kubectl/kubectl.go                    → main()
staging/src/k8s.io/kubectl/pkg/cmd/cmd.go → NewKubectlCommand()
staging/src/k8s.io/kubectl/pkg/cmd/get/   → kubectl get 实现
```

追踪 `kubectl get pods` 的执行路径：main() → Cobra 命令注册 → `get.NewCmdGet()` → `RunGet()` → 调用 client-go 发 REST 请求 → 格式化输出。K8s 的 kubectl 大量使用 Builder 模式和 Visitor 模式。

## 1.6 实操线：核心资源动手（全部手写 YAML，禁止生成器）

### 资源学习顺序

```
Pod → ReplicaSet → Deployment → Service → Ingress → ConfigMap/Secret → Namespace
```

每个资源回答五个问题：描述什么状态？谁在 reconcile？和上下游什么关系？status 反映什么？常见失败模式？

### 练习 1：Pod 生命周期

```bash
kubectl run nginx --image=nginx:1.25 --dry-run=client -o yaml > pod.yaml
kubectl apply -f pod.yaml
kubectl describe pod nginx        # 看 Events
kubectl logs nginx
kubectl exec -it nginx -- bash
kubectl delete pod nginx          # 删了就没了——引出为什么需要 Deployment

# 破坏实验：不存在的镜像
kubectl run bad --image=nginx:nonexistent
kubectl describe pod bad          # 观察 ImagePullBackOff
```

### 练习 2：Deployment 与自愈

```bash
kubectl apply -f deployment.yaml  # replicas: 3
kubectl get rs                    # 观察 ReplicaSet
kubectl delete pod <某个pod>       # 观察自愈
kubectl scale deployment nginx --replicas=5
kubectl set image deployment/nginx nginx=nginx:1.26
kubectl rollout status deployment/nginx
kubectl rollout history deployment/nginx
kubectl rollout undo deployment/nginx

# 破坏实验：让滚动更新卡住
kubectl set image deployment/nginx nginx=nginx:broken-tag
kubectl rollout status deployment/nginx   # 卡住
kubectl get pods                          # 新旧 Pod 共存
kubectl rollout undo deployment/nginx     # 回滚
```

### 练习 3：Service 暴露与 DNS

```bash
kubectl expose deployment nginx --port=80 --type=ClusterIP
kubectl get endpoints nginx       # 确认非空
kubectl run debug --rm -it --image=nicolaka/netshoot -- bash
> nslookup nginx.default.svc.cluster.local
> curl nginx:80

# 破坏实验：改 selector 让它匹配不到 Pod
kubectl edit svc nginx
kubectl get endpoints nginx       # 应变空
```

## 1.7 阶段验收

- [ ] 不看文档能手写 Deployment + Service YAML
- [ ] 能解释 Pod → ReplicaSet → Deployment 三层关系，并在源码里指出对应实现
- [ ] 能读懂 Deployment 控制器的 `syncDeployment()` 核心逻辑
- [ ] 能用 kubectl 排查 CrashLoopBackOff（describe → events → logs）
- [ ] 理解 label selector 是松耦合的核心机制，并能在 `ObjectMeta` 里找到字段定义

---

<a name="第二阶段"></a>
# 第二阶段：真实 Java 工作负载 + kubelet 源码（第 5-8 周）

把熟悉的 Spring Boot 应用搬进 K8s，这一步会暴露大量实际问题。

## 2.1 Spring Boot 容器化最佳实践

```dockerfile
FROM eclipse-temurin:17-jdk AS build
WORKDIR /app
COPY . .
RUN ./gradlew bootJar -x test

FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
# 关键：不要硬编码 -Xmx，让 JVM 感知容器 cgroup 限制
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75.0 -XX:+UseG1GC"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

**JVM 与容器内存的关系——必须搞清：**
- 容器 `limits.memory` = JVM 堆 + 堆外（Metaspace、线程栈、NIO Direct Buffer、JIT CodeCache）
- `MaxRAMPercentage=75.0` = 堆占容器内存 75%，剩 25% 给堆外
- 堆外超了 → 容器 OOMKilled（exit 137），但 JVM 不报 OutOfMemoryError
- 生产建议：limits.memory = 实测堆外峰值 + 堆大小 + 200MB 缓冲

## 2.2 健康检查探针（三种必须全懂）

```yaml
spec:
  containers:
  - name: app
    livenessProbe:       # 失败 → 重启容器（检测死锁等不可恢复状态）
      httpGet: { path: /actuator/health/liveness, port: 8080 }
      initialDelaySeconds: 30
      periodSeconds: 10
      failureThreshold: 3
    readinessProbe:      # 失败 → 从 Service endpoints 摘除（优雅流量摘除）
      httpGet: { path: /actuator/health/readiness, port: 8080 }
      periodSeconds: 5
      failureThreshold: 3
    startupProbe:        # 未通过前 liveness/readiness 不生效（保护慢启动）
      httpGet: { path: /actuator/health, port: 8080 }
      failureThreshold: 30   # 30 * 5s = 150s 最大启动时间
      periodSeconds: 5
```

Spring Boot Actuator 2.3+ 原生支持 liveness/readiness 端点：

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
  health:
    livenessState: { enabled: true }
    readinessState: { enabled: true }
```

## 2.3 文档线：工作负载与配置

### 工作负载

| 优先级 | 页面 | URL | 时间 | 备注 |
|--------|------|-----|------|------|
| ★ | Pods | /docs/concepts/workloads/pods/ | 25min | 最小调度单元 |
| ★ | Pod Lifecycle | /docs/concepts/workloads/pods/pod-lifecycle/ | 20min | **Phase/Conditions/容器状态转换** |
| ★ | Probes | /docs/concepts/workloads/pods/probes/ | 15min | 三种探针语义差异 |
| ★ | Init Containers | /docs/concepts/workloads/pods/init-containers/ | 10min | |
| ★ | Deployments | /docs/concepts/workloads/controllers/deployment/ | 30min | **精读全文** |
| ★ | ReplicaSet | /docs/concepts/workloads/controllers/replicaset/ | 10min | |
| ★ | StatefulSets | /docs/concepts/workloads/controllers/statefulset/ | 20min | 有状态服务部署 |
| ☆ | DaemonSet | /docs/concepts/workloads/controllers/daemonset/ | 10min | 每节点一个 Pod |
| ☆ | Jobs / CronJob | /docs/concepts/workloads/controllers/job/ | 25min | 一次性/定时任务 |
| ☆ | Disruptions | /docs/concepts/workloads/pods/disruptions/ | 15min | PDB 基础 |
| ☆ | Pod QoS Classes | /docs/concepts/workloads/pods/pod-qos/ | 10min | Guaranteed/Burstable/BestEffort |

### 配置与存储

| 优先级 | 页面 | URL | 时间 | 备注 |
|--------|------|-----|------|------|
| ★ | ConfigMaps | /docs/concepts/configuration/configmap/ | 15min | |
| ★ | Secrets | /docs/concepts/configuration/secret/ | 15min | 注意：base64 不是加密 |
| ★ | Resource Management | /docs/concepts/configuration/manage-resources-containers/ | 25min | **requests/limits 精确语义，Java 必读** |
| ★ | Volumes | /docs/concepts/storage/volumes/ | 20min | |
| ★ | Persistent Volumes | /docs/concepts/storage/persistent-volumes/ | 25min | **PV/PVC/StorageClass 三件套** |
| ★ | Storage Classes | /docs/concepts/storage/storage-classes/ | 15min | 动态 provisioning |

### 实操指南（Tasks）

| 优先级 | 页面 | URL |
|--------|------|-----|
| ★ | Configure Probes | /docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ |
| ★ | Assign Memory Resources | /docs/tasks/configure-pod-container/assign-memory-resource/ |
| ★ | Assign CPU Resources | /docs/tasks/configure-pod-container/assign-cpu-resource/ |
| ★ | Configure Pod to Use ConfigMap | /docs/tasks/configure-pod-container/configure-pod-configmap/ |
| ★ | Distribute Credentials Securely | /docs/tasks/inject-data-application/distribute-credentials-secure/ |

## 2.4 源码线：kubelet 与探针

**配合文档"Pod Lifecycle"和"Probes"。**

```
cmd/kubelet/kubelet.go
pkg/kubelet/kubelet.go              → Kubelet 主逻辑
pkg/kubelet/pod_workers.go          → ★ syncPod() Pod 生命周期管理核心
pkg/kubelet/prober/                 → ★ 探针实现（liveness/readiness/startup）
pkg/kubelet/container/runtime.go    → 容器运行时接口（CRI）
```

kubelet 是最复杂的组件，重点看：
- `syncPod()`：Pod 状态同步的核心方法
- `prober/`：探针怎么执行、失败后怎么处理（对照你配的三种探针在代码里的行为）

## 2.5 实操线：Java 应用全链路上 K8s

### 配置管理实战

```yaml
# ConfigMap 存 application-k8s.yml
apiVersion: v1
kind: ConfigMap
metadata: { name: skill-platform-config }
data:
  application-k8s.yml: |
    spring:
      datasource: { url: jdbc:postgresql://pg-service:5432/skilldb }
      redis: { host: redis-service, port: 6379 }

# Secret 存敏感信息
apiVersion: v1
kind: Secret
metadata: { name: skill-platform-secrets }
type: Opaque
stringData:
  DB_PASSWORD: "your-password"
  CLAUDE_API_KEY: "sk-ant-..."
```

ConfigMap 两种挂载方式都做一遍（环境变量注入 vs 文件挂载），观察区别：文件挂载会自动更新（有延迟），环境变量不会。

### 有状态服务（StatefulSet + PV/PVC）

理解 StatefulSet 与 Deployment 三个核心区别：稳定网络标识（pod-0/pod-1）、稳定持久存储（每 Pod 绑定自己 PVC）、有序部署删除。

实操：用 StatefulSet 跑一个 PostgreSQL（学习用，生产数据库通常不放 K8s）。

```bash
kubectl apply -f postgres-statefulset.yaml
kubectl get pvc               # 观察 STATUS 是否 Bound
kubectl get pv                # 看自动创建的 PV

# 破坏实验：触发 OOMKilled
# 部署内存限制 128Mi 但实际吃 256Mi 的 Pod
kubectl describe pod oom-test # Last State: Terminated, Reason: OOMKilled, Exit Code: 137
```

### 网络模型深度理解

必须内化四个事实：每个 Pod 有独立 IP；所有 Pod 不经 NAT 直接互通；Service ClusterIP 是虚拟 IP（kube-proxy 通过 iptables/IPVS 实现）；DNS 解析 `<svc>.<ns>.svc.cluster.local` → ClusterIP → 后端 Pod。

```bash
kubectl get endpoints nginx
# kind 环境进 node 看 iptables 规则
docker exec -it lab-worker iptables -t nat -L KUBE-SERVICES
```

## 2.6 阶段验收

- [ ] 把 Spring Boot 应用完整部署到 K8s（含 ConfigMap/Secret/Probe/Resource Limits）
- [ ] 能解释 OOMKilled 排查思路（dmesg → container limits vs JVM 堆外内存）
- [ ] 能在 `pkg/kubelet/prober/` 里指出三种探针的执行逻辑
- [ ] 能画请求从 Ingress → Service → Pod 的完整链路
- [ ] 能执行零停机滚动更新和回滚

---

<a name="第三阶段"></a>
# 第三阶段：生产级运维 + 调度器/proxy 源码（第 9-12 周）

## 3.1 文档线：调度

| 优先级 | 页面 | URL | 时间 | 备注 |
|--------|------|-----|------|------|
| ★ | Kubernetes Scheduler | /docs/concepts/scheduling-eviction/kube-scheduler/ | 15min | 调度流程 |
| ★ | Assigning Pods to Nodes | /docs/concepts/scheduling-eviction/assign-pod-node/ | 15min | nodeSelector/Affinity |
| ★ | Taints and Tolerations | /docs/concepts/scheduling-eviction/taint-and-toleration/ | 15min | |
| ★ | Pod Priority and Preemption | /docs/concepts/scheduling-eviction/pod-priority-preemption/ | 15min | |
| ☆ | Topology Spread Constraints | /docs/concepts/scheduling-eviction/topology-spread-constraints/ | 15min | 跨 AZ 均匀分布 |
| ☆ | Node-pressure Eviction | /docs/concepts/scheduling-eviction/node-pressure-eviction/ | 15min | |

## 3.2 源码线：调度器

```
cmd/kube-scheduler/scheduler.go
pkg/scheduler/scheduler.go          → ★ scheduleOne() 调度主循环
pkg/scheduler/framework/            → 调度框架（插件机制）
pkg/scheduler/framework/plugins/    → 内置调度插件
```

调度核心流程：`scheduleOne()` → **Filter**（过滤不可用节点）→ **Score**（给剩余节点打分）→ **Bind**（绑定 Pod 到 Node）。对照你配的 nodeAffinity/taint/topologySpread 在调度器代码里是哪个插件。

## 3.3 实操线：调度高级特性

```yaml
# Node Affinity
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - { key: node-type, operator: In, values: ["compute"] }
  # Pod Anti-Affinity - 同 Deployment 的 Pod 分散到不同节点
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels: { app: skill-platform }
        topologyKey: kubernetes.io/hostname

# Topology Spread - 跨可用区均匀分布
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels: { app: skill-platform }
```

```bash
# kind 3 节点集群在这里发挥作用
kubectl label nodes lab-worker gpu=true
kubectl taint nodes lab-worker2 dedicated=special:NoSchedule
# Deployment 3 副本 + podAntiAffinity，观察是否分散到 3 节点
```

## 3.4 资源管理与容量规划

**requests vs limits 精确语义：**

| | requests | limits |
|---|---|---|
| 调度 | 调度器据此选 Node | 不影响调度 |
| 运行时 | 保底资源，CFS 份额 | 硬上限，超 CPU 被 throttle，超 Memory 被 OOMKill |
| 建议 | 实测 P95 | requests 的 1.5-2 倍 |

**Java 应用特别注意：**
- CPU limits 触发 CFS throttling，对延迟敏感 Java 应用影响很大，很多团队只设 requests 不设 CPU limits
- Memory limits 必须设，且 >= JVM 堆 + 堆外上限

```yaml
# Namespace 级默认限制和配额
apiVersion: v1
kind: LimitRange
metadata: { name: default-limits }
spec:
  limits:
  - default: { cpu: "500m", memory: "512Mi" }
    defaultRequest: { cpu: "100m", memory: "128Mi" }
    type: Container
---
apiVersion: v1
kind: ResourceQuota
metadata: { name: team-quota }
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    pods: "50"
```

## 3.5 文档线：安全（RBAC）

| 优先级 | 页面 | URL | 时间 | 备注 |
|--------|------|-----|------|------|
| ★ | RBAC Authorization | /docs/reference/access-authn-authz/rbac/ | 30min | **你有 Sandhu RBAC 论文基础，降维打击** |
| ★ | Service Accounts | /docs/concepts/security/service-accounts/ | 15min | Pod 身份 |
| ★ | Pod Security Standards | /docs/concepts/security/pod-security-standards/ | 15min | Privileged/Baseline/Restricted |
| ★ | Pod Security Admission | /docs/concepts/security/pod-security-admission/ | 15min | 怎么启用 |
| ☆ | Security Context | /docs/tasks/configure-pod-container/security-context/ | 15min | runAsNonRoot 等 |

你翻译过 Sandhu 1996 的 RBAC96 论文，K8s 的 RBAC 实现会很亲切：

```
Subject (User/Group/ServiceAccount)
  ──RoleBinding/ClusterRoleBinding──→ Role/ClusterRole (apiGroups + resources + verbs)
```

**源码：** `staging/src/k8s.io/apiserver/plugin/pkg/authorizer/rbac/` —— 对照论文画出 K8s RBAC 与 RBAC96 的映射关系。

```yaml
# 给 CI/CD ServiceAccount 最小权限
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: deployer-role, namespace: production }
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "update", "patch"]
```

## 3.6 源码线：kube-proxy

```
cmd/kube-proxy/proxy.go
pkg/proxy/iptables/proxier.go       → iptables 模式实现
pkg/proxy/ipvs/proxier.go           → IPVS 模式实现
```

看 Service → iptables 规则的生成逻辑，理解 ClusterIP 为什么是"虚拟 IP"——它根本不绑在任何网卡上，纯粹是 iptables NAT 规则。

## 3.7 可观测性体系

```bash
# Prometheus + Grafana（Helm 的正确使用场景）
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

# 日志：Loki + Promtail（比 EFK 轻量）
helm install loki grafana/loki-stack --namespace monitoring --set promtail.enabled=true
```

Java 应用暴露 Prometheus 指标（micrometer-registry-prometheus）：

```yaml
management:
  endpoints:
    web:
      exposure: { include: health,info,prometheus }
# Pod annotations 让 Prometheus 自动发现
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/actuator/prometheus"
```

关键 Grafana Dashboard：K8s Cluster (6417)、K8s Pods (6336)、JVM Micrometer (4701)、Node Exporter (1860)。

## 3.8 Helm 包管理

到这阶段引入 Helm，本质是 **YAML 模板引擎 + 版本管理**。

```bash
helm create skill-platform
# skill-platform/
#   Chart.yaml / values.yaml（参数化入口）
#   templates/ (deployment.yaml / service.yaml / _helpers.tpl)

helm template skill-platform ./skill-platform --values values-dev.yaml  # 调试
helm install skill-platform ./skill-platform -f values-prod.yaml         # 多环境
```

## 3.9 client-go 深度理解（源码线进阶）

`client-go` 是 K8s 生态最重要的库，所有控制器/Operator/工具都依赖它。

```
staging/src/k8s.io/client-go/
├── informers/       → SharedInformerFactory
├── tools/cache/     → ★ SharedInformer/DeltaFIFO/Reflector/Indexer
├── kubernetes/      → Clientset（类型安全客户端）
└── util/workqueue/  → WorkQueue（限速/延迟/去重）
```

**核心数据流（K8s 控制面的引擎）：**

```
API Server (etcd)
    │
  Reflector       ← List + Watch API Server
    │
  DeltaFIFO       ← 增量事件队列（Added/Updated/Deleted）
    │
  Indexer (Store) ← 本地缓存（内存中的 etcd 副本）
    │
  EventHandler    ← OnAdd/OnUpdate/OnDelete 回调
    │
  WorkQueue       ← 放入 key（namespace/name），去重
    │
  Reconcile Loop  ← 取出 key，从 Indexer 读最新状态，执行 sync
```

理解这个数据流，就理解了 K8s 怎么做到最终一致。

## 3.10 阶段验收

- [ ] 能为 Namespace 配置 ResourceQuota + LimitRange + RBAC
- [ ] 能搭建 Prometheus + Grafana 监控并配告警
- [ ] 能编写完整 Helm chart 并用 values 管理多环境
- [ ] 能在调度器源码里指出 Filter/Score/Bind 三阶段
- [ ] 能画出 client-go 的 Reflector → DeltaFIFO → Indexer → WorkQueue 数据流
- [ ] 能对照 Sandhu RBAC96 论文解释 K8s RBAC 实现

---

<a name="第四阶段"></a>
# 第四阶段：故障排查与高级运维（第 13-16 周）

## 4.1 文档线：调试

| 优先级 | 页面 | URL |
|--------|------|-----|
| ★ | Debug Pods | /docs/tasks/debug/debug-application/debug-pods/ |
| ★ | Debug Services | /docs/tasks/debug/debug-application/debug-service/ |
| ★ | Debug Running Pods | /docs/tasks/debug/debug-application/debug-running-pod/ |
| ★ | Troubleshoot Clusters | /docs/tasks/debug/debug-cluster/ |
| ★ | Safely Drain a Node | /docs/tasks/administer-cluster/safely-drain-node/ |
| ☆ | Determine Reason for Pod Failure | /docs/tasks/debug/debug-application/determine-reason-pod-failure/ |
| ☆ | Debugging DNS | /docs/tasks/administer-cluster/dns-debugging-resolution/ |

## 4.2 系统化故障排查框架（刻进脑子里）

```
应用层  →  kubectl logs / describe pod / exec
  ↓
网络层  →  endpoints / service / DNS / NetworkPolicy
  ↓
调度层  →  describe pod Events / node resources / taints / affinity
  ↓
存储层  →  PVC status / StorageClass / mount 权限
  ↓
节点层  →  describe node / kubelet logs / container runtime
  ↓
控制面  →  API Server / etcd / controller-manager / scheduler
```

**这套框架配合源码理解威力倍增**——当你知道 endpoints 是 endpoint 控制器维护的、Pending 是调度器没找到节点、OOMKilled 是 kubelet 执行的 cgroup 限制，排查时就能直接定位到对应组件和源码。

## 4.3 高频故障场景排查手册

**场景 1：Pod 一直 Pending**
```bash
kubectl describe pod <name>       # 看 Events 的 FailedScheduling
# Insufficient cpu/memory → 扩容或减 requests
# node(s) had taint → 加 toleration
# 0/3 nodes available → 检查 nodeSelector/affinity
kubectl describe nodes | grep -A 5 "Allocated resources"
```

**场景 2：CrashLoopBackOff**
```bash
kubectl logs <pod> --previous     # 上次崩溃日志
kubectl describe pod <pod>        # 看 exit code
# 137 = OOMKilled / 1 = 应用错误 / 143 = SIGTERM
```

**场景 3：Service 不通**
```bash
kubectl get endpoints <svc>       # 空 = selector 没匹配到 Pod
kubectl get pods -l app=xxx       # READY 是否 1/1
kubectl run debug --rm -it --image=nicolaka/netshoot -- bash
> curl <svc>:<port>
> curl <pod-ip>:<port>            # 绕过 Service 直连 Pod
kubectl get networkpolicy -A
```

**场景 4：滚动更新卡住** → 新版本 readinessProbe 一直不过，`kubectl rollout undo`

**场景 5：Node NotReady**
```bash
kubectl describe node <name>      # 看 Conditions
systemctl status kubelet
journalctl -u kubelet -f
crictl ps
```

**场景 6：PVC 一直 Pending** → 检查 StorageClass / provisioner / 容量

## 4.4 优雅停机（Graceful Shutdown）

Java 应用在 K8s 优雅停机完整链路：

```
K8s 发 SIGTERM ──┬── Pod 从 Service endpoints 摘除（有延迟！）
                 └── Spring Boot 收到 SIGTERM 开始优雅关闭
                       拒绝新请求 → 等在途请求完成 → 关连接池/线程池
超过 terminationGracePeriodSeconds → SIGKILL 强杀
```

```yaml
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: app
        lifecycle:
          preStop:
            exec:
              command: ["sh", "-c", "sleep 5"]
              # endpoints 摘除和 SIGTERM 并行，sleep 给 kube-proxy 更新 iptables 的时间
```

```yaml
# Spring Boot
server: { shutdown: graceful }
spring:
  lifecycle: { timeout-per-shutdown-phase: 30s }
```

## 4.5 网络策略 / PDB / HPA

```yaml
# 默认拒绝所有入站（白名单模式）
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: deny-all-ingress, namespace: production }
spec:
  podSelector: {}
  policyTypes: [Ingress]
---
# PDB：Node drain 时至少保留 2 个 Pod
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: skill-platform-pdb }
spec:
  minAvailable: 2
  selector:
    matchLabels: { app: skill-platform }
---
# HPA：CPU/内存自动扩缩
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: skill-platform-hpa }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: skill-platform }
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target: { type: Utilization, averageUtilization: 70 }
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300   # 缩容冷却 5 分钟
```

## 4.6 源码线：delve 调试实战

把排查从"看现象"提升到"看代码执行"：

```bash
# 编译带调试信息的二进制（禁用优化）
make WHAT=cmd/kube-controller-manager GOFLAGS="-gcflags=all='-N -l'"

# delve 启动
dlv exec _output/bin/kube-controller-manager -- \
  --kubeconfig=/var/run/kubernetes/controller.kubeconfig --leader-elect=false

# 设断点
(dlv) break pkg/controller/deployment/deployment_controller.go:syncDeployment
(dlv) continue
# 另一个终端 kubectl apply 一个 Deployment，触发断点，单步看 Reconcile 全过程
```

这是把 K8s 从黑盒彻底变白盒的终极手段——你可以亲眼看到滚动更新时控制器是怎么一步步创建新 ReplicaSet、缩减旧 ReplicaSet 的。

## 4.7 生产部署检查清单

每次上线前过一遍：

```
□ Resource requests/limits 基于压测数据（不拍脑袋）
□ Liveness/Readiness/Startup 探针全配置
□ 反亲和性确保 Pod 分散在不同 Node
□ PDB 防止运维操作导致全部下线
□ HPA 配置自动扩缩容
□ 优雅停机 preStop hook + Spring Boot graceful shutdown
□ ConfigMap/Secret 不含硬编码敏感信息
□ 镜像用具体 tag（不用 latest）
□ SecurityContext（non-root, readOnlyRootFilesystem）
□ NetworkPolicy 限制网络访问范围
```

## 4.8 阶段验收

- [ ] 给定故障现象，5 分钟内定位到根因层，并能说出对应是哪个组件/控制器的源码
- [ ] 能配置完整生产部署（PDB + HPA + NetworkPolicy + 优雅停机）
- [ ] 能执行 Node drain 且服务零停机
- [ ] 能用 delve 在控制器源码里打断点观察 Reconcile
- [ ] 理解 SIGTERM → preStop → graceful shutdown 完整链路

---

<a name="第五阶段"></a>
# 第五阶段：进阶专题（第 17-20 周，按需深入）

根据实际业务需求选择性学习，不需要全部掌握。

## 5.1 Operator 与 CRD（源码能力的变现）

学完前四阶段的控制器源码后，你已经具备写 Operator 的全部知识。Operator 本质就是：自定义资源（CRD）+ 自定义控制器（复用你读过的 Informer + WorkQueue + Reconcile 骨架）。

对你的 Skill Platform 来说，如果未来需要管理有复杂生命周期的自定义资源（比如 Skill 实例的编排），Operator 是自然的选择。推荐用 kubebuilder 或 controller-runtime 框架。

## 5.2 GitOps（ArgoCD）

```bash
helm install argocd argo/argo-cd --namespace argocd --create-namespace
```

核心思想：Git 仓库是唯一真实来源。对 Skill Platform 的价值：所有部署变更可审计、可回滚、可 review。

## 5.3 Service Mesh（Istio 基础）

解决服务间通信的可观测性、流量管理、mTLS——不侵入业务代码。重点理解：Sidecar 注入、VirtualService/DestinationRule、金丝雀发布。只在微服务 > 10 且有明确流量管理需求时引入。

## 5.4 安全加固

```yaml
metadata:
  labels:
    pod-security.kubernetes.io/enforce: restricted
---
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities: { drop: ["ALL"] }
```

## 5.5 认证（可选）

```
CKA (Certified Kubernetes Administrator)
 → 验证运维能力，覆盖阶段 1-4
 → 2 小时纯实操，在终端解决问题（很适合你）
CKAD → 偏应用开发者，与 CKA 60% 重叠
CKS → 安全方向，需先持有 CKA
```

Killer Shell (killer.sh) 是最接近真实考试的模拟环境。

---

<a name="附录a"></a>
# 附录 A：官方文档完整阅读清单

> 基于 https://kubernetes.io/docs/ (v1.36)
> ★必读 / ☆推荐 / △进阶

正文各阶段已嵌入对应文档。以下是未在正文出现但值得补充的页面，以及完整索引。

## 网络（第二/三阶段补充）

| 优先级 | 页面 | URL |
|--------|------|-----|
| ★ | Service | /docs/concepts/services-networking/service/ |
| ★ | DNS for Services and Pods | /docs/concepts/services-networking/dns-pod-service/ |
| ★ | Ingress | /docs/concepts/services-networking/ingress/ |
| ★ | Ingress Controllers | /docs/concepts/services-networking/ingress-controllers/ |
| ★ | Network Policies | /docs/concepts/services-networking/network-policies/ |
| ★ | Cluster Networking | /docs/concepts/cluster-administration/networking/ |
| ☆ | EndpointSlices | /docs/concepts/services-networking/endpoint-slices/ |
| △ | Gateway API | /docs/concepts/services-networking/gateway/ |

## 容器

| 优先级 | 页面 | URL |
|--------|------|-----|
| ★ | Images | /docs/concepts/containers/images/ |
| ☆ | Container Lifecycle Hooks | /docs/concepts/containers/container-lifecycle-hooks/ |

## kubectl 参考

| 优先级 | 页面 | URL | 备注 |
|--------|------|-----|------|
| ★ | kubectl Cheat Sheet | /docs/reference/kubectl/cheatsheet/ | 打印贴墙上 |
| ☆ | JSONPath Support | /docs/reference/kubectl/jsonpath/ | `-o jsonpath` 语法 |

## Tutorials（第一阶段边读边做）

| 优先级 | 页面 | URL |
|--------|------|-----|
| ★ | Learn Kubernetes Basics（6 模块） | /docs/tutorials/kubernetes-basics/ |
| ☆ | WordPress + MySQL with PV | /docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/ |
| ☆ | ZooKeeper（分布式协调） | /docs/tutorials/stateful-application/zookeeper/ |

## 中文版策略

官方有中文版（/zh-cn/docs/），但翻译滞后于英文。建议：概念理解可先看中文快速建框架；具体配置和排查直接看英文；kubectl 输出和报错都是英文，长远习惯英文文档更高效。

---

<a name="附录b"></a>
# 附录 B：源码阅读路线全图

## 阅读原则

1. 每个组件从 `cmd/<component>/main.go` 开始，追 `main()` → `NewCommand()` → `Run()`
2. K8s 大量用 Cobra 框架做 CLI
3. 核心模式 Informer + WorkQueue + Reconcile 在所有控制器里都一样
4. 在 VS Code + Go 插件里跳转定义（F12）读，不要在 GitHub 网页读

## 文档与源码交叉推进对照表

| 文档阅读进度 | 对应源码 |
|-------------|---------|
| 阶段一：Overview/Components | 编译源码，`hack/local-up-cluster.sh` 启动，观察组件启动 |
| 阶段一：Controllers 概念 | `pkg/controller/deployment/deployment_controller.go` 的 Run()/syncDeployment() |
| 阶段一：Objects/Labels | `staging/src/k8s.io/api/core/v1/types.go` 的 ObjectMeta |
| 阶段一：kubectl 使用 | `cmd/kubectl/` → kubectl get 执行路径 |
| 阶段一：API 概念 | `cmd/kube-apiserver/` → 创建 Pod 请求路径 |
| 阶段二：Pods/Lifecycle | `pkg/kubelet/pod_workers.go` 的 syncPod() |
| 阶段二：Probes | `pkg/kubelet/prober/` |
| 阶段二：Deployments | Deployment 控制器完整 syncDeployment() |
| 阶段二：Service/DNS | `pkg/proxy/iptables/proxier.go` |
| 阶段三：Scheduler | `pkg/scheduler/scheduler.go` 的 scheduleOne() |
| 阶段三：RBAC | `staging/src/k8s.io/apiserver/plugin/pkg/authorizer/rbac/` |
| 阶段三：client-go | `staging/src/k8s.io/client-go/tools/cache/` |
| 阶段四：调试 | delve 断点 `pkg/controller/` |

## kube-apiserver 请求链路（重点追踪）

```
HTTP Request
  → Authentication（认证）
  → Authorization（鉴权，含 RBAC）
  → Admission（准入控制）
  → etcd CRUD
  → Response
```

不需要读完所有代码，追踪一个 `POST /api/v1/namespaces/default/pods` 的完整路径即可。

---

<a name="附录c"></a>
# 附录 C：学习资源汇总

## 文档与书籍

| 优先级 | 资源 | URL | 说明 |
|--------|------|-----|------|
| ★ | 官方文档 | https://kubernetes.io/docs/ | 最权威，Concepts + Tasks 反复读 |
| ★ | 《Kubernetes in Action》第二版 | Marko Lukša | 机制讲得深，适合追根溯源风格 |
| ☆ | 《Kubernetes Patterns》 | Bilgin Ibryam | 设计模式视角 |
| ★ | kubectl Cheat Sheet | /docs/reference/kubectl/cheatsheet/ | 打印贴墙上 |

## 源码相关

| 资源 | URL | 说明 |
|------|-----|------|
| K8s 主仓库 | https://github.com/kubernetes/kubernetes | |
| K8s Developer Guide | https://github.com/kubernetes/community/tree/master/contributors/devel | 官方开发者文档 |
| Tour of K8s Source Code (IBM) | https://developer.ibm.com/articles/a-tour-of-the-kubernetes-source-code/ | kubectl → API Server 代码追踪 |
| Build K8s-lite from scratch (Go) | https://medium.com/@owumifestus/building-kubernetes-a-lite-version-from-scratch-in-go-7156ed1fef9e | 用 Go 从零实现简化版控制面 |
| hackingnote: K8s Source Code | https://www.hackingnote.com/en/kubernetes/source-code/ | staging 同步机制讲解 |
| K8s build README | https://github.com/kubernetes/kubernetes/blob/master/build/README.md | 官方构建说明 |

## Go 语言

| 资源 | URL |
|------|-----|
| Go by Example | https://gobyexample.com/ |
| Effective Go | https://go.dev/doc/effective_go |

## 实战环境

| 资源 | URL | 说明 |
|------|-----|------|
| Killer Shell | killer.sh | CKA 考试模拟，即使不考证也值得练 |
| learnk8s networking | https://learnk8s.io/kubernetes-network-packets | 图解网络链路 |

---

<a name="附录d"></a>
# 附录 D：核心学习方法论

1. **白盒优先**：尽量用 `hack/local-up-cluster.sh` 而非 kind，让每个组件可见、可改、可调试。需要多节点时才切 kind。

2. **每个资源做"破坏实验"**：故意搞坏（删 Pod、改错 image、打满资源、断网、改 selector），观察控制器怎么反应。这比看十遍文档有效。

3. **`kubectl get <resource> -o yaml` 是最好的老师**：对比你写的 YAML 和 K8s 补全后的完整 spec，理解 defaulting、status 字段、managedFields。

4. **文档建模型，源码验理解**：读完一个概念，立刻去源码里找对应实现，确认你的心智模型和代码一致。两者矛盾时，源码为准。

5. **先手写，后工具**：前两阶段禁止用 Helm/Kustomize/生成器。手写 YAML 建立肌肉记忆后再引入抽象层。

6. **每周做一次"从零部署"**：删掉整个集群，从编译/启动开始重建所有组件。第三次之后速度快得飞起，说明知识已内化。

7. **读透一个控制器，胜过浏览十个**：所有控制器都是 Informer + WorkQueue + Reconcile 骨架。把 Deployment 控制器的 syncDeployment() 啃透，剩下的都是同构。