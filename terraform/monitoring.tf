# ─── Namespace para monitoring ────────────────────────────────────────────────
resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
  }

  depends_on = [aws_eks_node_group.main]
}

# ─── Prometheus + Grafana via kube-prometheus-stack ──────────────────────────
resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  namespace  = "monitoring"
  version    = "61.1.0"

  set {
    name  = "grafana.adminPassword"
    value = "admin123"
  }
  /*
  set {
    name  = "grafana.service.type"
    value = "LoadBalancer"
  }
*/
  set {
    name  = "prometheus.service.type"
    value = "ClusterIP"
  }

  set {
    name  = "alertmanager.enabled"
    value = "false"
  }

  set {
    name  = "grafana.service.type"
    value = "ClusterIP"
  }

  set {
    name  = "grafana.grafana\\.ini.server.root_url"
    value = "%(protocol)s://%(domain)s/grafana"
  }

  set {
    name  = "grafana.grafana\\.ini.server.serve_from_sub_path"
    value = "true"
  }
  depends_on = [
    kubernetes_namespace.monitoring,
    helm_release.lbc,
  ]
}
