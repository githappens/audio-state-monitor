#!/usr/bin/env python3
import os
import time
import subprocess
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment
AUDIO_DEVICE = os.environ.get('AUDIO_DEVICE')
SCAN_INTERVAL = int(os.environ.get('SCAN_INTERVAL', 3))
EVENT_NAME = os.environ.get('EVENT_NAME', 'audio_state_changed')
SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN', '')

# Try to read token from file if not in environment
if not SUPERVISOR_TOKEN and os.path.exists('/run/secrets/SUPERVISOR_TOKEN'):
    with open('/run/secrets/SUPERVISOR_TOKEN', 'r') as f:
        SUPERVISOR_TOKEN = f.read().strip()

# Supervisor service call API endpoint
SUPERVISOR_SERVICE_API = "http://supervisor/core/api/services/event/fire"

def get_audio_state():
    """
    Query PulseAudio for the state of the specified audio device.
    Returns: 'playing', 'idle', or None if error
    """
    try:
        # Run pactl command
        result = subprocess.run(
            ['pactl', 'list', 'sinks', 'short'],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Parse output
        for line in result.stdout.splitlines():
            if AUDIO_DEVICE in line:
                parts = line.split()
                if len(parts) >= 6:
                    state = parts[-1]  # Last column is state
                    if state == 'RUNNING':
                        return 'playing'
                    elif state == 'IDLE':
                        return 'idle'
                    else:
                        return 'idle'

        logger.warning(f"Audio device {AUDIO_DEVICE} not found")
        return None

    except subprocess.TimeoutExpired:
        logger.error("pactl command timed out")
        return None
    except Exception as e:
        logger.error(f"Error getting audio state: {e}")
        return None

def fire_event(state):
    """
    Fire a Home Assistant event via the Supervisor API using service call.
    """
    try:
        if not SUPERVISOR_TOKEN:
            logger.error("SUPERVISOR_TOKEN is missing!")
            return

        headers = {
            'Authorization': f'Bearer {SUPERVISOR_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Use service call to fire event
        data = {
            'event_type': EVENT_NAME,
            'event_data': {
                'state': state,
                'device': AUDIO_DEVICE
            }
        }

        logger.debug(f"Firing event via service call: {EVENT_NAME}")
        response = requests.post(
            SUPERVISOR_SERVICE_API,
            json=data,
            headers=headers,
            timeout=5
        )

        if response.status_code in [200, 201]:
            logger.info(f"Event fired successfully: {state}")
        else:
            logger.error(f"Failed to fire event: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"Error firing event: {e}")

def main():
    logger.info(f"Audio State Monitor started")
    logger.info(f"Monitoring: {AUDIO_DEVICE}")

    last_state = None

    while True:
        try:
            current_state = get_audio_state()

            # Fire event only on state change
            if current_state and current_state != last_state:
                logger.info(f"State changed: {last_state} -> {current_state}")
                fire_event(current_state)
                last_state = current_state

            time.sleep(SCAN_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Shutting down...")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
