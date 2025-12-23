---
name: docker-compose
description: Generate Docker Compose YAML for monitoring services. Use when creating docker-compose.yml, adding services like Prometheus, Grafana, Alertmanager, exporters, or Ntfy.
allowed-tools: Read, Write, Edit, Bash
---

# Docker Compose for Monitoring Stacks

## Service Patterns

### Exporter Service (node-exporter, blackbox, speedtest)
- Always use `restart: unless-stopped`
- Expose on 29xxx port range to avoid conflicts
- Mount only necessary paths as read-only

### Stateful Service (Prometheus, Grafana, Alertmanager)
- Use named volumes for data persistence
- Set appropriate retention/storage limits
- Configure via mounted config files

### Networking
- Use default bridge network (services communicate by container name)
- Only expose ports that need external access

## Validation
Always run `docker compose config` before `docker compose up -d` to catch YAML errors.

## Example Patterns

### Standard Exporter
```yaml
service-name:
  image: prom/exporter:latest
  container_name: service-name
  restart: unless-stopped
  ports:
    - "29XXX:9XXX"
  volumes:
    - ./config:/etc/config:ro
```

### Prometheus
```yaml
prometheus:
  image: prom/prometheus:latest
  container_name: prometheus
  restart: unless-stopped
  ports:
    - "29090:9090"
  volumes:
    - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    - ./prometheus/alerts:/etc/prometheus/alerts:ro
    - prometheus_data:/prometheus
  command:
    - '--config.file=/etc/prometheus/prometheus.yml'
    - '--storage.tsdb.path=/prometheus'
    - '--storage.tsdb.retention.time=90d'
    - '--web.enable-lifecycle'
```

### Grafana
```yaml
grafana:
  image: grafana/grafana:latest
  container_name: grafana
  restart: unless-stopped
  ports:
    - "29030:3000"
  volumes:
    - grafana_data:/var/lib/grafana
    - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=changeme
    - GF_USERS_ALLOW_SIGN_UP=false
```

### Alertmanager
```yaml
alertmanager:
  image: prom/alertmanager:latest
  container_name: alertmanager
  restart: unless-stopped
  ports:
    - "29093:9093"
  volumes:
    - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    - alertmanager_data:/alertmanager
```

### Blackbox Exporter
```yaml
blackbox:
  image: prom/blackbox-exporter:latest
  container_name: blackbox
  restart: unless-stopped
  ports:
    - "29115:9115"
  volumes:
    - ./blackbox/blackbox.yml:/etc/blackbox_exporter/config.yml
  cap_add:
    - NET_RAW  # Required for ICMP probes
```

### Node Exporter
```yaml
node-exporter:
  image: prom/node-exporter:latest
  container_name: node-exporter
  restart: unless-stopped
  ports:
    - "29100:9100"
  volumes:
    - /proc:/host/proc:ro
    - /sys:/host/sys:ro
    - /:/rootfs:ro
  command:
    - '--path.procfs=/host/proc'
    - '--path.sysfs=/host/sys'
    - '--path.rootfs=/rootfs'
    - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
```

### Ntfy (self-hosted notifications)
```yaml
ntfy:
  image: binwiederhier/ntfy:latest
  container_name: ntfy
  restart: unless-stopped
  ports:
    - "29080:80"
  volumes:
    - ntfy_data:/var/lib/ntfy
  command: serve
```

### Speedtest Exporter
```yaml
speedtest:
  image: miguelndecarvalho/speedtest-exporter:latest
  container_name: speedtest
  restart: unless-stopped
  ports:
    - "29798:9798"
```

## Port Mapping Reference

| Service | External Port | Internal Port |
|---------|---------------|---------------|
| Prometheus | 29090 | 9090 |
| Grafana | 29030 | 3000 |
| Alertmanager | 29093 | 9093 |
| Blackbox | 29115 | 9115 |
| Node Exporter | 29100 | 9100 |
| Ntfy | 29080 | 80 |
| Speedtest | 29798 | 9798 |

## Volume Declaration
```yaml
volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:
  ntfy_data:
```
