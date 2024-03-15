from pydantic import BaseModel
from abc import ABC, abstractmethod
from fastapi import File

class Parser(BaseModel):

    @abstractmethod
    def parse_dependencies(self) -> dict:
        pass