from __future__ import annotations
from dataclasses import dataclass, fields
import logging
from typing import Iterable, List, Union, Optional

from consts import QuadInstruction, QuadInstructionType, Dtype, CplBinaryOp
from quad_code import QuadCode

RECOVER_FROM_ERROR = False

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
        self._success = True
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
    
    @property
    def success(self) -> bool:
        """ 
        This property is used to check if the semantic analysis was successful.
        It is set to False if any semantic error was found.
        """
        return self._success
    
    def _visit_child(self, val) -> bool:
        """
        Visits a child property of the node, by it's name.
        """
        try:
            if isinstance(val, AstNode):
                    val.visit()
            elif isinstance(val, Iterable) and not isinstance(val, str):
                for element in val:
                    self._visit_child(element)
        except Exception as e:
            if RECOVER_FROM_ERROR:
                self._logger.error(f"Error while visiting {val}: {e}")
            else:
                raise 
            return False
        return True
    
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

            self._success &= self._visit_child(getattr(self, field.name))

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
        code.emit_op_dest(QuadInstructionType.ASN, self._id, expression_raw(self.expr))

@dataclass
class InputStmt(Stmt):
    id: Identifier
    def after(self):
        code.emit_op_dest(QuadInstructionType.INP, self.id)

@dataclass
class OutputStmt(Stmt):
    expr: Expression
    def after(self):
        code.emit_op_dest(QuadInstructionType.PRT, expression_raw(self.expr))

@dataclass
class IfStmt(Stmt):
    bool_expr: Expression
    
    @AstNode.after_visit('bool_expr')
    def after_boolexp(self):
        self.false_label = code.newlabel()
        self.end_label = code.newlabel()
        code.emit(QuadInstruction.JMPZ, expression_raw(self.bool_expr), self.false_label)

    true_stmts: StmtList
    
    @AstNode.before_visit('false_stmts')
    def before_false(self):
        code.emit(QuadInstruction.JUMP, self.end_label)
        code.emitlabel(self.false_label)
    
    false_stmts: StmtList
    def after(self):
        code.emitlabel(self.end_label)
    
@dataclass
class WhileStmt(Stmt):
    def before(self):
        self.boolexp_label = code.newlabel()
        self.exit_label = code.newlabel()
        code.push_break_scope(self.exit_label)

    bool_expr: Expression
    
    @AstNode.after_visit('bool_expr')
    def after_boolexp(self):
        code.emit(QuadInstruction.JMPZ, expression_raw(self.bool_expr), self.exit_label)
    
    stmts: StmtList
    
    def after(self):
        code.emit(QuadInstruction.JUMP, self.boolexp_label)
        code.emitlabel(self.exit_label)
        code.pop_break_scope()
    
@dataclass
class Case(AstNode):
    number: Number
    stmts: StmtList

    cmp_source: Optional[Expression] = None

    def before(self):
        self._end_label = code.newlabel()
        tmpname = code.emit_to_temp(QuadInstructionType.EQL, self.number, expression_raw(self.cmp_source))
        code.emit(QuadInstruction.JMPZ, tmpname, self._end_label)

    def after(self):
        code.emitlabel(self._end_label)

@dataclass
class SwitchStmt(Stmt):
    def before(self):
        code.push_break_scope(code.newlabel())

    expr: Expression

    @AstNode.before_visit('cases')
    def before_cases(self):
        # Each case should know where to compare from!
        exp_target = expression_raw(self.expr)
        for c in self.cases:
            c.cmp_source = exp_target

    cases: List[Case]
    default: StmtList

    def after(self):
        code.pop_break_scope()

@dataclass
class BreakStmt(Stmt):
    def after(self):
        try:
            code.emit(QuadInstruction.JUMP, code.peek_break_scope())
        except IndexError:
            raise ValueError("Break statement outside of loop or switch-case.")

@dataclass
class StmtList(AstNode):
    stmts: List[AstNode]

@dataclass
class BinaryOpExpression(AstNode):
    left: Expression
    right: Expression
    op: CplBinaryOp
    
    target: Optional[Identifier] = None
    
    def after(self):
        try:
            # Basic supported ops - are just compiled right away
            op, flip = self.op.to_quad_op()
            l, r = (self.right, self.left) if flip else (self.left, self.right)
            res = code.emit_to_temp(op, expression_raw(l), expression_raw(r))
            self.target = res
        except KeyError:
            if self.op not in (CplBinaryOp.AND, CplBinaryOp.OR):
                raise ValueError(f"Unsupported binary op: {self.op}")
            # AND, OR are special cases. They're actually like checking out the Addition result.
            add_res = code.emit_to_temp(QuadInstructionType.ADD, self.left.raw_result, self.right.raw_result)
            greater_thresh = 1 if self.op == CplBinaryOp.AND else 0
            res = code.emit_to_temp(QuadInstructionType.GRT, add_res, greater_thresh)
            self.target = res

@dataclass
class NotBoolExpr(AstNode):
    source: Expression
    target: Optional[Identifier] = None
    def after(self):
        self.target = code.emit_to_temp(QuadInstructionType.EQL, expression_raw(self.target), 0)

@dataclass
class Declarations(AstNode):
    declarations: List[Declaration]

@dataclass
class Declaration(AstNode):
    idlist: List[Identifier]
    _type: Dtype
    def after(self):
        for id in self.idlist:
            code.add_symbol(id, self._type)

@dataclass
class CastExpression(AstNode):
    arg: Expression
    _to_type: Dtype
    
    target: Optional[Identifier] = None
    def after(self):
        pass
        tname = code.newtemp(self._to_type)
        code.emit(QuadInstruction.ITOR if \
                    self._to_type == Dtype.INT else \
                    QuadInstruction.RTOI,
                    tname, self.arg.val)
        self.target = tname

@dataclass
class Program(AstNode):
    declarations: Declarations
    stmts: StmtList

    code: Optional[QuadCode] = None
    
    def after(self):
        code.emit(QuadInstruction.HALT)
        self.code = code

def expression_raw(expression: Optional[Expression]) -> Union[Number, Identifier]:
    assert expression is not None, "Expression is None!"
    if isinstance(expression, (BinaryOpExpression, CastExpression, NotBoolExpr)):
        target = expression.target
        assert target is not None, "Expression target is None!"
        return target
    return expression

Number = Union[int, float]
Identifier = str
Expression = Union[BinaryOpExpression, NotBoolExpr, Identifier, Number, CastExpression]
