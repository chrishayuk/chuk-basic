from .ast_node import ASTNode

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name