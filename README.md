
<img src="https://www.seven.io/wp-content/uploads/Logo-with-darkmode.svg" width=250>

# seven.io for Home Assistant

Automate SMS notifications and voice calls through your smart home. Get instant alerts for security events, temperature changes, or any Home Assistant trigger.

**💳 Pricing:** seven.io uses prepaid credits. SMS from €0.075, voice calls from €0.015 per minute. [View full pricing](https://www.seven.io/en/prices/)

## Prerequisites

- Home Assistant 2023.1.0 or newer
- A seven.io account with API key ([sign up free](https://app.seven.io/signup))
- Credits in your seven.io account for sending messages

## Installation

### Manually

Clone the repository to the custom_components directory:
```bash
cd ~/.homeassistant/custom_components/
git clone https://github.com/seven-io/home-assistant seven
```

After installation, restart Home Assistant.

### Via [HACS](https://hacs.xyz/)
- Navigate to HACS -> Integrations -> Custom repositories -> Add
- Set *Repository* to **https://github.com/seven-io/home-assistant**
- Set *Type* to **Integration**
- Confirm form submission and the repository should be appended to the list
- Install the integration through HACS
- Restart Home Assistant

## Configuration

### Basic Setup

For security, use `secrets.yaml` to store your API key:

**secrets.yaml:**
```yaml
seven_api_key: YOUR_ACTUAL_API_KEY_HERE
```

**configuration.yaml:**

```yaml
notify:
  - platform: seven
    sender: HomeAssist # defaults to hass - see https://help.seven.io/en/set-sender-id
    name: seven_sms
    api_key: !secret seven_api_key # see https://help.seven.io/en/api-key-access
    recipient: +491234567890 # or specify multiple numbers e.g. [+491234567890, +449876543210]
  - platform: seven
    sender: +491234567890 # - see https://help.seven.io/en/shared-numbers
    name: seven_voice
    api_key: !secret seven_api_key # see https://help.seven.io/en/api-key-access
    recipient: [+491234567890, +449876543210]
    type: 'voice'
```

See the [visual guide](./screenshots/automation_action_call_service.png) for GUI configuration.

### Minimal Configuration

You can also make a minimal configuration to `configuration.yaml` where all the remaining necessary configuration will be made in the automation:
```yaml
notify:
  - platform: seven
    name: seven_sms
    api_key: !secret seven_api_key
```

### Configuration Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `platform` | string | Yes | - | Must be `seven` |
| `name` | string | Yes | - | Service name (e.g., `seven_sms`) |
| `api_key` | string | Yes | - | Your seven.io API key |
| `sender` | string | No | `hass` | Sender ID (11 chars alphanumeric or valid phone number) |
| `recipient` | string/list | No | - | Default recipient(s) |
| `type` | string | No | `sms` | Message type: `sms` or `voice` |

## Automation Examples

### Sending Sensor Data

```yaml
service: notify.seven_sms
data:
  data:
    sender: HomeAssist
  message: '{{ states("sensor.temperature") }}°C'
  target: +491234567890
```

### Testing Your Setup

1. Go to **Developer Tools** → **Services**
2. Select `notify.seven_sms` (or your configured service name)
3. Enter a test message and click **Call Service**

For detailed testing steps, see [Home Assistant's notify testing guide](https://www.home-assistant.io/integrations/notify#test-if-it-works).

### Security Alert - Door Sensor
```yaml
alias: Door Open Alert
trigger:
  - platform: state
    entity_id: binary_sensor.front_door
    to: 'on'
action:
  - service: notify.seven_sms
    data:
      message: "Front door opened at {{ now().strftime('%H:%M') }}"
      target: +491234567890
```

### Environmental Monitoring - Temperature
```yaml
alias: High Temperature Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.living_room_temperature
    above: 30
action:
  - service: notify.seven_sms
    data:
      message: "Warning: Temperature is {{ states('sensor.living_room_temperature') }}°C"
```

**💡 Tip:** For frequent alerts, change the [automation mode](https://www.home-assistant.io/docs/automation/modes/) from `single` to `parallel` to handle multiple triggers simultaneously.

## SMS Character Limits

- **Standard SMS:** 160 characters for Latin alphabet
- **Unicode SMS:** 70 characters when using special characters or emojis
- **Long messages:** Automatically split into multiple SMS (concatenated)
- Messages longer than 160 characters will be billed as multiple SMS

Use the [SMS Character Counter](https://docs.seven.io/en/tools/sms-character-counter) to calculate message length and parts before sending.

## Debugging

To troubleshoot issues, check the Home Assistant logs:

1. Enable debug logging in `configuration.yaml`:
2. 
```yaml
logger:
  default: info
  logs:
    custom_components.seven: debug
```

2. Restart Home Assistant and check logs at **Settings → System → Logs**

3. Common issues:
   - **Authentication failed:** Check your API key
   - **Message not sent:** Verify you have credits in your seven.io account
   - **Invalid recipient:** Ensure phone numbers include country code (e.g., +49 for Germany)

## Uninstallation

### Via HACS
1. Navigate to HACS → Integrations
2. Find the seven integration
3. Click the three dots menu → Uninstall
4. Restart Home Assistant

### Manual
1. Remove the integration from `configuration.yaml`
2. Delete the folder `~/.homeassistant/custom_components/seven`
3. Restart Home Assistant  

## Security

- ✅ All API communications use HTTPS encryption
- ✅ API keys are never logged or exposed in the UI
- ✅ Store credentials in `secrets.yaml` (never in `configuration.yaml` directly) 

## Getting Help

- 📚 **Documentation:** [seven.io Docs](https://docs.seven.io)
- 💬 **Support:** [Contact seven.io](https://www.seven.io/en/company/contact/)
- 🐛 **Issues:** [GitHub Issues](https://github.com/seven-io/home-assistant/issues)
- 📧 **Email:** support@seven.io

[![MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)
