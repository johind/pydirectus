import json
import logging
from typing import Optional

from .models import Item, File

from .rest_adapter import RestAdapter, Result
from .utils import list_to_string


# handle_directus_result() ?
def handle_result(result: Result):
    if not result.success:
        return result.data["errors"]

    return result.data["data"]


class Directus:
    def __init__(
        self,
        hostname: str,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        ssl_verify: bool = False,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._rest_adapter = RestAdapter(
            hostname=hostname,
            api_key=api_key,
            username=username,
            password=password,
            ssl_verify=ssl_verify,
            logger=logger,
        )

    def get_items(
        self,
        collection: str,
        fields: list[str] = None,
        filter: dict = None,
        search: str = None,
        sort: list[str] = None,
        limit: int = -1,
        offset: int = None,
    ) -> list[Item]:
        """
        GET Items from Collection
        :param collection: a string representing the collection name
        :param fields: a list of fields that are returned in the current dataset
        :param filter: search items in a collection that match the filter
        :param search: perform a search on all string and text type fields within a collection
        :param sort: what field(s) to sort by. sorting defaults to ascending
        :param limit: set the maximum number of items that will be returned
        :param offset: skip the first n items in the response

        :return: list of dict
        """
        params = {
            "fields": list_to_string(fields),
            "filter": json.dumps(filter),
            "search": search,
            "sort": list_to_string(sort),
            "limit": limit,
            "offset": offset,
        }

        # TODO so oder wie zuvor?
        endpoint = f"/items/{collection}"
        result = self._rest_adapter.get(endpoint, params=params)

        return handle_result(result)

    def get_item_by_ID(
        self, collection: str, item_id: str, fields: list[str] = None
    ) -> dict:
        """
        GET Item from Collection by ID
        :param collection: a string representing the collection name
        :param item_id: a string representing the item ID
        :param fields: list of fields that are returned in the current dataset

        :return: item as dict
        """
        params = {"fields": fields}

        result = self._rest_adapter.get(
            endpoint=f"/items/{collection}/{item_id}", params=params
        )

        if not result.success:
            return result.data["errors"]

        return result.data["data"]

    def create_item(self, collection: str, data: dict) -> dict:
        """
        POST Item to Collection
        :param collection: a string representing the collection name
        :param data: item data as dict

        :return: created item as dict, if successful
        """
        result = self._rest_adapter.post(endpoint=f"/items/{collection}", data=data)

        if not result.success:
            return result.data["errors"]

        return result.data["data"]

    def update_item(self, collection: str, item_id: str, data: dict) -> dict:
        """
        PATCH Item in Collection
        :param collection: a string representing the collection name
        :param item_id: a string representing the item ID
        :param data: item data as dict

        :return: updated item as dict, if successful
        """
        result = self._rest_adapter.patch(
            endpoint=f"/items/{collection}/{item_id}", data=data
        )

        if not result.success:
            return result.data["errors"]

        return result.data["data"]

    def delete_item(self, collection: str, item_id: str):
        """
        DELETE Item in Collection
        :param collection: a string representing the collection name
        :param item_id: a string representing the item ID

        :return: a dict stating success
        """
        result = self._rest_adapter.delete(endpoint=f"/items/{collection}/{item_id}")

        if not result.success:
            return result.data["errors"]

        # TODO unsure of this solution, may get changed
        return {"success": result.success}

    def get_files(
        self,
        fields: list[str] = None,
        filter: dict = None,
        search: str = None,
        sort: list[str] = None,
        limit: int = -1,
        offset: int = None,
    ) -> list[File]:
        """
        GET Files
        :param fields: a list of fields that are returned in the current dataset
        :param filter: search files in a collection that match the filter
        :param search: perform a search on all string and text type fields within files
        :param sort: what field(s) to sort by. sorting defaults to ascending
        :param limit: set the maximum number of files that will be returned
        :param offset: skip the first n files in the response

        :return: list of dict
        """
        params = {
            "fields": list_to_string(fields),
            "filter": json.dumps(filter),
            "search": search,
            "sort": list_to_string(sort),
            "limit": limit,
            "offset": offset,
        }

        result = self._rest_adapter.get(endpoint=f"/files", params=params)

        if not result.success:
            return result.data["errors"]

        return result.data["data"]

    def get_file_by_ID(self, file_id: str, fields: list[str] = None) -> File:
        """
        GET File by ID
        :param file_id: a string representing the file ID
        :param fields: list of fields that are returned in the current dataset

        :return: file as dict
        """
        params = {"fields": fields}

        result = self._rest_adapter.get(endpoint=f"/files/{file_id}", params=params)

        if not result.success:
            return result.data["errors"]

        return result.data["data"]

    def create_file(self, data: dict) -> dict:
        """
        POST File
        :param data: file data as dict

        :return: created file as dict, if successful
        """
        result = self._rest_adapter.post(endpoint=f"/files", data=data)

        if not result.success:
            return result.data["errors"]

        return result.data["data"]

    def update_file(self, file_id: str, data: dict) -> dict:
        """
        PATCH File
        :param file_id: a string representing the file ID
        :param data: file data as dict

        :return: updated file as dict, if successful
        """
        result = self._rest_adapter.patch(endpoint=f"/files/{file_id}", data=data)

        if not result.success:
            return result.data["errors"]

        return result.data["data"]

    def delete_file(self, file_id: str) -> dict:
        """
        DELETE File
        :param file_id: a string representing the file ID

        :return: a dict stating success
        """
        result = self._rest_adapter.delete(endpoint=f"/files/{file_id}")

        if not result.success:
            return result.data["errors"]
        # TODO unsure of this solution, may get changed
        return {"success": result.success}
