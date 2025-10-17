# Audio State Monitor - Home Assistant Addon

Monitors PulseAudio state on a specific audio device and exposes state changes to Home Assistant via events.

## About

This addon monitors the state of a PulseAudio audio device (like your Soundcraft Notepad-12FX USB audio interface) and fires Home Assistant events when the state changes between `playing` and `idle`. Use these events to automate actions like turning on/off powered speakers.

## Installation

### Prerequisites
- Home Assistant OS with Supervisor
- A USB audio device connected to your Home Assistant host

### Steps

1. **Add the custom addon repository:**
   - In Home Assistant, navigate to: **Settings → Add-ons → Add-on Store (bottom right)**
   - Click the **three-dot menu** (⋮) in the top right
   - Select **Repositories**
   - Add this repository URL (or your local path if developing locally)
   - Click **Add** then **Close**

2. **Install the addon:**
   - Refresh the Add-on Store page
   - Find **Audio State Monitor** in the list
   - Click on it and press **Install**

3. **Configure the addon:**
   - Go to the **Configuration** tab
   - Update the `audio_device` name if needed (default is set for Soundcraft Notepad-12FX)
   - Adjust `scan_interval` if desired (default: 3 seconds)
   - Optionally change the `event_name` (default: `audio_state_changed`)

4. **Start the addon:**
   - Go to the **Info** tab
   - Enable **Start on boot** (optional but recommended)
   - Click **Start**

5. **Check the logs:**
   - Go to the **Log** tab
   - Verify the addon started successfully and is monitoring your device

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `audio_device` | `alsa_output.usb-Soundcraft_Notepad-12FX-00.analog-surround-40` | The PulseAudio sink name to monitor |
| `scan_interval` | `3` | How often to check the audio state (1-30 seconds) |
| `event_name` | `audio_state_changed` | The Home Assistant event name to fire |

### Finding your audio device name

If you need to find your audio device name:

1. SSH into your Home Assistant OS
2. Access the host audio system: `docker exec -it hassio_audio /bin/bash`
3. List audio sinks: `pactl list sinks short`
4. Copy the sink name (second column) and use it in the addon configuration

## Usage

Once the addon is running, it will fire Home Assistant events whenever the audio state changes.

### Event Data

The event includes the following data:
- `state`: Either `playing` or `idle`
- `device`: The audio device name being monitored

### Example Automation

Create an automation to toggle your speakers based on audio playback:

```yaml
automation:
  - alias: "Toggle Speakers on Audio Playback"
    trigger:
      - platform: event
        event_type: audio_state_changed
    action:
      - choose:
          - conditions:
              - condition: template
                value_template: "{{ trigger.event.data.state == 'playing' }}"
            sequence:
              - service: switch.turn_on
                target:
                  entity_id: switch.speakersplug
          - conditions:
              - condition: template
                value_template: "{{ trigger.event.data.state == 'idle' }}"
            sequence:
              - delay:
                  seconds: 10
              - service: switch.turn_off
                target:
                  entity_id: switch.speakersplug
```

This automation will:
- Turn on the speakers immediately when audio starts playing
- Turn off the speakers 10 seconds after audio stops

## Troubleshooting

### Addon won't start
- Check the logs for error messages
- Verify your Home Assistant has audio enabled
- Ensure the addon has proper permissions (audio: true in config.yaml)

### Audio device not found
- Verify the device name in the configuration matches exactly
- Check if the USB device is properly connected
- Use `pactl list sinks short` to confirm the device name

### Events not firing
- Check the addon logs to see if state changes are detected
- Verify events in Home Assistant: Developer Tools → Events → Listen to events
- Type in your event name (`audio_state_changed`) and click "Start listening"
- Play/pause audio and watch for events

### State changes not detected
- Try adjusting the scan_interval to a lower value (1-2 seconds)
- Verify your audio is actually playing through the configured device
- Check PulseAudio logs for issues

## Technical Details

- **Base Image:** Home Assistant base image for your architecture
- **Dependencies:** Python 3, pulseaudio-utils, requests
- **Resource Usage:** < 1% CPU, < 10MB RAM
- **Poll Interval:** Configurable (default 3 seconds)

## Support

For issues or feature requests, please open an issue on the GitHub repository.
