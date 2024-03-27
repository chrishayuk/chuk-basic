from ...ast.ast_statement import LetStatement
from ..expression_parser import parse_expression
from .base_statement_parser import BaseStatementParser

class LetStatementParser(BaseStatementParser):
    def parse(self):
        # set the position
        self.parser.advance()

        # parse the variable
        variable = self.parser.parse_variable()

        # skip the equals sign e.g. LET x = 1
        self.parser.advance()

        # parse the expression for the let e.g. LET x = 1
        expression = parse_expression(self.parser)

        # return the statement
        return LetStatement(variable, expression)