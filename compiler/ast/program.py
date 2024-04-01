import json
from .ast_node import ASTNode

class Program(ASTNode):
    def __init__(self):
        super().__init__()

        # Maps line numbers to lists of statements
        self.lines = {}

    def add_statement(self, line_number, statement):
        # Ensure there is a line number associated with the statement
        if line_number is None:
            raise ValueError("Statement lacks a 'line_number' property.")

        # Initialize the list for this line number if not already present
        if line_number not in self.lines:
            self.lines[line_number] = []

        # Add the statement to its corresponding line number
        print(f"Adding Statement to Line {line_number}: {statement}")
        self.lines[line_number].append(statement)

    def to_dict(self):
        # returns a dictionary of the program, recursively
        return {
            "type": "Program",
            "lines": [
                {
                    "line_number": line_number,
                    "statements": [stmt.to_dict() for stmt in statements]
                }
                for line_number, statements in sorted(self.lines.items())
            ]
        }
    
    def to_json(self):
        # returns a json representation of the dictionary
        return json.dumps(self.to_dict(), indent=2)
    
    def to_statements(self):
        """Convert the program's lines to a structured list of statements with their line numbers."""

        # emoty statement list
        statements_list = []

        # loop through a sorted version of the statements
        for line_number, statements in sorted(self.lines.items()):
            # loop through each statement
            for statement in statements:
                # convert to a dictionary
                statement_info = statement.to_dict() if hasattr(statement, 'to_dict') else str(statement)

                # set the line number
                statement_info['line_number'] = line_number

                # append the statement
                statements_list.append(statement_info)
        return statements_list
