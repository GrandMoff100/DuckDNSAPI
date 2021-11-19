"""A module for interacting with DuckDNS via HTTP requests"""

import requests
import dataclasses
from typing import Tuple

from duckdnsapi.errors import DuckDNSError
from duckdnsapi.responses import UpdateResponse, RecordResponse

DUCKDNS_API = "https://www.duckdns.org/update"


<<<<<<< Updated upstream
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


@dataclasses.dataclass()
class Response:
    """
    The base response class representing a response from DuckDNS.

    :param url: The url the response was returned from.
    :param text: The content of the response. Contains useful information when the verbose option is set to True.
    """

    url: str
    text: str


class RecordResponse(Response):
    """
    The response class representing responses from the DuckDNS TXT Record API.

    :param url: The url the response was returned from.
    :param text: The content of the response. Contains useful information when the verbose option is set to True.
    :ivar record: The text record returned from your DuckDNS
    :ivar updated: A boolean representing whether or not the txt record was updated in the request.
    """
    
    record: str
    updated: bool

    def __init__(self, url: str, text: str) -> None:
        super().__init__(url, text)
        self.updated = None
        self.record = None

        try:
            _, *record, status = text.splitlines()

            self.record = "\n".join(record)

            if status == "UPDATED":
                self.updated = True
            elif status == "NOCHANGE":
                self.updated = False
        except ValueError:
            pass


class UpdateResponse(Response):
    """
    The response class representing responses from the DuckDNS DDNS API.

    :param url: The url the response was returned from.
    :param text: The content of the response. Contains useful information when the verbose option is set to True.
    :ivar ip: The IP that the domains in the request now point to.
    :ivar updated: A boolean representing whether or not the ip was updated in the request.    
    """

    updated: bool
    ip: str

    def __init__(self, url: str, text: str) -> None:
        super().__init__(url, text)
        self.updated = None
        self.ip = None

        try:
            _, *ip, status = text.splitlines()

            self.ip = "\n".join(ip)

            if status == "UPDATED":
                self.updated = True
            elif status == "NOCHANGE":
                self.updated = False
        except ValueError:
            pass


=======
>>>>>>> Stashed changes
@dataclasses.dataclass()
class Client:
    """
    """
    token: str

    def update_ip(
        self,
        *domains: Tuple[str],
        ip: str = None,
        ipv6: str = None,
        verbose: bool = True
    ) -> UpdateResponse:
        """"""
        params = {}
        if ip is not None:
            params.update(ip=ip)
        elif ipv6 is not None:
            params.update(ipv6=ipv6)
        if verbose:
            params.update(verbose="true")
        response = self.request(*domains, params=params)
        return UpdateResponse(response.url, response.text)

    def clear_ip(self, *domains: Tuple[str]) -> UpdateResponse:
        """A method that clears whatever the existing ip is for the given domains."""
        return self.request(*domains, params={"clear": "true"})

    def set_txt_record(self, *domains: Tuple[str], content: str = None) -> RecordResponse:
        """Sets the content of the TXT record of the given domains to given content."""
        if content:
<<<<<<< Updated upstream
            return self.request(*domains, params={"txt": content, "verbose": "true"})
        
    def clear_txt_record(self, *domains: Tuple[str]) -> RecordResponse:
        """Clears the content of all the TXT records of the given domains."""
        return self.request(*domains, params={"txt": "", "clear": "true", "verbose": "true"})
        
=======
            resp = self.request(*domains, params={"txt": content, "verbose": "true"})
            return RecordResponse(resp.url, resp.text)
    
    def clear_txt_record(self, *domains: Tuple[str]) -> RecordResponse:
        """Clears the content of all the TXT records of the given domains."""
        resp = self.request(*domains, params={"txt": "", "clear": "true", "verbose": "true"})
        return RecordResponse(resp.url, resp.text)

>>>>>>> Stashed changes
    def request(self, *domains: Tuple[str], params: dict = {}) -> requests.Response:
        """The method that sends HTTP requests to the API with the appropriate authentication parameters."""
        params.update({
            "domains": ",".join(domains),
            "token": self.token
        })
        response = requests.get(
            DUCKDNS_API,
            params=params
        )
        return self.after_request(response)

    def after_request(self, response: requests.Response) -> requests.Response:
        """A post method for raising errors on bad responses and converting responses into data models for good responses."""
        if response.text == "KO":
            raise DuckDNSError(response)
        elif response.text.startswith("OK"):
            return response
