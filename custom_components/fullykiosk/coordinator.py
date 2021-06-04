"""Provides the The Fully Kiosk Browser DataUpdateCoordinator."""
import logging
from datetime import timedelta

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
from fullykiosk import FullyKiosk
from fullykiosk.exceptions import FullyKioskError
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class FullyKioskDataUpdateCoordinator(DataUpdateCoordinator):
    """Define an object to hold Fully Kiosk Browser data."""

    def __init__(
        self, hass: HomeAssistantType, session: ClientSession, host, port, password
    ):
        """Initialize."""
        self.fully = FullyKiosk(session, host, port, password)

        super().__init__(
            hass,
            _LOGGER,
            name=f"{host} deviceInfo",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            with timeout(15):
                return await self.fully.getDeviceInfo()
        except (FullyKioskError, ClientConnectorError) as error:
            raise UpdateFailed(error) from error
