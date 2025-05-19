#!/bin/bash

# Recibe una IP o hostname y devuelve 0 si responde al ping
check_connectivity() {
    local ip="$1"
    ping -c 1 -W 1 "$ip" &>/dev/null
    return $?
}
