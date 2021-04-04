import os

import svc


def get() -> dict:
    # TODO - make this an object OR maybe there is a package out there that can
    # do dict -> class
    cfg = {
        "elastic": {
            "client": svc.elastic.client(os.getenv("ELASTIC_HOST"), os.getenv("ELASTIC_PORT")),
            "host": os.getenv("ELASTIC_HOST"),
            "port": os.getenv("ELASTIC_PORT"),
        },
        "indices": {"users": get_index},
    }
    return cfg


def get_index() -> tuple:
    return ("users-v1", "vector")
