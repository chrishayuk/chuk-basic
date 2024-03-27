from ...ast.ast_statement import PrintStatement
from ..expression_parser import parse_expression
from .base_statement_parser import BaseStatementParser

class PrintStatementParser(BaseStatementParser):
    def parse(self):
        # set the position
        self.parser.advance()

        # parse the expression
        expression = parse_expression(self.parser)

        # return the statement
        return PrintStatement(expression)