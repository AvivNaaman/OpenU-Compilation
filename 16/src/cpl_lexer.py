"""
A Module containing the lexer for the CPL language, using the SLY library.
The lexical values of the tokens are customized to support the AST generation using the parser.
"""

from __future__ import annotations

from consts import Dtype
from consts import CplBinaryOp
from sly import Lexer

class CplLexer(Lexer):
    def __init__(self):
        super().__init__()
        self.lineno = 1

    # type: ignore
    tokens = { NUM, IF, ELSE, WHILE, BREAK,
              SWITCH, CASE, DEFAULT, FLOAT, INT,
              INPUT, OUTPUT, RELOP, ADDOP, MULOP, OR,
              AND, NOT, CAST, ID }
    literals = { '=', ';', '(', ')', '{', '}', ',', ':' }
    ignore = ' \t'
    # Multi-line c-style comment with option to put anything inside /* */:
    ignore_comment = r'/\*(.|\n)*?\*/'
    
    # Define a rule so we can track line numbers
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)
    

    BREAK = r'break'
    CASE = r'case'
    DEFAULT = r'default'
    ELSE = r'else'
    FLOAT = r'float'
    IF = r'if'
    INPUT = r'input'
    INT = r'int'
    OUTPUT = r'output'
    SWITCH = r'switch'
    WHILE = r'while'
    
    OR = r'\|\|'
    AND = r'&&'
    
    @_(r'((=|!)=)|((<|>)=?)')
    def RELOP(self, t):
        t.value = CplBinaryOp(t.value)
        return t
    
    NOT = r'!'
    
    @_(r'\+|-')
    def ADDOP(self, t):
        t.value = CplBinaryOp(t.value)
        return t
    
    @_(r'\*|/')
    def MULOP(self, t):
        t.value = CplBinaryOp(t.value)
        return t
    
    @_(r'static_cast<\s*(int|float)\s*>')
    def CAST(self, t):
        t.value = Dtype(t.value[12:-1].strip())
        return t
    
    @_(r'\d+(\.\d+)?')
    def NUM(self, t):
        # A number if float <==> has a decimal point.
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
        super().error(t)