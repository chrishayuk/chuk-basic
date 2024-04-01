from typing import List, Optional

from ..lexer.token import Token
from ..lexer.token_type import TokenType
from ..ast.program import Program
from ..ast.variable import Variable
from ..ast.expressions import BinaryExpression, Expression, FnExpression
from ..ast.statements import Statement
from .statements import EndStatementParser, InputStatementParser, LetStatementParser, PrintStatementParser, RemStatementParser, ReturnStatementParser, StopStatementParser, IfStatementParser,ForStatementParser,NextStatementParser, GosubStatementParser, GotoStatementParser, OnStatementParser, DefStatementParser, DimStatementParser, ReadStatementParser
from .expressions import BinaryExpressionParser, PrimaryExpressionParser, UnaryExpressionParser 

class Parser:
    """A parser for the BASIC programming language, transforming a series of tokens into an abstract syntax tree."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_pos = 0
        self.line_number = 0
        self.current_token = self.tokens[self.current_pos] if self.tokens else None

    def advance(self):
        """Advance to the next token in the stream."""
        self.current_pos += 1

        # check the current position
        if self.current_pos < len(self.tokens):
            # advance the position
            self.current_token = self.tokens[self.current_pos]

            # Check and update line number if the current token is a line number
            if self.current_token.token_type == TokenType.LINENO:
                self.line_number = self.current_token.value
        else:
            # no current token
            self.current_token = None

    def peek_next_token(self) -> Optional[Token]:
        # Look ahead to the next token without consuming it
        next_pos = self.current_pos + 1
        if next_pos < len(self.tokens):
            return self.tokens[next_pos]
        return None
    
    def parse(self) -> Program:
        program = Program()

        while self.current_token:
            # Debug print current token and line number
            print(f"Current Token: {self.current_token}, Line Number: {self.line_number}")

            if self.current_token.token_type == TokenType.LINENO:
                self.line_number = int(self.current_token.value)
                print(f"Line number updated to {self.line_number}")
                self.advance()

            if not self.current_token:
                break

            # Capture the current line number before parsing the statement
            current_line_number = self.line_number

            statement = self.parse_statement()

            if statement:
                # Directly use the captured line number for the statement
                statement.line_number = current_line_number

                # Debug print for parsed statement
                print(f"Parsed Statement: {statement}, with Line Number: {getattr(statement, 'line_number', 'Not Set')}")

                if hasattr(statement, 'to_statements'):
                    for stmt_info in statement.to_statements():
                        line_number = stmt_info.get('line_number', self.line_number)
                        # Debug print for adding multi-line statement
                        print(f"Adding Multi-line Statement to Line {line_number}: {stmt_info['statement']}")
                        program.add_statement(line_number, stmt_info['statement'])
                else:
                    # Debug print for adding simple statement
                    print(f"Adding Statement to Line {statement.line_number}: {statement}")
                    program.add_statement(statement.line_number, statement)

            self.advance()

        print("Finished parsing.")
        return program





    def parse_variable(self) -> Variable:
        """Parse a variable from the current token."""
        if self.current_token is not None:
            if self.current_token.token_type == TokenType.IDENTIFIER:
                var_name = self.current_token.value
                self.advance()

                # Check for array indices
                if self.current_token is not None and self.current_token.token_type == TokenType.LPAREN:
                    self.advance()
                    indices = []

                    while self.current_token.token_type != TokenType.RPAREN:
                        index = self.parse_expression()
                        indices.append(index)

                        if self.current_token.token_type == TokenType.COMMA:
                            self.advance()
                        else:
                            break

                    if self.current_token.token_type != TokenType.RPAREN:
                        raise SyntaxError("Expected ')' after array indices")
                    self.advance()

                    return Variable(var_name, indices)

                return Variable(var_name)

            elif self.current_token.token_type == TokenType.FN:
                self.advance()
                if self.current_token is not None and self.current_token.token_type == TokenType.IDENTIFIER:
                    var_name = f"FN{self.current_token.value}"
                    self.advance()

                    # Check for function array indices
                    if self.current_token is not None and self.current_token.token_type == TokenType.LPAREN:
                        self.advance()
                        indices = []

                        while self.current_token.token_type != TokenType.RPAREN:
                            index = self.parse_expression()
                            indices.append(index)

                            if self.current_token.token_type == TokenType.COMMA:
                                self.advance()
                            else:
                                break

                        if self.current_token.token_type != TokenType.RPAREN:
                            raise SyntaxError("Expected ')' after function array indices")
                        self.advance()

                        return Variable(var_name, indices)

                    return Variable(var_name)

                else:
                    raise SyntaxError(f"Expected function name after 'FN', but got {self.current_token.token_type}")

            else:
                raise SyntaxError("Expected variable or function name, but got unexpected token")
            
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
                return GotoStatementParser(self).parse()
            elif next_token_type == TokenType.SUB:
                return GosubStatementParser(self).parse()
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
            TokenType.NEXT: NextStatementParser,
            TokenType.ON: OnStatementParser,
            # functions
            TokenType.DEF: DefStatementParser,
            # others
            TokenType.DIM: DimStatementParser,
            TokenType.READ: ReadStatementParser,
        }
        parser_class = statement_parsers.get(token_type)
        if parser_class:
            return parser_class(self).parse()

        # Return None if no matching parser is found
        return None

