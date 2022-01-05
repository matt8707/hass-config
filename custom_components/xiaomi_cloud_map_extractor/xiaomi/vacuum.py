import gzip

from custom_components.xiaomi_cloud_map_extractor.common.map_data import MapData
from custom_components.xiaomi_cloud_map_extractor.common.vacuum import XiaomiCloudVacuum
from custom_components.xiaomi_cloud_map_extractor.xiaomi.map_data_parser import MapDataParserXiaomi


class XiaomiVacuum(XiaomiCloudVacuum):

    def __init__(self, connector, country, user_id, device_id, model):
        super().__init__(connector, country, user_id, device_id, model)

    def get_map_url(self, map_name):
        url = self._connector.get_api_url(self._country) + "/home/getmapfileurl"
        params = {
            "data": '{"obj_name":"' + map_name + '"}'
        }
        api_response = self._connector.execute_api_call_encrypted(url, params)
        if api_response is None or \
                "result" not in api_response or \
                api_response["result"] is None or \
                "url" not in api_response["result"]:
            return None
        return api_response["result"]["url"]

    def decode_map(self, raw_map, colors, drawables, texts, sizes, image_config) -> MapData:
        unzipped = gzip.decompress(raw_map)
        return MapDataParserXiaomi.parse(unzipped, colors, drawables, texts, sizes, image_config)

    def should_get_map_from_vacuum(self):
        return True

    def get_map_archive_extension(self):
        return "gz"
