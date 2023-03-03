from __future__ import annotations
from dataclasses import dataclass, fields
import logging
from typing import Dict, Iterable, List, Union
from consts import SupportedDtype, BinaryOp
from label import Labels
from .quad_code import QuadCode
@dataclass
class AstNode:
    """ 
    This class implements a base AST node.
    It provides an interface to visit the node and all it's children recursively,
    and bind action to visitation of a property.
    Use the @before_visit and @after_visit decorators to bind a method to a property visitation order.
    """
    def __post_init__(self):
        """
        This method is called right after the construction of an inheriting dataclass instance.
        It is used here to initialize the bound methods to a property visitation order.
        """
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
        
        self._logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def _visit_child(val):
        """
        Visits a child property of the node, by it's name.
        """
        if isinstance(val, AstNode):
                val.visit()
        elif isinstance(val, Iterable) and not isinstance(val, str):
            for element in val:
                AstNode._visit_child(element)
    
    def visit(self):
        """ 
        Visits a node and all it's children recursively in field definition order,
        applying the methods bound to visitation order.
        visit() method is called for each instance of an AstNode object.
        visit() will also be called for each instance of AstNode inside an Iterable.
        """
        self.before()
        for field in fields(self):
            for func in self._bounds[field.name][0]:
                func()

            self._visit_child(getattr(self, field.name))
                
            for func in self._bounds[field.name][1]:
                func()
        self.after()

    @staticmethod
    def before_visit(prop_name: str):
        """ Decorate a function to be called before visiting a property of the node, by it's name. """
        def decorate(func):
            setattr(func, '__before_visit', getattr(func, '__before_visit', set()) | {prop_name})
            return func
        return decorate

    @staticmethod
    def after_visit(prop_name: str):
        """ Decorate a function to be called after visiting a property of the node, by it's name. """
        def decorate(func):
            setattr(func, '__after_visit', getattr(func, '__after_visit', set()) | {prop_name})
            return func
        return decorate
    
    def before(self):
        """ Called before visiting the node's children. """
        pass
    
    def after(self):
        """ Called after visiting the node's children. """
        pass

labels = Labels()
symbols: Dict[Identifier, SupportedDtype] = {}
code: QuadCode = QuadCode()

@dataclass
class Stmt(AstNode):
    pass

@dataclass
class AssignStmt(Stmt):
    id: Identifier
    expr: AstNode
    def after(self):
        if self.id not in symbols:
            self._logger.error(f"Undeclared variable {self.id}!")
        code.emit()
    
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