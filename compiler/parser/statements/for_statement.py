from ...lexer.token_type import TokenType
from ...ast.variable import Variable
from ...ast.statements import ForStatement, NextStatement
from .base_statement_parser import BaseStatementParser

class ForStatementParser(BaseStatementParser):
    def parse(self):
        """Parse a FOR loop statement from the token stream."""

        # Advance past 'FOR'
        self.parser.advance()

        # Parse the loop variable
        variable = self.parser.parse_variable()

        # Expect and advance past '='
        if self.parser.current_token.token_type != TokenType.EQ:
            raise SyntaxError("Expected '=' after variable in FOR statement")
        self.parser.advance()

        # Parse the start expression
        start_expression = self.parser.parse_expression()

        # Expect and advance past 'TO'
        if self.parser.current_token.token_type != TokenType.TO:
            raise SyntaxError("Expected 'TO' keyword after start expression in FOR statement")
        self.parser.advance()

        # Parse the end expression
        end_expression = self.parser.parse_expression()

        # Optionally parse the 'STEP' expression
        step_expression = self.parse_step_expression()

        # Parse the loop body
        loop_body = self.parse_loop_body()

        # Expect 'NEXT' and validate loop variable
        self.expect_next_keyword()
        next_variable = self.expect_loop_variable(variable.name)

        return ForStatement(variable, start_expression, end_expression, step_expression, loop_body, NextStatement(next_variable))

    def parse_step_expression(self):
        """Parse the STEP expression if present."""
        step_expression = None

        # check for STEP keyword
        if self.parser.current_token.token_type == TokenType.STEP:
            # Advance past 'STEP'
            self.parser.advance()

            # parse the step expression
            step_expression = self.parser.parse_expression()
        return step_expression

    def parse_loop_body(self):
        """Parse the loop body enclosed within the FOR-NEXT loop."""
        loop_body = []
        while self.parser.current_token.token_type != TokenType.NEXT:
            statement = self.parser.parse_statement()
            if statement:
                loop_body.append(statement)
            else:
                self.parser.advance()  # Ensure progress through tokens
        return loop_body

    def expect_next_keyword(self):
        """Ensure 'NEXT' token is present."""
        if self.parser.current_token.token_type != TokenType.NEXT:
            raise SyntaxError("Expected 'NEXT' keyword after FOR loop body")
        
        # Advance past 'NEXT'
        self.parser.advance()

    def expect_loop_variable(self, expected_variable_name):
        """Validate the loop variable matches the one declared with 'FOR'."""

        # check the next variable is a valid variable
        if self.parser.current_token.token_type != TokenType.IDENTIFIER or self.parser.current_token.value != expected_variable_name:
            raise SyntaxError(f"Expected loop variable '{expected_variable_name}' after 'NEXT', got '{self.parser.current_token.value}'")
        
        # get the Next Variable
        next_variable = Variable(self.parser.current_token.value)

        # Advance past the NEXT variable
        self.parser.advance()

        # return the next variable
        return next_variable
