from __future__ import annotations
from dataclasses import dataclass, fields
import logging
from typing import Iterable, List, Union

from consts import QuadInstruction

from consts import QuadInstructionType

from consts import Dtype, BinaryOp
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

code: QuadCode = QuadCode()

@dataclass
class Stmt(AstNode):
    pass

@dataclass
class AssignStmt(Stmt):
    _id: Identifier
    expr: Expression

    def after(self):
        code.emit_op_dest(QuadInstructionType.ASN, self._id, (self.expr.val, self.expr.dtype))

@dataclass
class InputStmt(Stmt):
    id: Identifier
    def after(self):
        code.emit_op_dest(QuadInstructionType.INP, self.id)

@dataclass
class StmtList(AstNode):
    stmts: List[AstNode]

@dataclass
class OutputStmt(Stmt):
    expr: Expression
    def after(self):
        code.emit_op_dest(QuadInstructionType.PRT, self.expr.val)

@dataclass
class IfStmt(Stmt):
    bool_expr: BoolExpr
    
    @AstNode.after_visit('bool_expr')
    def after_boolexp(self):
        self.false_label = code.newlabel()
        code.emit(QuadInstruction.JMPZ, self.bool_expr.target, self.false_label)

    true_stmts: StmtList
    
    @AstNode.before_visit('false_stmts')
    def before_false(self):
        code.emitlabel(self.false_label)
    
    false_stmts: StmtList
    def after(self):
        code.emitlabel()
    
@dataclass
class WhileStmt(Stmt):
    def before(self):
        self.boolexp_label = code.newlabel()
        self.exit_label = code.newlabel()

    bool_expr: BoolExpr
    
    @AstNode.after_visit('bool_expr')
    def after_boolexp(self):
        code.emit(QuadInstruction.JMPZ, self.bool_expr.target, self.exit_label)
    
    stmts: StmtList
    
    def after(self):
        code.emit(QuadInstruction.JUMP, self.boolexp_label)
        code.emitlabel(self.exit_label)
    
@dataclass
class Case(AstNode):
    number: Number
    stmts: StmtList
    
    cmp_source: Identifier = None
    
    def before(self):
        code.emit_op_temp(QuadInstructionType.EQL, self.number, self.cmp_source)

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
    
    target: Identifier = None


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
    _type: Dtype

@dataclass
class CastExpression(AstNode):
    arg: Expression
    _to_type: Dtype

@dataclass
class Program(AstNode):
    declarations: Declarations
    stmts: StmtList

    @AstNode.after_visit("stmts")
    def print_hello(self):
        print("Hello!")

@dataclass
class Expression(AstNode):
    val: Union[BinaryOpExpression, Number, Identifier]
    dtype: Dtype

Number = Union[int, float]
Identifier = str