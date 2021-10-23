import requests
import dataclasses
from typing import Tuple


DUCKDNS_API = "https://www.duckdns.org/update"


@dataclasses.dataclass()
class Response:
    url: str
    text: str


@dataclasses.dataclass()
class Client:
    token: str

    def update(
        self,
        *domains: Tuple[str],
        ip: str = None,
        ipv6: str = None,
        verbose: bool = None,
        clear: bool = None
    ) -> Response:
        params = {}
        if ip is not None:
            params.update(ip=ip)
        elif ipv6 is not None:
            params.update(ipv6=ipv6)
        if verbose:
            params.update(verbose="true")
        if clear:
            params.update(clear="true")
        return self.request(*domains, params)

    def request(self, *domains, params: dict) -> Response:
        params.update(params = {
            "domains": ",".join(domains),
            "token": self.token
        })
        response = requests.get(
            DUCKDNS_API,
            params=params
        )
        return self.after_request(response)

    def after_request(self, response: requests.Response) -> Response:
        if response.text == "KO":
            self.bad_response()
        elif response.text.startswith("OK"):
            return self.convert_response(response)
    
    def convert_response(self, response: requests.Response) -> Response:
        return Response(response.url, response.text)