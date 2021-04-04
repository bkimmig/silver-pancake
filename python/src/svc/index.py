import elasticsearch

import svc


# add indices here and they will be created in the 'create' function
# should do something more robust, but this is pretty simple for now.
_indices = [
    {
        "name": "users-v1",
        "mapping": {
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "vector": {"type": "dense_vector", "dims": 64},
                    "sentence": {"type": "text"},
                }
            }
        },
    }
]


def create():
    for idx in _indices:
        try:
            created = svc.cfg["elastic"]["client"].indices.create(index=idx["name"], body=idx["mapping"])
        except elasticsearch.exceptions.RequestError as e:
            # TODO - better error catching
            print(e, "- index not created")
            created = False

        if created:
            print(f"Created: {created}")
