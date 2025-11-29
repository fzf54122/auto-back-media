__all__ = [
    'MediaUserSchemas',
    'MediaUserCreateSchemas',
    'MediaUserUpdateSchemas',
    'TaskManageSchemas',
    'TaskManageCreateSchemas',
    'TaskManageUpdateSchemas',
    'WebSchemas',
    'WebCreateSchemas',
    'WebUpdateSchemas'
]

from .MediaUserSchemas import (MediaUserSchemas,
                               MediaUserCreateSchemas,
                               MediaUserUpdateSchemas)
from .TaskManageSchemas import (TaskManageSchemas,
                               TaskManageCreateSchemas,
                               TaskManageUpdateSchemas)
from .WebSchemas import (WebSchemas,
                         WebCreateSchemas,
                         WebUpdateSchemas)