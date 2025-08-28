import json
import warnings

from configuration.interfaces import IConfig, _NotSet


class JsonConfig(IConfig):
    def __init__(self, filename: str):
        self.__filename = filename
        self._fetch()

    def _fetch(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as ex:
            data = dict()
            warnings.warn(f"File configuration haven't been read: {ex}")

        for key in dir(self):
            if not key.startswith("__"):
                setattr(self, key, data.get(key, _NotSet()))
