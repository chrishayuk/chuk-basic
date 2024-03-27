from ...ast.ast_statement import InputStatement
from .base_statement_parser import BaseStatementParser

class InputStatementParser(BaseStatementParser):
    def parse(self):
        # Advance past the 'INPUT' token
        self.parser.advance()

        # parse the variable
        variable = self.parser.parse_variable()

        # return the statement
        return InputStatement(variable)