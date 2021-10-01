import logging
from typing import Dict, Tuple

from PIL import Image
from PIL.Image import Image as ImageType

from custom_components.xiaomi_cloud_map_extractor.common.image_handler import ImageHandler
from custom_components.xiaomi_cloud_map_extractor.const import *

_LOGGER = logging.getLogger(__name__)


class ImageHandlerRoidmi(ImageHandler):
    MAP_WALL = 0
    MAP_OUTSIDE = 127
    MAP_UNKNOWN = 255

    @staticmethod
    def parse(raw_data, width, height, colors, image_config, room_numbers) \
            -> Tuple[ImageType, Dict[int, Tuple[int, int, int, int]]]:
        rooms = {}
        scale = image_config[CONF_SCALE]
        trim_left = int(image_config[CONF_TRIM][CONF_LEFT] * width / 100)
        trim_right = int(image_config[CONF_TRIM][CONF_RIGHT] * width / 100)
        trim_top = int(image_config[CONF_TRIM][CONF_TOP] * height / 100)
        trim_bottom = int(image_config[CONF_TRIM][CONF_BOTTOM] * height / 100)
        trimmed_height = height - trim_top - trim_bottom
        trimmed_width = width - trim_left - trim_right
        if trimmed_width == 0 or trimmed_height == 0:
            return ImageHandler.create_empty_map_image(colors), rooms
        image = Image.new('RGBA', (trimmed_width, trimmed_height))
        pixels = image.load()
        unknown_pixels = set()
        for img_y in range(trimmed_height):
            for img_x in range(trimmed_width):
                pixel_type = raw_data[img_x + trim_left + width * (img_y + trim_bottom)]
                x = img_x
                y = trimmed_height - 1 - img_y
                if pixel_type == ImageHandlerRoidmi.MAP_OUTSIDE:
                    pixels[x, y] = ImageHandler.__get_color__(COLOR_MAP_OUTSIDE, colors)
                elif pixel_type == ImageHandlerRoidmi.MAP_WALL:
                    pixels[x, y] = ImageHandler.__get_color__(COLOR_MAP_WALL_V2, colors)
                elif pixel_type == ImageHandlerRoidmi.MAP_UNKNOWN:
                    pixels[x, y] = ImageHandler.__get_color__(COLOR_UNKNOWN, colors)
                elif pixel_type in room_numbers:
                    room_x = img_x + trim_left
                    room_y = img_y + trim_bottom
                    room_number = pixel_type
                    if room_number not in rooms:
                        rooms[room_number] = (room_x, room_y, room_x, room_y)
                    else:
                        rooms[room_number] = (min(rooms[room_number][0], room_x),
                                              min(rooms[room_number][1], room_y),
                                              max(rooms[room_number][2], room_x),
                                              max(rooms[room_number][3], room_y))
                    default = ImageHandler.ROOM_COLORS[room_number % len(ImageHandler.ROOM_COLORS)]
                    pixels[x, y] = ImageHandler.__get_color__(f"{COLOR_ROOM_PREFIX}{room_number}", colors, default)
                else:
                    pixels[x, y] = ImageHandler.__get_color__(COLOR_UNKNOWN, colors)
                    unknown_pixels.add(pixel_type)
        if image_config["scale"] != 1 and trimmed_width != 0 and trimmed_height != 0:
            image = image.resize((int(trimmed_width * scale), int(trimmed_height * scale)), resample=Image.NEAREST)
        if len(unknown_pixels) > 0:
            _LOGGER.warning('unknown pixel_types: %s', unknown_pixels)
        return image, rooms
