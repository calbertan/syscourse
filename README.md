# Overview
Syscourse is a content-sharing platform that allows its user to upload educational resources and make them accessible to others. Users can:

- Upload educational resources

- Access shared content from other users

The system is built in Google Cloud using a microservices architecture deployed on Kubernetes, with serverless components and API Gateway integration to ensure performance and reliability.

## Goal
### High Performance: 
Latency should be kept below 300ms for 95% of requests over a 28-day period.
- Optimize code and use caching mechanisms to reduce latency.
- Use of containers to create a lightweight, isolated environment
- Use of small, independent serverless functions that execute in response to requests / events

### Highly Scalable
Microservices should be designed as serverless functions with loose coupling, capable of automatically scaling based on demand.
- Use of Kubernetes to provide auto-scaling
- Achieve loose coupling through the use of cloud functions
- Use Api Gateways

### Highly Available
Kubernetes nodes should have a 99% uptime over a 29-day period, achieved through proper autoscaling, automated container restarts, and workload balancing.
- Use of pub/sub to enable asynchronous communication between services 
- Setup multi-region firestore
- Automated container restarts by deploying to container orchestration service like k8s

### Secure
Calls to microservices should pass through an API Gateway and have the right Ingress setup to protect against unauthorized access.z
- Configure API Gateway to take requests from and forwards the requests to proper cloud functions
- Require JWT token when creating requests
- Use Ingress for secure communication.


## Note
This repo is a public release of forked private repo, hence why there is no history
