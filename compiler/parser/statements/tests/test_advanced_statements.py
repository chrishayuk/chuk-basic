from ....lexer.token_type import TokenType
from ....lexer.tokenizer import Tokenizer
from ....ast.variable import Variable
from ....ast.expressions import BinaryExpression, Literal
from ....ast.statements import DimStatement
from ...parser import Parser

def test_parse_dim_statement_single_dimension():
    input_string = "DIM x(10)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    statement = program.statements[0]
    assert isinstance(statement, DimStatement)
    assert statement.variable.name == "x"  # Verify the variable name
    assert len(statement.dimensions) == 1  # Verify the number of dimensions
    assert isinstance(statement.dimensions[0], Literal)
    assert statement.dimensions[0].value == 10  # Verify the dimension size

def test_parse_dim_statement_multiple_dimensions():
    input_string = "DIM matrix(5, 10)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    statement = program.statements[0]
    assert isinstance(statement, DimStatement)
    assert statement.variable.name == "matrix"  # Verify the variable name
    assert len(statement.dimensions) == 2  # Verify the number of dimensions
    assert isinstance(statement.dimensions[0], Literal)
    assert statement.dimensions[0].value == 5  # Verify the first dimension size
    assert isinstance(statement.dimensions[1], Literal)
    assert statement.dimensions[1].value == 10  # Verify the second dimension size

def test_parse_dim_statement_with_expressions():
    input_string = "DIM FNarr(n + 1, 2 * m)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    statement = program.statements[0]
    assert isinstance(statement, DimStatement)
    assert statement.variable.name == "FNarr"  # Verify the function array name
    assert len(statement.dimensions) == 2  # Verify the number of dimensions

    # Verify the first dimension expression
    assert isinstance(statement.dimensions[0], BinaryExpression)
    assert statement.dimensions[0].operator.token_type == TokenType.PLUS
    assert isinstance(statement.dimensions[0].left, Variable)
    assert statement.dimensions[0].left.name == "n"
    assert isinstance(statement.dimensions[0].right, Literal)
    assert statement.dimensions[0].right.value == 1

    # Verify the second dimension expression
    assert isinstance(statement.dimensions[1], BinaryExpression)
    assert statement.dimensions[1].operator.token_type == TokenType.MUL
    assert isinstance(statement.dimensions[1].left, Literal)
    assert statement.dimensions[1].left.value == 2
    assert isinstance(statement.dimensions[1].right, Variable)
    assert statement.dimensions[1].right.name == "m"