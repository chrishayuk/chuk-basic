from .ast_node import ASTNode

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements