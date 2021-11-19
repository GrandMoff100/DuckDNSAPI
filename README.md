# DuckDNS API

## Quick Example

```python
import os
from duckdnsapi import Client


client = Client(os.getenv("my_duckdns_token"))

resp = client.update_ip("mywebhook", ip="127.0.0.1", verbose=True)

print(resp)
```
