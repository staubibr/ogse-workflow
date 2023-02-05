from components.json_object import JsonObject


class Element(JsonObject):
    @property
    def element_type(self):
        return self._element_type

    def initialize(self):
        raise Exception("initialize function not implemented for {0}.".format(self.element_type))

    def validate_element(self, field, mandatory, repeatable, domain=None):
        if field not in self.json or self.json[field] is None:
            if mandatory:
                raise Exception("Missing element: {0} element is mandatory for {1}.".format(field, self.element_type))

        elif repeatable:
            if not isinstance(self.json[field], list) or len(self.json[field]) == 0:
                raise Exception("Invalid element: repeatable element {0} for {1} must be a non-zero length array.".format(field, self.element_type))

        elif domain is not None:
            if self.json[field] not in domain:
                raise Exception("Invalid domain: element {0} for {1} must be in domain ({2}).".format(field, self.element_type, ", ".join(domain)))

    def __init__(self, json):
        super().__init__(json)

        self._element_type = type(self).__name__

        if json is None:
            return

        self.initialize()
