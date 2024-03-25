from .ast_node import ASTNode

class ControlFlowStatement(ASTNode):
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k, v in self.__dict__.items()])})"

class IfStatement(ControlFlowStatement):
    def __init__(self, condition, then_statement, else_statement):
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

class ForStatement(ControlFlowStatement):
    def __init__(self, variable, start_expression, end_expression, step_expression, loop_body, next_statement):
        self.variable = variable
        self.start_expression = start_expression
        self.end_expression = end_expression
        self.step_expression = step_expression
        self.loop_body = loop_body
        self.next_statement = next_statement

class NextStatement(ControlFlowStatement):
    def __init__(self, variable):
        self.variable = variable

class GotoStatement(ControlFlowStatement):
    def __init__(self, line_number):
        self.line_number = line_number

class GosubStatement(ControlFlowStatement):
    def __init__(self, line_number):
        self.line_number = line_number