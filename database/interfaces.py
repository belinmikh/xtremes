from abc import ABC, abstractmethod

from datafile.interfaces import IMaterials


class IDatabase(ABC):
    @abstractmethod
    async def fill(self, data: IMaterials): ...

    @abstractmethod
    async def rnd(self): ...
