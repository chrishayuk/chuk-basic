# import pytest

# from ...lexer.tokenizer import Tokenizer
# from ...ast.ast_node import Variable
# from ...ast.ast_expression import BinaryExpression, FnExpression, Literal
# from ...ast.ast_statement import LetStatement
# from ...ast.ast_control_flow import GotoStatement, IfStatement
# from ...ast.ast_function import DefStatement, FnEndStatement
# from ..statement_parser import parse_statement
# from ..parser import Parser

# def test_parse_single_line_def_statement():
#     """Test parsing a single-line function definition."""
#     input_string = "DEF FNSquare(x) = x * x"
#     tokenizer = Tokenizer(input_string)
#     tokens = tokenizer.tokenize()
#     parser = Parser(tokens)
#     statement = parse_statement(parser)

#     assert isinstance(statement, DefStatement)
#     assert statement.function_name.name == "FNSquare"
#     assert len(statement.parameters) == 1
#     assert isinstance(statement.parameters[0], Variable)
#     assert statement.parameters[0].name == "x"
#     assert isinstance(statement.function_body, BinaryExpression)

# def test_parse_multi_line_def_statement():
#     """Test parsing a multi-line function definition."""
#     input_string = "10 DEF FNM(X,Y)\n" \
#                    "20 LET FNM = X\n" \
#                    "30 IF Y <= X THEN 50\n" \
#                    "40 LET FNM = Y\n" \
#                    "50 FNEND\n"
#     tokenizer = Tokenizer(input_string)
#     tokens = tokenizer.tokenize()
#     parser = Parser(tokens)
#     statement = parse_statement(parser)

#     assert isinstance(statement, DefStatement)
#     assert statement.function_name.name == "FNM"
#     assert len(statement.parameters) == 2
#     assert isinstance(statement.parameters[0], Variable)
#     assert statement.parameters[0].name == "X"
#     assert isinstance(statement.parameters[1], Variable)
#     assert statement.parameters[1].name == "Y"
#     assert len(statement.function_body) == 4
#     assert isinstance(statement.function_body[0], LetStatement)
#     assert isinstance(statement.function_body[0].variable, Variable)
#     assert statement.function_body[0].variable.name == "FNM"
#     assert isinstance(statement.function_body[0].expression, Variable)
#     assert statement.function_body[0].expression.name == "X"
#     assert isinstance(statement.function_body[1], IfStatement)
#     assert isinstance(statement.function_body[1].condition, BinaryExpression)
#     assert isinstance(statement.function_body[1].then_statement, GotoStatement)
#     assert statement.function_body[1].then_statement.line_number == 50
#     assert isinstance(statement.function_body[2], LetStatement)
#     assert isinstance(statement.function_body[2].variable, Variable)
#     assert statement.function_body[2].variable.name == "FNM"
#     assert isinstance(statement.function_body[2].expression, Variable)
#     assert statement.function_body[2].expression.name == "Y"
#     assert isinstance(statement.function_body[3], FnEndStatement)

# def test_parse_function_call():
#     """Test parsing a function call."""
#     input_string = "LET y = FNSquare(5)"
#     tokenizer = Tokenizer(input_string)
#     tokens = tokenizer.tokenize()
#     parser = Parser(tokens)
#     statement = parse_statement(parser)

#     assert isinstance(statement, LetStatement)
#     assert isinstance(statement.expression, FnExpression)
#     assert statement.expression.name.name == "FNSquare"
#     assert isinstance(statement.expression.argument, Literal)
#     assert statement.expression.argument.value == 5

# def test_parse_nested_function_call():
#     """Test parsing a nested function call."""
#     input_string = "LET z = FNSum(FNSquare(2), FNSquare(3))"
#     tokenizer = Tokenizer(input_string)
#     tokens = tokenizer.tokenize()
#     parser = Parser(tokens)
#     statement = parse_statement(parser)

#     assert isinstance(statement, LetStatement)
#     assert isinstance(statement.expression, FnExpression)
#     assert statement.expression.name.name == "FNSum"
#     assert len(statement.expression.arguments) == 2
#     assert isinstance(statement.expression.arguments[0], FnExpression)
#     assert statement.expression.arguments[0].name.name == "FNSquare"
#     assert isinstance(statement.expression.arguments[0].arguments[0], Literal)
#     assert statement.expression.arguments[0].arguments[0].value == 2
#     assert isinstance(statement.expression.arguments[1], FnExpression)
#     assert statement.expression.arguments[1].name.name == "FNSquare"
#     assert isinstance(statement.expression.arguments[1].arguments[0], Literal)
#     assert statement.expression.arguments[1].arguments[0].value == 3

# def test_parse_invalid_def_statement():
#     """Test parsing an invalid function definition."""
#     input_string = "DEF FNSquare(x) x * x"
#     tokenizer = Tokenizer(input_string)
#     tokens = tokenizer.tokenize()
#     parser = Parser(tokens)

#     with pytest.raises(SyntaxError):
#         parse_statement(parser)

# def test_parse_invalid_function_call():
#     """Test parsing an invalid function call."""
#     input_string = "y = FNSquare()"
#     tokenizer = Tokenizer(input_string)
#     tokens = tokenizer.tokenize()
#     parser = Parser(tokens)

#     with pytest.raises(SyntaxError):
#         parse_statement(parser)