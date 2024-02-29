# Zuul

[github](https://github.com/Netflix/zuul/wiki '')

## Why Zuul?
The volume and diversity of Netflix API traffic sometimes results in production issues arising quickly and without warning. We need a system that allows us to rapidly change behavior in order to react to these situations.

Zuul uses a range of different types of filters that enables us to quickly and nimbly apply functionality to our edge service. These filters help us perform the following functions:

- Authentication and Security - identifying authentication requirements for each resource and rejecting requests that do not satisfy them.
- Insights and Monitoring - tracking meaningful data and statistics at the edge in order to give us an accurate view of production.
- Dynamic Routing - dynamically routing requests to different backend clusters as needed.
- Stress Testing - gradually increasing the traffic to a cluster in order to gauge performance.
- Load Shedding - allocating capacity for each type of request and dropping requests that go over the limit.
- Static Response handling - building some responses directly at the edge instead of forwarding them to an internal cluster
- Multiregion Resiliency - routing requests across AWS regions in order to diversify our ELB usage and move our edge closer to our members


## zuul 1

![](../../static/images/zuul/zuul1.png "")

## zuul 2


![](../../static/images/zuul/zuul2.png "")