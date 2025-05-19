#!/bin/bash

echo "🔍 Estado del sistema de monitorización:"
echo "----------------------------------------"

echo "🧪 Cron activo:"
pgrep crond > /dev/null && echo "✅ crond está corriendo" || echo "❌ crond no está corriendo"

echo -e "\n📦 Dispositivos configurados:"
cat /shared-data/devices.json 2>/dev/null || echo "⚠️ No se encuentra el archivo devices.json"

echo -e "\n📜 Últimas 5 entradas del log:"
tail -n 5 /var/log/iot_monitor.log 2>/dev/null || echo "⚠️ Log no encontrado"
