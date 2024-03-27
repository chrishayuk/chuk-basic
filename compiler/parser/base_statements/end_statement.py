from ...ast.ast_statement import EndStatement
from .base_statement_parser import BaseStatementParser


class EndStatementParser(BaseStatementParser):
    def parse(self):
        # set the position
        self.parser.advance()

        # return the statement
        return EndStatement()