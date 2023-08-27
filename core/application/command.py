from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def handle(self, *args) -> None:
        pass
