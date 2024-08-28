"""Platform for sensor integration."""
from __future__ import annotations

import re
import requests

import voluptuous as vol
import logging
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    PLATFORM_SCHEMA,
)
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_API_KEY
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import Throttle

from datetime import timedelta, datetime, date

import random

#from fiobank import FioBank

MIN_TIME_BETWEEN_SCANS = timedelta(hours=6)

_LOGGER = logging.getLogger(__name__)
#_RESOURCE = 'https://www.fio.cz/ib_api/rest/'
_RESOURCE = 'https://fioapi.fio.cz/v1/rest/'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
    }
)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    api_key = config[CONF_API_KEY]
    add_entities([FiobankaSensor(api_key)])


class FiobankaSensor(SensorEntity):
    """Representation of a Sensor."""
    
    _attr_name = "Stav účtu"
    _attr_unique_id = "fio_banka"
    _attr_native_unit_of_measurement = "Kč"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:currency-usd"
    
    def __init__(self, api_key):
        self.api_key = api_key

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self) -> None:
        today = datetime.now()
        url = _RESOURCE + "periods/" + self.api_key +"/" + today.strftime("%Y-%m-%d") + "/" + today.strftime("%Y-%m-%d") + "/transactions.json"
        response = requests.get(url)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code == 200:
            if response.json()['accountStatement']['info']['closingBalance'] > 0:
                self._attr_native_value = response.json()['accountStatement']['info']['closingBalance']
                #_LOGGER.error("fiobank_sensor success string: %s", response.json())
            else:
                _LOGGER.error("fiobank_sensor error in number: %s", response.json())
        else:
            _LOGGER.error("fiobank_sensor error in download the json with status code: %s", response.status_code)
        