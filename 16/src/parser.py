from typing import Dict, Iterable

from consts import QuadInstructionFetcher, QuadInstructionType
from sly import Parser
from lexer import CplLexer
from consts import SupportedDtype

from dataclasses import dataclass
@dataclass
class CplDeclaration:
    identifiers: Iterable[str]
    dtype: SupportedDtype

class CplParser(Parser):
    tokens = CplLexer.tokens
    
    @_('symbols declarations stmt_block')
    def program(self, p):
        pass
    
    @_('')
    def symbols(self, p):
        """ Constructs the symbol table. """
        self.symbol_table: Dict[str, SupportedDtype] = {}
    
    @_('declarations declaration', 'declaration')
    def declarations(self, p):
        declr: CplDeclaration = p[1] if len(p) == 2 else p[0]
        self.symbol_table[declr.identifiers] = declr.dtype
    
    @_('idlist ":" type ";"')
    def declaration(self, p):
        return CplDeclaration(p[0], p[2])
    
    @_('INT', 'FLOAT')
    def _type(self, p):
        if p[0] == 'int':
            return SupportedDtype.INT
        elif p[0] == 'float':
            return SupportedDtype.FLOAT
        raise ValueError(f'Unknown type: {p[0]}')
    
    @_('idlist "," ID')
    def idlist(self, p):
        p[0].append(p[2])
        return p[0]
        
    @_('ID')
    def idlist(self, p):
        return [p[0]]
    
    @_('assign_stmt', 'input_stmt', 'output_stmt', 'if_stmt','while_stmt',
       'switch_stmt', 'break_stmt', 'stmt_block')
    def stmt(self, p):
        pass
    
    @_('ID "=" expr ";"')
    def assign_stmt(self, p):
        pass
    
    @_('INPUT "(" ID ")" ";"')
    def input_stmt(self, p):
        if p[2] not in self.symbol_table:
            raise ValueError(f'Undefined variable: {p[2]}!')
        inst = QuadInstructionFetcher.get_by1arg(QuadInstructionType.INP, p[2])
    
    @_('OUTPUT "(" expr ")" ";"')
    def output_stmt(self, p):
        if p[2] not in self.symbol_table:
            raise ValueError(f'Undefined variable: {p[2]}!')
        inst = QuadInstructionFetcher.get_by1arg(QuadInstructionType.OUT, p[2])
    
    @_('IF "(" boolexpr ")" stmt ELSE stmt')
    def if_stmt(self, p):
        pass
    
    @_('WHILE "(" boolexpr ")" stmt')
    def while_stmt(self, p):
        pass
    
    @_('SWITCH "(" expression ")" "{" caselist DEFAULT ":" stmtlist "}"')
    def switch_stmt(self, p):
        pass
    
    @_('caselist CASE NUM ":" stmtlist', "")
    def caselist(self, p):
        pass
    
    @_('BREAK ";"')
    def break_stmt(self, p):
        pass
    
    @_("boolexpr OR boolterm", "boolterm")
    def boolexpr(self, p):
        pass    
    
    @_('boolterm AND boolfactor', "boolfactor")
    def boolterm(self, p):
        pass
    
    @_('NOT "(" boolexpr ")"', "expression RELOP expression")
    def boolfactor(self, p):
        pass
    
    @_('expression ADDOP term', 'term')
    def expression(self, p):
        pass
    
    @_('term MULOP factor', 'factor')
    def term(self, p):
        pass
    
    @_('"(" expression ")"', 'CAST "(" expression ")"', 'ID', 'NUM')
    def factor(self, p):
        pass