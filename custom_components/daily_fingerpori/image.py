import logging
import os
from datetime import timedelta
import aiohttp
import xml.etree.ElementTree as ET
import re

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import dt as dt_util

from .const import FILENAME, FEED_URL, DEFAULT_NAME, CONF_REFRESH_INTERVAL
from .image_entity import FingerporiImage
from . import get_refresh_interval

_LOGGER = logging.getLogger(__name__)

# Helper to perform blocking file write on executor
def _write_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
):
    image_path = hass.config.path(f"www/{FILENAME}")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    async def update_image():
        try:
            async with aiohttp.ClientSession() as session:
                # Fetch RSS feed
                async with session.get(FEED_URL) as resp:
                    if resp.status != 200:
                        _LOGGER.warning("Failed to fetch feed: HTTP %s", resp.status)
                        return None
                    text = await resp.text()

                # Parse feed and find first item
                try:
                    root = ET.fromstring(text)
                except Exception as e:
                    _LOGGER.warning("Failed to parse RSS feed: %s", e)
                    return None

                items = root.findall(".//item")
                if not items:
                    _LOGGER.warning("No items found in RSS feed")
                    return None

                item = items[0]

                # Try enclosure tag first
                enclosure = item.find("enclosure")
                img_url = None
                if enclosure is not None and "url" in enclosure.attrib:
                    img_url = enclosure.attrib["url"]
                else:
                    # Fallback: search for an image URL in the item's serialized XML
                    item_xml = ET.tostring(item, encoding="unicode")
                    m = re.search(r'src=["\']([^"\']+\.(?:gif|png|jpe?g))["\']', item_xml, re.IGNORECASE)
                    if m:
                        img_url = m.group(1)

                if not img_url:
                    _LOGGER.warning("No image URL found in latest feed item")
                    return None

                # Download the image
                async with session.get(img_url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        # Write file on executor to avoid blocking the event loop
                        await hass.async_add_executor_job(_write_bytes, image_path, data)
                        _LOGGER.debug("Downloaded Fingerpori comic from feed: %s", img_url)
                        return data
                    else:
                        _LOGGER.warning("Failed to download image: HTTP %s", resp.status)
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
        try:
            async with aiohttp.ClientSession() as session:
                # Fetch RSS feed
                async with session.get(FEED_URL) as resp:
                    if resp.status != 200:
                        _LOGGER.warning("Failed to fetch feed: HTTP %s", resp.status)
                        return None
                    text = await resp.text()

                # Parse feed and find first item
                try:
                    root = ET.fromstring(text)
                except Exception as e:
                    _LOGGER.warning("Failed to parse RSS feed: %s", e)
                    return None

                items = root.findall(".//item")
                if not items:
                    _LOGGER.warning("No items found in RSS feed")
                    return None

                item = items[0]

                # Try enclosure tag first
                enclosure = item.find("enclosure")
                img_url = None
                if enclosure is not None and "url" in enclosure.attrib:
                    img_url = enclosure.attrib["url"]
                else:
                    # Fallback: search for an image URL in the item's serialized XML
                    item_xml = ET.tostring(item, encoding="unicode")
                    m = re.search(r'src=["\']([^"\']+\.(?:gif|png|jpe?g))["\']', item_xml, re.IGNORECASE)
                    if m:
                        img_url = m.group(1)

                if not img_url:
                    _LOGGER.warning("No image URL found in latest feed item")
                    return None

                # Download the image
                async with session.get(img_url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        # Write file on executor to avoid blocking the event loop
                        await hass.async_add_executor_job(_write_bytes, image_path, data)
                        _LOGGER.debug("Downloaded Fingerpori comic from feed: %s", img_url)
                        return data
                    else:
                        _LOGGER.warning("Failed to download image: HTTP %s", resp.status)
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
