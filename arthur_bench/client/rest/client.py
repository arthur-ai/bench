import logging
import os
from distutils.util import strtobool
from getpass import getpass
from platform import system
from typing import Optional


from arthur_bench.client.auth.helpers import get_current_org, user_login
from arthur_bench.client.auth.refresh import AuthRefresher
from arthur_bench.client.http.requests import HTTPClient
from arthur_bench.exceptions import MissingParameterError, UserValueError

# import sub-clients
from arthur_bench.client.rest.admin.client import ArthurAdminClient
from arthur_bench.client.rest.bench.client import ArthurBenchClient

# end import sub-clients

from arthur_bench.version import __version__

UNKNOWN_ORG_ID = "unknown-org"
ORG_ID_HEADER = "Arthur-Organization-ID"


logger = logging.getLogger(__name__)


class ArthurClient:
    def __init__(
        self,
        url: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
        organization_id: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        allow_insecure: bool = False,
        offline: bool = False,
    ):
        """
        REST client for logging and fetching data stored in the Arthur platform
        """
        # basic values
        if url is None:
            url = os.getenv("ARTHUR_API_URL")
        if url is None:
            raise MissingParameterError(
                "You must provide a URL through the 'url' parameter or the "
                "ARTHUR_API_URL environment variable"
            )
        if verify_ssl is None:  # if not provided
            # read from env var, or default to True if not present
            try:
                verify_ssl = bool(strtobool(os.getenv("ARTHUR_VERIFY_SSL", "true")))
            except ValueError:
                raise UserValueError(
                    f"ARTHUR_VERIFY_SSL environment variable must be a boolean value, "
                    f"got {os.getenv('ARTHUR_VERIFY_SSL')}"
                )

        # authorization
        if login is None:
            login = os.getenv("ARTHUR_LOGIN")
        if password is None:
            password = os.getenv("ARTHUR_PASSWORD")
        if api_key is None and login is None:
            api_key = os.getenv("ARTHUR_API_KEY")
        # validate only login or api key
        if login is not None and api_key is not None:
            raise UserValueError(
                "You may not provide both a login and api key, please ensure you are "
                "supplying only one through the login/api_key parameters and "
                "ARTHUR_LOGIN/ARTHUR_API_KEY environment "
                "variables"
            )
        if login is not None:  # login if provided
            # if password not supplied, get it from input
            if password is None:
                password = getpass(f"Please enter password for {login}: ")

            # Get session token from login and password
            auth_token = user_login(
                api_http_host=url, login=login, password=password, verify_ssl=verify_ssl
            )
            # create an auth refresher
            auth_refresher = AuthRefresher(
                url=url, login=login, password=password, verify_ssl=verify_ssl
            )
            header_refresh_func = auth_refresher.refresh
        elif api_key is not None:  # if api key provided, set that
            auth_token = api_key
            header_refresh_func = None
        else:
            raise MissingParameterError(
                "No authentication provided. Please supply a login (username or email) "
                "through the 'login' parameter or ARTHUR_LOGIN environment variable."
                "\n\n If this is a production environment, alternatively consider "
                "providing an API key through the 'api_key' parameter or ARTHUR_API_KEY"
                "environment variable."
            )

        # org id
        if offline:
            if organization_id is not None:
                raise UserValueError(
                    "You cannot specify an organization ID if you are offline."
                )
            else:
                organization_id = UNKNOWN_ORG_ID
        else:  # if online
            # fill org ID with environment variable if not provided
            if organization_id is None:
                organization_id = os.getenv("ARTHUR_ORGANIZATION_ID")
            # if still no org ID, fetch it from the API
            if organization_id is None:
                organization_id = get_current_org(
                    url, auth_token, verify_ssl=verify_ssl
                )

        # TODO: consider having the SDK override this?
        user_agent = f"arthur-client/{__version__} (system={system()})"
        headers = {
            "Accept": "application/json",
            "Authorization": auth_token,
            "User-Agent": user_agent,
            ORG_ID_HEADER: organization_id,
        }

        # setup http client construction arguments
        client_kwargs = {
            "base_url": url,
            "default_headers": headers,
            "verify_ssl": verify_ssl,
            "allow_insecure": allow_insecure,
            "header_refresh_func": header_refresh_func,
        }

        client = HTTPClient(**client_kwargs)  # type: ignore
        # create client object for each client subcomponent
        self.admin = ArthurAdminClient(client)
        self.bench = ArthurBenchClient(client)
        # end client object creation
