from __future__ import annotations

from typing import List

from cpl_ast import Stmt

from consts import CplBinaryOp

from sly import Parser
from cpl_lexer import CplLexer
from consts import Dtype

from cpl_ast import Program, OpBoolExpr, BinaryOpExpression, BoolExpr, Expression,\
    IfStmt, WhileStmt, SwitchStmt, Case, BreakStmt, AssignStmt,\
        InputStmt, OutputStmt, Declarations, Declaration, NotBoolExpr, CastExpression

class CplParser(Parser):
    tokens = CplLexer.tokens
    
    start = 'program'
    
    @_('declarations stmt_block')
    def program(self, p):
        return Program(p[0], p[1])
    
    @_('declarations declaration', 'declaration')
    def declarations(self, p) -> Declarations:
        if len(p) == 1:
            return Declarations([p[0]])
        
        return Declarations(p[0].declarations + [p[1]])
    
    @_('idlist ":" _type ";"')
    def declaration(self, p) -> Declaration:
        return Declaration(p[0], p[2])
    
    @_('INT', 'FLOAT')
    def _type(self, p):
        if p[0] == 'int':
            return Dtype.INT
        elif p[0] == 'float':
            return Dtype.FLOAT
        raise ValueError(f'Unknown type: {p[0]}')
    
    @_('idlist "," ID')
    def idlist(self, p) -> List[str]:
        return p[0] + [p[2]]
        
    @_('ID')
    def idlist(self, p) -> List[str]:
        return [p[0]]
    
    @_('assign_stmt', 'input_stmt', 'output_stmt', 'if_stmt','while_stmt',
       'switch_stmt', 'break_stmt', 'stmt_block')
    def stmt(self, p):
        return p[0]
    
    @_('"{" stmtlist "}"')
    def stmt_block(self, p) -> List[Stmt]:
        return p[1]
    
    @_('stmtlist stmt', '')
    def stmtlist(self, p):
        if len(p) == 0:
            return []
        return p[0] + [p[1]]
    
    @_('ID "=" expression ";"')
    def assign_stmt(self, p) -> AssignStmt:
        return AssignStmt(p[0], p[2])
    
    @_('INPUT "(" ID ")" ";"')
    def input_stmt(self, p) -> InputStmt:
        return InputStmt(p[2])
    
    @_('OUTPUT "(" expression ")" ";"')
    def output_stmt(self, p) -> OutputStmt:
        return OutputStmt(p[2])
    
    @_('IF "(" boolexpr ")" stmt ELSE stmt')
    def if_stmt(self, p) -> IfStmt:
        return IfStmt(p[2], p[4], p[6])

    @_('WHILE "(" boolexpr ")" stmt')
    def while_stmt(self, p) -> WhileStmt:
        return WhileStmt(p[2], p[4])

    @_('SWITCH "(" expression ")" "{" caselist DEFAULT ":" stmtlist "}"')
    def switch_stmt(self, p) -> SwitchStmt:
        return SwitchStmt(p[2], p[5], p[8])
    
    @_('caselist CASE NUM ":" stmtlist', "")
    def caselist(self, p) -> List[Case]:
        """ """
        if len(p) == 0:
            return []
        return p[0] + [Case(p[2], p[4])]

    @_('BREAK ";"')
    def break_stmt(self, p) -> BreakStmt:
        """ Break is a jump to the first label. Always. """
        return BreakStmt()
    
    @_("boolexpr OR boolterm", "boolterm")
    def boolexpr(self, p) -> Expression:
        if len(p) == 1:
            return p[0]
        return OpBoolExpr(p[0], p[1], CplBinaryOp.OR)
    
    @_('boolterm AND boolfactor', "boolfactor")
    def boolterm(self, p) -> Expression:
        if len(p) == 1:
            return p[0]
        return OpBoolExpr(p[0], p[1], CplBinaryOp.AND)
    
    @_('NOT "(" boolexpr ")"', "expression RELOP expression")
    def boolfactor(self, p) -> BoolExpr:
        if len(p) == 4:
            return NotBoolExpr(p[2])
        return OpBoolExpr(p[0], p[2], p[1])
    
    @_('expression ADDOP term', 'term')
    def expression(self, p):
        if len(p) == 1:
            return p[0]
        return BinaryOpExpression(p[0], p[1], CplBinaryOp.ADD if p[1].value == '+' else CplBinaryOp.SUB)
    
    @_('term MULOP factor', 'factor')
    def term(self, p):
        if len(p) == 1:
            return p[0]
        return BinaryOpExpression(p[0], p[1], CplBinaryOp.MLT if p[1].value == '*' else CplBinaryOp.DIV)
    
    @_('"(" expression ")"', 'CAST "(" expression ")"', 'ID', 'NUM')
    def factor(self, p):
        if len(p) == 3:
            return p[1]
        elif len(p) == 4:
            return CastExpression(p[2], p[0])
        return p[0]