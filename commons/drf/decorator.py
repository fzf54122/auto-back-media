from fastapi import Request


def api_meta(summary: str = None, description: str = None,
             tags: list = None, responses: dict = None):
    def decorator(func):
        if summary:
            setattr(func, "_summary", summary)
        if description:
            setattr(func, "_description", description)
        if tags:
            setattr(func, "_tags", tags)
        if responses:
            setattr(func, "_responses", responses)
        return func
    return decorator

def wrap_endpoint(endpoint):
    async def wrapper(*args, request: Request, **kwargs):
        return await endpoint(*args, request=request, **kwargs)
    return wrapper
