from typing import List
from .expression import Expression
from ..variable import Variable

class FnExpression(Expression):
    def __init__(self, name: Variable, arguments: List[Expression]):
        self.name = name
        self.arguments = arguments

    def to_dict(self):
        # function expression as a dictionary, handles recursion
        return {
            "type": "FnExpression",
            "name": self.name.to_dict() if hasattr(self.name, 'to_dict') else str(self.name),
            "arguments": [arg.to_dict() if hasattr(arg, 'to_dict') else str(arg) for arg in self.arguments],
        }
