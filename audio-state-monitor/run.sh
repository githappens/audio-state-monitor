#!/bin/sh
set -e

CONFIG_PATH=/data/options.json

echo "[INFO] Starting Audio State Monitor..."

# Read configuration from options.json
AUDIO_DEVICE=$(jq -r '.audio_device' $CONFIG_PATH)
SCAN_INTERVAL=$(jq -r '.scan_interval' $CONFIG_PATH)
EVENT_NAME=$(jq -r '.event_name' $CONFIG_PATH)

echo "[INFO] Monitoring device: ${AUDIO_DEVICE}"
echo "[INFO] Scan interval: ${SCAN_INTERVAL} seconds"

# Set environment variables for the Python script
export AUDIO_DEVICE
export SCAN_INTERVAL
export EVENT_NAME
export SUPERVISOR_TOKEN

# Run the monitor
exec python3 /monitor.py
