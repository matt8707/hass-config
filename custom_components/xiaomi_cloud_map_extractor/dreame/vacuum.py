from custom_components.xiaomi_cloud_map_extractor.common.vacuum_v2 import XiaomiCloudVacuumV2


class DreameVacuum(XiaomiCloudVacuumV2):

    def __init__(self, connector, country, user_id, device_id, model):
        super().__init__(connector, country, user_id, device_id, model)

    def get_map_archive_extension(self):
        return "b64"
