from typing import List, Optional
from contextlib import suppress
from ..lexer.token import Token
from ..lexer.token_type import TokenType
from ..ast.ast_node import Program, Variable
from ..ast.ast_expression import Expression
from .expression_parser import parse_expression as parse_top_level_expression
from ..lexer.token_type import TokenType
from .statements.end_statement import EndStatementParser
from .statements.input_statement import InputStatementParser
from .statements.let_statement import LetStatementParser
from .statements.print_statement import PrintStatementParser
from .statements.rem_statement import RemStatementParser
from .statements.return_statement import ReturnStatementParser
from .statements.stop_statement import StopStatementParser

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
        statements = []

        # loop through while we have tokens
        while self.current_token:
            # parse the end token
            statement = self.parse_statement()

            # append the end token
            if statement:
                statements.append(statement)

            # we got an end tokens
            if self.current_token and self.current_token.token_type == TokenType.END:
                # Exit the loop after processing the END statement
                break  
            else:
                # advance the token
                self.advance()

        # return the statements as a program
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
    
    def parse_basic_statement(self):
        token_type = self.current_token.token_type
        statement_parser = None

        # check the various statement types
        if token_type == TokenType.RETURN:
            statement_parser = ReturnStatementParser(self)
        elif token_type == TokenType.INPUT:
            statement_parser = InputStatementParser(self)
        elif token_type == TokenType.LET:
            statement_parser = LetStatementParser(self)
        elif token_type == TokenType.REM:
            statement_parser = RemStatementParser(self)
        elif token_type == TokenType.STOP:
            statement_parser = StopStatementParser(self)
        elif token_type == TokenType.PRINT:
            statement_parser = PrintStatementParser(self)
        elif token_type == TokenType.END:
            statement_parser = EndStatementParser(self)
        else:
            return None
        
        # parse
        return statement_parser.parse() if statement_parser else None
    

    def parse_statement(self):
        # get the current token type
        token_type = self.current_token.token_type

        # parse the statements
        #if token_type == TokenType.DEF:
        #    return parse_def_statement(parser)
        #else:
        #    # parse control statement
        #    basic = parse_control_flow_statement(parser)
        #    if basic is not None:
        #        return basic

        # parse basic statement
        basic = self.parse_basic_statement() 
        if basic is not None:
            return basic
            
        # not found
        return None