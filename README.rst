DuckDNS API
***************

Quick Example::
    import os
    from duckdnsapi import Client


    client = Client(os.getenv('token'))

    resp = client.update("nateswebhook", ip="", verbose=True)

    print(resp)
