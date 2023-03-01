from sly import Lexer

class CplLexer(Lexer):
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
    
    RELOP = r'==|!=|<=|>=|<|>'
    ADDOP = r'\+|-'
    MULOP = r'\*|/'
    
    OR = r'\|\|'
    AND = r'&&'
    NOT = r'!'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    @_(r'static_cast<\s*(int|float)\s*>')
    def CAST(self, t):
        t.value = t.value[14:-2].strip()
        return t
    
    @_(r'\d+\(\.\d+)?)')
    def NUM(self, t):
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
    
    tokens = { ID, NUM, IF, ELSE, WHILE, BREAK,
              SWITCH, CASE, DEFAULT, FLOAT, INT,
              INPUT, OUTPUT, RELOP, ADDOP, MULOP, OR,
              AND, NOT, CAST }
    literals = { '=', ';', '(', ')', '{', '}', ',', ':' }
    ignore = ' \t'
    ignore_comment = r'/\*.*?\*/'
    