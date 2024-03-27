from ...ast.ast_statement import RemStatement
from .base_statement_parser import BaseStatementParser


class RemStatementParser(BaseStatementParser):
    def parse(self):
        # set the position
        self.parser.advance()

        # get the comment
        comment = self.parser.current_token.value if self.parser.current_token else ""

        # set the position
        self.parser.advance()

        # return the statement
        return RemStatement(comment)