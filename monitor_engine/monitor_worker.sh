#!/bin/bash
set -e # Sal del script si algún comando devuelve un error (código distinto de 0)

CONFIG_FILE="/shared-data/devices.json"

# ─── Importar funciones ─────────────────────────────────────────────
source /usr/local/bin/utils/check_connectivity.sh
source /usr/local/bin/utils/check_latency.sh
source /usr/local/bin/utils/log_status.sh

# ─── Validaciones ───────────────────────────────────────────────────
if [[ ! -f "$CONFIG_FILE" ]]; then
    log_status "❌ ERROR: No se encontró el archivo de configuración: $CONFIG_FILE"
    exit 1
fi

device_count=$(jq length "$CONFIG_FILE")
if [[ "$device_count" -eq 0 ]]; then
    log_status "ℹ️ AVISO: No hay dispositivos configurados."
    exit 0
fi

log_status "🚀 Iniciando chequeo para $device_count dispositivos..."

# ─── Proceso por dispositivo ────────────────────────────────────────
jq -c '.[]' "$CONFIG_FILE" | while read -r device; do
    host=$(echo "$device" | jq -r '.host')
    threshold=$(echo "$device" | jq -r '.latency_ms')

    if ! check_connectivity "$host"; then
        log_status "🔴 OFFLINE: $host no responde."
        continue
    fi

    latency=$(check_latency "$host")
    latency_int=${latency%.*}

    if [[ "$latency_int" -le "$threshold" ]]; then
        log_status "✅ OK: $host — ${latency}ms"
    else
        log_status "🟡 LATENCIA ALTA: $host — ${latency}ms (umbral: ${threshold}ms)"
    fi
done

log_status "✅ Monitorización finalizada."
echo "" >> /var/log/iot_monitor.log
