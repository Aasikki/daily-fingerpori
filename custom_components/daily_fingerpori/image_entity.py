from homeassistant.components.image import ImageEntity
from homeassistant.core import HomeAssistant

class FingerporiImage(ImageEntity):
    def __init__(self, hass: HomeAssistant, coordinator, path: str):
        self.hass = hass
        self.coordinator = coordinator
        self._path = path
        self.entity_id = "image.comic_fingerpori"

    def _read_file(self) -> bytes:
        with open(self._path, "rb") as f:
            return f.read()

    async def async_image(self) -> bytes | None:
        """Return image bytes. Read file on executor to avoid blocking the event loop."""
        try:
            return await self.hass.async_add_executor_job(self._read_file)
        except FileNotFoundError:
            return None
        except Exception:
            _LOGGER.exception("Failed to read fingerpori image file")
            return None