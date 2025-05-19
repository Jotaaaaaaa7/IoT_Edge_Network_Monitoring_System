import os
import re
from collections import defaultdict
from datetime import datetime

LOG_PATH = "/var/log/iot_monitor.log"

def parse_log(max_rows=10):
    """
    Lee el log y devuelve las últimas entradas (por defecto 10).
    """
    if not os.path.exists(LOG_PATH):
        return []

    entries = []
    # Patrón que captura el formato real con emojis
    log_pattern = r"\[(.*?)\] (✅ OK|🟡 LATENCIA ALTA|🔴 OFFLINE): ([\d\.]+) ?(.*)"

    with open(LOG_PATH, "r") as f:
        for line in f:
            match = re.match(log_pattern, line)
            if match:
                timestamp, status, ip, extra = match.groups()
                entries.append({
                    "ip": ip,
                    "status": status,
                    "latency": extract_latency(extra),
                    "timestamp": timestamp
                })

    # Ordenar por timestamp (más reciente primero) y limitar a max_rows
    entries.sort(key=lambda x: x["timestamp"], reverse=True)
    return entries[:max_rows]


def extract_latency(extra):
    match = re.search(r"(\d+(\.\d+)?)ms", extra)
    return f"{match.group(1)} ms" if match else "-"
