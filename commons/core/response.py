from typing import Any, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class AutoResponse(JSONResponse):
    """
    通用响应类：
    - 成功返回: AutoResponse(data=..., message=..., code=200)
    - 分页返回: AutoResponse(data=..., total=..., page=..., page_size=...)
    - 失败返回: AutoResponse(data=..., code=400, status='error', message=...)
    """
    def __init__(
        self,
        data: Any = None,
        code: int = 200,
        status: str = "success",
        message: Optional[str] = None,
        total: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs,
    ):
        # 确保 Pydantic 或 datetime 可被序列化
        data = jsonable_encoder(data)

        content = {"code": code, "status": status, "data": data}

        # 如果传入分页参数就加入
        if total is not None:
            content["total"] = total
        if page is not None:
            content["page"] = page
        if page_size is not None:
            content["page_size"] = page_size

        content.update(kwargs)
        super().__init__(content=content, status_code=code)


