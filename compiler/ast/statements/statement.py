from ..ast_node import ASTNode

class Statement(ASTNode):
    def __init__(self, line_number=None):
        # call the base constructor
        super().__init__()

        # set the line number
        self.line_number = line_number

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k, v in self.__dict__.items()])})"
