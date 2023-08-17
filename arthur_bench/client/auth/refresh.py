from base64 import b64encode, b64decode
from datetime import datetime, timedelta
from typing import Dict, Tuple

import jwt
import pytz

from arthur_bench.client.auth.helpers import user_login


class AuthRefresher:
    AUTH_KEY = "Authorization"
    ALGORITHMS = ["HS256"]
    MINS_BEFORE_EXPIRY_TO_REFRESH = 5

    def __init__(self, url: str, login: str, password: str, verify_ssl: bool):
        self._url = url
        self._login = login
        # encode password to obfuscate a bit
        self._password_encoded = b64encode(password.encode())
        self._verify_ssl = verify_ssl

    @staticmethod
    def _get_refresh_wait_time(current_token: str) -> timedelta:
        """
        Given a JWT token with an 'exp' field, return how long to wait before refreshing
          the token
        :param current_token: the current token being used, containing an 'exp' field
        :return: the amount of time to wait before fetching a new token
        """
        # see when the token expires
        token_decoded = jwt.decode(
            current_token,
            algorithms=AuthRefresher.ALGORITHMS,
            options={"verify_signature": False},
        )
        expiry = datetime.fromtimestamp(token_decoded["exp"], tz=pytz.UTC)
        cur_time = datetime.now(tz=pytz.UTC)

        time_to_briefly_before_expiry = (
            expiry - timedelta(minutes=AuthRefresher.MINS_BEFORE_EXPIRY_TO_REFRESH)
        ) - cur_time
        # ensure time isn't negative
        if time_to_briefly_before_expiry < timedelta():
            return timedelta()
        else:
            return time_to_briefly_before_expiry

    def refresh(self) -> Tuple[Dict[str, str], timedelta]:
        """
        Authorization header update function for an HTTPClient

        Fetches a new session token and returns the new token, and how long to wait
        before refreshing it (by calling this method again)
        :return: Headers to update (Authorization), and time to wait before refreshing
            again
        """
        password = b64decode(self._password_encoded).decode()
        auth_token = user_login(
            api_http_host=self._url,
            login=self._login,
            password=password,
            verify_ssl=self._verify_ssl,
        )
        next_refresh_wait_time = self._get_refresh_wait_time(auth_token)
        return {self.AUTH_KEY: auth_token}, next_refresh_wait_time
