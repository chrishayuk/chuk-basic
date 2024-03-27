
# from contextlib import suppress
# from typing import List, Optional
# from ..lexer.token_type import TokenType
# from ..ast.ast_node import Variable
# from ..ast.ast_expression import Expression
# from ..ast.ast_statement import Statement
# from ..ast.ast_control_flow import IfStatement, ForStatement, NextStatement, GotoStatement, GosubStatement, OnStatement
# from .expression_parser import parse_expression
# from ..parser.basic_statement_parser import parse_basic_statement

# def parse_control_flow_statement(parser):
#     """ Handler for controlling control flow statements such as IF..THEN..ELSE, FOR..STEP..NEXT, GO..TO, GO..SUB, ON """

#     # get the current token type
#     token_type = parser.current_token.token_type

#     # parse the control flow statements
#     if token_type == TokenType.FOR:
#         return parse_for_statement(parser)
#     else:
#         return None
    

# def parse_for_statement(parser):
#     """ Parse a FOR statement from the token stream. """
#     # set the position
#     parser.advance()

#     # parse the for variable
#     variable = parser.parse_variable()

#     # expect the '=' token
#     with suppress(StopIteration):
#         if parser.current_token.token_type != TokenType.EQ:
#             raise SyntaxError(
#                 f"Expected '=' after variable in FOR statement, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
#             )
#     parser.advance()

#     # parse the start expression for the FOR keyword
#     start_expression = parse_expression(parser)

#     # expect the TO keyword
#     with suppress(StopIteration):
#         if parser.current_token.token_type != TokenType.TO:
#             raise SyntaxError(
#                 f"Expected 'TO' keyword after start expression in FOR statement, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
#             )
#     parser.advance()

#     # parse the TO expression
#     end_expression = parse_expression(parser)

#     # parse the step expression
#     step_expression = parse_step_expression(parser)

#     # parse the loop body
#     loop_body = parse_loop_body(parser)

#     # expect the NEXT keyword
#     expect_next_keyword(parser)

#     # expect the loop variable
#     next_variable = expect_loop_variable(parser, variable.name)

#     # create the NextStatement
#     next_statement = NextStatement(next_variable)

#     # return the for statement
#     return ForStatement(variable, start_expression, end_expression, step_expression, loop_body, next_statement)

# def parse_step_expression(parser) -> Optional[Expression]:
#     """ Parse the step expression for a FOR statement """
#     step_expression = None
#     if parser.current_token.token_type == TokenType.STEP:
#         # skip the step keyword
#         parser.advance()

#         # parse the step expression
#         step_expression = parse_expression(parser)

#     return step_expression

# def parse_loop_body(parser) -> List[Statement]:
#     """ Parse the loop body for a FOR statement. """
#     loop_body: List[Statement] = []
#     while parser.current_token.token_type != TokenType.NEXT:
#         statement = parse_basic_statement(parser)
#         if statement is not None:
#             loop_body.append(statement)

#     return loop_body

# def expect_next_keyword(parser):
#     """ Check if the current token is the NEXT keyword and raise a SyntaxError if it's not. """
#     with suppress(StopIteration):
#         if parser.current_token.token_type != TokenType.NEXT:
#             raise SyntaxError(
#                 f"Expected 'NEXT' keyword after FOR loop body, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
#             )
#     parser.advance()

# def expect_loop_variable(parser, expected_variable_name: str) -> Variable:
#     """ Check if the current token is the expected loop variable and raise a SyntaxError if it's not. """
#     # ensure we have an identifier
#     with suppress(StopIteration):
#         if parser.current_token.token_type != TokenType.IDENTIFIER or parser.current_token.value != expected_variable_name:
#             raise SyntaxError(
#                 f"Expected loop variable '{expected_variable_name}' after 'NEXT' keyword, but got '{parser.current_token.value}' ({parser.current_token.token_type})"
#             )
    
#     # parse and return return the next variable
#     next_variable = Variable(parser.current_token.value)
#     parser.advance()
#     return next_variable