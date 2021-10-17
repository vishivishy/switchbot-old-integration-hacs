"""Support for Switchbot Press Switch."""
from __future__ import annotations
from typing import Any
import switchbot
import voluptuous as vol
from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.const import CONF_MAC, CONF_NAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.restore_state import RestoreEntity

DEFAULT_NAME = "Switchbot_Old_Hacs"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_MAC): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    mac_addr = config[CONF_MAC]
    password = config.get(CONF_PASSWORD)
    add_entities([SwitchBot(mac_addr, name, password)])


class SwitchBot(SwitchEntity, RestoreEntity):

    def __init__(self, mac, name, password) -> None:
        self._state = None
        self._last_run_success = None
        self._name = name
        self._mac = mac
        self._device = switchbot.Switchbot(mac=mac, password=password)

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if not state:
            return
        self._state = state.state == "on"

    def turn_on(self, **kwargs) -> None:
        if self._device.turn_on():
            self._state = True
            self._last_run_success = True
        else:
            self._last_run_success = False

    def turn_off(self, **kwargs) -> None:
        if self._device.turn_off():
            self._state = False
            self._last_run_success = True
        else:
            self._last_run_success = False

    @property
    def assumed_state(self) -> bool:
        return True

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def unique_id(self) -> str:
        return self._mac.replace(":", "")

    @property
    def name(self) -> str:
        return self._name

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"last_run_success": self._last_run_success}