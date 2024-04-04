from .fn_end_statement import FnEndStatement
from .statement import Statement

class DefStatement(Statement):
    def __init__(self, function_name, parameters, function_body):
        super().__init__()
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body

        # Initialize line_number to None
        self.line_number = None  

    def to_statements(self):
        """Convert the DEF statement into a list of separate statements."""
        statements = []

        # Add the DefStatement itself
        statements.append({
            'line_number': self.line_number,
            'statement': self
        })

        # Add the statements within the function body
        for stmt in self.function_body:
            statements.append({
                'line_number': stmt.line_number,
                'statement': stmt
            })

        # Add the FNEND statement separately
        statements.append({
            'line_number': self.fnend_line_number,
            'statement': FnEndStatement(self.fnend_line_number)
        })

        return statements