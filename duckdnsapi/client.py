import requests
import dataclasses
from typing import Tuple


DUCKDNS_API = "https://www.duckdns.org/update"


@dataclasses.dataclass()
class Response:
    url: str
    text: str


class RecordResponse(Response):
    pass


class UpdateResponse(Response):
    pass


@dataclasses.dataclass()
class Client:
    token: str

    def update(
        self,
        *domains: Tuple[str],
        ip: str = None,
        ipv6: str = None,
        verbose: bool = None
    ) -> Response:
        params = {}
        if ip is not None:
            params.update(ip=ip)
        elif ipv6 is not None:
            params.update(ipv6=ipv6)
        if verbose:
            params.update(verbose="true")
        response = self.request(*domains, params)
        return UpdateResponse(response.url, response.text)

    def clear(self, *domains: Tuple[str]):
        pass

    def get_txt_record(self, *domains: Tuple[str]):
        pass

    def set_txt_record(self, *domains: Tuple[str]):
        pass

    def clear_txt_record(self, *domains: Tuple[str]):
        pass

    def request(self, *domains: Tuple[str], params: dict = {}) -> Response:
        params.update(params = {
            "domains": ",".join(domains),
            "token": self.token
        })
        response = requests.get(
            DUCKDNS_API,
            params=params
        )
        return self.after_request(response)

    def after_request(self, response: requests.Response) -> requests.Response:
        if response.text == "KO":
            self.bad_response()
        elif response.text.startswith("OK"):
            return response
    