class FileInfo:
    def __init__(self, file_info):
        self.components = file_info["components"]
        self.parent = file_info["parent"]
        self.name = file_info["name"]
        self.extension = file_info.get("extension","")
        self.toString = file_info["toString"]

    def _get_components(self):
        return self._components

    def _set_components(self, value):
        self._components = value

    def _get_parent(self):
        return self._parent

    def _set_parent(self, value):
        self._parent = value

    def _get_name(self):
        return self._name

    def _set_name(self, value):
        self._name = value

    def _get_extension(self):
        return self._extension

    def _set_extension(self, value):
        self._extension = value

    def _get_to_string(self):
        return self._toString

    def _set_to_string(self, value):
        self._toString = value

    components = property(_get_components, _set_components, doc="The components the file reside in.")

    parent = property(_get_parent, _set_parent, doc="The parent folder the file resides in.")

    name = property(_get_name, _set_name, doc="The name of the file.")

    extension = property(_get_extension, _set_extension, doc="The extension of the file.")

    toString = property(_get_to_string, _set_to_string,
                        doc="A string value representing the full path from repository root.")
