from src.tree import DependencyTree
from src.dependency import Dependency

class PythonDependencyTree(DependencyTree):
    def __init__(self, dependency: Dependency):
        super().__init__(dependency)
    
    def build_tree(self) -> dict:
        dependency_data = self.root_dependency.get_dependencies()