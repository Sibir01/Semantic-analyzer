import re

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_pos = 0

        self.token_specification = [
            ('COMMENT_SINGLE', r'//[^\n]*'),
            ('COMMENT_MULTI', r'/\*.*?\*/'),
            ('KEYWORD', r'\b(public|class|int|if|else|return|void|for)\b'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER', r'\b\d+\b'),
            ('STRING', r'"[^"]*"'),
            ('OPERATOR', r'[+\-*/=<>!&|]'),
            ('DOT', r'\.'),
            ('LBRACE', r'{'),
            ('RBRACE', r'}'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACKET', r'\['),
            ('RBRACKET', r'\]'),
            ('SEMICOLON', r';'),
            ('COMMA', r','),
            ('COLON', r':'),
            ('QUESTION', r'\?'),
            ('SKIP', r'[ \t\n]+'),
            ('MISMATCH', r'.'),
        ]

        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification)

    def tokenize(self):
        for match in re.finditer(self.token_regex, self.code, re.DOTALL):
            kind = match.lastgroup
            value = match.group()
            if kind in {'SKIP', 'COMMENT_SINGLE', 'COMMENT_MULTI'}:
                continue
            elif kind == 'MISMATCH':
                raise ValueError(f"Неизвестный символ: {value}")
            else:
                self.tokens.append(Token(kind, value))

        return self.tokens

    def print_tokens(self):
        for token in self.tokens:
            print(token)
