from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from typing import List, Union
from consts import SupportedDtype, BinaryOp
@dataclass
class AstNode:
    pass

@dataclass
class Stmt(AstNode):
    pass

@dataclass
class AssignStmt(Stmt):
    id: Identifier
    expr: AstNode
    
@dataclass
class InputStmt(Stmt):
    id: Identifier

@dataclass
class StmtList(AstNode):
    stmts: List[AstNode]

@dataclass
class OutputStmt(Stmt):
    expr: Expression

@dataclass
class IfStmt(Stmt):
    bool_expr: BoolExpr
    true_stmts: StmtList
    false_stmts: StmtList
    
@dataclass
class WhileStmt(Stmt):
    bool_expr: BoolExpr
    stmts: StmtList
    
@dataclass
class Case(AstNode):
    number: Number
    stmts: StmtList

@dataclass
class SwitchStmt(Stmt):
    expr: Expression
    cases: List[Case]
    default: StmtList
    
@dataclass
class BreakStmt(Stmt):
    pass

@dataclass
class StmtList(AstNode):
    stmts: List[AstNode]

@dataclass
class BinaryOpExpression(AstNode):
    left: Expression
    right: Expression
    op: Identifier


@dataclass
class BoolExpr(AstNode):
    pass

@dataclass
class OpBoolExpr(BoolExpr):
    left: BoolExpr
    right: BoolExpr
    op: BinaryOp

@dataclass
class NotBoolExpr(BoolExpr):
    expr: BoolExpr

@dataclass
class Declarations(AstNode):
    declarations: List[Declaration]

@dataclass
class Declaration(AstNode):
    idlist: List[Identifier]
    _type: SupportedDtype

@dataclass
class CastExpression(AstNode):
    arg: Expression
    _to_type: SupportedDtype

@dataclass
class Program(AstNode):
    declarations: Declarations
    stmts: StmtList
    
Number = Union[int, float]
Identifier = str
Expression = Union[BinaryOpExpression, Number, Identifier]