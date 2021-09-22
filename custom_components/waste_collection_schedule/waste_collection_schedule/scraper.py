#!/usr/bin/env python3

import datetime
import importlib
import itertools
import logging
from typing import Dict, List, Optional

from .collection import Collection, CollectionGroup

_LOGGER = logging.getLogger(__name__)


class Customize:
    """Customize one waste collection type."""

    def __init__(self, waste_type, alias=None, show=True, icon=None, picture=None):
        self._waste_type = waste_type
        self._alias = alias
        self._show = show
        self._icon = icon
        self._picture = picture

    @property
    def waste_type(self):
        return self._waste_type

    @property
    def alias(self):
        return self._alias

    @property
    def show(self):
        return self._show

    @property
    def icon(self):
        return self._icon

    @property
    def picture(self):
        return self._picture

    def __repr__(self):
        return f"Customize{{waste_type={self._waste_type}, alias={self._alias}, show={self._show}, icon={self._icon}, picture={self._picture}}}"


def filter_function(entry: Collection, customize: Dict[str, Customize]):
    c = customize.get(entry.type)
    if c is None:
        return True
    else:
        return c.show


def customize_function(entry: Collection, customize: Dict[str, Customize]):
    c = customize.get(entry.type)
    if c is not None:
        if c.alias is not None:
            entry.set_type(c.alias)
        if c.icon is not None:
            entry.set_icon(c.icon)
        if c.picture is not None:
            entry.set_picture(c.picture)
    return entry


class Scraper:
    def __init__(
        self,
        source,
        customize: Dict[str, Customize],
        title: str,
        description: str,
        url: Optional[str],
        calendar_title: Optional[str],
    ):
        self._source = source
        self._customize = customize
        self._title = title
        self._description = description
        self._url = url
        self._calendar_title = calendar_title
        self._refreshtime = None
        self._entries: List[Collection] = []

    @property
    def source(self):
        return self._source

    @property
    def refreshtime(self):
        return self._refreshtime

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return self._url

    @property
    def calendar_title(self):
        return self._calendar_title or self._title

    def fetch(self):
        """Fetch data from source."""
        try:
            # fetch returns a list of Collection's
            entries = self._source.fetch()
            self._refreshtime = datetime.datetime.now()

            # strip whitespaces
            for e in entries:
                e.set_type(e.type.strip())

            # filter hidden entries
            entries = filter(lambda x: filter_function(x, self._customize), entries)

            # customize fetched entries
            entries = map(lambda x: customize_function(x, self._customize), entries)

            self._entries = list(entries)
        except Exception as error:
            _LOGGER.error(f"fetch failed for source {self._source}: {error}")

    def get_types(self):
        """Return set() of all collection types."""
        types = set()
        for e in self._entries:
            types.add(e.type)
        return types

    def get_upcoming(self, count=None, leadtime=None, types=None, include_today=False):
        """Return list of all entries, limited by count and/or leadtime.

        Keyword arguments:
        count -- limits the number of returned entries (default=10)
        leadtime -- limits the timespan in days of returned entries (default=7, 0 = today)
        """
        return self._filter(
            self._entries,
            count=count,
            leadtime=leadtime,
            types=types,
            include_today=include_today,
        )

    def get_upcoming_group_by_day(
        self, count=None, leadtime=None, types=None, include_today=False
    ):
        """Return list of all entries, grouped by day, limited by count and/or leadtime."""
        entries = []

        iterator = itertools.groupby(
            self._filter(
                self._entries,
                leadtime=leadtime,
                types=types,
                include_today=include_today,
            ),
            lambda e: e.date,
        )

        for key, group in iterator:
            entries.append(CollectionGroup.create(list(group)))
        if count is not None:
            entries = entries[:count]

        return entries

    def _filter(
        self, entries, count=None, leadtime=None, types=None, include_today=False
    ):
        # remove unwanted waste types
        if types is not None:
            # generate set
            types_set = {t for t in types}
            entries = list(filter(lambda e: e.type in types_set, self._entries))

        # remove expired entries
        now = datetime.datetime.now().date()
        if include_today:
            entries = list(filter(lambda e: e.date >= now, entries))
        else:
            entries = list(filter(lambda e: e.date > now, entries))

        # remove entries which are too far in the future (0 = today)
        if leadtime is not None:
            x = now + datetime.timedelta(days=leadtime)
            entries = list(filter(lambda e: e.date <= x, entries))

        # ensure that entries are sorted by date
        entries.sort(key=lambda e: e.date)

        # remove surplus entries
        if count is not None:
            entries = entries[:count]

        return entries

    @staticmethod
    def create(
        source_name: str,
        customize: Dict[str, Customize],
        source_args,
        calendar_title: Optional[str] = None,
    ):
        # load source module

        # for home-assistant, use the last 3 folders, e.g. custom_component/wave_collection_schedule/waste_collection_schedule
        # otherwise, only use waste_collection_schedule
        try:
            source_module = importlib.import_module(
                f"waste_collection_schedule.source.{source_name}"
            )
        except ImportError:
            _LOGGER.error(f"source not found: {source_name}")
            return

        # create source
        source = source_module.Source(**source_args)  # type: ignore

        # create scraper
        g = Scraper(
            source=source,
            customize=customize,
            title=source_module.TITLE,  # type: ignore[attr-defined]
            description=source_module.DESCRIPTION,  # type: ignore[attr-defined]
            url=source_module.URL,  # type: ignore[attr-defined]
            calendar_title=calendar_title,
        )

        return g
