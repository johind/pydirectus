from typing import Optional

import requests

from .exceptions import DirectusAuthException
from .utils import current_time_in_ms


class DirectusAuth(requests.auth.AuthBase):
    def __init__(
        self,
        hostname: str,
        static_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.hostname = hostname
        self.static_token = static_token
        self.username = username
        self.password = password

        if not (self.username and self.password) and not self.static_token:
            raise DirectusAuthException(
                "No static_token or username and password have been provided!"
            )

        # temporary access token to be used in follow-up requests.
        self.access_token = None
        # token that can be used to retrieve a new access token.
        self.refresh_token = None
        # how long before the access token will expire (in ms).
        self.token_expires = None
        # timestamp of last token request (in ms).
        self.token_timestamp = None

    def _get_access_token(self, auth_type: str) -> None:
        request_url = f"http://{self.hostname}/auth/{auth_type}"

        match auth_type:
            case "login":
                data = {"email": self.username, "password": self.password}
            case "refresh":
                data = {"refresh_token": self.refresh_token}
            case _:
                raise ValueError("Parameter auth_type must be set to either 'login' or 'refresh'!")

        response = requests.request(method="POST", url=request_url, json=data)

        out_data = response.json()

        if "errors" in out_data:
            raise DirectusAuthException(out_data["errors"])

        self.access_token = out_data["data"]["access_token"]
        self.refresh_token = out_data["data"]["refresh_token"]
        self.token_expires = out_data["data"]["expires"]

    def __call__(self, r: requests.Request):
        if self.static_token:
            bearer_token = self.static_token
        elif self.access_token:
            current_time = current_time_in_ms()
            if current_time >= self.token_timestamp + self.token_expires:
                self._get_access_token(auth_type="refresh")
                self.token_timestamp = current_time_in_ms()
            bearer_token = self.access_token
        else:
            self._get_access_token(auth_type="login")
            self.token_timestamp = current_time_in_ms()
            bearer_token = self.access_token

        r.headers["Authorization"] = f"Bearer {bearer_token}"

        return r
