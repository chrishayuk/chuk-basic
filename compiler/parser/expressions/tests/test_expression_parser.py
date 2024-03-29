from ....lexer.token_type import TokenType
from ....lexer.tokenizer import Tokenizer
from ....ast.variable import Variable
from ....ast.statements import LetStatement, PrintStatement
from ....ast.expressions import BinaryExpression, FnExpression, Literal, UnaryExpression
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

def test_parse_binary_expression_with_mixed_operators_and_parentheses():
    input_string = "10 LET result = (x + 2) * (y - 3) / 4"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    let_statement = program.statements[0]
    assert isinstance(let_statement, LetStatement)
    assert isinstance(let_statement.expression, BinaryExpression)
    assert let_statement.expression.operator.token_type == TokenType.DIV

    left_expr = let_statement.expression.left
    assert isinstance(left_expr, BinaryExpression)
    assert left_expr.operator.token_type == TokenType.MUL
    assert isinstance(left_expr.left, BinaryExpression)
    assert left_expr.left.operator.token_type == TokenType.PLUS
    assert isinstance(left_expr.left.left, Variable)
    assert left_expr.left.left.name == "x"
    assert isinstance(left_expr.left.right, Literal)
    assert left_expr.left.right.value == 2
    assert isinstance(left_expr.right, BinaryExpression)
    assert left_expr.right.operator.token_type == TokenType.MINUS
    assert isinstance(left_expr.right.left, Variable)
    assert left_expr.right.left.name == "y"
    assert isinstance(left_expr.right.right, Literal)
    assert left_expr.right.right.value == 3

    assert isinstance(let_statement.expression.right, Literal)
    assert let_statement.expression.right.value == 4

def test_parse_binary_expression_with_string_operands():
    input_string = '40 PRINT "Hello" + " " + "World!"'
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    print_statement = program.statements[0]
    assert isinstance(print_statement, PrintStatement)
    assert isinstance(print_statement.expression, BinaryExpression)
    assert print_statement.expression.operator.token_type == TokenType.PLUS

    left_expr = print_statement.expression.left
    assert isinstance(left_expr, BinaryExpression)
    assert left_expr.operator.token_type == TokenType.PLUS
    assert isinstance(left_expr.left, Literal)
    assert left_expr.left.value == "Hello"
    assert isinstance(left_expr.right, Literal)
    assert left_expr.right.value == " "

    assert isinstance(print_statement.expression.right, Literal)
    assert print_statement.expression.right.value == "World!"

def test_parse_binary_expression_with_user_defined_function():
    input_string = '50 LET result = FNSquare(x) + FNDouble(y)'
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    let_statement = program.statements[0]
    assert isinstance(let_statement, LetStatement)
    assert isinstance(let_statement.expression, BinaryExpression)

    binary_expression = let_statement.expression
    assert binary_expression.operator.token_type == TokenType.PLUS

    left_expr = binary_expression.left
    assert isinstance(left_expr, FnExpression)
    assert left_expr.name.name == "Square"
    assert len(left_expr.arguments) == 1
    assert isinstance(left_expr.arguments[0], Variable)
    assert left_expr.arguments[0].name == "x"

    right_expr = binary_expression.right
    assert isinstance(right_expr, FnExpression)
    assert right_expr.name.name == "Double"
    assert len(right_expr.arguments) == 1
    assert isinstance(right_expr.arguments[0], Variable)
    assert right_expr.arguments[0].name == "y"
    
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

def test_parse_unary_expression_with_negative_literal():
    input_string = "10 PRINT -42"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    print_statement = program.statements[0]
    assert isinstance(print_statement, PrintStatement)
    assert isinstance(print_statement.expression, Literal)
    assert print_statement.expression.value == -42


def test_parse_unary_expression_with_parentheses():
    input_string = "20 LET x = -(y + 3)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    let_statement = program.statements[0]
    assert isinstance(let_statement, LetStatement)
    assert isinstance(let_statement.expression, UnaryExpression)
    assert let_statement.expression.operator.token_type == TokenType.MINUS
    assert isinstance(let_statement.expression.operand, BinaryExpression)
    assert let_statement.expression.operand.operator.token_type == TokenType.PLUS
    assert isinstance(let_statement.expression.operand.left, Variable)
    assert let_statement.expression.operand.left.name == "y"
    assert isinstance(let_statement.expression.operand.right, Literal)
    assert let_statement.expression.operand.right.value == 3

def test_parse_unary_expression_with_builtin_function():
    input_string = "30 PRINT -ABS(-10)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    print_statement = program.statements[0]
    assert isinstance(print_statement, PrintStatement)
    assert isinstance(print_statement.expression, UnaryExpression)
    assert print_statement.expression.operator.token_type == TokenType.MINUS
    assert isinstance(print_statement.expression.operand, FnExpression)
    assert print_statement.expression.operand.name.name == "ABS"
    assert len(print_statement.expression.operand.arguments) == 1
    assert isinstance(print_statement.expression.operand.arguments[0], Literal)
    assert print_statement.expression.operand.arguments[0].value == -10


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



