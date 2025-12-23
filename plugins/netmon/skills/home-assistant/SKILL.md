---
name: home-assistant
description: Generate Home Assistant automations, webhook handlers, and template sensors. Use when integrating Alertmanager with Home Assistant, creating notifications, or TTS announcements.
allowed-tools: Read, Write, Edit
---

# Home Assistant Integration Patterns

## Generate Webhook ID

```python
import secrets
print(secrets.token_urlsafe(32))
```

Or via bash:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Webhook Automation for Alertmanager

Complete automation to handle Alertmanager webhooks:

```yaml
- id: network_alert_handler
  alias: "Network Monitoring Alert Handler"
  trigger:
    - platform: webhook
      webhook_id: "YOUR_WEBHOOK_ID"
      allowed_methods:
        - POST
      local_only: false
  action:
    - variables:
        alert_status: "{{ trigger.json.status }}"
        alert_name: "{{ trigger.json.alerts[0].labels.alertname }}"
        severity: "{{ trigger.json.alerts[0].labels.severity }}"
        summary: "{{ trigger.json.alerts[0].annotations.summary }}"
        description: "{{ trigger.json.alerts[0].annotations.description }}"
    - choose:
        # Critical alerts: notification + TTS
        - conditions:
            - condition: template
              value_template: "{{ severity == 'critical' and alert_status == 'firing' }}"
          sequence:
            - service: notify.mobile_app_YOUR_PHONE
              data:
                title: "Network Alert"
                message: "{{ summary }}"
                data:
                  priority: high
                  channel: network_critical
                  importance: high
                  ttl: 0
            - service: tts.speak
              target:
                entity_id: tts.piper
              data:
                cache: false
                media_player_entity_id: media_player.YOUR_SPEAKER
                message: "Network alert: {{ summary }}"

        # Warning alerts: notification only
        - conditions:
            - condition: template
              value_template: "{{ severity == 'warning' and alert_status == 'firing' }}"
          sequence:
            - service: notify.mobile_app_YOUR_PHONE
              data:
                title: "Network Warning"
                message: "{{ summary }}"
                data:
                  priority: normal
                  channel: network_warning

        # Resolved alerts
        - conditions:
            - condition: template
              value_template: "{{ alert_status == 'resolved' }}"
          sequence:
            - service: notify.mobile_app_YOUR_PHONE
              data:
                title: "Resolved"
                message: "{{ alert_name }} is now resolved"
```

## Alertmanager Configuration

Add to `alertmanager/alertmanager.yml`:

```yaml
receivers:
  - name: 'critical'
    webhook_configs:
      - url: 'http://YOUR_HA_IP:8123/api/webhook/YOUR_WEBHOOK_ID'
        send_resolved: true

  - name: 'warning'
    webhook_configs:
      - url: 'http://YOUR_HA_IP:8123/api/webhook/YOUR_WEBHOOK_ID'
        send_resolved: true
```

## Notification Patterns

### Mobile Push (Android/iOS)
```yaml
- service: notify.mobile_app_PHONE
  data:
    title: "Title"
    message: "Message body"
    data:
      priority: high  # high, normal, low
      channel: channel_name
      importance: high  # Android only
      ttl: 0  # Time to live
```

### TTS Announcement (Standard speakers)
```yaml
- action: tts.speak
  target:
    entity_id: tts.piper  # or tts.google_translate, tts.home_assistant_cloud
  data:
    media_player_entity_id: media_player.SPEAKER
    message: "Announcement text"
    cache: false
```

### Assist Satellite Announcement (HA Voice devices)
```yaml
- action: assist_satellite.announce
  target:
    entity_id: assist_satellite.YOUR_DEVICE
  data:
    message: "Announcement text"
```

Note: Home Assistant Voice devices are "Assist Satellites" and use `assist_satellite.announce` instead of `tts.speak`. Find your entity at Developer Tools > States, filter by `assist_satellite`.

### Persistent Notification (HA UI)
```yaml
- service: persistent_notification.create
  data:
    title: "Network Alert"
    message: "{{ summary }}"
    notification_id: "network_alert_{{ alert_name }}"
```

## Template Sensors

### Network Health Sensor
```yaml
template:
  - sensor:
      - name: "Network Health"
        unique_id: network_health
        state: >
          {% if is_state('binary_sensor.internet_up', 'off') %}
            Internet Down
          {% elif is_state('binary_sensor.router_up', 'off') %}
            Router Down
          {% else %}
            Healthy
          {% endif %}
        icon: >
          {% if this.state == 'Healthy' %}
            mdi:check-network
          {% else %}
            mdi:alert-network
          {% endif %}
```

### Pull Metrics from Prometheus

```yaml
sensor:
  - platform: rest
    name: "Internet Latency"
    resource: "http://YOUR_SERVER:29090/api/v1/query?query=avg(probe_duration_seconds{job='blackbox_icmp_external'})*1000"
    value_template: "{{ value_json.data.result[0].value[1] | round(1) }}"
    unit_of_measurement: "ms"
    scan_interval: 60

  - platform: rest
    name: "Download Speed"
    resource: "http://YOUR_SERVER:29090/api/v1/query?query=speedtest_download_bits_per_second/1000000"
    value_template: "{{ value_json.data.result[0].value[1] | round(0) }}"
    unit_of_measurement: "Mbps"
    scan_interval: 1800
```

## Test Webhook

Send a test alert via curl:

```bash
curl -X POST http://YOUR_HA_IP:8123/api/webhook/YOUR_WEBHOOK_ID \
  -H "Content-Type: application/json" \
  -d '{
    "status": "firing",
    "alerts": [{
      "labels": {"alertname": "TestAlert", "severity": "warning"},
      "annotations": {"summary": "Test notification", "description": "Testing integration"}
    }]
  }'
```

## Troubleshooting

Check HA logs for webhook events:
```bash
# In HA, go to Settings > System > Logs
# Filter by "webhook"
```

Check automation trace:
- Settings > Automations > Click automation > Traces

Test webhook directly:
```bash
curl -X POST http://HA_IP:8123/api/webhook/WEBHOOK_ID \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```
