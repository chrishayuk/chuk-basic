from .statement import Statement

class ReadStatement(Statement):
    def __init__(self, variables):
        # call the base constructor
        super().__init__()

        # set the variables
        self.variables = variables

    def to_dict(self):
        return {
            "type": "ReadStatement",
            "variables": [variable.to_dict() for variable in self.variables]
        }