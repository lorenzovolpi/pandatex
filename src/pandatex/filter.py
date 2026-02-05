from typing import Any, Callable, Literal, TypeAlias

from pandatex.condval import CondValue
from pandatex.table import Table

FilterRule: TypeAlias = Callable[[Any, str | tuple[str], str | tuple[str]], bool]


class Filter:
    def __init__(self):
        self.rules: RuleStack = RuleStack.and_()

    def check(self, val, col, idx):
        if self.rules is None:
            return True

        return all(rule(val, col, idx) for rule in self.rules)

    def rule(self, rule: FilterRule) -> "Filter":
        if rule is None:
            return self

        if not isinstance(rule, callable):
            raise TypeError("Rule must be a callable function.")

        self.rules.add(rule)
        return self

    def col(self, _col):
        return self.rule(lambda _v, _c, _r: _c == _col)

    def row(self, _row):
        return self.rule(lambda _v, _c, _r: _r == _row)

    def and_(self, other: FilterRule) -> "Filter":
        if not isinstance(other, FilterRule):
            raise TypeError("Can only combine with another FilterRule instance.")
        new_filter = Filter()
        new_filter.rules = RuleStack.and_().add(self.rules).add(other)
        return new_filter

    def or_(self, other: FilterRule) -> "Filter":
        if not isinstance(other, Filter):
            raise TypeError("Can only combine with another Filter instance.")
        new_filter = Filter()
        new_filter.rules = RuleStack.and_().add(RuleStack.or_().add(self.rules).add(other.rules))
        return new_filter

    def __and__(self, other: "Filter") -> "Filter":
        return self.and_(other)

    def __or__(self, other: "Filter") -> "Filter":
        return self.or_(other)

    def __lt__(self, val: Any) -> "Filter":
        if isinstance(val, CondValue):
            self.rule(lambda _v, _c, _r: _v < val.get())
        else:
            self.rule(lambda _v, _c, _r: _v < val)

    def __le__(self, val: Any) -> "Filter":
        if isinstance(val, CondValue):
            self.rule(lambda _v, _c, _r: _v <= val.get())
        else:
            self.rule(lambda _v, _c, _r: _v <= val)

    def __gt__(self, val: Any) -> "Filter":
        if isinstance(val, CondValue):
            self.rule(lambda _v, _c, _r: _v > val.get())
        else:
            self.rule(lambda _v, _c, _r: _v > val)

    def __ge__(self, val: Any) -> "Filter":
        if isinstance(val, CondValue):
            self.rule(lambda _v, _c, _r: _v >= val.get())
        else:
            self.rule(lambda _v, _c, _r: _v >= val)

    def __eq__(self, val: Any) -> "Filter":
        if isinstance(val, CondValue):
            self.rule(lambda _v, _c, _r: _v == val.get())
        else:
            self.rule(lambda _v, _c, _r: _v == val)

    def __ne__(self, val: Any) -> "Filter":
        if isinstance(val, CondValue):
            self.rule(lambda _v, _c, _r: _v != val.get())
        else:
            self.rule(lambda _v, _c, _r: _v != val)


class RuleStack:
    def __init__(self, type: Literal["and", "or"]):
        self.type = type
        self.rules: list[RuleStack | FilterRule] | None = None

    def add(self, rule: "RuleStack" | FilterRule) -> "RuleStack":
        if self.rules is None:
            self.rules = []
        self.rules.append(rule)
        return self

    def check(self, _v, _col, _row):
        if self.rules is None and self.type == "and":
            return True
        elif self.rules is None and self.type == "or":
            return False

        rule_array = []
        for r in self.rules:
            if isinstance(r, RuleStack):
                rule_array.append(r.check(_v, _col, _row))
            elif isinstance(r, FilterRule):
                rule_array.append(r(_v, _col, _row))

        if self.type == "and":
            return all(rule_array)
        elif self.type == "or":
            return any(rule_array)

    @classmethod
    def and_(cls) -> "RuleStack":
        return cls("and")

    @classmethod
    def or_(cls) -> "RuleStack":
        return cls("or")
