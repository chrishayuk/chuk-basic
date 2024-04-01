from ...lexer.token_type import TokenType
from ...ast.variable import Variable
from ...ast.statements import DefStatement
from .base_statement_parser import BaseStatementParser

class DefStatementParser(BaseStatementParser):
    def parse(self):
        # Capture the line number of the DEF statement
        def_line_number = self.parser.line_number

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
            function_body, fnend_line_number = self.parse_multi_line_function_body()

            # Construct and return the function definition
            def_statement = DefStatement(function_name, parameters, function_body)
            def_statement.line_number = def_line_number  # Set the line_number attribute to the DEF statement line number
            def_statement.fnend_line_number = fnend_line_number  # Set the fnend_line_number attribute
            return def_statement

    def parse_multi_line_function_body(self):
        """Parse the body of a multi-line function definition, expecting to end with 'FNEND'."""
        body = []
        fnend_line_number = None

        while True:
            if not self.parser.current_token:
                raise SyntaxError("Unexpected end of input while parsing function body")
            if self.parser.current_token.token_type == TokenType.FNEND:
                fnend_line_number = self.parser.line_number  # Capture the line number of FNEND
                self.parser.advance()  # Advance past 'FNEND'
                break

            # Capture the current line number before parsing the statement
            current_line_number = self.parser.line_number

            # Parse the statement
            statement = self.parser.parse_statement()
            if statement:
                # Assign the captured line number to the statement
                statement.line_number = current_line_number
                body.append(statement)

            self.parser.advance()

        return body, fnend_line_number