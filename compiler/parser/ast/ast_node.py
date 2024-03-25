class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k, v in self.__dict__.items()])})"
    
class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name