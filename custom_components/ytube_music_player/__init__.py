"""Provide the initial setup."""
import logging
import asyncio
from integrationhelper.const import CC_STARTUP_VERSION
from ytmusicapi import YTMusic
from .const import *
from homeassistant.helpers.storage import STORAGE_DIR
import os.path

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
	"""Provide Setup of platform."""
	return True


async def async_setup_entry(hass, config_entry):
	"""Set up this integration using UI/YAML."""
	config_entry.data = ensure_config(config_entry.data)  # make sure that missing storage values will be default (const function)
	config_entry.options = config_entry.data
	config_entry.add_update_listener(update_listener)
	# Add sensor
	hass.async_add_job(
		hass.config_entries.async_forward_entry_setup(config_entry, PLATFORM)
	)
	return True



async def async_remove_entry(hass, config_entry):
	"""Handle removal of an entry."""
	try:
		await hass.config_entries.async_forward_entry_unload(config_entry, PLATFORM)
		_LOGGER.info(
			"Successfully removed sensor from the integration"
		)
	except ValueError:
		pass


async def update_listener(hass, entry):
	"""Update listener."""
	entry.data = entry.options
	await hass.config_entries.async_forward_entry_unload(entry, PLATFORM)
	hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, PLATFORM))
