from typing import List, Optional

from ..lexer.token import Token
from ..lexer.token_type import TokenType
from ..ast.ast_node import Program, Variable
from ..ast.ast_expression import Expression
from ..ast.ast_statement import Statement
# Ensure all statement and control flow statement parsers are correctly imported
from .statements.end_statement import EndStatementParser
from .statements.input_statement import InputStatementParser
from .statements.let_statement import LetStatementParser
from .statements.print_statement import PrintStatementParser
from .statements.rem_statement import RemStatementParser
from .statements.return_statement import ReturnStatementParser
from .statements.stop_statement import StopStatementParser
from .statements.if_statement import IfStatementParser
from .statements.for_statement import ForStatementParser
from .statements.gosub_statement import GoSubStatementParser
from .statements.goto_statement import GoToStatementParser
from .statements.on_statement import OnStatementParser


class Parser:
    """A parser for the BASIC programming language, transforming a series of tokens into an abstract syntax tree."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_pos = 0
        self.current_token = self.tokens[self.current_pos] if self.tokens else None

    def advance(self):
        """Advance to the next token in the stream."""
        self.current_pos += 1
        self.current_token = self.tokens[self.current_pos] if self.current_pos < len(self.tokens) else None

    def parse(self) -> Program:
        """Parse the token stream to generate a Program AST node."""
        statements = []
        while self.current_token:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            self.advance()  # Always advance at the end of the loop
        return Program(statements)

    def parse_variable(self) -> Variable:
        """Parse a variable from the current token."""
        if self.current_token.token_type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            self.advance()
            return Variable(var_name)
        raise SyntaxError(f"Expected variable, but got {self.current_token.token_type}")

    def parse_statement(self) -> Optional[Statement]:
        """Parse a single statement from the current token."""
        token_type = self.current_token.token_type
        
        # Special handling for GOTO and GOSUB statements
        if token_type == TokenType.GO:
            # Look ahead to the next token to decide if it's GOTO or GOSUB
            next_token_type = self.tokens[self.current_pos + 1].token_type if self.current_pos + 1 < len(self.tokens) else None
            if next_token_type == TokenType.TO:
                return GoToStatementParser(self).parse()
            elif next_token_type == TokenType.SUB:
                return GoSubStatementParser(self).parse()
            else:
                raise SyntaxError("Expected 'TO' or 'SUB' after 'GO'")

        # Basic and other control flow statements parsing
        statement_parsers = {
            TokenType.RETURN: ReturnStatementParser,
            TokenType.INPUT: InputStatementParser,
            TokenType.LET: LetStatementParser,
            TokenType.REM: RemStatementParser,
            TokenType.STOP: StopStatementParser,
            TokenType.PRINT: PrintStatementParser,
            TokenType.END: EndStatementParser,
            TokenType.IF: IfStatementParser,
            TokenType.FOR: ForStatementParser,
            TokenType.ON: OnStatementParser,
            # Additional control flow or other statements can be added here
        }
        parser_class = statement_parsers.get(token_type)
        if parser_class:
            return parser_class(self).parse()

        # Return None if no matching parser is found
        return None
