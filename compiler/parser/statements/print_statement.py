from ...ast.ast_statement import PrintStatement
from .base_statement_parser import BaseStatementParser

class PrintStatementParser(BaseStatementParser):
    def parse(self):
        # Advance past 'PRINT'
        self.parser.advance()

        # parse the expression
        expression = self.parser.parse_expression()

        # return the statement
        return PrintStatement(expression)