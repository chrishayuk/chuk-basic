from .function_statement import FunctionStatement

class DefStatement(FunctionStatement):
    def __init__(self, function_name, parameters, function_body):
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body