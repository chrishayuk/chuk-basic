
from ....lexer.token_type import TokenType
from ....lexer.tokenizer import Tokenizer
from ....lexer.token import Token
from ....ast.ast_node import Variable
from ....ast.ast_statement import LetStatement, PrintStatement
from ....ast.ast_expression import BinaryExpression, FnExpression, Literal, UnaryExpression
from ...parser import Parser

def test_parse_literal_expression():
    input_string = "10 PRINT 42"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert isinstance(program.statements[0], PrintStatement)
    assert isinstance(program.statements[0].expression, Literal)
    assert program.statements[0].expression.value == 42


def test_parse_variable_expression():
    input_string = "10 LET x = 20"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    let_statement = program.statements[0]
    assert isinstance(let_statement, LetStatement)
    assert let_statement.variable.name == "x"
    assert isinstance(let_statement.expression, Literal)
    assert let_statement.expression.value == 20


def test_parse_binary_expression():
    input_string = "20 LET result = x + 5 * 3"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    let_statement = program.statements[0]
    assert isinstance(let_statement, LetStatement)
    assert isinstance(let_statement.expression, BinaryExpression)
    assert let_statement.expression.operator.token_type == TokenType.PLUS
    assert isinstance(let_statement.expression.left, Variable)
    assert let_statement.expression.left.name == "x"
    assert isinstance(let_statement.expression.right, BinaryExpression)
    assert let_statement.expression.right.operator.token_type == TokenType.MUL
    assert isinstance(let_statement.expression.right.left, Literal)
    assert let_statement.expression.right.left.value == 5
    assert isinstance(let_statement.expression.right.right, Literal)
    assert let_statement.expression.right.right.value == 3

def test_parse_unary_expression():
    input_string = "30 LET y = -x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.statements) == 1
    let_statement = program.statements[0]
    assert isinstance(let_statement, LetStatement)
    assert isinstance(let_statement.expression, UnaryExpression)
    assert isinstance(let_statement.expression.operand, Variable)
    assert let_statement.expression.operand.name == "x"


def test_parse_parenthesized_expression():
    input_string = "40 LET z = (x + 5) * 3"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    let_statement = program.statements[0]
    assert isinstance(let_statement, LetStatement)
    assert isinstance(let_statement.expression, BinaryExpression)
    assert let_statement.expression.operator.token_type == TokenType.MUL
    assert isinstance(let_statement.expression.left, BinaryExpression)
    assert let_statement.expression.left.operator.token_type == TokenType.PLUS
    assert isinstance(let_statement.expression.left.left, Variable)
    assert let_statement.expression.left.left.name == "x"
    assert isinstance(let_statement.expression.left.right, Literal)
    assert let_statement.expression.left.right.value == 5
    assert isinstance(let_statement.expression.right, Literal)
    assert let_statement.expression.right.value == 3

def test_parse_fn_expression():
    input_string = "10 PRINT FNSquare(5)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.statements) == 1
    print_statement = program.statements[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "Square"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 5



