from .const import DOMAIN

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    await hass.config_entries.async_forward_entry_setups(entry, ["image"])
    return True

def get_refresh_interval(entry):
    # Default to 1 hour if not set
    return entry.options.get("refresh_interval", 1)