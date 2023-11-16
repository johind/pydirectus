import time
from typing import Optional

from .exceptions import DirectusException
from .rest_adapter import Result


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


def handle_directus_response(result: Result):
    if not result.success:
        raise DirectusException(result.data["errors"])

    return result.data["data"]
