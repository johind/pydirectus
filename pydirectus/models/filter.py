from typing import TypedDict


# Implementation based on https://github.com/directus/directus/blob/main/packages/types/src/filter.ts


class FieldFilterOperator(TypedDict):
    _eq: str | int | bool | None
    _neq: str | int | bool | None
    _lt: str | int | None
    _lte: str | int | None
    _gt: str | int | None
    _gte: str | int | None
    _in: list[str | int] | None
    _nin: list[str | int] | None
    _null: bool | None
    _nnull: bool | None
    _contains: str | None
    _ncontains: str | None
    _icontains: str | None
    _starts_with: str | None
    _nstarts_with: str | None
    _istarts_with: str | None
    _nistarts_with: str | None
    _ends_with: str | None
    _nends_with: str | None
    _iends_with: str | None
    _niends_with: str | None
    _between: list[str | int] | None
    _nbetween: list[str | int] | None
    _empty: bool | None
    _nempty: bool | None
    _intersects: str | None
    _nintersects: str | None
    _intersects_bbox: str | None
    _nintersects_bbox: str | None


class FieldValidationOperator(TypedDict):
    _submitted: bool | None
    _regex: str | None


FieldFilter = dict[str, "FieldFilterOperator | FieldValidationOperator | FieldFilter"]


class LogicalFilterOR(TypedDict):
    _or: list["LogicalFilter | FieldFilter"]


class LogicalFilterAND(TypedDict):
    _and: list["LogicalFilter | FieldFilter"]


LogicalFilter = LogicalFilterOR | LogicalFilterAND


Filter = LogicalFilter | FieldFilter
