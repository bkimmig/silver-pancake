from typing import List
import time

import requests
import elasticsearch
from elasticsearch import Elasticsearch


TIMEOUT = 500


def is_up(host: str, port: int):
    # TODO - catch exception better here
    r = None
    try:
        r = requests.get(f"http://{host}:{port}")
    except:
        return False
    if r is not None:
        if r.status_code == 200:
            return True
    return False


def wait_for_it(host: str, port: int):
    i = 0
    while not is_up(host, port):
        if i > TIMEOUT:
            break
        time.sleep(1)
        i += 1


def client(host: List[str] = None, port: int = None) -> Elasticsearch:
    # client is best used as a singleton - "Best practice is to create a single
    # global instance of the client and use it throughout your application."
    if host is None:
        host = "elasticsearch"
    if port is None:
        port = 9200
    # TODO - make this better; wait for ES cluster to be up
    wait_for_it(host, port)
    return Elasticsearch(host, port=port)
