from .statement import Statement

class ForStatement(Statement):
    def __init__(self, variable, start_expression, end_expression, step_expression, loop_body, next_statement):
        self.variable = variable
        self.start_expression = start_expression
        self.end_expression = end_expression
        self.step_expression = step_expression
        self.loop_body = loop_body
        self.next_statement = next_statement

class NextStatement(Statement):
    def __init__(self, variable):
        self.variable = variable