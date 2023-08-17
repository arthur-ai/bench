import logging
from urllib.parse import urlparse

from arthur_bench.exceptions import UserValueError


logger = logging.getLogger(__name__)


def construct_url(*parts: str, validate=True, default_https=True) -> str:
    """Construct a URL from various parts

    Useful for joining pieces which may or may not have leading and/or trailing
    slashes. e.g. construct_url("https://arthur.ai/", "/api/v3", "/users") will yield
    the same valid url as construct_url("https://arthur.ai", "api/v3/", "users/"):
    "https://arthur.ai/api/v3/users".

    :param validate: if True, validate that the URL is valid
    :param default_https: if True, allow urls without a scheme and use https by default
    :param parts: strings from which to construct the url
    :return: a fully joined url, with NO trailing slash
    """
    # join parts
    url = "/".join(s.strip("/") for s in parts)

    # add scheme
    parsed_url = urlparse(url)
    if parsed_url.scheme is None or parsed_url.scheme == "":
        if default_https:
            logger.warning("No url scheme provided, defaulting to https")
            url = "https://" + url
            parsed_url = urlparse(url)
        elif validate:
            raise UserValueError(f"No scheme provided in URL {url}")

    # validate
    if validate and (
        parsed_url.scheme is None
        or parsed_url.scheme == ""
        or parsed_url.netloc is None
        or parsed_url.netloc == ""
    ):
        joiner = "', '"
        raise UserValueError(
            f"Invalid url, cannot construct URL from parts '{joiner.join(parts)}'"
        )

    return url
