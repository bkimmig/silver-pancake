from typing import Optional
import time

from fastapi import FastAPI, HTTPException

import svc

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # TODO - improve this
    svc.elastic.wait_for_it(svc.cfg["elastic"]["host"], svc.cfg["elastic"]["port"])
    svc.index.create()


@app.get("/")
async def read_root():
    return {"data": f"Hello! Welcome to the User Similarity API!"}


# TODO: could version the endpoints - likely put at the beginning v1/users/
# v1/X/ then create a function that can version all endpoints at once while keeping around
# the current version.
@app.get("/users/{id}")
async def similar_users(id: int, size: Optional[int] = 10, q_type: str = "and", q: Optional[str] = None):
    # TODO - add some sort of query validation to the q param, for now just say
    # it can't be longer than 50 chars #hacky - there is probably something in
    # ES?

    # TODO - make the query functionality better; the AND/OR is
    # really working at the moment.
    if q is None:
        q = "*"
    elif len(q) > 50:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        if q_type == "and":
            link = " AND "
        else:
            link = " OR "
        q = q.replace(",", link)
        q = f"sentence:({q})"

    # TODO - can make this object more robust - could take an arg, maybe handle
    # be pointed at another algo to the best index for that user
    # for now just return static config values.
    idx, v_field = svc.cfg["indices"]["users"]()
    resp = svc.query.similar_users(id, query=q, index=idx, vec_field=v_field, size=size)

    # TODO  - [possible] add a "generic" user and pull that one - if the instead if the api
    # contract is always to return (cold start... or maybe our cron just hasn't
    # run yet or something)
    if not resp:
        raise HTTPException(status_code=404, detail=f"User {id} not found")

    # TODO - fix up the response, maybe add more info about query hits
    out = {"user": id, "similar_users": [], "scores": []}
    for r in resp:
        out["scores"].append(r["_score"])
        out["similar_users"].append(r["_id"])
    return out
