#!/bin/bash

# Recibe una IP y devuelve la latencia en ms como número decimal
check_latency() {
    local ip="$1"
    ping -c 1 -W 1 "$ip" 2>/dev/null | grep 'time=' | sed -n 's/.*time=\([0-9.]*\) ms/\1/p'
}
