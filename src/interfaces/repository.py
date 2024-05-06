from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Sequence, TypeVar

EntryType = TypeVar("EntryType")
ColumnType = TypeVar("ColumnType")


class AbstractRepository(ABC):
    async def create(self, **values: Mapping[str, Any]) -> Optional[EntryType]:
        """Create a new entry in the data storage using the provided values."""
        raise NotImplementedError

    @abstractmethod
    async def select_many(
        self,
        *clauses: Optional[ColumnType],
        offset: Optional[int],
        limit: Optional[int],
    ) -> Sequence[EntryType]:
        """Select and retrieve multiple entries from the data
        storage based on the provided clauses and pagination
        options.
        """
        raise NotImplementedError
