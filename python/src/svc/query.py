import elasticsearch

import svc


def _vector(vec: list, vec_field: str, query: str = "*") -> dict:

    # TODO: add other types of scoring and add that to the function arg
    score_fn = f"doc['{vec_field}'].size() == 0 ? 0 : cosineSimilarity(params.queryVector, '{vec_field}') + 1.0"

    return {
        "query": {
            "script_score": {
                "query": {"query_string": {"query": query}},
                "script": {
                    "source": score_fn,
                    # f"cosineSimilarity(params.queryVector, doc['{vec_field}']) + 1.0",
                    "params": {"queryVector": vec},
                }
                # "script": {"source": score_fn, "params": {"vector": vec}},
            }
        }
    }


def get_vector(id: int, index: str = "users-v1", vec_field: str = "vector") -> list:
    try:
        response = svc.cfg["elastic"]["client"].get(index=index, id=id)
    except elasticsearch.exceptions.NotFoundError as e:
        # TODO: add better error handling
        # print(e)
        return []
    src = response["_source"]
    if vec_field in src:
        return src[vec_field]
    return []


def similar_users(
    handle: int, query: str = "*", index: str = "users-v1", vec_field: str = "vector", size: int = 20
) -> list:
    vec = get_vector(handle, index, vec_field)
    if not vec:
        return []
    q = _vector(vec, vec_field, query)
    results = svc.cfg["elastic"]["client"].search(index=index, body=q, from_=1, size=size)
    return results["hits"]["hits"]
