from __future__ import annotations
from abc import ABC, abstractmethod

from src.interfaces import repository


class AbstractUnitOfWork(ABC):
    weather: repository.AbstractRepository

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
