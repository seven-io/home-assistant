![sms77.io Logo](https://www.sms77.io/wp-content/uploads/2019/07/sms77-Logo-400x79.png "sms77.io Logo")

# Official Home Assistant integration

This integration adds the possibility of sending SMS and making text-to-speech calls via [sms77](https://wwww.sms77.io).

## Installation

### Manually

Clone the repository to a folder called "custom_components" in your Home
Assistant root directory, e.g. `git clone https://github.com/seven-io/home-assistant ~/.homeassistant/custom_components/seven`

### Via [HACS](https://hacs.xyz/)
- Navigate to HACS -> Integrations -> Custom repositories -> Add
- Set *Repository* to **https://github.com/seven-io/home-assistant**
- Set *Type* to **Integration**
- Confirm form submission and the repository should be appended to the list

## Configuration

Add to `configuration.yaml` - usually in `~/.homeassistant/`:

```yaml
notify:
  - platform: seven
    sender: HomeAssist # defaults to hass - see https://help.sms77.io/en/set-sender-id
    name: seven_sms
    api_key: INSERT_YOUR_SMS77_API_KEY_HERE # see https://help.sms77.io/en/api-key-access
    recipient: 01716992343 # or specify multiple numbers e.g. [01771783130, 01716992343]
  - platform: seven
    sender: +491771783130 # - see https://help.sms77.io/en/shared-numbers
    name: seven_voice
    api_key: INSERT_YOUR_SMS77_API_KEY_HERE # see https://help.sms77.io/en/api-key-access
    recipient: [01771783130, 01716992343]
    type: 'voice'
```

Check out the [example](./screenshots/automation_action_call_service.png) on how to
configure a service call on automation.

## Support

Need help? Feel free to [contact us](https://www.sms77.io/en/company/contact/).

[![MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)