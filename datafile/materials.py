from typing import Iterable

from datafile.interfaces import IMaterials


class Materials(IMaterials):
    __data: tuple[str, ...]

    def __init__(self, data: Iterable[str], include: Iterable[str]):
        self.__data = tuple(
            item for item in data
            if any(keyword in item for keyword in include)
        )

    def __len__(self) -> int:
        return len(self.__data)

    def __getitem__(self, item: int) -> str:
        return self.__data[item]
