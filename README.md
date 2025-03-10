# kubelet-stats-exporter
This is a Prometheus exporter to expose a Pods ephemeral storage usage stats from the Kubelets

The Kubernetes Kubelet has some metrics on ephemeral storage usage that are not currently exposed elsewhere. It may be useful to present these in a format that can be collected by Prometheus. Note the kubelet of Docker Desktop does not expose these metrics, so it is not a useful environment for testing.

It accesses the Kubelet on each node, via the Kubernetes API proxy. Authentication is done to the kubelet using a service account that is configured in `k8s-resources/ns-rbac.yaml`.

## Background reading:

Although these metrics are exposed by the kubelet API, they are not exposed on the kubelets `/metrics` endpoint, nor are they currently collected or exported with kube-state-metrics. Some issues with similar requests can be seen here:

https://github.com/kubernetes/kube-state-metrics/issues/1046 (https://github.com/kubernetes/kube-state-metrics/issues/1046#issuecomment-640161305)

https://github.com/kubernetes/kubernetes/issues/69507

## Requirements
The following `pip` libraries are required:
- flask
- kubernetes
- prometheus_client
- python-json-logger
- requests
## Configuration

The following environment variables are useful to configure the application:

|Name|Type|Default|Description|
|--|--|--|--|
|EXPORTER_PORT|int|9118|Port exposing prometheus metrics|
|JSON_LOGGER|bool|true|Application logs on JSON Format for easier centralization using log shippers such as FluentBit|
|LOG_LEVEL|str|INFO|Logging Level. Werkzeug requests only logged on DEBUG level for log centralization costs saving purposes|
|KUBERNETES_API_TIMEOUT|int|5|Kubernetes API Scrape timeout. **Make sure `KUBERNETES_API_TIMEOUT` is smaller than Prometheus Scrape timeout**.|

## Exporter Endpoints

- `/health` - Application Status for Kubernetes readiness & liveness probes check.
- `/metrics` - Prometheus metrics endpoint.

## Docker Release 

Build the Docker image: `docker build -t $repository/kubelet-stats-exporter .`

Push Docker image to registry: `docker push $repository/kubelet-stats-exporter`

## Deployment
### Kubernetes Manifests

Apply Kubernetes resources: `kubectl apply -f ./k8s-resources `

If you're using the PrometheusOperator, and want to configure a ServiceMonitor, apply the `extra/servicemonitor.yaml` file.

Example dashboards for Grafana can be seen in the `extra` folder.

### Helm Chart

You could use [kubelet-stats-exporter chart](https://github.com/sequra/helm-charts/tree/master/charts/prometheus-kubelet-stats-exporter) to deploy `kubelet-stats-exporter` using helm.

```
helm repo add sequra-community https://sequra.github.io/helm-charts
helm repo update
helm install [RELEASE_NAME] sequra-community/prometheus-kubelet-stats-exporter
```
