from ...ast.ast_statement import StopStatement
from .base_statement_parser import BaseStatementParser


class StopStatementParser(BaseStatementParser):
    def parse(self):
        # Advance past 'STOP'
        self.parser.advance()

        # return the statement
        return StopStatement()