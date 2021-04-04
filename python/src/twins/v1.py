import pandas as pd
import numpy as np
import tensorflow as tf

from typing import List

import twins

# TODO - remove dep on the service in this repo; create a package that gets
# imported into both things (parent). But for sake of time just use the
# svc client here
import svc


def _join(x) -> str:
    cols = ["interest_tag", "course_id", "assessment_tag"]
    s = []
    for i in cols:
        if isinstance(x[i], str):
            s.append(x[i])
    return " ".join(s)


def _load() -> List[dict]:
    datasets = [
        {"name": "user_interests", "apply_col": "interest_tag"},
        {"name": "user_course_views", "apply_col": "course_id"},
        {"name": "user_assessment_scores", "apply_col": "assessment_tag"},
    ]
    for i in range(len(datasets)):
        datasets[i]["df"] = twins.dataset.load(datasets[i]["name"])
    return datasets


def _transform(data: List[dict]) -> List[dict]:
    fcn = lambda x: " ".join(np.unique(x))
    for i in range(len(data)):
        data[i]["transformed"] = twins.utils.create_sentence(
            data[i]["df"], group_col="user_handle", apply_col=data[i]["apply_col"], transform=fcn
        )
    return data


def _combine(data: List[dict]) -> pd.DataFrame:
    df = data[0]["transformed"].copy()
    for i in range(1, len(data)):
        df = pd.merge(df, data[i]["transformed"], how="left", on="user_handle")

    df["sentence"] = df.apply(_join, axis=1)
    return df


# --------------------------
def train():
    steps = [_transform, _combine]

    train_data = twins.pipeline.build(_load(), steps)
    print("training model v1")
    # TODO - persist this model then create a "predict" step that loads it in
    # and can predict for any dataset.
    model = twins.models.BagOfPCA(vocab_size=500, rank=64)
    user_vecs = model.fit_transform(train_data.sentence.values)
    print("trained model v1")
    return train_data, user_vecs, model


def train_predict():
    dat, vecs, mdl = train()
    print("writing recs to db")
    # TODO - parallelize this
    for i in range(len(dat)):
        r = dat.iloc[i]
        user = int(r["user_handle"])
        sentence = str(r["sentence"])
        vector = list(vecs[i])
        body = {"vector": vector, "sentence": sentence, "id": user}
        svc.cfg["elastic"]["client"].index(index="users-v1", id=user, body=body)
    print("completed writing recs to db")
