"""A module for interacting with DuckDNS via HTTP requests"""

import requests
import dataclasses
from typing import Tuple

from duckdnsapi.errors import DuckDNSError
from duckdnsapi.responses import UpdateResponse, RecordResponse

DUCKDNS_API = "https://www.duckdns.org/update"


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
            resp = self.request(*domains, params={"txt": content, "verbose": "true"})
            return RecordResponse(resp.url, resp.text)
    
    def clear_txt_record(self, *domains: Tuple[str]) -> RecordResponse:
        """Clears the content of all the TXT records of the given domains."""
        resp = self.request(*domains, params={"txt": "", "clear": "true", "verbose": "true"})
        return RecordResponse(resp.url, resp.text)

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
