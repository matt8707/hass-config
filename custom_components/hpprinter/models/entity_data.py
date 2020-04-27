from ..helpers.const import *


class EntityData:
    unique_id: str
    name: str
    state: bool
    attributes: dict
    icon: str
    device_name: str
    status: str

    def __init__(self):
        self.unique_id = ""
        self.name = ""
        self.state = False
        self.attributes = {}
        self.icon = ""
        self.device_name = ""
        self.status = ENTITY_STATUS_CREATED

    def __repr__(self):
        obj = {
            ENTITY_UNIQUE_ID: self.unique_id,
            ENTITY_NAME: self.name,
            ENTITY_STATE: self.state,
            ENTITY_ATTRIBUTES: self.attributes,
            ENTITY_ICON: self.icon,
            ENTITY_DEVICE_NAME: self.device_name,
            ENTITY_STATUS: self.status,
        }

        to_string = f"{obj}"

        return to_string
