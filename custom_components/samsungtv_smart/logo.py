
import aiohttp
import aiofiles
import asyncio
import json
import logging
import numpy as np
import os
import re
import traceback

from datetime import timedelta, datetime
from enum import Enum
from typing import Optional


# Logo feature constants
class LogoOption(Enum):
    Disabled = 1
    WhiteColor = 2
    BlueColor = 3
    BlueWhite = 4
    DarkWhite = 5
    TransparentColor = 6
    TransparentWhite = 7


LOGO_OPTIONS_MAPPING = {
    LogoOption.Disabled: "none",
    LogoOption.WhiteColor: "fff-color",
    LogoOption.BlueColor: "05a9f4-color",
    LogoOption.BlueWhite: "05a9f4-white",
    LogoOption.DarkWhite: "282c34-white",
    LogoOption.TransparentColor: "transparent-color",
    LogoOption.TransparentWhite: "transparent-white",
}
LOGO_OPTION_DEFAULT = [LogoOption.WhiteColor.value, "fff-color"]
LOGO_BASE_URL = "https://jaruba.github.io/channel-logos/"
LOGO_FILE = "logo_paths.json"
LOGO_FILE_DOWNLOAD = "logo_paths_download.json"
LOGO_FILE_DAYS_BEFORE_UPDATE = 1
LOGO_MIN_SCORE_REQUIRED = 80
LOGO_MEDIATITLE_KEYWORD_REMOVAL = ["HDTV", "HD"]
LOGO_MAX_PATHS = 30000
LOGO_NO_MATCH = "NO_MATCH"
MAX_LOGO_CACHE = 200

_LOGGER = logging.getLogger(__name__)


class Logo:
    """ Class that fetches logos for Samsung TV Tizen. Works with https://github.com/jaruba/channel-logos. """

    def __init__(
        self,
        logo_option: int,
        logo_file_download: str = None,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        self._media_image_base_url = None
        self._logo_option = None
        self.set_logo_color(logo_option)
        if session:
            self._session = session
        else:
            self._session = aiohttp.ClientSession()

        self._images_paths = None
        self._logo_cache = {}
        self._last_check = None

        app_path = os.path.dirname(os.path.realpath(__file__))
        self._logo_file_path = os.path.join(app_path, LOGO_FILE)
        self._logo_file_download_path = (
            logo_file_download or
            os.path.join(app_path, LOGO_FILE_DOWNLOAD)
        )

    def set_logo_color(self, logo_option):
        """ Sets the logo color option and image base url if not already set to this option """
        logo_option = (
            LOGO_OPTIONS_MAPPING[LogoOption(logo_option)]
            if logo_option
            else LOGO_OPTION_DEFAULT[1]
        )
        if self._logo_option and self._logo_option == logo_option:
            return

        _LOGGER.debug("Setting logo option to %s", logo_option)
        if logo_option in LOGO_OPTIONS_MAPPING.values():
            self._logo_option = logo_option
        else:
            _LOGGER.warning(
                "Unrecognized value '%s' for 'Display logos' option. Using default value.",
                logo_option,
            )
            self._logo_option = LOGO_OPTION_DEFAULT[1]

        if logo_option == LOGO_OPTIONS_MAPPING[LogoOption.Disabled]:
            self._media_image_base_url = None
        else:
            self._media_image_base_url = f"{LOGO_BASE_URL}export/{self._logo_option}"

    async def check_requested(self):
        """Check if a new file update is requested."""
        if self._media_image_base_url is None:
            return False

        check_time = datetime.utcnow().astimezone()
        if (
            self._last_check is not None and
            self._last_check > check_time-timedelta(days=LOGO_FILE_DAYS_BEFORE_UPDATE)
        ):
            return False

        return True

    async def _async_ensure_latest_path_file(self):
        """ Does check if logo paths file exists and if it does - is it out of date or not."""
        if not self.check_requested():
            return

        check_time = datetime.utcnow().astimezone()
        update_file = not os.path.isfile(self._logo_file_download_path)
        if not update_file:
            file_date = datetime.utcfromtimestamp(
                os.path.getmtime(self._logo_file_download_path)
            ).astimezone()
            if file_date > check_time-timedelta(days=LOGO_FILE_DAYS_BEFORE_UPDATE):
                self._last_check = file_date
                return

            try:
                async with self._session.head(
                    LOGO_BASE_URL + "logo_paths.json"
                ) as response:
                    url_date = datetime.strptime(
                        response.headers.get("Last-Modified"),
                        "%a, %d %b %Y %X %Z",
                    ).astimezone()
                    update_file = (url_date > file_date)
            except (aiohttp.ClientError, asyncio.TimeoutError):
                _LOGGER.warning(
                    "Not able to check for latest paths file for logos from %s%s. "
                    "Check if the URL is accessible from this machine",
                    LOGO_BASE_URL,
                    "logo_paths.json",
                )

        self._last_check = check_time
        if update_file:
            if await self._download_latest_path_file():
                await self._read_path_file(True)

    async def _download_latest_path_file(self):
        """Download the last available logo file."""
        try:
            async with self._session.get(LOGO_BASE_URL + "logo_paths.json") as response:
                response = (await response.read()).decode("utf-8")
                if response:
                    async with aiofiles.open(
                        self._logo_file_download_path, mode="w+", encoding="utf-8"
                    ) as paths_file:
                        await paths_file.write(response)

            return True

        except (aiohttp.ClientError, asyncio.TimeoutError):
            _LOGGER.warning(
                "Not able to download latest paths file for logos from %s%s. "
                "Check if the URL is accessible from this machine.",
                LOGO_BASE_URL,
                "logo_paths.json",
            )
        except PermissionError:
            _LOGGER.warning(
                "No permission while trying to write the downloaded paths file to %s. "
                "Please check file writing permissions.",
                self._logo_file_download_path,
            )
        except OSError as e:
            _LOGGER.warning(
                "Not able to write to write the downloaded paths file to %s. "
                "Disk might be full or another OS error occurred",
                self._logo_file_download_path,
            )
            _LOGGER.warning(traceback.print_exc())

        return False

    async def _read_path_file(self, force_read=False):
        """Read the logo path file and store result locally."""
        if self._images_paths and not force_read:
            return

        logo_file = None
        if os.path.isfile(self._logo_file_download_path):
            logo_file = self._logo_file_download_path
        elif os.path.isfile(self._logo_file_path):
            logo_file = self._logo_file_path

        if not logo_file:
            _LOGGER.warning(
                "Not able to search for a logo. Logo paths file might be missing at %s or %s",
                self._logo_file_download_path,
                self._logo_file_path,
            )
            return

        try:
            async with aiofiles.open(logo_file, "r") as f:
                image_paths = json.loads(await f.read())
        except:
            _LOGGER.warning("Failed to read logo paths file %s", logo_file)
            return

        if image_paths:
            self._logo_cache = {}
            self._images_paths = image_paths

    def _add_to_cache(self, media_title, logo_path=LOGO_NO_MATCH):
        """Add a new item to the logo cache."""
        if len(self._logo_cache) > MAX_LOGO_CACHE:
            self._logo_cache.popitem()
        self._logo_cache[media_title] = logo_path

    async def async_find_match(self, media_title):
        """ Finds a match in the logo_paths file for a given media_title """
        if media_title is None:
            _LOGGER.warning("No media title right now! Not able to find a matching logo")
            return
        if self._media_image_base_url is None:
            _LOGGER.warning("Media image base url was not set! Not able to find a matching logo")
            return
        _LOGGER.debug("Matching media title for %s", media_title)
        await self._async_ensure_latest_path_file()

        # remove string between parenthesis ()
        removal = re.finditer(r"\((.*?)\)", media_title)
        for match in removal:
            media_title = media_title.replace(match.group(), "")

        # remove specific strings
        for word in LOGO_MEDIATITLE_KEYWORD_REMOVAL:
            media_title = media_title.lower().replace(word.lower(), "")

        # remove leading and trailing spaces
        media_title = media_title.lower().strip()

        # check if log is in the cache
        cached_logo = self._logo_cache.get(media_title)
        if cached_logo:
            if cached_logo == LOGO_NO_MATCH:
                return None
            return self._media_image_base_url + cached_logo

        # search best matching logo
        await self._read_path_file()
        if not self._images_paths:
            return None

        best_match = {"ratio": None, "title": None, "path": None}
        paths_checked = 0
        for image_path in iter(self._images_paths.items()):
            if paths_checked > LOGO_MAX_PATHS:
                _LOGGER.warning(
                    "Exceeded maximum amount of paths (%d) while searching for a match. Halting the search",
                    LOGO_MAX_PATHS,
                )
                break
            ratio = _levenshtein_ratio(media_title, image_path[0].lower())
            if best_match["ratio"] is None or ratio > best_match["ratio"]:
                best_match = {
                    "ratio": ratio,
                    "title": image_path[0],
                    "path": image_path[1],
                }
            if best_match["ratio"] == 1:
                break
            paths_checked += 1

        best_ratio = best_match["ratio"] or 0.0
        best_path = best_match["path"] or ""
        if best_ratio >= LOGO_MIN_SCORE_REQUIRED / 100 and best_path:
            found_logo = self._media_image_base_url + best_path
            _LOGGER.debug(
                "Match found for %s: %s (%f) %s",
                media_title,
                best_match["title"],
                best_ratio,
                found_logo,
            )
            self._add_to_cache(media_title, best_path)
            return found_logo

        _LOGGER.debug(
            "No match found for %s: best candidate was %s (%f) %s",
            media_title,
            best_match["title"],
            best_ratio,
            self._media_image_base_url + best_path,
        )
        self._add_to_cache(media_title)
        return None


def _levenshtein_ratio(s: str, t: str):
    """Calculate match ratio between 2 strings."""
    if not (s and t):
        return 0.0

    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows, cols), dtype=int)

    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 2
            distance[row][col] = min(
                distance[row - 1][col] + 1,
                distance[row][col - 1] + 1,
                distance[row - 1][col - 1] + cost,
            )

    ratio = ((len(s) + len(t)) - distance[rows-1][cols-1]) / (len(s) + len(t))
    return ratio
