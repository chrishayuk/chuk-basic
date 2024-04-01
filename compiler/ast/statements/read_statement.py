from .statement import Statement

class ReadStatement(Statement):
    def __init__(self, variables):
        super().__init__()
        self.variables = variables

    def to_dict(self):
        return {
            "type": "ReadStatement",
            "variables": [variable.to_dict() for variable in self.variables]
        }