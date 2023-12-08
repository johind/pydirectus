import logging
from json import JSONDecodeError, dumps
from typing import Any, Optional

import requests

from .exceptions import DirectusException


class Result:
    def __init__(
        self,
        success: bool,
        status_code: int,
        message: str = "",
        data: list[dict] | dict = None,
    ):
        """
        Result returned from low-level RestAdapter
        :param success: True if HTTP Request was successful, False if not
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.success = bool(success)
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data


class RestAdapter:
    def __init__(
        self,
        hostname: str,
        auth_handler: Any = None,
        ssl_verify: bool = False,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._url = hostname
        self._auth = auth_handler

        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)

        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def _serialize_nested_params(self, params: dict) -> dict:
        """
        Serialize nested params for correct query

        """
        for key, value in params.items():
            if isinstance(value, dict):
                params[key] = dumps(value)

        return params

    def _do(
        self,
        http_method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Result:
        """
        Private method for GET, POST, PATCH, DELETE methods
        :param http_method: Any str representing the HTTP Method ('GET', 'POST', etc.)
        :param endpoint: A str representing the endpoint after the base URL
        :param params: A dict of Endpoint Parameters
        :param data: A dict of data sent in the body
        :return: Result object
        """
        request_url = f"{self._url}{endpoint}"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json;charset=UTF-8",
        }
        serialized_params = self._serialize_nested_params(params) if params else None

        try:
            log_line = f"method={http_method}, url={request_url}, params={params}"
            self._logger.debug(msg=log_line)
            response = requests.request(
                method=http_method,
                url=request_url,
                verify=self._ssl_verify,
                params=serialized_params,
                headers=headers,
                auth=self._auth,
                json=data,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise DirectusException(str(e)) from e

        # on delete return data is empty. handle this case here
        if response.status_code == 204:
            data_out = None
        else:
            # Deserialize JSON output to Python object, or return failed Result on exception
            try:
                data_out = response.json()
            except (ValueError, JSONDecodeError) as e:
                log_line = (
                    f"success=False, status_code={response.status_code}, message={e}"
                )
                self._logger.warning(msg=log_line)

                return Result(False, response.status_code, message=str(e))

        is_success = 299 >= response.status_code >= 200
        log_line = f"success={is_success}, status_code={response.status_code}, message={response.reason}"
        self._logger.debug(msg=log_line)

        return Result(
            is_success,
            response.status_code,
            message=response.reason,
            data=data_out,
        )

    def get(self, endpoint: str, params: Optional[dict] = None) -> Result:
        """
        GET method for Directus
        :param endpoint: A str representing the endpoint after the base URL
        :param params: A dict of Endpoint Parameters
        :return: Result object
        """
        return self._do(http_method="GET", endpoint=endpoint, params=params)

    def post(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Result:
        """
        POST method for Directus
        :param endpoint: A str representing the endpoint after the base URL
        :param params: A dict of Endpoint Parameters
        :param data: A dict of data sent in the body
        :return: Result object
        """
        return self._do(http_method="POST", endpoint=endpoint, params=params, data=data)

    def patch(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Result:
        """
        PATCH method for Directus
        :param endpoint: A str representing the endpoint after the base URL
        :param params: A dict of Endpoint Parameters
        :param data: A dict of data sent in the body
        :return: Result object
        """
        return self._do(
            http_method="PATCH", endpoint=endpoint, params=params, data=data
        )

    def delete(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Result:
        """
        DELETE method for Directus
        :param endpoint: A str representing the endpoint after the base URL
        :param params: A dict of Endpoint Parameters
        :param data: A dict of data sent in the body
        :return: Result object
        """
        return self._do(
            http_method="DELETE", endpoint=endpoint, params=params, data=data
        )
