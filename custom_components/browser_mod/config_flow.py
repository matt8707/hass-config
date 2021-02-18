from homeassistant import config_entries

from .const import DOMAIN

class BrowserModConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_import(self, import_info):
        return self.async_create_entry(title="Browser Mod", data={})
