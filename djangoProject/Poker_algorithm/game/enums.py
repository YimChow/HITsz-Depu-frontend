from enum import IntEnum
# 枚举变量的类的定义


class ActionType(IntEnum):

    CALL = 0
    RAISE = 1
    FOLD = 2


class Round(IntEnum):

    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    """
    def __add__(self, other):
        return Round(self.value+other)  # ’+‘运算符重载

    def __eq__(self, other):
        return self.value == other      # ‘==‘运算符重载

    class CardType(IntEnum):
        HOLE = 0
        PUBLIC = 1
"""