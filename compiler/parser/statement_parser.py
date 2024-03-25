from contextlib import suppress
from typing import Optional
from ..lexer.token_type import TokenType
from .ast.ast_node import Variable
from .ast.ast_statement import PrintStatement, ReturnStatement, LetStatement, RemStatement, InputStatement, EndStatement, StopStatement
from .ast.ast_control_flow import IfStatement, ForStatement, NextStatement, GotoStatement, GosubStatement
from .expression_parser import parse_expression, parse_fn_expression

def parse_statement(parser):
    # get the current token type
    token_type = parser.current_token.token_type

    # parse the statements
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
    elif token_type == TokenType.RETURN:
        return parse_return_statement(parser)
    elif token_type == TokenType.INPUT:
        return parse_input_statement(parser)
    elif token_type == TokenType.LET:
        return parse_let_statement(parser)
    elif token_type == TokenType.REM:
        return parse_rem_statement(parser)
    elif token_type == TokenType.STOP:
        return parse_stop_statement(parser)
    elif token_type == TokenType.PRINT:
        return parse_print_statement(parser)
    elif token_type == TokenType.DEF:
        return parse_def_statement(parser)
    elif token_type == TokenType.FN:
        return parse_fn_expression(parser)
    elif token_type == TokenType.END:
        return parse_end_statement(parser)
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
    then_statement = parse_statement(parser)
    if then_statement is None:
        raise SyntaxError("Expected a statement after 'THEN' keyword")

    # check if there is an ELSE clause
    else_statement = None
    if parser.current_token is not None and parser.current_token.token_type == TokenType.ELSE:
        # skip the ELSE keyword
        parser.advance()

        # parse the ELSE statement
        else_statement = parse_statement(parser)
        if else_statement is None:
            raise SyntaxError("Expected a statement after 'ELSE' keyword")

    # if statement
    return IfStatement(condition, then_statement, else_statement)

def parse_for_statement(parser):
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

    # check for STEP keyword
    step_expression = None
    if parser.current_token.token_type == TokenType.STEP:
        # skip the step keyword
        parser.advance()

        # parse the step expression
        step_expression = parse_expression(parser)

    # parse the loop body
    loop_body = parse_statement(parser)

    # expect the NEXT keyword
    with suppress(StopIteration):
        if parser.current_token.token_type != TokenType.NEXT:
            raise SyntaxError(
                f"Expected 'NEXT' keyword after FOR loop body, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
            )
    parser.advance()

    # expect the loop variable
    with suppress(StopIteration):
        if parser.current_token.token_type != TokenType.IDENTIFIER or parser.current_token.value != variable.name:
            raise SyntaxError(
                f"Expected loop variable '{variable.name}' after 'NEXT' keyword, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
            )
    next_variable = Variable(parser.current_token.value)
    parser.advance()

    # create the NextStatement
    next_statement = NextStatement(next_variable)

    # return the for statement
    return ForStatement(variable, start_expression, end_expression, step_expression, loop_body, next_statement)

def parse_next_statement(parser):
    # set the position
    parser.advance()

    # parse the variable
    variable = parser.parse_variable()

    # return the statement
    return NextStatement(variable)

def parse_goto_statement(parser):
    # set the position
    parser.advance()

    # expect the TO keyword
    if parser.current_token.token_type != TokenType.TO:
        raise SyntaxError("Expected 'TO' keyword after 'GO'")
    
    # set the position
    parser.advance()

    # parse the line number for the GOTO
    line_number = parse_expression(parser)

    # return the statement
    return GotoStatement(line_number)

def parse_gosub_statement(parser):
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

def parse_return_statement(parser):
    # set the position
    parser.advance()

    # return the statement
    return ReturnStatement()

def parse_input_statement(parser):
    # set the position
    parser.advance()

    # parse the variable
    variable = parser.parse_variable()

    # return the statement
    return InputStatement(variable)

def parse_let_statement(parser):
    # set the position
    parser.advance()
    
    # parse the variable
    variable = parser.parse_variable()

    # parse the expression
    parser.advance()  # skip '='
    expression = parse_expression(parser)

    # return the statement
    return LetStatement(variable, expression)

def parse_rem_statement(parser):
    # set the position
    parser.advance()

    # check we have a current token
    if parser.current_token is not None:
        # get the comment
        comment = parser.current_token.value

        # move to the next token
        parser.advance()  
    else:
        # empty comment
        comment = ""

    # return the statement
    return RemStatement(comment)

def parse_stop_statement(parser):
    # set the position
    parser.advance()

    # return the statement
    return StopStatement()

def parse_print_statement(parser):
    # set the position
    parser.advance()

    # parse the expression
    expression = parse_expression(parser)

    # return the statement
    return PrintStatement(expression)

def parse_end_statement(parser):
    # set the position
    parser.advance()

    # return the statement
    return EndStatement()

def parse_def_statement(parser):
    # set the position
    parser.advance()

    # parse the function name
    function_name = parser.parse_variable()

    # expect the opening parenthesis
    if parser.current_token.token_type != TokenType.LPAREN:
        raise SyntaxError("Expected '(' after function name in DEF statement")
    parser.advance()

    # parse the parameter list
    parameters = []
    while parser.current_token.token_type != TokenType.RPAREN:
        parameter = parser.parse_variable()
        parameters.append(parameter)
        if parser.current_token.token_type == TokenType.COMMA:
            parser.advance()
        else:
            break

    # expect the closing parenthesis
    if parser.current_token.token_type != TokenType.RPAREN:
        raise SyntaxError("Expected ')' after parameter list in DEF statement")
    parser.advance()

    # expect the '=' sign
    if parser.current_token.token_type != TokenType.EQ:
        raise SyntaxError("Expected '=' after parameter list in DEF statement")
    parser.advance()

    # parse the function body
    function_body = parse_expression(parser)

    # return the statement
    return DefStatement(function_name, parameters, function_body)