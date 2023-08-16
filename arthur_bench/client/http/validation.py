# flake8: noqa
import requests
from http import HTTPStatus
from http.client import responses
from typing import List, Optional, Union, Tuple, Any


from arthur_bench.exceptions import (
    InternalValueError,
    ResponseRedirectError,
    ResponseClientError,
    ResponseServerError,
    InternalTypeError,
    ArthurUserError,
    ArthurInternalError,
    PaymentRequiredError,
    ForbiddenError,
    UnauthorizedError,
    NotFoundError,
)


def _format_response(response: requests.Response) -> str:
    try:
        content = response.json()
    except ValueError:
        content = str(response.content)

    return f"{response.status_code} {responses[response.status_code]}: {content}"


def _format_status_code(status_code: int) -> str:
    return f"{status_code} {responses[status_code]}"


def validate_response_status(
    response_or_code: Union[requests.Response, int],
    expected_status_code: Optional[int] = None,
    allow_redirects: Optional[bool] = False,
) -> None:
    """
    Validate the status code of a requests.Response object or (int) status code.
    :param response_or_code: the requests.Response object or status code to validate
    :param expected_status_code: the expected status code to check for. If None, all
    codes <300 will be valid, and 3XX codes will be subject to allow_redirects
    :param allow_redirects: if True will not raise an exception for 3XX status codes
    :return: None
    :raises InternalValueError: if expected_status_code is not None and does not match
    the response code
    :raises ResponseServerError: if the response has a 5XX status code
    :raises ResponseClientError: if the response has a 4XX status code
    :raises ResponseRedirectError: if the response has a 3XX status code
    """

    formatter_func: Any
    if isinstance(response_or_code, requests.Response):
        formatter_func = _format_response
        status_code = response_or_code.status_code
    elif isinstance(response_or_code, int):
        formatter_func = _format_status_code
        status_code = response_or_code
    else:
        raise InternalTypeError(
            f"{response_or_code} is of type {type(response_or_code)}, not"
            "requests.Response or int"
        )

    # make HTTPStatus (which extends int) if just raw int
    status_code = HTTPStatus(status_code)

    # if an exact status code is supplied and it matches return, to let through
    # expected codes >= 400
    if expected_status_code is not None and status_code == expected_status_code:
        return

    # then check for code ranges with their own exceptions
    elif status_code >= 500:
        raise ResponseServerError(formatter_func(response_or_code))

    elif status_code >= 400:
        # 401 error code corresponding specifically to unauthorized response
        if status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError(
                "Unauthorized, please ensure your access information is correct"
            )
        # 402 error code corresponding specifically to requesting paid features from a
        # free account
        if status_code == HTTPStatus.PAYMENT_REQUIRED:
            raise PaymentRequiredError(formatter_func(response_or_code))
        # 403 error code corresponding specifically to forbidden
        if status_code == HTTPStatus.FORBIDDEN:
            raise ForbiddenError(formatter_func(response_or_code))
        # 404 error code corresponding specifically to not found
        if status_code == HTTPStatus.NOT_FOUND:
            raise NotFoundError(formatter_func(response_or_code))

        raise ResponseClientError(formatter_func(response_or_code))

    elif status_code >= 300 and not allow_redirects:
        raise ResponseRedirectError(formatter_func(response_or_code))

    # finally if an expected code is supplied but doesn't match, raise an
    # InternalValueError
    elif expected_status_code is not None and status_code != expected_status_code:
        parsed_response = formatter_func(response_or_code)
        raise InternalValueError(
            f"expected response with status code {expected_status_code} but received "
            + parsed_response
        )


def validate_multistatus_response_and_get_failures(
    response: requests.Response, raise_on_failures: bool = False
) -> Tuple[List[dict], List[dict]]:
    """Validate a 207 MultiStatus response and return the failures it contains.

    :param response: requests.Response object to validate, with the following body format:

        .. code-block:: JSON

            {
                "counts": {
                    "success": 0,
                    "failure": 0,
                    "total": 0
                },
                "results": [
                    {
                        "message": "success",
                        "status": 200
                    }
                ]
            }
    :param raise_on_failures: if True, raise an exception if the response contains any
    failures
    :return: a tuple of two lists: user-caused failures and internal failures
    :raises ArthurInternalValueError: If the response does not have 207 status code, or
    is incorrectly formatted,
     or 'counts' and 'results' do not agree
    :raises ResponseClientError: if `raise_on_failures` and the response contains only
    client errors
    :raises ResponseServerError: if `raise_on_failures` and the response contains server
    errors
    """
    # initial input validation
    validate_response_status(response, HTTPStatus.MULTI_STATUS)
    body = response.json()
    if type(body) != dict:
        raise InternalValueError("response body is incorrectly formatted")
    if "counts" not in body.keys():
        raise InternalValueError("response body does not have 'counts' field")
    if set(body["counts"].keys()) != {"success", "failure", "total"}:
        raise InternalValueError(
            f"response counts keys {set(body['counts'].keys())} are invalid"
        )
    if "results" not in body.keys():
        raise InternalValueError("response body does not have 'results' field")
    if type(body["results"]) != list:
        raise InternalValueError("response 'results' field must be a list")

    # pass through results, gathering failures
    user_failures = []
    internal_failures = []
    for result in body["results"]:
        if "status" not in result.keys():
            raise InternalValueError("response result does not contain 'status'")
        try:
            validate_response_status(result["status"])
        except ArthurUserError:
            user_failures.append(result)
        except ArthurInternalError:
            internal_failures.append(result)

    # check that failure counts match ours
    if len(user_failures) + len(internal_failures) != body["counts"]["failure"]:
        raise InternalValueError(
            f"provided response failure count {body['counts']['failure']} does not "
            f"match {len(user_failures) + len(internal_failures)} results with status "
            f"code >= 300"
        )

    # raise an exception if specified
    if raise_on_failures:
        # build messages
        internal_message, user_message = None, None
        if len(internal_failures) > 0:
            internal_message = (
                f"{len(internal_failures)} Arthur internal exceptions occurred in the "
                f"multi-status response: {internal_failures}"
            )
        if len(user_failures) > 0:
            user_message = (
                f"{len(user_failures)} client errors occurred, the following must be "
                f"corrected: {user_failures}"
            )
        # if there are internal errors always raise an internal error
        if internal_message is not None:
            # but include user errors in the message if present as well
            if user_message is not None:
                message = internal_message + "\nadditionally " + user_message
            else:
                message = internal_message
            raise ResponseServerError(message)
        # if only user errors raise user error
        elif user_message is not None:
            raise ResponseClientError(user_message)

    return user_failures, internal_failures
