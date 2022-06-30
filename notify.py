"""seven SMS & text-to-speech calling for notify component."""
from http import HTTPStatus
import logging

import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_MESSAGE,
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import (
    CONF_API_KEY,
    CONF_RECIPIENT,
    CONF_SENDER,
    CONF_TYPE,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
BASE_API_URL = "https://gateway.sms77.io/api/"
TIMEOUT = 5
TYPE_SMS = "sms"
PLATFORM_SCHEMA = vol.Schema(vol.All(PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_RECIPIENT, default=[]): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_SENDER, default="hass"): cv.string,
})))


def get_service(hass, config, discovery_info=None):
    """Get the seven notification service."""
    if not _authenticate(config):
        _LOGGER.error("You are not authorized to access seven")
        return None
    return SevenNotificationService(config)


class SevenNotificationService(BaseNotificationService):
    """Implementation of a notification service for the seven service."""

    def __init__(self, config):
        """Initialize the service."""
        self.api_key = config[CONF_API_KEY]
        self.recipients = config[CONF_RECIPIENT]
        self.sender = config[CONF_SENDER]
        self.type = config.get(CONF_TYPE, TYPE_SMS)

    def send_message(self, message="", **kwargs):
        """Send a message to a user."""
        data = kwargs.get(ATTR_DATA) or {}
        type = data.get(CONF_TYPE, self.type)
        sender = data.get(CONF_SENDER, self.sender)
        is_sms = type is TYPE_SMS
        url = f"{BASE_API_URL}{type}"
        headers = _build_headers(self.api_key)
        recipients = kwargs.get(ATTR_TARGET, self.recipients)

        if is_sms:
            recipients = [','.join(recipients)]

        for recipient in recipients:
            res = requests.post(
                url,
                json={
                    "from": sender,
                    "json": True,
                    "text": message,
                    "to": recipient,
                },
                headers=headers,
                timeout=TIMEOUT,
            )

            success = res.json().get('success')

            if res.status_code is not HTTPStatus.OK or (success not in ['100', '101']):
                _LOGGER.error("Error %s : (Code %s)", res.status_code, success)


def _authenticate(config):
    """Authenticate with seven."""
    res = requests.get(
        f"{BASE_API_URL}balance",
        headers=_build_headers(config[CONF_API_KEY]),
        timeout=TIMEOUT,
    )

    return res.status_code == HTTPStatus.OK and "." in res.text


def _build_headers(api_key, sent_with="home-assistant"):
    return {
        "SentWith": sent_with,
        "X-Api-Key": api_key,
    }
