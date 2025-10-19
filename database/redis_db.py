import asyncio
from random import randint

from redis.asyncio import Redis

from database.exceptions import UnfilledDatabaseException
from database.interfaces import IDatabase
from datafile.interfaces import IMaterials


class RedisDB(IDatabase):
    __rds: Redis
    __size: int
    __lock: bool

    def __init__(self, host: str, port: int, db: int):
        self.__rds = Redis(host=host, port=port, db=db)
        self.__size = 0
        self.__lock = False

    async def fill(self, data: IMaterials):
        self.__lock = True
        await self.__rds.flushdb()
        await asyncio.gather(
            *(self.__rds.set(bytes(i), data[i]) for i in range(len(data)))
        )
        self.__size = await self.__rds.dbsize()
        self.__lock = False

    async def rnd(self):
        while self.__lock:
            await asyncio.sleep(0.1)
        if not self.__size:
            self.__size = await self.__rds.dbsize()
        if not self.__size:
            raise UnfilledDatabaseException(
                "Redis is empty! Ensure calling RedisDB.fill"
            )
        return await self.__rds.get(bytes(randint(0, self.__size - 1)))

    @property
    def size(self) -> int:
        return self.__size
