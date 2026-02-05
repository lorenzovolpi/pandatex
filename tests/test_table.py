import numpy as np
import pandas as pd
import pytest

import pandatex as px


@pytest.fixture
def df():
    arr = np.arange(20).reshape(5, 4)
    return pd.DataFrame(arr, columns=["a", "b", "c", "d"])


@pytest.fixture
def tbl(df):
    return px.Table(df, columns=["a", "b"], index="c", values="d")


class TestTable:
    @pytest.mark.parametrize(
        "columns, index, values",
        [
            (["a"], ["c", "d"], ["b"]),
            (["a"], ["b"], ["c"]),
            (["a", "c"], ["d"], "b"),
            ("a", "b", "c"),
        ],
    )
    def test_init(self, df, columns, index, values):
        tbl = px.Table(df, columns=columns, index=index, values=values)

        columns = [columns] if isinstance(columns, str) else list(columns)
        index = [index] if isinstance(index, str) else list(index)
        values = [values] if isinstance(values, str) else list(values)

        assert tbl.columns == columns
        assert tbl.index == index
        assert tbl.values == values

    @pytest.mark.parametrize(
        "cols1,cols2",
        [
            (["a", "b", "c"], "d"),
            (["a", "b"], ["c", "d"]),
            (["c"], ["a", "b", "c"]),
        ],
    )
    def test_init_invalid_columns(self, df, cols1, cols2):
        with pytest.raises(ValueError, match="All specified columns must be present in the DataFrame."):
            _ = px.Table(df, columns="e", index=cols1, values=cols2)
        with pytest.raises(ValueError, match="All specified indexes must be present in the DataFrame."):
            _ = px.Table(df, index="e", columns=cols1, values=cols2)
        with pytest.raises(ValueError, match="All specified values must be present in the DataFrame."):
            _ = px.Table(df, values="e", columns=cols1, index=cols2)

    @pytest.mark.parametrize(
        "columns, index, values",
        [
            (["a", "b"], ["c", "d"], ["a"]),
            (["a"], ["b", "c"], ["c"]),
            (["a", "b", "c"], ["c"], "d"),
        ],
    )
    def test_init_overlapping_columns(self, df, columns, index, values):
        with pytest.raises(ValueError, match="columns, indexes, and values must not overlap."):
            _ = px.Table(df, columns=columns, index=index, values=values)

    @pytest.mark.parametrize(
        "cols",
        [
            ["a", "a"],
        ],
    )
    def test_init_not_unique_columns(self, df, cols):
        with pytest.raises(ValueError, match="columns, indexes, and values must be unique."):
            _ = px.Table(df, columns=cols, index="c", values="d")
            _ = px.Table(df, index=cols, columns="c", values="d")
            _ = px.Table(df, values=cols, columns="c", index="d")


class TestFilter:
    # fmt: off
    @pytest.mark.parametrize(
        "val, op, val_make_true, bool_matrix",
        [
            (5, "lt", 2, [[True, True, True, True], [True, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]),
            (6, "gt", 7, [[False, False, False, False], [False, False, False, True], [True, True, True, True], [True, True, True, True], [True, True, True, True]]),
            (9, "eq", 9, [[False, False, False, False], [False, False, False, False], [False, True, False, False], [False, False, False, False], [False, False, False, False]]),
            (3, "ne", 8, [[True, True, True, False], [True, True, True, True], [True, True, True, True], [True, True, True, True], [True, True, True, True]]),
            (4, "le", 4, [[True, True, True, True], [True, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]),
            (11, "ge", 18, [[False, False, False, False], [False, False, False, False], [False, False, False, True], [True, True, True, True], [True, True, True, True]]),
        ],
    )
    def test_each(self, tbl: px.Table, val, op, val_make_true, bool_matrix):
        match op:
            case "lt":
                f = tbl.each() < val
            case "gt":
                f = tbl.each() > val
            case "eq":
                f = tbl.each() == val
            case "ne":
                f = tbl.each() != val
            case "le":
                f = tbl.each() <= val
            case "ge":
                f = tbl.each() >= val
            case _:
                raise ValueError(f"Unknown operation: {op}")

        assert f._check(val_make_true)
        assert f._table == tbl
        assert np.all(f.indexer() == np.array(bool_matrix))
    # fmt: on
