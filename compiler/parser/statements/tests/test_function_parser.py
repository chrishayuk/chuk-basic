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
    statement = DefStatementParser(parser).parse()

    assert isinstance(statement, DefStatement)
    assert statement.function_name.name == "M"
    assert len(statement.parameters) == 2
    assert isinstance(statement.parameters[0], Variable)
    assert statement.parameters[0].name == "X"
    assert isinstance(statement.parameters[1], Variable)
    assert statement.parameters[1].name == "Y"
    assert len(statement.function_body) == 4
    assert isinstance(statement.function_body[0], LetStatement)
    assert isinstance(statement.function_body[0].variable, Variable)
    assert statement.function_body[0].variable.name == "M"
    assert isinstance(statement.function_body[0].expression, Variable)
    assert statement.function_body[0].expression.name == "X"
    assert isinstance(statement.function_body[1], IfStatement)
    assert isinstance(statement.function_body[1].condition, BinaryExpression)
    assert isinstance(statement.function_body[1].then_statement, GotoStatement)
    assert statement.function_body[1].then_statement.line_number == 50
    assert isinstance(statement.function_body[2], LetStatement)
    assert isinstance(statement.function_body[2].variable, Variable)
    assert statement.function_body[2].variable.name == "M"
    assert isinstance(statement.function_body[2].expression, Variable)
    assert statement.function_body[2].expression.name == "Y"
    assert isinstance(statement.function_body[3], FnEndStatement)

def test_parse_invalid_def_statement():
    """Test parsing an invalid function definition."""
    input_string = "DEF FNSquare(x) x * x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)

    with pytest.raises(SyntaxError):
        DefStatementParser(parser).parse()