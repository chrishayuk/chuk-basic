
from contextlib import suppress
from typing import List, Optional
from ..lexer.token_type import TokenType
from ..ast.ast_node import Variable
from ..ast.ast_expression import Expression
from ..ast.ast_statement import Statement
from ..ast.ast_control_flow import IfStatement, ForStatement, NextStatement, GotoStatement, GosubStatement, OnStatement
from .expression_parser import parse_expression
from ..parser.basic_statement_parser import parse_basic_statement

def parse_control_flow_statement(parser):
    # get the current token type
    token_type = parser.current_token.token_type

    # parse the control flow statements
    if token_type == TokenType.IF:
        return parse_if_statement(parser)
    elif token_type == TokenType.FOR:
        return parse_for_statement(parser)
    elif token_type == TokenType.GO:
        if parser.current_pos + 1 < len(parser.tokens) and parser.tokens[parser.current_pos + 1].token_type == TokenType.TO:
            return parse_goto_statement(parser)
        elif parser.current_pos + 1 < len(parser.tokens) and parser.tokens[parser.current_pos + 1].token_type == TokenType.SUB:
            return parse_gosub_statement(parser)
        else:
            raise SyntaxError("Expected 'TO' or 'SUB' keyword after 'GO'")
    elif token_type == TokenType.ON:
        return parse_on_statement(parser)
    else:
        return None
    
def parse_if_statement(parser) -> Optional[IfStatement]:
    """Parse an IF statement from the token stream."""
    # set the position
    parser.advance()

    # parse expression
    condition = parse_expression(parser)

    # skip the THEN keyword
    with suppress(StopIteration):
        if parser.current_token.token_type != TokenType.THEN:
            raise SyntaxError(
                f"Expected 'THEN' keyword after condition, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
            )
        parser.advance()

    # parse the THEN statement
    then_statement = parse_basic_statement(parser)
    if then_statement is None:
        raise SyntaxError("Expected a statement after 'THEN' keyword")

    # check if there is an ELSE clause
    else_statement = None
    if parser.current_token is not None and parser.current_token.token_type == TokenType.ELSE:
        # skip the ELSE keyword
        parser.advance()

        # parse the ELSE statement
        else_statement = parse_basic_statement(parser)
        if else_statement is None:
            raise SyntaxError("Expected a statement after 'ELSE' keyword")

    # if statement
    return IfStatement(condition, then_statement, else_statement)

def parse_for_statement(parser):
    """ Parse a FOR statement from the token stream. """
    # set the position
    parser.advance()

    # parse the for variable
    variable = parser.parse_variable()

    # expect the '=' token
    with suppress(StopIteration):
        if parser.current_token.token_type != TokenType.EQ:
            raise SyntaxError(
                f"Expected '=' after variable in FOR statement, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
            )
    parser.advance()

    # parse the start expression for the FOR keyword
    start_expression = parse_expression(parser)

    # expect the TO keyword
    with suppress(StopIteration):
        if parser.current_token.token_type != TokenType.TO:
            raise SyntaxError(
                f"Expected 'TO' keyword after start expression in FOR statement, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
            )
    parser.advance()

    # parse the TO expression
    end_expression = parse_expression(parser)

    # parse the step expression
    step_expression = parse_step_expression(parser)

    # parse the loop body
    loop_body = parse_loop_body(parser)

    # expect the NEXT keyword
    expect_next_keyword(parser)

    # expect the loop variable
    next_variable = expect_loop_variable(parser, variable.name)

    # create the NextStatement
    next_statement = NextStatement(next_variable)

    # return the for statement
    return ForStatement(variable, start_expression, end_expression, step_expression, loop_body, next_statement)

def parse_step_expression(parser) -> Optional[Expression]:
    """ Parse the step expression for a FOR statement """
    step_expression = None
    if parser.current_token.token_type == TokenType.STEP:
        # skip the step keyword
        parser.advance()

        # parse the step expression
        step_expression = parse_expression(parser)

    return step_expression

def parse_loop_body(parser) -> List[Statement]:
    """ Parse the loop body for a FOR statement. """
    loop_body: List[Statement] = []
    while parser.current_token.token_type != TokenType.NEXT:
        statement = parse_basic_statement(parser)
        if statement is not None:
            loop_body.append(statement)

    return loop_body

def expect_next_keyword(parser):
    """ Check if the current token is the NEXT keyword and raise a SyntaxError if it's not. """
    with suppress(StopIteration):
        if parser.current_token.token_type != TokenType.NEXT:
            raise SyntaxError(
                f"Expected 'NEXT' keyword after FOR loop body, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
            )
    parser.advance()

def expect_loop_variable(parser, expected_variable_name: str) -> Variable:
    """ Check if the current token is the expected loop variable and raise a SyntaxError if it's not. """
    # ensure we have an identifier
    with suppress(StopIteration):
        if parser.current_token.token_type != TokenType.IDENTIFIER or parser.current_token.value != expected_variable_name:
            raise SyntaxError(
                f"Expected loop variable '{expected_variable_name}' after 'NEXT' keyword, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
            )
    
    # parse and return return the next variable
    next_variable = Variable(parser.current_token.value)
    parser.advance()
    return next_variable

def parse_goto_statement(parser) -> GotoStatement:
    """ Parse a GOTO statement from the token stream. """
    # set the position
    parser.advance()

    # expect the TO keyword
    if parser.current_token.token_type != TokenType.TO:
        raise SyntaxError("Expected 'TO' keyword after 'GO'")

    # set the position
    parser.advance()

    # parse the line number for the GOTO
    line_number = parse_expression(parser)

    # retun the goto statement
    return GotoStatement(line_number)

def parse_gosub_statement(parser) -> GosubStatement:
    """ Parse a GOSUB statement from the token stream. """
    # set the position
    parser.advance()

    # expect the SUB keyword
    if parser.current_token.token_type != TokenType.SUB:
        raise SyntaxError("Expected 'SUB' keyword after 'GO'")
    
    # set the position
    parser.advance()

    # parse the line number for the GOSUB
    line_number = parse_expression(parser)

    # return the statement
    return GosubStatement(line_number)

def parse_on_statement(parser) -> OnStatement:
    """
    Parse an ON statement from the token stream.

    Args:
        parser (Parser): The parser instance.

    Returns:
        OnStatement: The parsed ON statement.

    Raises:
        SyntaxError: If the ON statement is not well-formed.
    """
    # set the position
    parser.advance()

    # parse the expression
    expression = parse_expression(parser)
    if expression is None:
        raise SyntaxError("Expected an expression after 'ON' keyword")

    # expect the GOTO or GOSUB keyword
    is_gosub = False
    if parser.current_token.token_type == TokenType.GO:
        parser.advance()
        if parser.current_token.token_type == TokenType.TO:
            is_gosub = False
        elif parser.current_token.token_type == TokenType.SUB:
            is_gosub = True
        else:
            raise SyntaxError("Expected 'TO' or 'SUB' keyword after 'GO' in ON statement")
        parser.advance()
    else:
        raise SyntaxError("Expected 'GOTO' or 'GOSUB' keyword after expression in ON statement")

    # parse the line numbers
    line_numbers = []
    if parser.current_token is not None:
        while parser.current_token.token_type != TokenType.NEWLINE:
            line_number = parse_expression(parser)
            if line_number is not None:
                line_numbers.append(line_number)
            if parser.current_token is not None and parser.current_token.token_type == TokenType.COMMA:
                parser.advance()
            else:
                break
    else:
        raise SyntaxError("Expected at least one line number after 'GOTO' or 'GOSUB' keyword in ON statement")

    return OnStatement(expression, line_numbers, is_gosub)
