from abc import ABC, abstractmethod

class Parser(ABC):

    @abstractmethod
    def parse_dependencies(self) -> dict:
        pass