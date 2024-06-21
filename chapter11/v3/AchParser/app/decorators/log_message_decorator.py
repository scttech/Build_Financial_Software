from fastapi import Request
from functools import wraps


def log_message(message: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request", None)
            if request:
                request.state.log_message = message
            return await func(*args, **kwargs)

        return wrapper

    return decorator
