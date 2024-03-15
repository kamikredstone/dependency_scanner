from pydantic import BaseModel
from abc import ABC, abstractmethod
from src.dependency import Dependency

class DependencyTree(BaseModel, ABC):
    def __init__(self, dependency: Dependency):
        self.root_dependency = dependency
        self.branch_dependency = None

    @abstractmethod
    def build_tree(self):
        pass