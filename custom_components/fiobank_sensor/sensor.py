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

from fiobank import FioBank

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
        client = FioBank(token=self.api_key, decimal=True)
        info = client.info()
        self._attr_native_value = info["balance"]
        
