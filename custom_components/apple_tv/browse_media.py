"""Support for media browsing."""

from homeassistant.components.media_player import BrowseMedia
from homeassistant.components.media_player.const import (
    MEDIA_CLASS_APP,
    MEDIA_CLASS_DIRECTORY,
    MEDIA_TYPE_APP,
    MEDIA_TYPE_APPS,
)


def build_app_list(app_list):
    """Create response payload for app list."""
    title = None
    media = None
    children_media_class = None

    title = "Apps"
    media = [
        {"app_id": app_id, "title": app_name, "type": MEDIA_TYPE_APP}
        for app_name, app_id in app_list.items()
    ]
    children_media_class = MEDIA_CLASS_APP

    return BrowseMedia(
        media_class=MEDIA_CLASS_DIRECTORY,
        media_content_id=None,
        media_content_type=MEDIA_TYPE_APPS,
        title=title,
        can_play=True,
        can_expand=False,
        children=[item_payload(item) for item in media],
        children_media_class=children_media_class,
    )


def item_payload(item):
    """
    Create response payload for a single media item.

    Used by async_browse_media.
    """
    return BrowseMedia(
        title=item["title"],
        media_class=MEDIA_CLASS_APP,
        media_content_type=MEDIA_TYPE_APP,
        media_content_id=item["app_id"],
        can_play=False,
        can_expand=False,
    )
