from functools import wraps
from typing import Callable, Any

from .client import make_request
from .exceptions import SoteriaValidationError

def guard_prompt(guard_name: str, prompt_arg: str) -> Callable:
    """
    Decorator factory to apply a remote Guard to a function's argument.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            prompt = kwargs.get(prompt_arg)
            if prompt is None:
                raise ValueError(f"Argument '{prompt_arg}' not found in function call.")
            
            outcome = make_request(prompt=prompt, guard_name=guard_name, metadata={})
            
            if not outcome.get("is_valid"):
                raise SoteriaValidationError(
                    f"Input prompt was blocked by Guard '{guard_name}'. "
                    f"Summary: {outcome.get('validation_summaries')}"
                )
            
            # Replace the original prompt with the processed one
            kwargs[prompt_arg] = outcome.get("processed_prompt")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator