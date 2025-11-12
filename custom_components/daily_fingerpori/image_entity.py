import logging
import uuid
import os
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.image import ImageEntity
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from datetime import datetime
from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

class FingerporiImage(CoordinatorEntity, ImageEntity):
    def __init__(self, hass: HomeAssistant, coordinator, path: str, config_entry_id: str | None = None, name: str | None = None):
        # Initialize CoordinatorEntity so the entity receives coordinator updates
        super().__init__(coordinator)
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
        # Timestamp when the image was last refreshed (timezone-aware UTC datetime)
        self._last_refreshed: datetime | None = None

    async def async_added_to_hass(self) -> None:
        """Register a listener to rotate the access token when coordinator updates."""
        # coordinator.async_add_listener returns an unsubscribe callable
        self._remove_coordinator_listener = self.coordinator.async_add_listener(self._on_coordinator_update)

        # Initialize last_refreshed only if coordinator already has data (first successful refresh)
        # Coordinator.update_method returns the downloaded image bytes when a new image was fetched
        # and returns None when nothing changed; use this to avoid updating the timestamp on empty refreshes.
        if getattr(self.coordinator, "data", None) is not None:
            # Prefer coordinator-provided timestamps if available, otherwise use now
            coordinator_time = None
            for attr in ("last_update_time", "last_update_at", "last_update", "_last_update", "_last_update_time", "_last_update_at"):
                coordinator_time = getattr(self.coordinator, attr, None)
                if isinstance(coordinator_time, datetime):
                    break
            self._last_refreshed = coordinator_time or dt_util.utcnow()
        else:
            self._last_refreshed = None

    async def async_will_remove_from_hass(self) -> None:
        if hasattr(self, "_remove_coordinator_listener") and callable(self._remove_coordinator_listener):
            self._remove_coordinator_listener()

    def _on_coordinator_update(self) -> None:
        """Rotate access token and write state so the frontend reloads the image."""
        self._access_token = uuid.uuid4().hex
        self._access_tokens = [self._access_token]
        # Update last refreshed timestamp only when coordinator has non-None data
        # (update_image returns bytes when a new image was actually downloaded)
        if getattr(self.coordinator, "data", None) is not None:
            self._last_refreshed = dt_util.utcnow()
        # Trigger HA state update so frontend will use the new token/url
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional state attributes for the entity.

        Return any extra attributes for the entity. We no longer expose last_refreshed
        as an attribute because it will be shown as the entity state instead.
        """
        return {}

    @property
    def state(self) -> str | None:
        """Return the entity state.

        Use ISO 8601 UTC timestamp of last refresh as the entity state so it matches
        integrations like the Roborock image entity.
        """
        if not self._last_refreshed:
            return None

        try:
            return dt_util.as_utc(self._last_refreshed).isoformat()
        except Exception:
            return getattr(self._last_refreshed, "isoformat", lambda: str(self._last_refreshed))()

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