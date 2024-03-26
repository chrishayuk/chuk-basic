from ..tokenizer import Tokenizer
from ..token_type import TokenType

def test_empty_input():
    tokenizer = Tokenizer("")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 0

def test_line_number():
    tokenizer = Tokenizer("10 PRINT")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 2
    assert tokens[0].token_type == TokenType.LINENO
    assert tokens[0].value == 10
    assert tokens[1].token_type == TokenType.PRINT
    assert tokens[1].value == "PRINT"

def test_string_literal():
    tokenizer = Tokenizer('"Hello, world!"')
    tokens = tokenizer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].token_type == TokenType.STRING
    assert tokens[0].value == "Hello, world!"

def test_rem_statement():
    tokenizer = Tokenizer("REM This is a comment")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].token_type == TokenType.REM
    assert tokens[0].value == "This is a comment"

def test_data_statement():
    tokenizer = Tokenizer("DATA 1, 2, 3")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].token_type == TokenType.DATA
    assert tokens[0].value == "1, 2, 3"

def test_keywords():
    tokenizer = Tokenizer("PRINT LET IF THEN")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 4
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.LET
    assert tokens[2].token_type == TokenType.IF
    assert tokens[3].token_type == TokenType.THEN

def test_operators():
    tokenizer = Tokenizer("= <> <= < >= > + - * / ^")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 11
    assert tokens[0].token_type == TokenType.EQ
    assert tokens[1].token_type == TokenType.NE
    assert tokens[2].token_type == TokenType.LE
    assert tokens[3].token_type == TokenType.LT
    assert tokens[4].token_type == TokenType.GE
    assert tokens[5].token_type == TokenType.GT
    assert tokens[6].token_type == TokenType.PLUS
    assert tokens[7].token_type == TokenType.MINUS
    assert tokens[8].token_type == TokenType.MUL
    assert tokens[9].token_type == TokenType.DIV
    assert tokens[10].token_type == TokenType.POW

def test_punctuation():
    tokenizer = Tokenizer(", : ; ( ) $ %")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 7
    assert tokens[0].token_type == TokenType.COMMA
    assert tokens[1].token_type == TokenType.COLON
    assert tokens[2].token_type == TokenType.SEMI
    assert tokens[3].token_type == TokenType.LPAREN
    assert tokens[4].token_type == TokenType.RPAREN
    assert tokens[5].token_type == TokenType.DOLLAR
    assert tokens[6].token_type == TokenType.PERCENT

def test_numbers():
    # Test regular numbers
    tokenizer = Tokenizer("PRINT 123 456")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 3
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[1].value == 123
    assert tokens[2].token_type == TokenType.NUMBER
    assert tokens[2].value == 456

    # Test line numbers
    tokenizer = Tokenizer("10 PRINT 123\n20 PRINT 456")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 6
    assert tokens[0].token_type == TokenType.LINENO
    assert tokens[0].value == 10
    assert tokens[1].token_type == TokenType.PRINT
    assert tokens[2].token_type == TokenType.NUMBER
    assert tokens[2].value == 123
    assert tokens[3].token_type == TokenType.LINENO
    assert tokens[3].value == 20
    assert tokens[4].token_type == TokenType.PRINT
    assert tokens[5].token_type == TokenType.NUMBER
    assert tokens[5].value == 456

def test_identifiers():
    tokenizer = Tokenizer("variable1 variable2 x y")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 4
    assert tokens[0].token_type == TokenType.IDENTIFIER
    assert tokens[0].value == "variable1"
    assert tokens[1].token_type == TokenType.IDENTIFIER
    assert tokens[1].value == "variable2"
    assert tokens[2].token_type == TokenType.IDENTIFIER
    assert tokens[2].value == "x"
    assert tokens[3].token_type == TokenType.IDENTIFIER
    assert tokens[3].value == "y"

def test_library_functions():
    tokenizer = Tokenizer("SIN(0) COS(0) RND(1) LEFT$(A$, 3)")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 18
    assert tokens[0].token_type == TokenType.SIN
    assert tokens[1].token_type == TokenType.LPAREN
    assert tokens[2].token_type == TokenType.NUMBER
    assert tokens[2].value == 0
    assert tokens[3].token_type == TokenType.RPAREN
    assert tokens[4].token_type == TokenType.COS
    assert tokens[5].token_type == TokenType.LPAREN
    assert tokens[6].token_type == TokenType.NUMBER
    assert tokens[6].value == 0
    assert tokens[7].token_type == TokenType.RPAREN
    assert tokens[8].token_type == TokenType.RND
    assert tokens[9].token_type == TokenType.LPAREN
    assert tokens[10].token_type == TokenType.NUMBER
    assert tokens[10].value == 1
    assert tokens[11].token_type == TokenType.RPAREN
    assert tokens[12].token_type == TokenType.LEFT_DOLLAR
    assert tokens[13].token_type == TokenType.LPAREN
    assert tokens[14].token_type == TokenType.IDENTIFIER
    assert tokens[14].value == "A$"
    assert tokens[15].token_type == TokenType.COMMA
    assert tokens[16].token_type == TokenType.NUMBER
    assert tokens[16].value == 3
    assert tokens[17].token_type == TokenType.RPAREN

def test_def_keyword():
    tokenizer = Tokenizer("DEF FNSquare(X) = X * X")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 10
    assert tokens[0].token_type == TokenType.DEF
    assert tokens[1].token_type == TokenType.FN
    assert tokens[2].token_type == TokenType.IDENTIFIER
    assert tokens[2].value == "Square"
    assert tokens[3].token_type == TokenType.LPAREN
    assert tokens[4].token_type == TokenType.IDENTIFIER
    assert tokens[4].value == "X"
    assert tokens[5].token_type == TokenType.RPAREN
    assert tokens[6].token_type == TokenType.EQ
    assert tokens[7].token_type == TokenType.IDENTIFIER
    assert tokens[7].value == "X"
    assert tokens[8].token_type == TokenType.MUL
    assert tokens[9].token_type == TokenType.IDENTIFIER
    assert tokens[9].value == "X"

def test_fn_keyword():
    tokenizer = Tokenizer("PRINT FNSquare(5)")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 6
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.FN
    assert tokens[2].token_type == TokenType.IDENTIFIER
    assert tokens[2].value == "Square"    
    assert tokens[3].token_type == TokenType.LPAREN
    assert tokens[4].token_type == TokenType.NUMBER
    assert tokens[4].value == 5
    assert tokens[5].token_type == TokenType.RPAREN

def test_next_keyword():
    tokenizer = Tokenizer("10 FOR I = 1 TO 5\n20 PRINT I\n30 NEXT I")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 13
    assert tokens[0].token_type == TokenType.LINENO
    assert tokens[0].value == 10
    assert tokens[1].token_type == TokenType.FOR
    assert tokens[2].token_type == TokenType.IDENTIFIER
    assert tokens[2].value == "I"
    assert tokens[7].token_type == TokenType.LINENO
    assert tokens[7].value == 20
    assert tokens[10].token_type == TokenType.LINENO
    assert tokens[10].value == 30
    assert tokens[11].token_type == TokenType.NEXT
    assert tokens[12].token_type == TokenType.IDENTIFIER
    assert tokens[12].value == "I"

def test_end_keyword():
    tokenizer = Tokenizer("10 PRINT \"Hello\"\n20 END")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 5
    assert tokens[0].token_type == TokenType.LINENO
    assert tokens[0].value == 10
    assert tokens[1].token_type == TokenType.PRINT
    assert tokens[2].token_type == TokenType.STRING
    assert tokens[2].value == "Hello"
    assert tokens[3].token_type == TokenType.LINENO
    assert tokens[3].value == 20
    assert tokens[4].token_type == TokenType.END
    
def test_complex_program():
    # a representive BASIC program for testing
    program = '''
    10 PRINT "Hello, world!"
    20 LET X = 10
    30 IF X > 0 THEN PRINT "Positive"
    40 FOR I = 1 TO 5
    50   PRINT I
    60 NEXT I
    70 INPUT "Enter your name: "; NAME$
    80 PRINT "Hello, " + NAME$
    90 END
    '''

    # tokenize
    tokenizer = Tokenizer(program)

    # tokenize
    tokens = tokenizer.tokenize()

    # test
    assert len(tokens) == 41