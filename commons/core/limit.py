import os 

from slowapi import Limiter
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)
def apply_rate_limit(rate="5/minute"):
    """根据环境应用限流装饰器"""

    def decorator(func):

        if os.getenv("TESTING", "false").lower() == "true":
            return func  # 测试环境不应用限流
        return limiter.limit(rate)(func)

    return decorator