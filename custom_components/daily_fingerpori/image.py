import logging
import os
from datetime import timedelta
import aiohttp

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import dt as dt_util

from .const import FILENAME, URL, DEFAULT_NAME
from .image_entity import FingerporiImage
from . import get_refresh_interval

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
):
    image_path = hass.config.path(f"www/{FILENAME}")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    async def update_image():
        today = dt_util.utcnow()
        date_str = today.strftime("%d_%m_%y")
        url = URL.format(date=date_str)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        with open(image_path, "wb") as f:
                            f.write(data)
                        _LOGGER.debug("Downloaded Fingerpori comic for %s", date_str)
                        return data
        except Exception as e:
            _LOGGER.warning("Failed to download Fingerpori comic: %s", e)
        return None

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="fingerpori_image",
        update_method=update_image,
        update_interval=timedelta(hours=1),  # fallback for platform setup
    )

    await coordinator.async_refresh()
    async_add_entities([FingerporiImage(hass, coordinator, image_path)])

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    image_path = hass.config.path(f"www/{FILENAME}")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    async def update_image():
        today = dt_util.utcnow()
        date_str = today.strftime("%d_%m_%y")
        url = URL.format(date=date_str)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        with open(image_path, "wb") as f:
                            f.write(data)
                        _LOGGER.debug("Downloaded Fingerpori comic for %s", date_str)
                        return data
        except Exception as e:
            _LOGGER.warning("Failed to download Fingerpori comic: %s", e)
        return None

    interval = get_refresh_interval(entry)
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="fingerpori_image",
        update_method=update_image,
        update_interval=timedelta(hours=interval),
    )
    await coordinator.async_refresh()
    async_add_entities([FingerporiImage(hass, coordinator, image_path)])
