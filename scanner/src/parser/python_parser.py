from src.parser import Parser
import requirements

class PythonParser(Parser):
    def parse_dependencies(self, file):
        """
        Parses the requirements file and returns a list of dependencies
        """
        return [requirements.parse(dependency) for dependency in self._data]
    
    def parse_json_pypi_api(self):
        """
        Parses the returned json from the pypi API endpoint which is:
        https://pypi.org/pypi/<dependency_name>/<dependency_version>/json
        """

            
