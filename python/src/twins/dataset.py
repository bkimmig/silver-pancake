from typing import List
import os

import pandas as pd


PATH = "/data/data_files_ml_engineer"


def load(name: str) -> pd.DataFrame:
    file = os.path.join(PATH, f"{name}.csv")
    return pd.read_csv(file)


def describe() -> List[str]:
    files = os.listdir(PATH)
    for file in files:
        print(f"{file.split('.')[0]}")
    return files
