import logging
import uuid
from homeassistant.components.image import ImageEntity
from homeassistant.core import HomeAssistant
from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

class FingerporiImage(ImageEntity):
    def __init__(self, hass: HomeAssistant, coordinator, path: str, config_entry_id: str | None = None, name: str | None = None):
        self.hass = hass
        self.coordinator = coordinator
        self._path = path
        # do not set a fixed entity_id — let HA assign one based on name/unique_id

        # minimal access token support required by the image component
        # generate a stable token per entity instance (sufficient for local testing)
        self._access_token = uuid.uuid4().hex
        self._access_tokens = [self._access_token]

        # keep a stable unique id per config entry (or per filename when no entry)
        # This makes Home Assistant reuse the same registry entry and link it to the integration
        if config_entry_id:
            self._unique_id = f"{DOMAIN}_{config_entry_id}"
        else:
            # fallback unique id based on filename path
            self._unique_id = f"{DOMAIN}_{os.path.basename(self._path)}"

        self._name = name or DEFAULT_NAME

    @property
    def access_tokens(self) -> list[str]:
        """Return access tokens used by the image helper."""
        return self._access_tokens

    @property
    def unique_id(self) -> str:
        """Return unique id for the entity (used by the entity registry)."""
        return self._unique_id

    @property
    def name(self) -> str:
        """Return the entity name shown in the UI."""
        return self._name

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