import logging
from homeassistant.components.media_player import (
        SUPPORT_PLAY, SUPPORT_PLAY_MEDIA,
        SUPPORT_PAUSE, SUPPORT_STOP,
        SUPPORT_VOLUME_SET, SUPPORT_VOLUME_MUTE,
        MediaPlayerEntity,
    )
from homeassistant.const import (
        STATE_UNAVAILABLE,
        STATE_PAUSED,
        STATE_PLAYING,
        STATE_IDLE,
        STATE_UNKNOWN,
    )

from .helpers import setup_platform, BrowserModEntity

_LOGGER = logging.getLogger(__name__)

PLATFORM = 'media_player'

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    return setup_platform(hass, config, async_add_devices, PLATFORM, BrowserModPlayer)


async def async_setup_entry(hass, config_entry, async_add_entities):
    await async_setup_platform(hass, {}, async_add_entities)


class BrowserModPlayer(MediaPlayerEntity, BrowserModEntity):
    domain = PLATFORM

    def __init__(self, hass, connection, deviceID, alias=None):
        super().__init__(hass, connection, deviceID, alias)
        self.last_seen = None

    def updated(self):
        self.schedule_update_ha_state()

    @property
    def device_state_attributes(self):
        return {
                "type": "browser_mod",
                "deviceID": self.deviceID,
                }

    @property
    def state(self):
        if not self.connection.connection:
            return STATE_UNAVAILABLE
        state = self.data.get("state", "unknown")
        return {
                "playing": STATE_PLAYING,
                "paused": STATE_PAUSED,
                "stopped": STATE_IDLE,
                }.get(state, STATE_UNKNOWN)
    @property
    def supported_features(self):
        return (
            SUPPORT_PLAY | SUPPORT_PLAY_MEDIA |
            SUPPORT_PAUSE | SUPPORT_STOP |
            SUPPORT_VOLUME_SET | SUPPORT_VOLUME_MUTE
            )
    @property
    def volume_level(self):
        return self.data.get("volume", 0)
    @property
    def is_volume_muted(self):
        return self.data.get("muted", False)
    @property
    def media_content_id(self):
        return self.data.get("src", "")

    def set_volume_level(self, volume):
        self.connection.send("set_volume", volume_level=volume)
    def mute_volume(self, mute):
        self.connection.send("mute", mute=mute)

    def play_media(self, media_type, media_id, **kwargs):
        self.connection.send("play", media_content_id=media_id)
    def media_play(self):
        self.connection.send("play")
    def media_pause(self):
        self.connection.send("pause")
    def media_stop(self):
        self.connection.send("stop")
