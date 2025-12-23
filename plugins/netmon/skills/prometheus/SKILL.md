---
name: prometheus
description: Generate Prometheus configuration including scrape configs, relabeling, and alert rules. Use when writing prometheus.yml, creating blackbox exporter jobs, or defining PromQL alert expressions.
allowed-tools: Read, Write, Edit
---

# Prometheus Configuration Patterns

## Basic prometheus.yml Structure

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - /etc/prometheus/alerts/*.yml

scrape_configs:
  # Jobs defined below
```

## Scrape Config Basics

```yaml
scrape_configs:
  - job_name: 'example'
    scrape_interval: 15s  # Override global if needed
    static_configs:
      - targets: ['host:port']
        labels:
          custom_label: value
```

## Blackbox Exporter Relabeling

For probe-based checks (ICMP, HTTP, DNS, TCP), use this pattern:

```yaml
- job_name: 'blackbox_icmp'
  metrics_path: /probe
  params:
    module: [icmp]
  static_configs:
    - targets:
        - 1.1.1.1
        - 8.8.8.8
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: blackbox:9115
```

### HTTP Probes
```yaml
- job_name: 'blackbox_http'
  metrics_path: /probe
  params:
    module: [http_2xx]
  static_configs:
    - targets:
        - https://www.google.com/generate_204
        - https://github.com
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: blackbox:9115
```

### DNS Probes
```yaml
- job_name: 'blackbox_dns'
  metrics_path: /probe
  params:
    module: [dns]
  static_configs:
    - targets:
        - 1.1.1.1:53
        - 8.8.8.8:53
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: blackbox:9115
```

## Alert Rule Patterns

### Basic Alert Structure
```yaml
groups:
  - name: group_name
    rules:
      - alert: AlertName
        expr: metric_expression > threshold
        for: 2m
        labels:
          severity: critical|warning|info
        annotations:
          summary: "Short description"
          description: "Detailed description with {{ $labels.instance }}"
```

### Probe Success/Failure
```yaml
- alert: TargetDown
  expr: probe_success{job="blackbox_icmp"} == 0
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "{{ $labels.instance }} is unreachable"
```

### Aggregated Check (all probes failing)
```yaml
- alert: InternetDown
  expr: sum(probe_success{job="blackbox_icmp_external"}) == 0
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Internet connectivity lost"
    description: "All external ICMP probes failing"
```

### Latency Threshold
```yaml
- alert: HighLatency
  expr: probe_duration_seconds{job="blackbox_icmp"} > 0.1
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High latency to {{ $labels.instance }}"
    description: "Latency is {{ $value | humanizeDuration }}"
```

### Packet Loss
```yaml
- alert: PacketLoss
  expr: (1 - avg_over_time(probe_success{job="blackbox_icmp"}[5m])) > 0.05
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Packet loss to {{ $labels.instance }}"
    description: "{{ $value | humanizePercentage }} packet loss"
```

### Speedtest Threshold
```yaml
- alert: SlowInternetSpeed
  expr: speedtest_download_bits_per_second / 1000000 < 100
  for: 1h
  labels:
    severity: info
  annotations:
    summary: "Internet speed below expected"
    description: "Download speed is {{ $value | printf \"%.0f\" }} Mbps"
```

## Blackbox Modules (blackbox.yml)

```yaml
modules:
  icmp:
    prober: icmp
    timeout: 5s
    icmp:
      preferred_ip_protocol: ip4

  http_2xx:
    prober: http
    timeout: 10s
    http:
      valid_http_versions: ["HTTP/1.1", "HTTP/2.0"]
      valid_status_codes: []  # Defaults to 2xx
      method: GET
      follow_redirects: true
      preferred_ip_protocol: ip4

  dns:
    prober: dns
    timeout: 5s
    dns:
      query_name: google.com
      query_type: A
      preferred_ip_protocol: ip4

  tcp_connect:
    prober: tcp
    timeout: 5s
```

## Useful PromQL Queries

```promql
# Internet status (1 = up, 0 = down)
min(probe_success{job="blackbox_icmp_external"})

# Average latency
avg(probe_duration_seconds{job="blackbox_icmp"}) * 1000  # in ms

# Packet loss percentage
(1 - avg_over_time(probe_success[1h])) * 100

# Uptime percentage over 24h
avg_over_time(probe_success[24h]) * 100

# Speedtest in Mbps
speedtest_download_bits_per_second / 1000000
speedtest_upload_bits_per_second / 1000000
```

## Reload Configuration

```bash
# Hot reload via API (if --web.enable-lifecycle is set)
docker compose exec prometheus kill -HUP 1

# Or restart container
docker compose restart prometheus
```
