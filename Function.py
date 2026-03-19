from MathInterface import MathInterface
from numbers import Number
from MNumber import MNumber

class MFunction(MathInterface):
    def __init__(self, arg=1):
        if isinstance(arg, Number):
            arg = MNumber(arg)
        if isinstance(arg, MathInterface):
            self.contents = arg
        else:
            raise TypeError("Incorrect args to Ln(): "+str(arg))

    def __eq__(self, other):
        if type(other) == type(self):
            return self.contents == other.contents
        return super().__eq__(other)