from functools import wraps

from fastapi import Request


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
