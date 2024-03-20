from ast import *
from ..lexer.token_type import TokenType
from .expression_parser import parse_expression
from .ast import LetStatement, PrintStatement, Program, Variable

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.current_pos = 0

    def parse(self):
        self.current_token = self.tokens[self.current_pos]
        statements = []
        while self.current_token.token_type != TokenType.END:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            self.current_pos += 1
            if self.current_pos < len(self.tokens):
                self.current_token = self.tokens[self.current_pos]
        return Program(statements)

    def parse_statement(self):
        if self.current_token.token_type == TokenType.PRINT:
            self.current_pos += 1
            expression = parse_expression(self)
            return PrintStatement(expression)
        elif self.current_token.token_type == TokenType.LET:
            self.current_pos += 1
            variable = self.parse_variable()
            self.current_pos += 1  # Skip '='
            expression = parse_expression(self)
            return LetStatement(variable, expression)
        else:
            return None

    def parse_variable(self):
        token = self.tokens[self.current_pos]
        if token.token_type == TokenType.CHAR:
            self.current_pos += 1
            return Variable(token.value)
        else:
            return None