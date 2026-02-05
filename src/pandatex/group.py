from pandatex.filter import Filter
from pandatex.table import Table


class Group:
    def __init__(self, tbl: Table, filter: Filter | None = None):
        self.tbl = tbl
        self.filter = Filter(tbl) if filter is None else filter

    def min(self):
        raise NotImplementedError("min() method is not implemented.")

    def max(self):
        raise NotImplementedError("max() method is not implemented.")

    def get_values(self):
        raise NotImplementedError("get_values() method is not implemented.")
