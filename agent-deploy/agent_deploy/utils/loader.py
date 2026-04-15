import importlib
import sys
from pathlib import Path
from typing import Any

def import_from_string(import_str: str) -> Any:
    """
    Imports an object from a string format "module.submodule:obj_name"
    Adds the current directory to sys.path to ensure local modules are found.
    """
    if "." not in sys.path:
        sys.path.insert(0, str(Path(".").absolute()))

    if ":" not in import_str:
        raise ValueError(f"Invalid entrypoint format: {import_str}. Expected 'module:object'")

    module_str, obj_name = import_str.split(":", 1)
    
    try:
        module = importlib.import_module(module_str)
        return getattr(module, obj_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Could not import {obj_name} from {module_str}: {e}")
