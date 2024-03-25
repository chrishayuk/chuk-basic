from typing import List, Optional
from contextlib import suppress
from ..lexer.token import Token
from ..lexer.token_type import TokenType
from .ast.ast_node import Program, Variable
from .ast.ast_expression import Expression
from .expression_parser import parse_expression as parse_top_level_expression
from .statement_parser import parse_statement

class Parser:
    """A parser for the BASIC programming language."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_pos = 0
        self.current_token = self.tokens[self.current_pos] if self.tokens else None

    def advance(self):
        self.current_pos += 1
        if self.current_pos < len(self.tokens):
            self.current_token = self.tokens[self.current_pos]
        else:
            self.current_token = None

    def parse(self) -> Program:
        """Parse the token stream and return an AST representation."""
        self.current_token = self.tokens[self.current_pos]
        statements = []
        while self.current_token and self.current_token.token_type != TokenType.END:
            statement = parse_statement(self)
            if statement:
                statements.append(statement)
            self.advance()
        return Program(statements)

    def parse_top_level_expression(self) -> Optional[Expression]:
        """Parse and return the top-level expression in the token stream."""
        return parse_top_level_expression(self)
    
    def parse_variable(self):
        token = self.current_token
        if token.token_type == TokenType.IDENTIFIER:
            self.advance()
            return Variable(token.value)
        else:
            raise SyntaxError(f"Expected variable, but got {token.token_type}")