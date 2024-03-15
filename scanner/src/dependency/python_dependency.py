from src.dependency import Dependency
import requests

class PythonDependency(Dependency):
    
    def __init__(self, name: str, version: str, children: dict):
        super().__init__(name, version, children)

    def get_dependencies(self):
        BASE_URL = f"https://pypi.org/pypi/{self._name}/{self._version}/json"
        json_data = requests.get(BASE_URL).json()
        json_data.raise_for_status()
        return json_data["info"]["requires_dist"]
         
    def set_dependencies(self):
        super().set_dependencies()
        
    
