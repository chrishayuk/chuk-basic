from ..lexer.token_type import TokenType
from ..ast.ast_node import Variable
from ..ast.ast_function import DefStatement
from .basic_statement_parser import parse_basic_statement
from .expression_parser import parse_expression


def parse_def_statement(parser):
    # set the position
    parser.advance()

    # parse the function name
    if parser.current_token.token_type != TokenType.FN:
        raise SyntaxError("Expected 'FN' prefix before function name in DEF statement")
    parser.advance()
    function_name = Variable(f"FN{parser.current_token.value}")
    parser.advance()

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

    # expect the '=' sign or a newline
    print(parser.current_token.token_type)
    if parser.current_token.token_type not in [TokenType.EQ, TokenType.NEWLINE]:
        raise SyntaxError("Expected '=' or newline after parameter list in DEF statement")

    # Initialize the function body container
    function_body = []

    # Handle the function body
    if parser.current_token.token_type == TokenType.EQ:
        # Handle single-line function definition
        parser.advance()
        expression = parse_expression(parser)  # Parses the expression right after '='
        function_body.append(expression)
    elif parser.current_token.token_type == TokenType.NEWLINE:
        # Handle multi-line function definition
        parser.advance()
        while parser.current_token is not None and parser.current_token.token_type != TokenType.FNEND:
            statement = parse_basic_statement(parser)  # Parses statements until FNEND
            if statement is not None:
                function_body.append(statement)
            # Advance only if the next token is NEWLINE, ensuring not to skip important tokens
            if parser.current_token is not None and parser.current_token.token_type == TokenType.NEWLINE:
                parser.advance()
            else:
                # This else statement was causing an early break from the loop
                # Removed to ensure the loop continues until FNEND or file end
                pass

        # Expect the FNEND token for multi-line function definitions
        if parser.current_token is None or parser.current_token.token_type != TokenType.FNEND:
            raise SyntaxError("Expected 'FNEND' at the end of multi-line function definition")
        parser.advance()
    else:
        # This condition handles missing '=' or newline after the parameter list
        raise SyntaxError("Expected '=' or newline after parameter list in DEF statement")

    # Return the constructed function definition statement
    return DefStatement(function_name, parameters, function_body)