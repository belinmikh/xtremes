from typing import Type, Any

from configuration.interfaces import IConfig, _NotSet


class Field[T]:
    __attr_name: str
    __type: Type[T]
    __dft: T | _NotSet
    __opt: bool

    def __init__(
        self, _t: Type[T], *, default: T | _NotSet = _NotSet(), optional: bool = False
    ):
        self.__type = _t
        self.__dft = default
        self.__opt = optional

    def __set_name__(self, owner: Any, name: str):
        self.__attr_name = name

    def __set__(self, instance: IConfig, value: T | _NotSet = _NotSet()):
        if isinstance(value, _NotSet):
            value = self.__dft
        if isinstance(value, _NotSet) and not self.__opt:
            raise ValueError(f"Missing {self.__attr_name} field")
        if not isinstance(value, self.__type):
            try:
                value = self.__type(value)
            except Exception as ex:
                raise TypeError(
                    f"Can't change {type(value)} to {self.__type} in {self.__attr_name} field"
                ) from ex
        instance.__dict__[self.__attr_name] = value

    def __get__(self, instance, owner) -> T:
        val = instance.__dict__[self.__attr_name]
        if isinstance(val, _NotSet):
            raise AttributeError
        return val
