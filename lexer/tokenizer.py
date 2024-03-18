import re
from lexer.token import Token
from lexer.token_type import TokenType

class TokenizationError(Exception):
    pass

class Tokenizer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.current_pos = 0

    def tokenize(self):
        # empty list of tokens
        tokens = []

        # loop from current position until end of string
        while self.current_pos < len(self.input_string):
            # get the next token
            token = self.get_next_token()

            # check if we got a token back
            if token:
                # append the token to the token list
                tokens.append(token)
            else:
                # skip any whitespace
                self.skip_whitespace()

                # check if we're at the end of the string
                if self.current_pos < len(self.input_string):
                    # unexpected character
                    raise TokenizationError(f"Unexpected character: {self.input_string[self.current_pos]}")
        return tokens

    def get_next_token(self):
        self.skip_whitespace()  # Skip leading whitespace

        if self.current_pos == 0 or self.input_string[self.current_pos - 1] == '\n':
            lineno_match = re.match(r'\d+', self.input_string[self.current_pos:])
            if lineno_match:
                self.current_pos += len(lineno_match.group(0))
                self.skip_whitespace()  # Skip whitespace after line number
                return Token(TokenType.LINENO, int(lineno_match.group(0)))

        string_match = re.match(r'"([^"]*)"', self.input_string[self.current_pos:])
        if string_match:
            self.current_pos += len(string_match.group(0))
            return Token(TokenType.STRING, string_match.group(1))

        rem_match = re.match(r'REM\s*(.*)', self.input_string[self.current_pos:], re.IGNORECASE)
        if rem_match:
            self.current_pos += len(rem_match.group(0))
            return Token(TokenType.REM, rem_match.group(1))

        data_match = re.match(r'DATA\s*(.*)', self.input_string[self.current_pos:], re.IGNORECASE)
        if data_match:
            self.current_pos += len(data_match.group(0))
            return Token(TokenType.DATA, data_match.group(1))

        for keyword, token_type in TokenType.get_keyword_token_map().items():
            if self.input_string[self.current_pos:].lower().startswith(keyword.lower()):
                self.current_pos += len(keyword)
                return Token(token_type, keyword)
            
        for library, token_type in TokenType.get_library_token_map().items():
            if self.input_string[self.current_pos:].lower().startswith(library.lower()):
                self.current_pos += len(library)
                return Token(token_type, library)
        
        for operator, token_type in TokenType.get_operator_token_map().items():
            if self.input_string[self.current_pos:].startswith(operator):
                self.current_pos += len(operator)
                return Token(token_type, operator)
        
        for punctuation, token_type in TokenType.get_punctuation_token_map().items():
            if self.input_string[self.current_pos:].startswith(punctuation):
                self.current_pos += len(punctuation)
                return Token(token_type, punctuation)

        number_match = re.match(r'\d+', self.input_string[self.current_pos:])
        if number_match:
            self.current_pos += len(number_match.group(0))
            return Token(TokenType.NUMBER, int(number_match.group(0)))

        char_match = re.match(r'[A-Za-z]', self.input_string[self.current_pos:])
        if char_match:
            self.current_pos += 1
            return Token(TokenType.CHAR, char_match.group(0))

        return None

    def skip_whitespace(self):
        # loops from current position until either we hit the end of the string, or until we hit a space
        while self.current_pos < len(self.input_string) and self.input_string[self.current_pos].isspace():
            # move the position along
            self.current_pos += 1