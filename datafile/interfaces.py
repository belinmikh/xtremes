from abc import ABC, abstractmethod
from typing import Type, Iterable


class IMaterials(ABC):
    @abstractmethod
    def __init__(self, data: Iterable[str], include: Iterable[str]): ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __getitem__(self, item: int) -> str: ...


class IFileSchema(ABC):
    @abstractmethod
    def read_from(
        self,
        filename: str,
        include: Iterable[str],
        _imat_type: Type[IMaterials] | None = None,
    ) -> None: ...

    @property
    @abstractmethod
    def data(self) -> IMaterials: ...
