import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from .const import DOMAIN, DEFAULT_NAME

CONF_REFRESH_INTERVAL = "Comic Update Interval (hours)"

class FingerporiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=DEFAULT_NAME, data={}, options={
                CONF_REFRESH_INTERVAL: user_input[CONF_REFRESH_INTERVAL]
            })
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional(CONF_REFRESH_INTERVAL, default=1): int
            })
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return FingerporiOptionsFlowHandler(config_entry)

class FingerporiOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data={
                CONF_REFRESH_INTERVAL: user_input[CONF_REFRESH_INTERVAL]
            })
        options = self.config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(CONF_REFRESH_INTERVAL, default=options.get(CONF_REFRESH_INTERVAL, 1)): int
            })
        )
