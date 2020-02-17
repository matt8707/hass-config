from aiohttp import web
from homeassistant.components.http import HomeAssistantView

from .const import FRONTEND_SCRIPT_URL, DATA_EXTRA_MODULE_URL


def setup_view(hass):
    if DATA_EXTRA_MODULE_URL not in hass.data:
        hass.data[DATA_EXTRA_MODULE_URL] = set()
    url_set = hass.data[DATA_EXTRA_MODULE_URL]
    url_set.add(FRONTEND_SCRIPT_URL)

    hass.http.register_view(ModView(hass, FRONTEND_SCRIPT_URL))

class ModView(HomeAssistantView):

    name = "browser_mod_script"
    requires_auth = False

    def __init__(self, hass, url):
        self.url = url
        self.config_dir = hass.config.path()

    async def get(self, request):
        path = "{}/custom_components/browser_mod/browser_mod.js".format(self.config_dir)

        filecontent = ""

        try:
            with open(path, mode="r", encoding="utf-8", errors="ignore") as localfile:
                filecontent = localfile.read()
                localfile.close()
        except Exception as exception:
            pass

        return web.Response(body=filecontent, content_type="text/javascript", charset="utf-8")
