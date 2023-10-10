import time
from typing import Optional


def list_to_string(s: Optional[list[str]]) -> Optional[str]:
    """ 
    Convert a list of strings to one string.

    """
    return ",".join(s) if s else None


def current_time_in_ms():
    """ 
    Calculate current time in milliseconds.

    """
    return time.time() * 1000
