import requests


class Error(Exception):
    """
    The base Exception class for all DuckDNSAPI exceptions.
    """


class DuckDNSError(Error):
    """
    An Error raised when DuckDNS sends a bad response. (A "KO" response.)
    """

    def __init__(self, response: requests.Response) -> None:
        super().__init__(f"Bad request made to url {response.url!r}")
