from enum import Enum

class TokenType(Enum):
    # identifiers
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    CHAR = 'CHAR'
    LINENO = 'LINENO'
    IDENTIFIER = 'IDENTIFIER'

    # punctuation
    COMMA = ','
    COLON = ':'
    SEMI = ';'
    LPAREN = '('
    RPAREN = ')'
    DOLLAR = '$'
    PERCENT = '%'

    # operators
    EQ = '='
    NE = '<>'
    LE = '<='
    LT = '<'
    GE = '>='
    GT = '>'
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    POW = '^'
    DOT = '.'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'

    # Keywords
    LET = 'LET'
    READ = 'READ'
    DATA = 'DATA'
    PRINT = 'PRINT'
    GO = 'GO'
    TO = 'TO'
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    FOR = 'FOR'
    NEXT = 'NEXT'
    END = 'END'
    STOP = 'STOP'
    DEF = 'DEF'
    SUB = 'SUB'
    RETURN = 'RETURN'
    DIM = 'DIM'
    REM = 'REM'
    ON = 'ON'
    STEP = 'STEP'
    FN = 'FN'
    PRINT_QUESTION = '?'
    INPUT = 'INPUT'
    RANDOMIZE = 'RANDOMIZE'
    RESTORE = 'RESTORE'

    # Library Functions
    SIN = 'SIN'
    COS = 'COS'
    ATN = 'ATN'
    INT = 'INT'
    TAN = 'TAN'
    EXP = 'EXP'
    ABS = 'ABS'
    LOG = 'LOG'
    SQR = 'SQR'
    RND = 'RND'
    CHR_DOLLAR = 'CHR$'
    LEFT_DOLLAR = 'LEFT$'
    RIGHT_DOLLAR = 'RIGHT$'
    MID_DOLLAR = 'MID$'
    SGN = 'SGN'
    STR_DOLLAR = 'STR$'
    VAL = 'VAL'
    SPC = 'SPC'
    TAB = 'TAB'

    @staticmethod
    def get_keyword_token_map():
        return {token.value: token for token in TokenType if token.value.isalpha() and token.value.isupper() and token.value not in TokenType.get_library_token_map()}

    @staticmethod
    def get_operator_token_map():
        return {token.value: token for token in TokenType if not token.value.isalpha() and not token.value.isalnum() and token.value not in TokenType.get_punctuation_token_map()}

    @staticmethod
    def get_punctuation_token_map():
        return {token.value: token for token in TokenType if len(token.value) == 1 and not token.value.isalnum()}

    @staticmethod
    def get_library_token_map():
        return {token.value: token for token in TokenType if token.value.isalpha() and token.value.isupper() and token.name.endswith('_DOLLAR') or token.name in ['SIN', 'COS', 'ATN', 'INT', 'TAN', 'EXP', 'ABS', 'LOG', 'SQR', 'RND', 'SGN', 'VAL', 'SPC']}