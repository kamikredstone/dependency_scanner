from pydantic import BaseModel
from abc import ABC, abstractmethod

class Dependency(BaseModel, ABC):
    
    def __init__(self, name: str, version: str, children: list = None):
        self._name = name
        self._version = version
        self.dependencies = children

    def set_dependencies(self):
        self.dependencies = self.get_dependencies()

    @abstractmethod
    def get_dependencies(self):
        pass

