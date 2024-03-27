from ...ast.ast_statement import ReturnStatement
from .base_statement_parser import BaseStatementParser


class ReturnStatementParser(BaseStatementParser):
    def parse(self):
        # set the position
        self.parser.advance()

        # return the statement
        return ReturnStatement()