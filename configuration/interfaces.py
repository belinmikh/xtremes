from abc import ABC, abstractmethod


class IConfig(ABC):
    @abstractmethod
    def _fetch(self): ...


class _NotSet: ...
