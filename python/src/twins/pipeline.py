import copy


def build(data, steps: list):
    data = copy.deepcopy(data)
    for step in steps:
        data = step(data)
    return data
