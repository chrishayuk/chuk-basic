# test_builtin_functions.py
import decimal
from ....lexer.tokenizer import Tokenizer
from ....ast.statements import PrintStatement
from ....ast.expressions import FnExpression, Literal
from ...parser import Parser

def test_parse_builtin_sin_function():
    input_string = "10 PRINT SIN(30)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[10]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "SIN"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 30

def test_parse_builtin_cos_function():
    input_string = "20 PRINT COS(45)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[20]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "COS"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 45

def test_parse_builtin_tan_function():
    input_string = "30 PRINT TAN(60)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[30]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "TAN"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 60

def test_parse_builtin_abs_function():
    input_string = "40 PRINT ABS(-10)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[40]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "ABS"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == -10

def test_parse_builtin_log_function():
    input_string = "50 PRINT LOG(10)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[50]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "LOG"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 10

def test_parse_builtin_exp_function():
    input_string = "60 PRINT EXP(2)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[60]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "EXP"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 2

def test_parse_builtin_sqr_function():
    input_string = "70 PRINT SQR(25)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[70]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "SQR"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 25

def test_parse_builtin_rnd_function():
    input_string = "90 PRINT RND(1)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[90]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "RND"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 1

def test_parse_builtin_atn_function():
    input_string = "100 PRINT ATN(45)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[100]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "ATN"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 45

def test_parse_builtin_chr_dollar_function():
    input_string = "110 PRINT CHR$(65)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[110]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "CHR$"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 65

def test_parse_builtin_left_dollar_function():
    input_string = "120 PRINT LEFT$(\"HELLO\", 2)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[120]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "LEFT$"
    assert len(fn_expression.arguments) == 2
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == "HELLO"
    assert isinstance(fn_expression.arguments[1], Literal)
    assert fn_expression.arguments[1].value == 2

def test_parse_builtin_right_dollar_function():
    input_string = "130 PRINT RIGHT$(\"HELLO\", 2)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[130]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "RIGHT$"
    assert len(fn_expression.arguments) == 2
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == "HELLO"
    assert isinstance(fn_expression.arguments[1], Literal)
    assert fn_expression.arguments[1].value == 2

def test_parse_builtin_mid_dollar_function():
    input_string = "140 PRINT MID$(\"HELLO\", 2, 3)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[140]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "MID$"
    assert len(fn_expression.arguments) == 3
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == "HELLO"
    assert isinstance(fn_expression.arguments[1], Literal)
    assert fn_expression.arguments[1].value == 2
    assert isinstance(fn_expression.arguments[2], Literal)
    assert fn_expression.arguments[2].value == 3

def test_parse_builtin_sgn_function():
    input_string = "150 PRINT SGN(-5)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[150]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "SGN"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == -5

def test_parse_builtin_spc_function():
    input_string = "180 PRINT SPC(5)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[180]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "SPC"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 5

def test_parse_builtin_tab_function():
    input_string = "190 PRINT TAB(10)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[190]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "TAB"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 10

def test_parse_builtin_int_function():
    input_string = "80 PRINT INT(3.14)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[80]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "INT"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)

    expected_value = decimal.Decimal('3.14')
    actual_value = fn_expression.arguments[0].value
    assert abs(actual_value.quantize(decimal.Decimal('1.00'), rounding=decimal.ROUND_HALF_UP) - expected_value) < decimal.Decimal('1e-9'), f"Expected {expected_value}, got {actual_value}"

def test_parse_builtin_val_function():
    input_string = "170 PRINT VAL(\"123.45\")"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[170]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "VAL"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)

    expected_value = decimal.Decimal('123.45')
    actual_value = fn_expression.arguments[0].value
    assert abs(actual_value.quantize(decimal.Decimal('1.00'), rounding=decimal.ROUND_HALF_UP) - expected_value) < decimal.Decimal('1e-9'), f"Expected {expected_value}, got {actual_value}"

def test_parse_builtin_str_dollar_function():
    input_string = "160 PRINT STR$(123.45)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.lines) == 1
    line = program.lines[160]
    assert len(line) == 1
    print_statement = line[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "STR$"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)

    expected_value = decimal.Decimal('123.45')
    actual_value = fn_expression.arguments[0].value
    assert abs(actual_value.quantize(decimal.Decimal('1.00'), rounding=decimal.ROUND_HALF_UP) - expected_value) < decimal.Decimal('1e-9'), f"Expected {expected_value}, got {actual_value}"

def test_parse_randomize_function():
    input_string = "RANDOMIZE(42)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    expression = parser.parse_expression()

    assert isinstance(expression, FnExpression)
    assert expression.name.name == "RANDOMIZE"
    assert len(expression.arguments) == 1
    assert isinstance(expression.arguments[0], Literal)
    assert expression.arguments[0].value == 42

