from ...ast.statements import RemStatement
from .base_statement_parser import BaseStatementParser


class RemStatementParser(BaseStatementParser):
    def parse(self):
        # Advance past 'REM'
        self.parser.advance()

        # get the comment
        comment = self.parser.current_token.value if self.parser.current_token else ""

        # Advance past the comment
        self.parser.advance()

        # return the statement
        return RemStatement(comment)