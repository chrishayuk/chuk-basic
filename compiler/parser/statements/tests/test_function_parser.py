import pytest

from ....lexer.tokenizer import Tokenizer
from ....ast.ast_node import Variable
from ....ast.ast_expression import BinaryExpression, FnExpression, Literal
from ....ast.ast_statement import LetStatement
from ....ast.ast_control_flow import GotoStatement, IfStatement
from ....ast.ast_function import DefStatement, FnEndStatement
from ...parser import Parser
from ...statements.def_statement import DefStatementParser

def test_parse_single_line_def_statement():
    """Test parsing a single-line function definition."""
    input_string = "DEF FNSquare(x) = x * x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = DefStatementParser(parser).parse()

    assert isinstance(statement, DefStatement)
    assert statement.function_name.name == "Square"
    assert len(statement.parameters) == 1
    assert isinstance(statement.parameters[0], Variable)
    assert statement.parameters[0].name == "x"
    assert isinstance(statement.function_body, list)
    assert len(statement.function_body) == 1
    assert isinstance(statement.function_body[0], BinaryExpression)

def test_parse_multi_line_def_statement():
    """Test parsing a multi-line function definition."""
    input_string = "10 DEF FNM(X,Y)\n" \
                   "20 LET FNM = X\n" \
                   "30 IF Y <= X THEN 50\n" \
                   "40 LET FNM = Y\n" \
                   "50 FNEND\n"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()  # Parse the entire program instead of directly invoking DefStatementParser

    # Assuming DEF statements are parsed and included in the program's statements,
    # you may need to adjust the logic below based on how DEF statements are actually incorporated into your AST
    # This is a simple way to find the first DEF statement parsed, if any
    def_statement = next((stmt for stmt in program.statements if isinstance(stmt, DefStatement)), None)

    # Now perform your assertions on def_statement to verify it was parsed correctly
    assert def_statement is not None, "No DEF statement parsed."
    assert def_statement.function_name.name == "M", "Incorrect function name."
    # Add more assertions as needed to validate the parsed DEF statement


def test_parse_invalid_def_statement():
    """Test parsing an invalid function definition."""
    input_string = "DEF FNSquare(x) x * x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)

    with pytest.raises(SyntaxError):
        DefStatementParser(parser).parse()