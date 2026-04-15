import functools
from typing import Callable, Any, Dict, Optional

def agent(name: str, version: str = "0.1.0"):
    """
    Decorator to mark a function as an agent-deploy entrypoint.
    """
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Attach metadata for detection
        wrapper._adeploy_agent = True
        wrapper._adeploy_name = name
        wrapper._adeploy_version = version
        return wrapper
    return decorator
