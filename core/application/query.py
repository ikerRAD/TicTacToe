from abc import ABC, abstractmethod

from core.application.query_response import QueryResponse


class Query(ABC):
    @abstractmethod
    def handle(self, *args) -> QueryResponse:
        pass
