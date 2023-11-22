import json
import logging
from typing import Optional

from .auth import DirectusAuth
from .models import File, Item, Query
from .rest_adapter import RestAdapter
from .utils import handle_directus_response, list_to_string


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
        query: Query = None,
    ) -> list[Item]:
        """
        GET Items from Collection
        :param collection: a string representing the collection name
        :param query: a dictionary specifying the query parameters for filtering, searching, sorting, etc.
          - fields: A list of fields that are returned.
          - filter: Search items in a collection that match the filter.
          - search: Perform a search on all string and text type fields within a collection.
          - sort: What field(s) to sort by. Sorting defaults to ascending.
          - limit: Set the maximum number of items that will be returned.
          - offset: Skip the first n items in the response.
          - page: Specify the page number when paginating results.
          - deep: Set any of the other query parameters on a nested relational dataset.
          - alias: Rename fields and request the same nested data set multiple times using different filters

        :return: List[Item] - A list of items retrieved from the collection.
        """
        endpoint = f"/items/{collection}"
        response = self._rest_adapter.get(endpoint, params=query)

        return handle_directus_response(response)

    def read_item(self, collection: str, item_id: str, query: Query = None) -> Item:
        """
        GET Item from Collection by ID
        :param collection: a string representing the collection name
        :param item_id: a string representing the item ID
        :param query:
          - fields: A list of fields that are returned.

        :return: item as dict
        """

        endpoint = f"/items/{collection}/{item_id}"
        response = self._rest_adapter.get(endpoint, params=query)

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
        query: Query = None,
    ) -> list[File]:
        """
        GET Files
        :param query: a dictionary specifying the query parameters for filtering, searching, sorting, etc.
          - fields: A list of fields that are returned.
          - filter: Search items in a collection that match the filter.
          - search: Perform a search on all string and text type fields within a collection.
          - sort: What field(s) to sort by. Sorting defaults to ascending.
          - limit: Set the maximum number of items that will be returned.
          - offset: Skip the first n items in the response.
          - page: Specify the page number when paginating results.
          - deep: Set any of the other query parameters on a nested relational dataset.
          - alias: Rename fields and request the same nested data set multiple times using different filters

        :return: list of dict
        """
        endpoint = "/files"
        response = self._rest_adapter.get(endpoint, params=query)

        return handle_directus_response(response)

    def read_file(self, file_id: str, query: Query = None) -> File:
        """
        GET File by ID
        :param file_id: a string representing the file ID
        :param query:
          - fields: A list of fields that are returned.

        :return: file as dict
        """
        endpoint = f"/files/{file_id}"
        response = self._rest_adapter.get(endpoint, params=query)

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
