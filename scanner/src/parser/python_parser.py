from src.parser import Parser
from src.utils import SingletonLogger
import requirements
import re
from httpx import HTTPStatusError, TimeoutException, AsyncClient

class PythonParser(Parser):

    cache = {}

    @staticmethod
    def parse_dependencies(data: str) -> list:
        """
        Parses the requirements file and returns a list of dependencies
        """
        # Ensure that '\n' in the string is treated as actual new lines
        formatted_data = data.replace("\\n", "\n")
        dependencies = list(requirements.parse(formatted_data))
        
        parsed_dependencies = []
        for req in dependencies:
            dependency_info = {
                'name': req.name,
                'specs': req.specs,
                'extras': req.extras
            }
            parsed_dependencies.append(dependency_info)
        
        return parsed_dependencies
    
    @classmethod
    async def fetch_dependency_info(cls, package_name, package_version):
        logger = SingletonLogger()
        url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
        cache_key = f"{package_name}-{package_version}"
        if cache_key in cls.cache:
            return cls.cache[cache_key]
        try:
            async with AsyncClient() as client:
                response = await client.get(url, timeout=5.0) # Timeout set to 5 seconds
                response.raise_for_status()
                cls.cache[cache_key] = response.json()
                return response.json()
        except (HTTPStatusError, TimeoutException) as e:
            logger.error(f"Error fetching {package_name} {package_version}: {e}")
            logger.exception("Exception stack trace:")

    @classmethod    
    async def build_dependency_tree(cls, package_name, package_version, tree=None):
        """
        Recursively build a dependency tree for the given package and version.
        """
        if tree is None:
            tree = {}

        info = await cls.fetch_dependency_info(package_name, package_version)
        dependencies = info.get("info", {}).get("requires_dist", [])

        if dependencies:
            tree[package_name] = {"version": package_version, "dependencies": {}}
            for dep in dependencies:
                # Simple split to obtain package name and version - will need refinement in the future
                dep_name_version = dep.split(';')[0].strip()  # Simplistic split; ignores environment markers
                match = re.match(r"(?P<name>[\w\d\.-]+)\s*(?P<specifier>[<>=!~]*=?)\s*(?P<version>[\w\d\.-]+)?", dep_name_version)
                if match:
                    dep_name = match.group("name")
                    dep_version = match.group("version")
                    dep_specifier = match.group("specifier")
                    # Only processing '==' specifier for now for simplicity
                    if dep_version and dep_specifier == "==":
                        await cls.build_dependency_tree(dep_name, dep_version, tree[package_name]["dependencies"])
        else:
            tree[package_name] = {"version": package_version, "dependencies": None}

        return tree

            
