from typing import Any, Callable, TypeAlias

import numpy as np

from pandatex.group import Group

CondValOp: TypeAlias = Callable[[np.ndarray], Any]


class CondValue:
    def __init__(self, group: Group, op: CondValOp):
        self.group = group
        self.op = op

    def get(self):
        return self.op(self.group.get_values())
