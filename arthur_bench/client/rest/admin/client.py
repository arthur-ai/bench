import requests
from typing import Dict, Tuple, cast
from http import HTTPStatus
from requests.cookies import RequestsCookieJar

# import http client
from arthur_bench.client.http.requests import HTTPClient

from arthur_bench.client.rest.admin.models import (
    LoginRequest,
    AuthenticationInfo,
    UserResponse,
    User,
)


PATH_PREFIX = "/api/v3"


class ArthurAdminClient:
    """
    A Python client to interact with the Arthur Admin API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurAdminClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to
        use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def login(self, json_body: LoginRequest) -> Tuple[User, RequestsCookieJar]:
        """
        If the login attempt is successful, the user will be returned in the response
        body and an HttpOnly, set-cookie \"Authorization\" header will be returned
        that contains a JWT to be used in subsequent requests to the API in either
        the \"Authorization\" or cookie header

        :param json_body:
        """

        raw_resp = cast(
            requests.Response,
            self.http_client.post(
                "/login",
                json=json_body.dict(),
                validation_response_code=HTTPStatus.OK,
                return_raw_response=True,
            ),
        )
        return User(**raw_resp.json()), raw_resp.cookies

    def get_current_user(self) -> UserResponse:
        """
        Returns the currently authenticated user

        """

        parsed_resp = cast(
            Dict,
            self.http_client.get("/users/me", validation_response_code=HTTPStatus.OK),
        )
        return UserResponse(**parsed_resp)

    def authenticate(self) -> AuthenticationInfo:
        """
        Returns authentication info for the calling, token-bearing user

        """

        parsed_resp = cast(
            Dict,
            self.http_client.get(
                "/users/me/auth_info", validation_response_code=HTTPStatus.OK
            ),
        )
        return AuthenticationInfo(**parsed_resp)
