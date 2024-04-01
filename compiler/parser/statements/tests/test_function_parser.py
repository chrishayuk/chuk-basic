import pytest
from ...parser import Parser
from ....lexer.token_type import TokenType
from ....lexer.tokenizer import Tokenizer
from ....ast.variable import Variable
from ....ast.expressions import BinaryExpression
from ....ast.statements import DefStatement
from ....ast.statements import FnEndStatement
from ...statements.def_statement import DefStatementParser
from ...statements.let_statement import LetStatement
from ...statements.if_statement import IfStatement

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
    input_string = "10 DEF FNM(X,Y)\n" \
                   "20 LET FNM = X\n" \
                   "30 IF Y <= X THEN 50\n" \
                   "40 LET FNM = Y\n" \
                   "50 FNEND\n"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    # Output for debugging purposes
    for line_number, statements in program.lines.items():
        print(f"Line {line_number}: {statements}")

    # Check that the correct number of lines have been parsed
    assert len(program.lines) == 5, f"Expected 5 lines, got {len(program.lines)}"

    # Now check that each line number has the correct statement type and contents
    for line_number in [10, 20, 30, 40, 50]:
        assert line_number in program.lines, f"Line {line_number} is not in program.lines"

        # Get the statement(s) for the line
        statements = program.lines[line_number]

        # There should only be one statement per line for this test
        assert len(statements) == 1, f"Expected 1 statement on line {line_number}, got {len(statements)}"
        statement = statements[0]

        # Perform type-specific checks here
        if line_number == 10:
            assert isinstance(statement, DefStatement), f"Expected DefStatement on line {line_number}"
        elif line_number in [20, 40]:
            assert isinstance(statement, LetStatement), f"Expected LetStatement on line {line_number}"
        elif line_number == 30:
            assert isinstance(statement, IfStatement), f"Expected IfStatement on line {line_number}"
        elif line_number == 50:
            # This should be the end of the DEF statement; check for FNEND token or equivalent
            assert isinstance(statement, FnEndStatement), f"Expected FnEndStatement on line {line_number}"
def test_parse_invalid_def_statement():
    """Test parsing an invalid function definition."""
    input_string = "DEF FNSquare(x) x * x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)

    with pytest.raises(SyntaxError):
        DefStatementParser(parser).parse()