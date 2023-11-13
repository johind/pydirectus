import json
import logging
from typing import Optional

from .auth import DirectusAuth
from .exceptions import DirectusException
from .models import File, Item
from .rest_adapter import RestAdapter, Result
from .utils import list_to_string


def handle_directus_response(result: Result):
    if not result.success:
        raise DirectusException(result.data["errors"])

    return result.data["data"]


class DirectusClient:
    def __init__(
        self,
        hostname: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        static_token: Optional[str] = None,
        ssl_verify: bool = False,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.auth_handler = DirectusAuth(
            hostname=hostname,
            static_token=static_token,
            username=username,
            password=password,
        )
        self._rest_adapter = RestAdapter(
            hostname=hostname,
            auth_handler=self.auth_handler,
            ssl_verify=ssl_verify,
            logger=logger,
        )

    def read_items(
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
            "filter": json.dumps(filter) if filter else {},
            "search": search,
            "sort": list_to_string(sort),
            "limit": limit,
            "offset": offset,
        }

        endpoint = f"/items/{collection}"
        response = self._rest_adapter.get(endpoint, params=params)

        return handle_directus_response(response)

    def read_item(
        self, collection: str, item_id: str, fields: list[str] = None
    ) -> Item:
        """
        GET Item from Collection by ID
        :param collection: a string representing the collection name
        :param item_id: a string representing the item ID
        :param fields: list of fields that are returned in the current dataset

        :return: item as dict
        """
        params = {"fields": fields}

        endpoint = f"/items/{collection}/{item_id}"
        response = self._rest_adapter.get(endpoint, params=params)

        return handle_directus_response(response)

    def create_item(self, collection: str, data: dict) -> Item:
        """
        POST Item to Collection
        :param collection: a string representing the collection name
        :param data: item data as dict

        :return: created item as dict, if successful
        """

        endpoint = f"/items/{collection}"
        response = self._rest_adapter.post(endpoint, data=data)

        return handle_directus_response(response)

    def update_item(self, collection: str, item_id: str, data: dict) -> Item:
        """
        PATCH Item in Collection
        :param collection: a string representing the collection name
        :param item_id: a string representing the item ID
        :param data: item data as dict

        :return: updated item as dict, if successful
        """
        endpoint = f"/items/{collection}/{item_id}"
        response = self._rest_adapter.patch(endpoint, data=data)

        return handle_directus_response(response)

    def delete_item(self, collection: str, item_id: str) -> None:
        """
        DELETE Item in Collection
        :param collection: a string representing the collection name
        :param item_id: a string representing the item ID

        :return: None
        """
        endpoint = f"/items/{collection}/{item_id}"
        response = self._rest_adapter.delete(endpoint)

    def read_files(
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

        endpoint = "/files"
        response = self._rest_adapter.get(endpoint, params=params)

        return handle_directus_response(response)

    def read_file(self, file_id: str, fields: list[str] = None) -> File:
        """
        GET File by ID
        :param file_id: a string representing the file ID
        :param fields: list of fields that are returned in the current dataset

        :return: file as dict
        """
        params = {"fields": fields}

        endpoint = f"/files/{file_id}"
        response = self._rest_adapter.get(endpoint, params=params)

        return handle_directus_response(response)

    def create_file(self, data: dict) -> File:
        """
        POST File
        :param data: file data as dict

        :return: created file as dict, if successful
        """
        endpoint = "/files"
        response = self._rest_adapter.post(endpoint, data=data)

        return handle_directus_response(response)

    def update_file(self, file_id: str, data: dict) -> File:
        """
        PATCH File
        :param file_id: a string representing the file ID
        :param data: file data as dict

        :return: updated file as dict, if successful
        """
        endpoint = f"/files/{file_id}"
        response = self._rest_adapter.patch(endpoint, data=data)

        return handle_directus_response(response)

    def delete_file(self, file_id: str) -> None:
        """
        DELETE File
        :param file_id: a string representing the file ID

        :return: None
        """
        endpoint = f"/files/{file_id}"
        response = self._rest_adapter.delete(endpoint)
