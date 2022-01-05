import json
import logging
from typing import Dict, List, Optional, Tuple

from custom_components.xiaomi_cloud_map_extractor.common.map_data import Area, ImageData, MapData, Path, Point, Room, \
    Wall
from custom_components.xiaomi_cloud_map_extractor.common.map_data_parser import MapDataParser
from custom_components.xiaomi_cloud_map_extractor.const import *
from custom_components.xiaomi_cloud_map_extractor.roidmi.image_handler import ImageHandlerRoidmi

_LOGGER = logging.getLogger(__name__)


class MapDataParserRoidmi(MapDataParser):

    @staticmethod
    def parse(raw: bytes, colors, drawables, texts, sizes, image_config) -> MapData:
        scale = float(image_config[CONF_SCALE])
        map_image_size = raw.find(bytes([127, 123]))
        map_image = raw[16:map_image_size + 1]
        map_info_raw = raw[map_image_size + 1:]
        map_info = json.loads(map_info_raw)
        width = map_info["width"]
        height = map_info["height"]
        x_min = map_info["x_min"]
        y_min = map_info["y_min"]
        resolution = map_info["resolution"]
        x_min_calc = x_min / resolution
        y_min_calc = y_min / resolution
        map_data = MapData(0, 1000)
        map_data.rooms = MapDataParserRoidmi.parse_rooms(map_info)
        image = MapDataParserRoidmi.parse_image(map_image, width, height, x_min_calc, y_min_calc, resolution,
                                                colors, image_config, map_data.rooms)
        map_data.image = image
        map_data.path = MapDataParserRoidmi.parse_path(map_info)
        map_data.vacuum_position = MapDataParserRoidmi.parse_vacuum_position(map_info)
        map_data.charger = MapDataParserRoidmi.parse_charger_position(map_info)
        map_data.no_go_areas, map_data.no_mopping_areas, map_data.walls = MapDataParserRoidmi.parse_areas(map_info)
        if not map_data.image.is_empty:
            MapDataParserRoidmi.draw_elements(colors, drawables, sizes, map_data, image_config)
            if len(map_data.rooms) > 0 and map_data.vacuum_position is not None:
                map_data.vacuum_room = MapDataParserRoidmi.get_current_vacuum_room(map_image, map_data, width)
                if map_data.vacuum_room is not None:
                    map_data.vacuum_room_name = map_data.rooms[map_data.vacuum_room].name
            ImageHandlerRoidmi.rotate(map_data.image)
            ImageHandlerRoidmi.draw_texts(map_data.image, texts)
        return map_data

    @staticmethod
    def get_current_vacuum_room(map_image: bytes, map_data: MapData, original_width: int) -> Optional[int]:
        p = map_data.image.dimensions.img_transformation(map_data.vacuum_position)
        room_number = map_image[int(p.x) + int(p.y) * original_width]
        if room_number in map_data.rooms:
            return room_number
        return None

    @staticmethod
    def map_to_image(p: Point, resolution, min_x, min_y) -> Point:
        return Point(p.x / 1000 / resolution - min_x, p.y / 1000 / resolution - min_y)

    @staticmethod
    def image_to_map(p: Point, resolution, min_x, min_y) -> Point:
        return Point((p.x + min_x) * resolution * 1000, (p.y + min_y) * resolution * 1000)

    @staticmethod
    def parse_image(map_image: bytes, width: int, height: int, min_x: float, min_y: float, resolution: float,
                    colors: Dict, image_config: Dict, rooms: Dict[int, Room]) -> ImageData:
        image_top = 0
        image_left = 0
        room_numbers = rooms.keys()
        image, rooms_raw = ImageHandlerRoidmi.parse(map_image, width, height, colors, image_config, room_numbers)
        for number, room in rooms_raw.items():
            pf = lambda p: MapDataParserRoidmi.image_to_map(p, resolution, min_x, min_y)
            p1 = pf(Point(room[0] + image_left, room[1] + image_top))
            p2 = pf(Point(room[2] + image_left, room[3] + image_top))
            rooms[number].x0 = p1.x
            rooms[number].y0 = p1.y
            rooms[number].x1 = p2.x
            rooms[number].y1 = p2.y
        return ImageData(width * height, image_top, image_left, height, width, image_config, image,
                         lambda p: MapDataParserRoidmi.map_to_image(p, resolution, min_x, min_y))

    @staticmethod
    def parse_path(map_info: dict) -> Path:
        path_points = []
        if "posArray" in map_info:
            raw_points = json.loads(map_info["posArray"])
            for raw_point in raw_points:
                point = Point(raw_point[0], raw_point[1])
                path_points.append(point)
        return Path(None, None, None, path_points)

    @staticmethod
    def parse_vacuum_position(map_info: dict) -> Point:
        vacuum_position = None
        if "robotPos" in map_info and "robotPhi" in map_info:
            vacuum_position = Point(map_info["robotPos"][0], map_info["robotPos"][1], map_info["robotPhi"])
        elif "posX" in map_info and "posY" in map_info and "posPhi" in map_info:
            vacuum_position = Point(map_info["posX"], map_info["posY"], map_info["posPhi"])
        return vacuum_position

    @staticmethod
    def parse_charger_position(map_info: dict) -> Point:
        charger_position = None
        if "chargeHandlePos" in map_info:
            charger_position = Point(map_info["chargeHandlePos"][0], map_info["chargeHandlePos"][1])
        return charger_position

    @staticmethod
    def parse_rooms(map_info: dict) -> Dict[int, Room]:
        rooms = {}
        areas = []
        if "autoArea" in map_info:
            areas = map_info["autoArea"]
        elif "autoAreaValue" in map_info and map_info["autoAreaValue"] is not None:
            areas = map_info["autoAreaValue"]
        for area in areas:
            id = area["id"]
            name = area["name"]
            pos_x = area["pos"][0] if "pos" in area else None
            pos_y = area["pos"][1] if "pos" in area else None
            rooms[id] = Room(id, None, None, None, None, name, pos_x, pos_y)
        return rooms

    @staticmethod
    def parse_areas(map_info: dict) -> Tuple[List[Area], List[Area], List[Wall]]:
        no_go_areas = []
        no_mopping_areas = []
        walls = []
        if "area" in map_info:
            areas = map_info["area"]
            for area in areas:
                if "active" in area and area["active"] == "forbid" and "vertexs" in area and len(area["vertexs"]) == 4:
                    vertexs = area["vertexs"]
                    x0 = vertexs[0][0]
                    y0 = vertexs[0][1]
                    x1 = vertexs[1][0]
                    y1 = vertexs[1][1]
                    x2 = vertexs[2][0]
                    y2 = vertexs[2][1]
                    x3 = vertexs[3][0]
                    y3 = vertexs[3][1]
                    no_area = Area(x0, y0, x1, y1, x2, y2, x3, y3)
                    if "forbidType" in area and area["forbidType"] == "mop":
                        no_mopping_areas.append(no_area)
                    if "forbidType" in area and area["forbidType"] == "all":
                        no_go_areas.append(no_area)
                if "active" in area and area["active"] == "forbid" and "vertexs" in area and len(area["vertexs"]) == 2:
                    vertexs = area["vertexs"]
                    x0 = vertexs[0][0]
                    y0 = vertexs[0][1]
                    x1 = vertexs[1][0]
                    y1 = vertexs[1][1]
                    wall = Wall(x0, y0, x1, y1)
                    if "forbidType" in area and area["forbidType"] == "all":
                        walls.append(wall)
        return no_go_areas, no_mopping_areas, walls
