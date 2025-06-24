from homeassistant.components.image import ImageEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DEFAULT_NAME

class FingerporiImage(CoordinatorEntity, ImageEntity):
    _attr_name = DEFAULT_NAME
    _attr_should_poll = False
    _attr_unique_id = "comic_fingerpori"

    def __init__(self, hass, coordinator, path):
        CoordinatorEntity.__init__(self, coordinator)
        ImageEntity.__init__(self, hass)
        self._path = path
        self.entity_id = "image.comic_fingerpori"

    @property
    def image_content(self):
        try:
            with open(self._path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_image(self):
        """Return bytes of image (async)."""
        return self.image_content