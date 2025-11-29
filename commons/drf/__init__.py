__all__ = [
    "ListModelMixin",
    "RetrieveModelMixin",
    'CreateModelMixin',
    'UpdateModelMixin',
    'PartialUpdateModelMixin',
    'DestroyModelMixin',
    'DestroyManyModelMixin',
    'GenericViewSet'
    'CustomViewSet',
    'api_meta'
]
from .decorator import api_meta
from .generics import GenericViewSet
from .mixins import (
                                ListModelMixin,
                                RetrieveModelMixin,
                                CreateModelMixin,
                                UpdateModelMixin,
                                PartialUpdateModelMixin,
                                DestroyModelMixin,
                                DestroyManyModelMixin
                            )

class CustomViewSet(
                    ListModelMixin,
                    RetrieveModelMixin,
                    CreateModelMixin,
                    UpdateModelMixin,
                    PartialUpdateModelMixin,
                    DestroyModelMixin,
                    DestroyManyModelMixin,):
    pass