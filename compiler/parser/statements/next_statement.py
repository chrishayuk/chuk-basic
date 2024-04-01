from ...lexer.token_type import TokenType
from ...ast.variable import Variable
from ...ast.statements import NextStatement
from .base_statement_parser import BaseStatementParser

class NextStatementParser(BaseStatementParser):
    def parse(self):
        # Get the line number
        line_number = self.parser.line_number

        # Advance past 'NEXT'
        self.parser.advance()

        # Parse the loop variable
        variable = self.parser.parse_variable()

        # Return the NextStatement with the correct line number
        return NextStatement(variable, line_number)