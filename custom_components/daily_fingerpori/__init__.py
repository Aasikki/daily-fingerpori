from .const import DOMAIN, CONF_REFRESH_INTERVAL

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    # Initialize domain data storage if it doesn't exist
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    
    # The coordinator will be created in image platform setup
    # Store a reference to it so the button platform can access it
    hass.data[DOMAIN][entry.entry_id] = {}
    
    await hass.config_entries.async_forward_entry_setups(entry, ["image", "button"])
    return True

def get_refresh_interval(entry):
    # Default to 3 hours if not set
    return entry.options.get(CONF_REFRESH_INTERVAL, 3)