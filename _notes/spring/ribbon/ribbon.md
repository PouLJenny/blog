# Ribbon


## 负载均衡算法

- RoundRobin轮训算法

```java
private int incrementAndGetModulo(int modulo) {
	for (;;) {
		int current = nextIndex.get();
		int next = (current + 1) % modulo;
		if (nextIndex.compareAndSet(current, next) && current < modulo)
			return current;
	}
}
```

## IPing机制

Spring Cloud整合的ribbo里默认的ping是 com.netflix.niws.loadbalancer.NIWSDiscoveryPing
```java
	public boolean isAlive(Server server) {
		boolean isAlive = true;
		if (server!=null && server instanceof DiscoveryEnabledServer){
			DiscoveryEnabledServer dServer = (DiscoveryEnabledServer)server;	            
			InstanceInfo instanceInfo = dServer.getInstanceInfo();
			if (instanceInfo!=null){	                
				InstanceStatus status = instanceInfo.getStatus();
				if (status!=null){
					isAlive = status.equals(InstanceStatus.UP);
				}
			}
		}
		return isAlive;
	}
```

## 阅读源码

```java
	@Override
	public ClientHttpResponse intercept(final HttpRequest request, final byte[] body,
			final ClientHttpRequestExecution execution) throws IOException {
		final URI originalUri = request.getURI();
		String serviceName = originalUri.getHost();
		Assert.state(serviceName != null, "Request URI does not contain a valid hostname: " + originalUri);
		return this.loadBalancer.execute(serviceName, requestFactory.createRequest(request, body, execution));
	}
```