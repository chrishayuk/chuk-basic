from typing import List, Optional
from ..lexer.token import Token
from ..lexer.token_type import TokenType
from ..ast.program import Program
from ..ast.variable import Variable
from ..ast.expressions import BinaryExpression, Expression, FnExpression
from ..ast.statements import Statement
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
from .statements.def_statement import DefStatementParser
from .expressions.binary_expression import BinaryExpressionParser
from .expressions.primary_expression import PrimaryExpressionParser
from .expressions.unary_expression import UnaryExpressionParser 


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

    def peek_next_token(self) -> Optional[Token]:
        # Look ahead to the next token without consuming it
        next_pos = self.current_pos + 1
        if next_pos < len(self.tokens):
            return self.tokens[next_pos]
        return None

    def parse(self) -> Program:
        statements = []

        # loop through each token
        while self.current_token:
            # Debug print
            print(f"Current token: {self.current_token}")

            # check if we're a number
            if self.current_token.token_type == TokenType.NUMBER:
                # peek the next token
                next_token = self.peek_next_token()
                print(f"Next token: {next_token}")  # Debug print

                # if next token is a statement, skip on
                if next_token and next_token.token_type in [TokenType.DEF, TokenType.LET, TokenType.IF, TokenType.PRINT, ...]:
                    self.advance()
                    print(f"Advanced to token: {self.current_token}")  # Debug print

            # parse the statement
            statement = self.parse_statement()

            # if a statement
            if statement:
                # add the statement to the list
                statements.append(statement)

            # skip past the statement
            self.advance()

        # finished parsing
        print("Finished parsing.")

        # return the program
        return Program(statements)

    def parse_variable(self) -> Variable:
        """Parse a variable from the current token."""
        if self.current_token.token_type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            self.advance()
            return Variable(var_name)
        elif self.current_token.token_type == TokenType.FN:
            self.advance()
            if self.current_token.token_type == TokenType.IDENTIFIER:
                var_name = f"FN{self.current_token.value}"
                self.advance()
                return Variable(var_name)
            else:
                raise SyntaxError(f"Expected function name after 'FN', but got {self.current_token.token_type}")
        raise SyntaxError(f"Expected variable or function name, but got {self.current_token.token_type}")
        
    
    def parse_expression(self) -> Expression:
        """Parse an expression from the current token."""

        # Check if the current token is a unary operator
        if self.current_token and self.current_token.token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            # Parse a unary expression
            return UnaryExpressionParser(self).parse()

        # Parse a primary expression
        left_expression = PrimaryExpressionParser(self).parse()

        # Check if the left expression is a function expression
        if isinstance(left_expression, FnExpression):
            # Handle the case where a function expression is followed by a binary operator
            return self.parse_function_expression_with_binary_operator(left_expression)

        # Check if the current token is a binary operator
        while self.current_token and self.current_token.token_type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.POW,
            TokenType.AND, TokenType.OR,
            TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE
        ]:
            # Parse a binary expression
            left_expression = BinaryExpressionParser(self).parse(left_expression)

        return left_expression

    def parse_function_expression_with_binary_operator(self, function_expression):
        while self.current_token and self.current_token.token_type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.POW,
            TokenType.AND, TokenType.OR,
            TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE
        ]:
            operator = self.current_token
            self.advance()
            right_expression = PrimaryExpressionParser(self).parse()
            function_expression = BinaryExpression(function_expression, operator, right_expression)

        return function_expression

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
            # basic
            TokenType.RETURN: ReturnStatementParser,
            TokenType.INPUT: InputStatementParser,
            TokenType.LET: LetStatementParser,
            TokenType.REM: RemStatementParser,
            TokenType.STOP: StopStatementParser,
            TokenType.PRINT: PrintStatementParser,
            TokenType.END: EndStatementParser,
            # control flows
            TokenType.IF: IfStatementParser,
            TokenType.FOR: ForStatementParser,
            TokenType.ON: OnStatementParser,
            # functions
            TokenType.DEF: DefStatementParser,
        }
        parser_class = statement_parsers.get(token_type)
        if parser_class:
            return parser_class(self).parse()

        # Return None if no matching parser is found
        return None
