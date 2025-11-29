import os
import sys

from conf import settings

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "application"))

TORTOISE_ORM = settings.TORTOISE_ORM