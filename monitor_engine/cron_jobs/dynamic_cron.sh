#!/bin/bash

CONFIG_FILE="/shared-data/devices.json"
CRON_FILE="/etc/cron.d/monitor_cron"
LOG_FILE="/var/log/iot_monitor.log"

mkdir -p /var/log

# Validar existencia de config
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "[$(TZ='Europe/Madrid' date '+%Y-%m-%d %H:%M:%S')] ❌ No se encontró $CONFIG_FILE" >> "$LOG_FILE"
    exit 1
fi

# Calcular frecuencia mínima
min_freq=$(jq -r '.[].frequency_min' "$CONFIG_FILE" | sort -n | head -n 1)

if [[ -z "$min_freq" || "$min_freq" -lt 1 ]]; then
    echo "[$(TZ='Europe/Madrid' date '+%Y-%m-%d %H:%M:%S')] ❌ Frecuencia inválida: '$min_freq'" >> "$LOG_FILE"
    exit 1
fi

# Crear cron file con redirección de logs
echo "*/$min_freq * * * * root /usr/local/bin/monitor_worker.sh >> $LOG_FILE 2>&1" > "$CRON_FILE"

# Permisos correctos para cron.d
chmod 0644 "$CRON_FILE"

echo "[$(TZ='Europe/Madrid' date '+%Y-%m-%d %H:%M:%S')] ✅ Cron actualizado para ejecutarse cada $min_freq minuto(s)" >> "$LOG_FILE"
