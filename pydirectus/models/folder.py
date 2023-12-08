from __future__ import annotations
from typing import TypedDict


class Folder(TypedDict):
    # Primary key of the folder.
    id: str
    # Name of the folder.
    name: str
    # Parent folder. Many-to-one to folders (recursive).
    parent: str | Folder | None  # TODO gibt es none oder ist es dann string??
