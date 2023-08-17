import functools
import inspect


# Base Error
class ArthurError(Exception):
    """
    Base Error for Arthur SDK. This class should not be used directly, Arthur exceptions
    should inherit from either ArthurUserError or ArthurInternalError.
    """

    pass


# Two Secondary Errors which differentiate between exceptions that are the user's fault
# and Arthur's fault
class ArthurUserError(ArthurError):
    """
    Exception raised due to incorrect user input to the Arthur SDK. Can be used directly
    but children are preferred.
    """

    pass


class ArthurInternalError(ArthurError):
    """
    Exception raised when user input is correct but an error occurs. Can be used
    directly but children are preferred.
    """

    pass


# User Exceptions
class MissingParameterError(ArthurUserError):
    """
    Exception raised when parameters supplied to the Arthur SDK are missing.
    """

    pass


class UserValueError(ArthurUserError, ValueError):
    """
    Exception raised when a user supplies an invalid value to the Arthur SDK.
    """

    pass


class UserTypeError(ArthurUserError, TypeError):
    """
    Exception raised when a user supplies an argument of the incorrect type to the
    Arthur SDK.
    """

    pass


class MethodNotApplicableError(ArthurUserError):
    """
    Exception raised when the method called is not valid for the resource.
    """

    pass


class ResponseClientError(ArthurUserError):
    """
    Exception raised when a 4XX response is received from the API.
    """

    pass


class UnauthorizedError(ResponseClientError):
    """
    Exception raised when a 401 Unauthorized response is received from the API.
    """

    pass


class PaymentRequiredError(ResponseClientError):
    """
    Exception raised when a 402 response is received from the API due to a user trying
    to access features not available in their plan.
    """

    pass


class ForbiddenError(ResponseClientError):
    """
    Exception raised when a 403 Forbidden response is received from the API.
    """

    pass


class NotFoundError(ResponseClientError):
    """
    Exception raised when a 404 Not Found response is received from the API.
    """

    pass


# Arthur Internal Exceptions
class ExpectedParameterNotFoundError(ArthurInternalError):
    """
    Exception raised when a field or property should be available from Arthur but is
    unexpectedly missing.
    """

    pass


class InternalValueError(ArthurInternalError, ValueError):
    """

    Exception raised when a value is unexpected.
    """

    pass


class InternalTypeError(ArthurInternalError, TypeError):
    """

    Exception raised when a value is unexpected.
    """

    pass


class ResponseServerError(ArthurInternalError):
    """
    Exception raised when a 5XX response is received from the API.
    """


class ResponseRedirectError(ArthurInternalError):
    """
    Exception raised when a 3XX response is unexpectedly received from the API.
    """


def arthur_excepted(message=None):
    """
    Decorator to wrap user-facing Arthur functions with exception handling that
    describes to the user whether the error is their fault or is our fault and should be
    reported.
    :param message: an optional message to prefix the error with, should describe the
        failure e.g. "failed to send
    inferences" or "an error occurred while creating the model."
    :return: the decorator function
    """
    if message is None:
        prefix = ""
    else:
        prefix = message + " because "

    def decorator_arthur_excepted(func):
        @functools.wraps(func)
        def wrapper_arthur_excepted(*args, **kwargs):
            # ensure all required parameters are present: check manually because
            # TypeErrors from internal calls should not be UserErrors
            try:
                inspect.signature(func).bind(*args, **kwargs)
                success = True
                err_msg = None
            except TypeError as e:
                success = False
                err_msg = str(e)
            if not success:
                raise MissingParameterError(err_msg)

            # call the function
            try:
                return func(*args, **kwargs)
            # if it is a user error simply re-raise
            except ArthurUserError as e:
                raise e
            # otherwise wrap it in a message saying it's not the user's fault
            except ArthurInternalError as e:
                raise ArthurInternalError(
                    prefix + "an internal exception occurred, please report to Arthur"
                ) from e
            except Exception as e:
                raise ArthurInternalError(
                    prefix + "there was an unexpected internal exception, "
                    "please report to Arthur"
                ) from e

        return wrapper_arthur_excepted

    return decorator_arthur_excepted
