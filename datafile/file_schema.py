import csv
import logging
from typing import Type, Iterable

from aiofile import async_open, AIOFile

from datafile.csv_reader import AsyncDictReader
from datafile.exceptions import UnfilledAttrException
from datafile.interfaces import IFileSchema, IMaterials
from datafile.materials import Materials


class FileSchema(IFileSchema):
    __data_column: str
    __delimiter: str
    __encoding: str

    __data: IMaterials | None

    def __init__(self, data_column: str = "Материал", delimiter: str = ";", encoding: str = "Windows-1251"):
        self.__data_column = data_column
        self.__delimiter = delimiter
        self.__encoding = encoding
        self.__data = None

    def read_from(self, filename: str, include: Iterable[str], _imat_type: Type[IMaterials] | None = None) -> None:
        if _imat_type is None:
            _imat_type = Materials
        with open(filename, "r", encoding=self.__encoding) as file:
            csv_reader = csv.DictReader(file, delimiter=self.__delimiter)
            self.__data = _imat_type(
                (
                    item.get(self.__data_column, "")
                    for item in csv_reader
                ),
                include
            )


    @property
    def data(self) -> IMaterials:
        if self.__data is None:
            raise UnfilledAttrException("FileSchema.data is not set! Use await FileSchema.read_from before accessing this attribute")
        return self.__data
