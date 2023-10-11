import logging
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Optional, Union

import requests

from .auth import DirectusAuth
from .exceptions import DirectusException


# TODO Dataclass needed? Maybe change to #1
# Maybe let this be a Typed Dict and change it
# to Item/File Typed Dict in Directus API wrapper
@dataclass
class Result:
    success: bool
    status_code: int
    message: str
    data: Optional[Union[list[dict], dict]] = None


class RestAdapter:
    def __init__(
        self,
        hostname: str,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        ssl_verify: bool = False,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.url = hostname
        self._api_key = api_key
        self._username = username
        self._password = password
        self._ssl_verify = ssl_verify

        self._logger = logger or logging.getLogger(__name__)
        self._auth = DirectusAuth(
            hostname=self.url,
            static_token=self._api_key,
            username=self._username,
            password=self._password,
        )

        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

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
        request_url = f"http://{self.url}{endpoint}"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json;charset=UTF-8",
        }

        try:
            log_line = f"method={http_method}, url={request_url}, params={params}"
            self._logger.debug(msg=log_line)
            response = requests.request(
                method=http_method,
                url=request_url,
                verify=self._ssl_verify,
                params=params,
                headers=headers,
                auth=self._auth,
                json=data,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise DirectusException(str(e))

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
