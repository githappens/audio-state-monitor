#!/usr/bin/env bashio

# Read configuration
AUDIO_DEVICE=$(bashio::config 'audio_device')
SCAN_INTERVAL=$(bashio::config 'scan_interval')
EVENT_NAME=$(bashio::config 'event_name')

bashio::log.info "Starting Audio State Monitor..."
bashio::log.info "Monitoring device: ${AUDIO_DEVICE}"
bashio::log.info "Scan interval: ${SCAN_INTERVAL} seconds"

# Set environment variables for the Python script
export AUDIO_DEVICE
export SCAN_INTERVAL
export EVENT_NAME
export SUPERVISOR_TOKEN

# Run the monitor
exec python3 /monitor.py
