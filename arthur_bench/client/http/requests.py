# flake8: noqa
import logging
import threading
from datetime import timedelta
from io import BytesIO
from time import sleep

import requests
from requests.exceptions import RequestException
from typing import Dict, List, Union, Optional, BinaryIO, Tuple, Any, Callable
import json as jsonlib
from urllib.parse import urlparse

from requests_toolbelt import MultipartEncoder

from arthur_bench.client.http.helper import construct_url
from arthur_bench.client.http import validation
from arthur_bench.exceptions import (
    InternalTypeError,
    ResponseServerError,
    ResponseRedirectError,
    ArthurInternalError,
    UserValueError,
)

logger = logging.getLogger(__name__)


def _parse_response(response: requests.Response) -> Union[Dict, List, bytes, BytesIO]:
    """Depending on the type of response from the server, parses the response and
    returns

    :param response: response from the REST call
    :return: parsed response
    """
    if response is None:
        return bytes()
    # return error codes as raw responses
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    if response.status_code >= 400:
        return response.content
    if response.request.headers.get("Accept") == "application/octet-stream":
        return BytesIO(response.content)
    # return the content if the return type is image/binary/csv
    if response.headers.get("Content-Type") in (
        "image/jpeg",
        "text/csv",
        "avro/binary",
        "parquet/binary",
    ):
        return response.content

    try:
        return response.json()
    except ValueError:
        return response.content


def _validate_base_url(base_url: str, allow_insecure=True) -> None:
    """
    Validate that a base URL does not contain any paths or query parameters
    :param base_url: the base URL to validate
    :param allow_insecure: flag for http urls
    :return: None
    :raises UserValueError: if the URL is invalid
    """
    # add scheme and initial validation from construct_url function
    parsed = urlparse(construct_url(base_url))

    # validate
    if parsed.scheme not in ("http", "https"):
        raise UserValueError(
            f"Base URL scheme '{parsed.scheme}' is invalid, should be 'http' or 'https'"
        )
    if parsed.scheme == "http" and not allow_insecure:
        raise UserValueError(
            "Must set allow_secure flag to be True in order to use an http url."
        )
    if parsed.path is not None and parsed.path not in ("", "/"):
        raise UserValueError(f"Base URL {base_url} should not contain a path")
    if parsed.query is not None and parsed.query != "":
        raise UserValueError(f"Base URL {base_url} should not contain query parameters")
    if parsed.params is not None and parsed.params != "":
        raise UserValueError(f"Base URL {base_url} should not contain a path parameter")
    if parsed.fragment is not None and parsed.fragment != "":
        raise UserValueError(f"Base URL {base_url} should not contain a fragment")


class HTTPClient:
    """
    A `requests`-based HTTP Client intended for interacting with JSON-based APIs.
    Supports response validation, retries, connection reuse, and multipart requests.
    """

    def __init__(
        self,
        base_url: str,
        path_prefix: Optional[str] = None,
        default_headers: Optional[Dict[str, str]] = None,
        verify_ssl: bool = True,
        timeout_sec: float = 300.0,
        allow_insecure: bool = True,
        header_refresh_func: Optional[
            Callable[[], Tuple[Dict[str, str], timedelta]]
        ] = None,
    ):
        """
        :param base_url:
        :param path_prefix:
        :param default_headers:
        :param verify_ssl:
        :param timeout_sec:
        :param allow_insecure:
        :param header_refresh_func: function to refresh headers, returning headers to
        update and time to wait before
            next refresh
        """
        self.session = requests.Session()
        if default_headers is not None:
            self.session.headers.update(default_headers)
        self.session.verify = verify_ssl
        self.timeout = timeout_sec

        # exponential backoff settings
        self.BACKOFF_CONSTANT = 0.1
        self.BACKOFF_EXPONENT_BASE = 1.5

        try:
            _validate_base_url(base_url, allow_insecure)
        except UserValueError as e:
            raise UserValueError(
                "Base URL is invalid, see nested exception for details. Base URL should "
                "not contain a "
                "/path or &query=parameters, a /path;parameter, or a #fragment"
            ) from e

        if path_prefix is None:
            self.api_base_url = construct_url(base_url, validate=True)
        else:
            self.api_base_url = construct_url(base_url, path_prefix, validate=True)

        self._header_refresh_func = header_refresh_func
        self._update_headers()

    def set_path_prefix(self, path_prefix: str) -> None:
        """
        Update the client's path prefix

        This update the path prefix which is prepended to 'endpoint' paths.
        """
        # get current url
        parsed_url = urlparse(self.api_base_url)

        # remove trailing slash from supplied path if present
        if path_prefix[-1] == "/":
            path_prefix = path_prefix[:-1]

        # if existing URL has a path, warn we're overriding it
        if parsed_url.path not in ("", "/") and parsed_url.path != path_prefix:
            logger.warning(
                f"Overriding existing client base URL path '{parsed_url.path}' with "
                "supplied '{path_prefix}"
            )

        # assign the path to the parsed URL and write that back to our base url
        parsed_url = parsed_url._replace(path=path_prefix)
        self.api_base_url = parsed_url.geturl()

    def _update_headers(self):
        if self._header_refresh_func is None:
            return

        # fetch updates and next refresh wait time
        header_updates, next_refresh_wait = self._header_refresh_func()
        # update headers
        self.session.headers.update(header_updates)

        # schedule next refresh
        thread = threading.Timer(
            next_refresh_wait.total_seconds(), self._update_headers
        )
        thread.daemon = True
        thread.start()

    def send(
        self,
        endpoint: str,
        method: str = "GET",
        json: Optional[Union[Dict, List, str, bytes]] = None,
        files: Optional[
            Union[Dict[str, BinaryIO], List[Tuple], Dict[str, Tuple]]
        ] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Union[Dict, bytes]] = None,
        return_raw_response: bool = False,
        retries: int = 0,
        validate_response_status: bool = True,
        validation_response_code: Optional[int] = None,
    ) -> Union[Dict, List, bytes, BytesIO, requests.Response]:
        """Send an HTTP request

        :param endpoint: the specific endpoint to append to the client URL
        :param method: the HTTP method to use
        :param headers: headers to use for this request in addition to the client
        d   efault headers
        :param json: data to send as JSON, either a string/bytes to send directly or a
            dictionary/list to serialize. if
            `files` is also supplied, this should be a map from name to content,
            to be sent along with the `files` as a multipart request
        :param files: a map from file names to file-like objects, to be sent as
            multipart/form-data
        :param params: query parameters to add to the request
        :param return_raw_response: if true, return the requests.Response object
            received; otherwise attempt to parse the response
        :param retries: number of times to retry the request on failure.
            uses exponential backoff
        :param validate_response_status: if True, raise an ArthurException if the status
            code is not 2XX or does not match `validation_response_code`
        :param validation_response_code: expected status code of the response to
            validate. if None, allow any 2XX
        :return: if return_raw_response is true, return the requests.Response object
            received; otherwise attempt to parse the response
        :raises ArthurUserError: failed due to user error
        :raises ArthurInternalError: failed due to an internal error
        """
        if headers is None:
            headers = {}

        # VALIDATION AND PREPROCESSING
        if retries < 0:
            raise UserValueError(f"retries must be greater than or equal to 0")
        if validation_response_code is None and retries > 0:
            logger.warning(
                f"retries was specified as {retries} but validation_response_code was "
                "not set, response "
                f"contents will not be evaluated."
            )
        # automatically add json content type headers and serialize json if `json` is
        # supplied but no (multipart) files are supplied
        multipart: bool = files is not None or (
            "Content-Type" in headers.keys()
            and headers["Content-Type"] == "multipart/form-data"
        )
        if json is not None and not multipart:
            logger.debug("serializing JSON and adding Content-Type header")
            # headers
            if "Content-Type" not in headers.keys():
                headers["Content-Type"] = "application/json"
            elif headers["Content-Type"] != "application/json":
                logger.debug(
                    f"Content-Type header is specified as {headers['Content-Type']}, "
                    "not overwriting"
                )
            # body
            if type(json) != str and type(json) != bytes:
                try:
                    json = jsonlib.dumps(json)
                except TypeError as e:
                    raise InternalTypeError("failed to serialize 'json' input") from e

        # multipart request preparation
        me: Optional[MultipartEncoder] = None
        if multipart:
            data: Dict[str, Any] = {}
            # if json will be sent as multipart clean it up
            if json is not None:
                if not isinstance(json, dict):
                    raise InternalTypeError(
                        f"Received 'json' parameter with a multipart request but was of "
                        f"type {type(json)} not dict."
                    )
                for field_name, field_value in json.items():
                    # validate key type
                    if not isinstance(field_name, str):
                        raise InternalTypeError(
                            f"both 'files' and 'json' were supplied but 'json' keys type"
                            f"is {type(field_name)} not str"
                        )
                    # serialize the values if needed
                    if isinstance(field_value, dict) or isinstance(field_value, list):
                        try:
                            field_value = jsonlib.dumps(field_value)
                        except TypeError as e:
                            raise InternalTypeError(
                                f"failed to serialize 'json' input for key '{field_name}'"
                            ) from e
                    # convert strings to BytesIO
                    if isinstance(field_value, str):
                        field_value = BytesIO(bytes(field_value, encoding="utf-8"))

                    # check that our final value is file-like
                    try:
                        field_value.seek(0)
                    except AttributeError as e:
                        raise InternalTypeError(
                            f"Received 'data' dict but could not convert field '{field_name}' "
                            f"of type '{type(json[field_name])}' to file-like object"
                        ) from e
                    # set value in our newly-built data
                    data[field_name] = field_value

            if files is not None:
                # if list, must be of tuples like ("fname", data, [encoding]) -- add to
                # data in dict format
                if isinstance(files, list):
                    for entry in files:
                        if not (
                            isinstance(entry, tuple)
                            and len(entry) >= 2
                            and isinstance(entry[0], str)
                        ):
                            raise InternalTypeError(
                                f"received list for files argument but did not contain "
                                f"tuples in the correct format, entry was of type "
                                f"{type(entry)}: {entry}"
                            )
                        data[entry[0]] = entry
                # if dict, ensure in tuple format like ("fname", data, [encoding]) or
                # reformat if not
                elif isinstance(files, dict):
                    for fname in files.keys():
                        file_obj = files[fname]
                        if isinstance(file_obj, tuple):
                            data[fname] = file_obj
                        elif hasattr(file_obj, "read"):
                            data[fname] = (fname, file_obj)
                        else:
                            raise InternalTypeError(
                                f"files['{fname}'] is of type {type(file_obj)}, not a"
                                f"tuple or file-like"
                            )
                else:
                    raise InternalTypeError(
                        f"received 'files' argument but was of type '{type(files)}; not "
                        "list or dict"
                    )

        url = construct_url(self.api_base_url, endpoint)

        # REQUEST SENDING AND RESPONSE PARSING
        resp: Optional[requests.Response] = None
        success = False
        error = None
        attempts = 0
        while not success and attempts <= retries:
            if attempts > 0:
                if resp is not None:
                    encoding = resp.encoding if resp.encoding is not None else "utf-8"
                    logger.debug(
                        f"Request failed with status {resp.status_code} auto retry {attempts}/{retries}:\n"
                        f"{resp.content.decode(encoding)}"
                    )
                wait_time = self.BACKOFF_CONSTANT * (
                    self.BACKOFF_EXPONENT_BASE**attempts
                )
                sleep(wait_time)
            try:
                if multipart:
                    logger.debug(
                        "Sending multipart request: %s %s\nHeaders: %s",
                        method,
                        url,
                        headers,
                    )
                    # create multipart encoder
                    #  note: it will re-seek to the beginning of all files so retries
                    # are safe we want to stream the multipart upload: i.e. send the
                    # data in sections read from disk, rather than
                    # loading it all into memory at once before starting the request.
                    # however the requests library can only stream data from file-like
                    # objects. we need something to properly construct the multipart
                    # request with its content boundaries and such
                    # (see https://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.2)
                    # and turn it into a file-like object. this is what the
                    # MultipartEncoder does.
                    me = MultipartEncoder(fields=data)
                    headers["Content-Type"] = me.content_type
                    resp = self.session.request(
                        method,
                        url,
                        params=params,
                        data=me,
                        headers=headers,
                        timeout=self.timeout,
                    )
                else:
                    logger.debug(
                        "Sending request: %s %s\nHeaders: %s\nData: %s",
                        method,
                        url,
                        headers,
                        json,
                    )
                    resp = self.session.request(
                        method,
                        url,
                        params=params,
                        headers=headers,
                        data=json,
                        timeout=self.timeout,
                    )
                if validate_response_status:
                    validation.validate_response_status(
                        resp, expected_status_code=validation_response_code
                    )
                success = True
            except (ResponseServerError, ResponseRedirectError, RequestException) as e:
                error = e
                logger.debug(e)

            attempts += 1

        if success and resp is not None:
            logger.debug(
                f"[{threading.current_thread().name}] Rest Call Response Time: "
                f"{resp.elapsed.total_seconds() * 1000} ms"
            )
            logger.debug(
                "Received response: %d %s\nHeaders: %s\nContent: %s",
                resp.status_code,
                resp.url,
                resp.headers,
                resp.content,
            )

        if not success:
            if error is None:
                # should never happen but just in case
                raise ArthurInternalError(f"failed to send request but error is None")
            raise error

        if resp is None:
            raise InternalTypeError("Response object was None")
        elif return_raw_response:
            return resp
        else:
            return _parse_response(resp)

    def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Union[Dict, bytes]] = None,
        return_raw_response: bool = False,
        retries: int = 0,
        validate_response_status: bool = True,
        validation_response_code: Optional[int] = None,
    ) -> Union[Dict, List, bytes, BytesIO, requests.Response]:
        """Send an HTTP GET request

        :param endpoint: the specific endpoint to append to the client URL
        :param headers: headers to use for this request in addition to the client
            default headers
        :param params: query parameters to add to the request
        :param return_raw_response: if true, return the requests.Response object
            received; otherwise attempt to parse the response
        :param retries: number of times to retry the request on failure.
            uses exponential backoff
        :param validate_response_status: if True, raise an ArthurException if the status
            code is not 2XX or does not match `validation_response_code`
        :param validation_response_code: expected status code of the response to
            validate. if None, allow any 2XX
        :return: if return_raw_response is true, return the requests.Response object
            received; otherwise attempt to parse the response
        :raises ArthurUserError: failed due to user error
        :raises ArthurInternalError: failed due to an internal error
        """
        return self.send(
            endpoint,
            method="GET",
            headers=headers,
            params=params,
            return_raw_response=return_raw_response,
            retries=retries,
            validate_response_status=validate_response_status,
            validation_response_code=validation_response_code,
        )

    def post(
        self,
        endpoint: str,
        json: Optional[Union[Dict, List, str, bytes]] = None,
        files: Optional[
            Union[Dict[str, BinaryIO], List[Tuple], Dict[str, Tuple]]
        ] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Union[Dict, bytes]] = None,
        return_raw_response: bool = False,
        retries: int = 0,
        validate_response_status: bool = True,
        validation_response_code: Optional[int] = None,
    ) -> Union[Dict, List, bytes, BytesIO, requests.Response]:
        """Send an HTTP POST request

        :param endpoint: the specific endpoint to append to the client URL
        :param headers: headers to use for this request in addition to the client
            default headers
        :param json: data to send as JSON, either a string/bytes to send directly or a
            dictionary/list to serialize. if `files` is also supplied, this should be a
            map from name to content, to be sent along with the `files` as a multipart
            request
        :param files: a map from file names to file-like objects, to be sent as
            multipart/form-data
        :param params: query parameters to add to the request
        :param return_raw_response: if true, return the requests.Response object
            received; otherwise attempt to parse the response
        :param retries: number of times to retry the request on failure.
            uses exponential backoff
        :param validate_response_status: if True, raise an ArthurException if the status
            code is not 2XX or does not match `validation_response_code`
        :param validation_response_code: expected status code of the response to
            validate. if None, don't validate
        :return: if return_raw_response is true, return the requests.Response object
            received; otherwise attempt to parse the response
        """
        return self.send(
            endpoint,
            method="POST",
            headers=headers,
            json=json,
            files=files,
            params=params,
            return_raw_response=return_raw_response,
            retries=retries,
            validate_response_status=validate_response_status,
            validation_response_code=validation_response_code,
        )

    def put(
        self,
        endpoint: str,
        json: Optional[Union[Dict, List, str, bytes]] = None,
        files: Optional[
            Union[Dict[str, BinaryIO], List[Tuple], Dict[str, Tuple]]
        ] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Union[Dict, bytes]] = None,
        return_raw_response: bool = False,
        retries: int = 0,
        validate_response_status: bool = True,
        validation_response_code: Optional[int] = None,
    ) -> Union[Dict, List, bytes, BytesIO, requests.Response]:
        """Send an HTTP PUT request

        :param endpoint: the specific endpoint to append to the client URL
        :param headers: headers to use for this request in addition to the client
            default headers
        :param json: data to send as JSON, either a string/bytes to send directly or a
            dictionary/list to serialize. if `files` is also supplied, this should be a
            map from name to content, to be sent along with the `files` as a
            multipart request
        :param files: a map from file names to file-like objects,
            to be sent as multipart/form-data
        :param params: query parameters to add to the request
        :param return_raw_response: if true, return the requests.Response object
            received; otherwise attempt to parse the response
        :param retries: number of times to retry the request on failure.
            uses exponential backoff
        :param validate_response_status: if True, raise an ArthurException if the status
            code is not 2XX or does not match `validation_response_code`
        :param validation_response_code: expected status code of the response to
            validate. if None, don't validate
        :return: if return_raw_response is true, return the requests.Response object
            received; otherwise attempt to parse the response
        """
        return self.send(
            endpoint,
            method="PUT",
            headers=headers,
            json=json,
            files=files,
            params=params,
            return_raw_response=return_raw_response,
            retries=retries,
            validate_response_status=validate_response_status,
            validation_response_code=validation_response_code,
        )

    def patch(
        self,
        endpoint: str,
        json: Optional[Union[Dict, List, str, bytes]] = None,
        files: Optional[
            Union[Dict[str, BinaryIO], List[Tuple], Dict[str, Tuple]]
        ] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Union[Dict, bytes]] = None,
        return_raw_response: bool = False,
        retries: int = 0,
        validate_response_status: bool = True,
        validation_response_code: Optional[int] = None,
    ) -> Union[Dict, List, bytes, BytesIO, requests.Response]:
        """Send an HTTP POST request

        :param endpoint: the specific endpoint to append to the client URL
        :param headers: headers to use for this request in addition to the client
            default headers
        :param json: data to send as JSON, either a string/bytes to send directly or a
            dictionary/list to serialize.
            if `files` is also supplied, this should be a map from name to content,
            to be sent along with the `files` as a multipart request
        :param files: a map from file names to file-like objects, to be sent as
            multipart/form-data
        :param params: query parameters to add to the request
        :param return_raw_response: if true, return the requests.Response object
            received; otherwise attempt to parse the response
        :param retries: number of times to retry the request on failure.
            uses exponential backoff
        :param validate_response_status: if True, raise an ArthurException if the
            status code is not 2XX or does not match `validation_response_code`
        :param validation_response_code: expected status code of the response to
            validate. if None, don't validate
        :return: if return_raw_response is true, return the requests.Response object
            received; otherwise attempt to parse the response
        """
        return self.send(
            endpoint,
            method="PATCH",
            headers=headers,
            json=json,
            files=files,
            params=params,
            return_raw_response=return_raw_response,
            retries=retries,
            validate_response_status=validate_response_status,
            validation_response_code=validation_response_code,
        )

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        return_raw_response: bool = False,
        params: Optional[Union[Dict, bytes]] = None,
        retries: int = 0,
        validate_response_status: bool = True,
        validation_response_code: Optional[int] = None,
    ) -> Union[Dict, List, bytes, BytesIO, requests.Response]:
        """Send an HTTP DELETE request

        :param endpoint: the specific endpoint to append to the client URL
        :param headers: headers to use for this request in addition to the client
            default headers
        :param return_raw_response: if true, return the requests.Response object
            received; otherwise attempt to parse the response
        :param params: query parameters to add to the request
        :param retries: number of times to retry the request on failure.
            uses exponential backoff
        :param validate_response_status: if True, raise an ArthurException if the
            status code is not 2XX or does not match validation_response_code
        :param validation_response_code: expected status code of the response to
            validate. if None, don't validate
        :return: if return_raw_response is true, return the requests.Response object
            received; otherwise attempt to parse the response
        """
        return self.send(
            endpoint,
            method="DELETE",
            headers=headers,
            return_raw_response=return_raw_response,
            retries=retries,
            validate_response_status=validate_response_status,
            params=params,
            validation_response_code=validation_response_code,
        )
