from ...ast.statements import ReturnStatement
from .base_statement_parser import BaseStatementParser


class ReturnStatementParser(BaseStatementParser):
    def parse(self):
        # Advance past 'RETURN'
        self.parser.advance()

        # return the statement
        return ReturnStatement()