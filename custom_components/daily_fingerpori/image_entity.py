import logging
import uuid
from homeassistant.components.image import ImageEntity
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class FingerporiImage(ImageEntity):
    def __init__(self, hass: HomeAssistant, coordinator, path: str):
        self.hass = hass
        self.coordinator = coordinator
        self._path = path
        self.entity_id = "image.comic_fingerpori"

        # minimal access token support required by the image component
        # generate a stable token per entity instance (sufficient for local testing)
        self._access_token = uuid.uuid4().hex
        self._access_tokens = [self._access_token]

    @property
    def access_tokens(self) -> list[str]:
        """Return access tokens used by the image helper."""
        return self._access_tokens

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