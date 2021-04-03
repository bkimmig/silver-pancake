from typing import List

import pandas as pd


def create_sentence(
    df: pd.DataFrame, group_col: str, apply_col: str, transform: callable = lambda x: x
) -> pd.DataFrame:
    return df.groupby(group_col)[apply_col].apply(transform).reset_index().copy()
