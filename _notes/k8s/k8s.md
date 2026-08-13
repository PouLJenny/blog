# kubernetes

[官网](https://kubernetes.io/)

[github](https://github.com/kubernetes/kubernetes)

## 名词

- Container
- Pod
- Node
- Cluster

## 集群架构

### Control plane components

- kube-apiserver
- etcd
- kube-scheduler
- kube-controller-manager
    - Node controller
    - Job controller
    - Endpoint controller
    - ServiceAccount controller
- cloud-controller-manager
    - Node controller
    - Route controller
    - Service controller


### Node components

- kubelet
- kube-proxy
- container runtime
    - containerd
    - CRI-O

### Addons

- DNS
- Web UI
- Container resource mointoring 
- Cluster-level Logging
- Network plugins

### Architecture variations

- Control plane deployment options
    - Traditional deployment
    - Static Pods
    - Self-hosted
    - Managed Kubernetes services
- Workload placement considerations
- Cluster management tools
- Customization and extensibility

# EOF