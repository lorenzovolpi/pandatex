from abc import ABC
from typing import Iterable

import numpy as np
import pandas as pd


class Table(ABC):
    def __init__(
        self, df: pd.DataFrame, columns: str | Iterable[str], index: str | Iterable[str], values: str | Iterable[str]
    ):
        if columns is None or index is None or values is None:
            raise ValueError("columns, rows, and values cannot be None.")
        if columns == [] or index == [] or values == []:
            raise ValueError("columns, rows, and values cannot be empty lists.")

        if isinstance(columns, str):
            columns = [columns]
        if isinstance(index, str):
            index = [index]
        if isinstance(values, str):
            values = [values]

        if any(c not in df.columns for c in columns):
            raise ValueError("All specified columns must be present in the DataFrame.")
        if any(r not in df.columns for r in index):
            raise ValueError("All specified indexes must be present in the DataFrame.")
        if any(v not in df.columns for v in values):
            raise ValueError("All specified values must be present in the DataFrame.")

        if len(columns) != len(set(columns)) or len(index) != len(set(index)) or len(values) != len(set(values)):
            raise ValueError("columns, indexes, and values must be unique.")

        if set(columns) & set(index) or set(columns) & set(values) or set(index) & set(values):
            raise ValueError("columns, indexes, and values must not overlap.")

        self.df = df
        self.columns = columns
        self.index = index
        self.values = values
