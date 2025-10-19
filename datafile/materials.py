import logging
from typing import Iterable

from datafile.interfaces import IMaterials


class Materials(IMaterials):
    __data: tuple[str, ...]

    def __init__(self, data: Iterable[str], include: Iterable[str]):
        data_lst = []
        total = 0
        for item in data:
            if any(keyword in item for keyword in include):
                data_lst.append(item)
            total += 1
        self.__data = tuple(data_lst)
        logging.info(f"Filtered {len(self.__data)} rows out of {total} total")

    def __len__(self) -> int:
        return len(self.__data)

    def __getitem__(self, item: int) -> str:
        return self.__data[item]
