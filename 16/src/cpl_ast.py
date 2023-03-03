from __future__ import annotations
from dataclasses import dataclass, fields
from typing import Iterable, List, Union
from consts import SupportedDtype, BinaryOp

@dataclass
class AstNode:
    """ 
    This class implements a base AST node.
    """
    def __post_init__(self):
        self._bounds = {}
        for field in fields(self):
            self._bounds[field.name] = ([], [])
            
        for func in dir(self):
            if hasattr(getattr(self, func), '__before_visit'):
                for prop in getattr(getattr(self, func), '__before_visit'):
                    self._bounds[prop][0].append(getattr(self, func))
            if hasattr(getattr(self, func), '__after_visit'):
                for prop in getattr(getattr(self, func), '__after_visit'):
                    self._bounds[prop][1].append(getattr(self, func))

    def _visit_child(self, val):
        if isinstance(val, AstNode):
                val.visit()
        elif isinstance(val, Iterable) and not isinstance(val, str):
            for element in val:
                self._visit_child(element)
    
    def visit(self):
        for field in fields(self):
            for func in self._bounds[field.name][0]:
                func()

            self._visit_child(getattr(self, field.name))
                
            for func in self._bounds[field.name][1]:
                func()

    @staticmethod
    def before_visit(prop_name: str):
        def decorator(func):
            setattr(func, '__before_visit', getattr(func, '__before_visit', set()) | {prop_name})
            return func
        return decorator

    @staticmethod
    def after_visit(prop_name: str):
        def decorator(func):
            setattr(func, '__after_visit', getattr(func, '__after_visit', set()) | {prop_name})
            return func
        return decorator
    


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

    @AstNode.after_visit("stmts")
    def print_hello(self):
        print("Hello!")
    
Number = Union[int, float]
Identifier = str
Expression = Union[BinaryOpExpression, Number, Identifier]