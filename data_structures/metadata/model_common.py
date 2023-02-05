from data_structures.metadata.message_type import MessageType
from data_structures.metadata.model_dcmi import ModelDCMI
from data_structures.metadata.port import Port


class ModelCommon(ModelDCMI):
    @property
    def behavior(self):
        return self.json["behavior"]

    @property
    def port(self):
        return self._port

    @property
    def message_type(self):
        return self._message_type

    def __init__(self, json):
        super().__init__(json)

        if "port" in self.json and self.json["port"] is not None:
            self._port = [Port(p) for p in self.json["port"]]

        if "message type" in self.json and self.json["message type"] is not None:
            self._message_type = [MessageType(mt) for mt in self.json["message type"]]

    def initialize(self):
        super().initialize()
        self.validate_element("behavior", False, False)
        self.validate_element("port", False, True)
        self.validate_element("message type", False, True)
