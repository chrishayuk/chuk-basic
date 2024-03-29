from typing import List
from .expression import Expression
from ..variable import Variable

class FnExpression(Expression):
    def __init__(self, name: Variable, arguments: List[Expression]):
        self.name = name
        self.arguments = arguments