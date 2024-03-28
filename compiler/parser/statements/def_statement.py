from compiler.parser.statements.if_statement import IfStatementParser
from compiler.parser.statements.let_statement import LetStatementParser
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

        # Parse the parameter list
        parameters = []
        while self.parser.current_token.token_type != TokenType.RPAREN:
            parameter = self.parser.parse_variable()
            parameters.append(parameter)
            if self.parser.current_token.token_type == TokenType.COMMA:
                self.parser.advance()
            else:
                break

        # Expect the closing parenthesis
        if self.parser.current_token.token_type != TokenType.RPAREN:
            raise SyntaxError("Expected ')' after parameter list in DEF statement")
        self.parser.advance()

        # Check if the next token is an equal sign '='
        if self.parser.current_token.token_type == TokenType.EQ:
            # Single-line function definition
            self.parser.advance()  # Move past the equal sign
            function_body = self.parser.parse_expression()
            return DefStatement(function_name, parameters, [function_body])
        else:
            # Multi-line function definition
            function_body = self.parse_multi_line_function_body()

        # Construct and return the function definition
        return DefStatement(function_name, parameters, function_body)

    def parse_multi_line_function_body(self):
        """Parse the body of a multi-line function definition, expecting to end with 'FNEND'."""
        body = []
        while self.parser.current_token is not None and self.parser.current_token.token_type != TokenType.FNEND:
            # Skip line numbers and newlines until a valid statement or 'FNEND' is encountered
            while self.parser.current_token.token_type in [TokenType.LINENO, TokenType.NEWLINE]:
                self.parser.advance()

            # Check if 'FNEND' is encountered
            if self.parser.current_token.token_type == TokenType.FNEND:
                break

            # Parse the next statement in the function body
            if self.parser.current_token.token_type == TokenType.LET:
                statement = LetStatementParser(self.parser).parse()
            elif self.parser.current_token.token_type == TokenType.IF:
                statement = IfStatementParser(self.parser).parse(in_function_body=True)  # Pass in_function_body=True
            else:
                raise SyntaxError(f"Unexpected token '{self.parser.current_token.value}'  in function body")
            
            if statement:
                body.append(statement)

        # Ensure 'FNEND' is present to properly close the function definition
        if self.parser.current_token.token_type != TokenType.FNEND:
            raise SyntaxError("Expected 'FNEND' at the end of multi-line function definition")
        self.parser.advance()  # Move past 'FNEND'

        return body

