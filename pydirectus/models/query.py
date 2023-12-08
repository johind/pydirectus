from __future__ import annotations

from typing import TypedDict

from .filter import Filter


# Implementation based on https://github.com/directus/directus/blob/main/packages/types/src/query.ts


class Query(TypedDict):
    fields: list[str] | None
    filter: Filter | None
    search: str | None
    sort: list[str] | None
    limit: int | None
    offset: int | None
    page: int | None
    deep: NestedDeepQuery | None
    alias: dict | None


class DeepQuery(TypedDict):
    _fields: list[str] | None
    _sort: list[str] | None
    _filter: Filter | None
    _limit: int | None
    _offset: int | None
    _page: int | None
    _search: int | None
    # _group: list[str] | None
    # _aggregate: any | None


# Python 3.12: type NestedDeepQuery = dict[str, DeepQuery | "NestedDeepQuery"]
NestedDeepQuery = dict[str, "DeepQuery | NestedDeepQuery"]
