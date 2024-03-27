from ...lexer.token_type import TokenType
from ...ast.ast_node import Variable
from ...ast.ast_function import DefStatement
from .base_statement_parser import BaseStatementParser

class DefStatementParser(BaseStatementParser):
    def parse(self):
        # Expect the DEF keyword
        if self.parser.current_token.token_type != TokenType.DEF:
            raise SyntaxError("Expected 'DEF' keyword at the start of function definition")
        self.parser.advance()

        # Expect the FN keyword
        if self.parser.current_token.token_type != TokenType.FN:
            raise SyntaxError("Expected 'FN' keyword after 'DEF' in function definition")
        self.parser.advance()

        # Parse the function name
        if self.parser.current_token.token_type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function name after 'FN' in function definition")
        function_name = Variable(self.parser.current_token.value)
        self.parser.advance()

        # Expect the opening parenthesis
        if self.parser.current_token.token_type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after function name in function definition")
        self.parser.advance()

        # parse the parameter list
        parameters = []
        while self.parser.current_token.token_type != TokenType.RPAREN:
            parameter = self.parser.parse_variable()
            parameters.append(parameter)
            if self.parser.current_token.token_type == TokenType.COMMA:
                self.parser.advance()
            else:
                break

        # expect the closing parenthesis
        if self.parser.current_token.token_type != TokenType.RPAREN:
            raise SyntaxError("Expected ')' after parameter list in DEF statement")
        self.parser.advance()

        # expect the '=' sign or a newline
        if self.parser.current_token.token_type not in [TokenType.EQ, TokenType.NEWLINE]:
            raise SyntaxError("Expected '=' or newline after parameter list in DEF statement")

        # Initialize the function body container
        function_body = []

        # Handle the function body
        if self.parser.current_token.token_type == TokenType.EQ:
            # Handle single-line function definition
            self.parser.advance()
            expression = self.parser.parse_expression()
            function_body.append(expression)
        elif self.parser.current_token.token_type == TokenType.NEWLINE:
            # Handle multi-line function definition
            self.parser.advance()
            while self.parser.current_token is not None and self.parser.current_token.token_type != TokenType.FNEND:
                statement = self.parser.parse_expression()
                if statement is not None:
                    function_body.append(statement)
                # Advance only if the next token is NEWLINE, ensuring not to skip important tokens
                if self.parser.current_token is not None and self.parser.current_token.token_type == TokenType.NEWLINE:
                    self.parser.advance()

            # Expect the FNEND token for multi-line function definitions
            if self.parser.current_token is None or self.parser.current_token.token_type != TokenType.FNEND:
                raise SyntaxError("Expected 'FNEND' at the end of multi-line function definition")
            self.parser.advance()
        else:
            # This condition handles missing '=' or newline after the parameter list
            raise SyntaxError("Expected '=' or newline after parameter list in DEF statement")

        # Return the constructed function definition statement
        return DefStatement(function_name, parameters, function_body)