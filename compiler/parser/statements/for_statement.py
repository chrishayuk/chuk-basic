from ...lexer.token_type import TokenType
from ...ast.statements import ForStatement, NextStatement
from .base_statement_parser import BaseStatementParser

class ForStatementParser(BaseStatementParser):
    def parse(self):
        """Parse a FOR loop statement from the token stream."""
        # Get the line number
        line_number = self.parser.line_number

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
        loop_body = self.parse_loop_body(variable)

        # Parse the NEXT statement
        next_statement = self.parse_next_statement(variable)

        # Return the ForStatement with the line number and NextStatement
        return ForStatement(variable, start_expression, end_expression, step_expression, loop_body, next_statement, line_number)

    def parse_step_expression(self):
        """Parse the STEP expression if present."""
        step_expression = None

        # Check for STEP keyword
        if self.parser.current_token.token_type == TokenType.STEP:
            # Advance past 'STEP'
            self.parser.advance()

            # Parse the step expression
            step_expression = self.parser.parse_expression()

        return step_expression

    def parse_loop_body(self, loop_variable):
        """Parse the loop body until the corresponding NEXT statement is encountered."""
        loop_body = []
        current_line_number = self.parser.line_number

        while self.parser.current_token:
            # Capture the current line number before parsing the statement
            current_line_number = self.parser.line_number

            # Check if the next token is a NEXT statement for the loop variable
            if self.parser.current_token.token_type == TokenType.NEXT:
                next_statement = self.parse_next_statement(loop_variable)
                if next_statement.variable.name == loop_variable.name:
                    break
                else:
                    raise SyntaxError(f"Unexpected NEXT statement: {next_statement}")

            # Parse the statement
            main_statement = self.parser.parse_statement()
            if main_statement:
                # Assign the captured line number to the statement
                main_statement.line_number = current_line_number
                loop_body.append(main_statement)

            self.parser.advance()

        else:
            raise SyntaxError("Unexpected end of input while parsing loop body")

        return loop_body

    def parse_next_statement(self, loop_variable):
        """Parse the NEXT statement associated with the loop variable."""
        next_statement = NextStatement(loop_variable, self.parser.line_number)

        # Advance past 'NEXT'
        self.parser.advance()

        # Check if there are more tokens available
        if self.parser.current_token is None:
            return next_statement

        # Parse the loop variable (should match the loop variable)
        parsed_variable = self.parser.parse_variable()

        # Check if the parsed variable is None (reached end of input)
        if parsed_variable is None:
            return next_statement

        print("parsed variable")
        print(parsed_variable)

        # Check for next statement
        if parsed_variable.name != loop_variable.name:
            raise SyntaxError(f"Expected NEXT statement for variable '{loop_variable.name}', but got '{parsed_variable.name}'")

        # Return next statement
        return next_statement
