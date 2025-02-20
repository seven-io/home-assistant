
<img src="https://www.seven.io/wp-content/uploads/Logo-with-darkmode.svg" width=250>

# Home Assistant integration

This integration adds the possibility of sending SMS and making text-to-speech calls via [sms77](https://www.sms77.io).

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
configure a service call on automation when using the GUI.

Note that you can also make a minimal configuration to `configuration.yaml` where all the remaining necessary configuartion will be made in the automation like:
```yaml
notify:
  - platform: seven
    name: seven_sms
    api_key: INSERT_YOUR_SMS77_API_KEY_HERE # see https://help.sms77.io/en/api-key-access
```

Use the following yaml example, entered via the automation GUI, if you want to manually configure the automation like when sending sensor data. Just add into the message field `'{{ states("sensor.sensor_name") }}'` and manual configuration will be enabled:

```yaml
service: notify.seven_sms
data:
  data:
    sender: From_Name
  message: '{{ states("sensor.sensor_name") }}'
  target: Recipient_Phone_Number(s)
```

Follow the [Home Assistant - TEST IF IT WORKS](https://www.home-assistant.io/integrations/notify#test-if-it-works) documentation for testing your automation.

Consider changing the [automation mode](https://www.home-assistant.io/docs/automation/modes/) for the automation which defaults to `single` when created. If you expect a series of consecutive triggers for the same automation, only the current running will be processed when `single` is defined and a log warning is written . Setting this to `parallel` will process them all one by another.  

## API Communication Security

When there is communication via the API to the `seven.io` host, this communication is secured via `https`. 

## Support

Need help? Feel free to [contact us](https://www.sms77.io/en/company/contact/).

[![MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)
