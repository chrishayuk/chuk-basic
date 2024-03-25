from .ast_node import ASTNode

class FunctionStatement(ASTNode):
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k, v in self.__dict__.items()])})"

class DefStatement(FunctionStatement):
    def __init__(self, function_name, parameters, function_body):
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body