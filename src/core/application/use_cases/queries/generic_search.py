from dataclasses import dataclass
from typing import Any

from src.core.domain import AbstractRepository, PageRequest, SearchCriteria


@dataclass(frozen=True)
class SearchRequestDTO:
    """Data transfer object for search request"""

    filters: dict[str, Any]
    page: int = 1
    page_size: int = 10


@dataclass(frozen=True)
class SearchResponseDTO[T]:
    """Data transfer object for search response"""

    data: list[T]
    meta: dict[str, int]


class GenericSearchUseCase[T]:
    """Use case for search entities of type T"""

    def __init__(self, repository: AbstractRepository[T]) -> None:
        """Initialize the search use case"""

        self._repository = repository

    async def execute(self, request: SearchRequestDTO) -> SearchResponseDTO[T]:
        """Execute the use case"""

        criteria = SearchCriteria(
            filters=request.filters,
            pagination=PageRequest(page=request.page, page_size=request.page_size),
        )

        result = await self._repository.search(criteria=criteria)

        return SearchResponseDTO(
            data=result.items,
            meta={
                "total_items": result.total_items,
                "page": result.page,
                "page_size": result.page_size,
                "total_pages": result.total_pages,
            },
        )
