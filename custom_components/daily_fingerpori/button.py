"""Button platform for Daily Fingerpori integration."""
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button entity from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([FingerporiUpdateButton(coordinator, entry)])


class FingerporiUpdateButton(ButtonEntity):
    """Button entity to manually update the Fingerpori comic."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialize the button entity."""
        self._coordinator = coordinator
        self._entry = entry
        self._attr_name = f"{entry.title or DEFAULT_NAME} Update"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_update_button"
        self._attr_icon = "mdi:refresh"

    @property
    def device_info(self):
        """Return device information to group with the image entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title or DEFAULT_NAME,
            "manufacturer": "Fingerpori",
            "model": "Daily Comic",
        }

    async def async_press(self) -> None:
        """Handle the button press - trigger a manual update."""
        _LOGGER.debug("Manual update button pressed, triggering coordinator refresh")
        await self._coordinator.async_request_refresh()
