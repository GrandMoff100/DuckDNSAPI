import dataclasses
import re


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
    url: str

    def __init__(self, url: str, text: str) -> None:
        super().__init__(url, text)
        self.updated = None
        self.record = None

        try:
            pattern = r'OK\n(?P<record>.*)\n(?P<status>[A-Z]+)'
            (record, status), *_ = re.findall(pattern, self.text, flags=re.DOTALL)
            self.record = record
            if status == "UPDATED":
                self.updated = True
            elif status == "NOCHANGE":
                self.updated = False
        except ValueError:
            pass

    @property
    def nochange(self):
        return not self.updated

    def __repr__(self):
        return f'RecordResponse(updated={self.updated}, nochange={self.nochange}, record={self.record!r})'


class UpdateResponse(Response):
    """
    The response class representing responses from the DuckDNS DDNS API.

    :param url: The url the response was returned from.
    :param text: The content of the response. Contains useful information when the verbose option is set to True.
    :ivar ip: The IP that the domains in the request now point to.
    :ivar updated: A boolean representing whether or not the ip was updated in the request.
    """

    updated: bool = None
    ip: str = None


    def __init__(self, url: str, text: str):
        super().__init__(url, text)
        try:
            pattern = r'OK\n(?P<ip>.*)\n\n(?P<status>[A-Z]+)'
            (ip, status), *_ = re.findall(pattern, self.text)
            self.ip = ip
            if status == "UPDATED":
                self.updated = True
            elif status == "NOCHANGE":
                self.updated = False
        except ValueError:
            pass

    @property
    def nochange(self):
        return not self.updated

    def __repr__(self):
        return f'UpdateResponse(updated={self.updated}, nochange={self.nochange}, ip={self.ip!r})'