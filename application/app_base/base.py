from typing import TypeVar
from tortoise.models import Model

ModelType = TypeVar("ModelType", bound=Model)

class AutoService:
    def __init__(self, model: type[ModelType]):
        self.model = model