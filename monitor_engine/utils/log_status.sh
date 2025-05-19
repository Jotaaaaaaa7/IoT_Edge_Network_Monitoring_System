#!/bin/bash

LOG_FILE="/var/log/iot_monitor.log"
mkdir -p "$(dirname "$LOG_FILE")"

log_status() {
    echo "[$(TZ='Europe/Madrid' date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}
