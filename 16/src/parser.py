from __future__ import annotations

from typing import Dict, Iterable

from consts import QuadInstruction

from consts import QuadInstructionFetcher, QuadInstructionType
from sly import Parser
from lexer import CplLexer
from consts import SupportedDtype
from label import Labels

from dataclasses import dataclass, field


temp_counter: int = 0
def next_temp() -> int:
    global temp_counter
    temp_counter += 1
    return temp_counter

@dataclass
class TempVar:
    var_id: int = field(default_factory=next_temp)

@dataclass
class CplDeclaration:
    identifiers: Iterable[str]
    dtype: SupportedDtype
    
@dataclass
class Expression:
    target: TempVar
    
@dataclass
class NumericExpression(Expression):
    dtype: SupportedDtype
    
    def combine(self, other: NumericExpression) -> NumericExpression:
        return NumericExpression(TempVar(),
            SupportedDtype.FLOAT if self.dtype == SupportedDtype.FLOAT or \
                other.dtype == SupportedDtype.FLOAT else SupportedDtype.INT)

class CplParser(Parser):
    tokens = CplLexer.tokens
    
    @_('init declarations stmt_block')
    def program(self, p):
        pass
    
    @_('')
    def init(self, p):
        """ Constructs the symbol table. """
        self.symbol_table: Dict[str, SupportedDtype] = {}
        self.code = []
        self.code_counter = 0
        self.labels = Labels()

    def gen(self, inst: QuadInstruction, *args) -> int:
        self.code.append((inst, *args))
        self.code_counter += 1
        return self.code_counter
    
    def label(self, lbl: str):
        self.code.append((lbl + ":",))
    
    @_('declarations declaration', 'declaration')
    def declarations(self, p):
        declr: CplDeclaration = p[1] if len(p) == 2 else p[0]
        self.symbol_table[declr.identifiers] = declr.dtype
    
    @_('idlist ":" _type ";"')
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
        self.gen(inst, p[2])
    
    @_('OUTPUT "(" expr ")" ";"')
    def output_stmt(self, p):
        if p[2] not in self.symbol_table:
            raise ValueError(f'Undefined variable: {p[2]}!')
        inst = QuadInstructionFetcher.get_by1arg(QuadInstructionType.OUT, p[2])
        self.gen(inst, p[2])

    @_('')
    def _2labels(self, p):
        self.labels.enqueue(2)
    
    @_('')
    def _popgenlabel(self):
        lbl = self.labels.pop()
        self.label(lbl)
    
    @_('')
    def _dequeuelabel(self):
        self.labels.dequeue()
        
    @_('')
    def _poplabel(self):
        self.labels.pop()
    
    @_('')
    def _pushlabel(self):
        self.labels.enqueue()
    
    @_('')
    def _genlabel(self):
        self.label(self.labels[0])

    @_('')
    def _jump_to1(self, p):
        self.gen(QuadInstruction.JUMP, self.curr_labels[2])
        
    @_('')
    def _jump_to2(self, p):
        self.gen(QuadInstruction.JUMP, self.curr_labels[2])
        
    @_('')
    def _jmpz_to1(self, p):
        self.gen(QuadInstruction.JMPZ, self.curr_labels[0])

    @_('')
    def _jmpz_to2(self, p):
        self.gen(QuadInstruction.JMPZ, self.curr_labels[0])
    
    @_('IF _2labels "(" boolexpr _jmpz_to1 ")" stmt _jump_to2 ELSE _popgenlabel stmt _popgenlabel')
    def if_stmt(self, p):
        assert len(self.curr_labels) == 0
    
    # first label is to check boolean expression again and again, second is to exit loop
    @_('WHILE _2labels _genlabel "(" boolexpr ")" _jmpz_to_2 stmt _jump_to1 _dequeuelabel _popgenlabel')
    def while_stmt(self, p):
        assert len(self.curr_labels) == 0
    
    # Switch cast: expression has a target, it'll be stored in the class as a variable.
    # case will generate a label at it's end - we'll jump there in case of comparison failure.
    # to handle breaks, we'll be having a label at the top of the label stack during the whole expression.
    @_('SWITCH "(" expression ")" "{" caselist DEFAULT ":" stmtlist "}"')
    def switch_stmt(self, p):
        expression_target: TempVar = p[2].target
    
    @_('caselist _casenum ":" stmtlist _poplabel', "")
    def caselist(self, p):
        """ """
        pass
    
    @_("_pushlabel CASE NUM ")
    def _casenum(self, p):
        """ """
        self.gen(QuadInstructionFetcher.get_by1arg(QuadInstructionType.EQL, ))
        
    
    @_('BREAK ";"')
    def break_stmt(self, p):
        """ Break is a jump to the first label. Always. """
        self.gen(QuadInstruction.JUMP, self.curr_labels[0])
    
    @_("boolexpr OR boolterm", "boolterm")
    def boolexpr(self, p) -> Expression:
        pass    
    
    @_('boolterm AND boolfactor', "boolfactor")
    def boolterm(self, p) -> Expression:
        pass
    
    @_('NOT "(" boolexpr ")"', "expression RELOP expression")
    def boolfactor(self, p) -> Expression:
        pass
    
    @_('expression ADDOP term', 'term')
    def expression(self, p) -> NumericExpression:
        pass
    
    @_('term MULOP factor', 'factor')
    def term(self, p) -> NumericExpression:
        pass
    
    @_('"(" expression ")"', 'CAST "(" expression ")"', 'ID', 'NUM')
    def factor(self, p) -> NumericExpression:
        if p[0].value == "CAST":
            pass
