from ast import *
from ..lexer.token_type import TokenType
from .expression_parser import parse_expression
from .statement_parser import parse_statement
from .ast import Program, Variable

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0
        self.current_token = self.tokens[self.current_pos] if self.tokens else None

    def advance(self):
        self.current_pos += 1
        if self.current_pos < len(self.tokens):
            self.current_token = self.tokens[self.current_pos]
        else:
            self.current_token = None

    def parse(self):
        self.current_token = self.tokens[self.current_pos]
        statements = []
        while self.current_token is not None and self.current_token.token_type != TokenType.END:
            statement = parse_statement(self)
            if statement:
                statements.append(statement)
            self.advance()
        return Program(statements)

    def parse_variable(self):
        token = self.current_token
        if token.token_type == TokenType.IDENTIFIER:
            self.advance()
            return Variable(token.value)
        else:
            raise SyntaxError(f"Expected variable, but got {token.token_type}")

    def parse_expression(self):
        return parse_expression(self)