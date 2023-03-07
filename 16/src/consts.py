from __future__ import annotations
from enum import Enum, auto
from typing import Dict, Tuple

class Dtype(Enum):
    """ This enum describes the data types supported by the compiler. """
    INT = "int"
    FLOAT = "float"
    
    def affective_type(self: Dtype, *others: Dtype) -> Dtype:
        """
        Given a list of data types, returns the most general type.
        For CPL, the float type is selected when at least one of the types is float,
        otherwise, all types are int.
        """
        if self == Dtype.FLOAT or any(other == Dtype.FLOAT for other in others):
            return Dtype.FLOAT
        return Dtype.INT
    
class SemanticError(Exception):
    """ 
    This exception is raised when a semantic error is encountered.
    The semantic analyzer catches this exception and prints the error message.
    """
    pass

class QuadInstruction(Enum):
    """ This enum describes the instruction set of the Quad code. """
    IASN = 1
    IPRT = auto()
    IINP = auto()
    IEQL = auto()
    INQL = auto()
    ILSS = auto()
    IGRT = auto()
    IADD = auto()
    ISUB = auto()
    IMLT = auto()
    IDIV = auto()  
    RASN = auto()
    RPRT = auto()
    RINP = auto()
    REQL = auto()
    RNQL = auto()
    RLSS = auto()
    RGRT = auto()
    RADD = auto()
    RSUB = auto()
    RMLT = auto()
    RDIV = auto()
    ITOR = auto()
    RTOI = auto()
    JUMP = auto()
    JMPZ = auto()
    HALT = auto()  

class CplBinaryOp(Enum):
    """
    This enum describes the binary operators supported by the compiler - 
    meaning ANY operation that gets 2 inputs and returns a single output.
    """
    ADD = "+"
    SUB = "-"
    MLT = "*"
    DIV = "/"
    
    EQL = "=="
    NQL = "!="
    LSS = "<"
    LSSEQ = "<="
    GRT = ">"
    GRTEQ = ">="
    
    AND = "&&"
    OR = "||"
    
    def to_quad_op(self) -> Tuple[QuadInstructionType, bool]:
        """
        Converts the CplBinaryOp to the QuadInstructionType, returns it's value, combined
        with an optional boolean value to indicate whether flipping the operand order is required. 
        """
        return {
            self.ADD: (QuadInstructionType.ADD, False),
            self.SUB: (QuadInstructionType.SUB, False),
            self.MLT: (QuadInstructionType.MLT, False),
            self.DIV: (QuadInstructionType.DIV, False),
            self.EQL: (QuadInstructionType.EQL, False),
            self.NQL: (QuadInstructionType.NQL, False),
            self.LSS: (QuadInstructionType.LSS, False),
            self.GRT: (QuadInstructionType.GRT, False),
            self.GRTEQ: (QuadInstructionType.LSS, True),
            self.LSSEQ: (QuadInstructionType.GRT, True),
        }[self]

    def isrelop(self) -> bool:
        """ Returns whether the operator is a relational operator. """
        return self in {self.EQL, self.NQL, self.LSS, self.GRT, self.GRTEQ, self.LSSEQ}


class QuadInstructionType(Enum):
    """ 
    This enum abstracts the data type off of the QuadInstruction enum.
    You may use it, combined with the get_bytype method, to get the QuadInstruction
    By a QuadInstructionType and a Dtype for the operation.
    Note - this is not a complete list of all QuadInstructions, but rather a list of
    basic supported operations, to make the AST code generation easier.
    """
    ASN = 1
    PRT = auto()
    INP = auto()
    EQL = auto()
    NQL = auto()
    LSS = auto()
    GRT = auto()
    ADD = auto()
    SUB = auto()
    MLT = auto()
    DIV = auto()    
    ITOR = auto()
    RTOI = auto()
    JUMP = auto()
    JMPZ = auto()
    HALT = auto()
    

    def get_bytype(self: QuadInstructionType, arg: Dtype) -> QuadInstruction:
        """ 
        Returns the QuadInstruction with the given argument type
        matching the QuadInstructionType specified. 
        """
        return _arg_map[self][arg]



_arg_map: Dict[QuadInstructionType, Dict[Dtype, QuadInstruction]] = {
    QuadInstructionType.ASN: {
        Dtype.INT: QuadInstruction.IASN,
        Dtype.FLOAT: QuadInstruction.RASN
    },
    QuadInstructionType.PRT: {
        Dtype.INT: QuadInstruction.IPRT,
        Dtype.FLOAT: QuadInstruction.RPRT
    },
    QuadInstructionType.INP: {
        Dtype.INT: QuadInstruction.IINP,
        Dtype.FLOAT: QuadInstruction.RINP
    },
    QuadInstructionType.EQL: {
        Dtype.INT: QuadInstruction.IEQL,
        Dtype.FLOAT: QuadInstruction.REQL
    },
    QuadInstructionType.NQL: {
        Dtype.INT: QuadInstruction.INQL,
        Dtype.FLOAT: QuadInstruction.RNQL
    },
    QuadInstructionType.LSS: {
        Dtype.INT: QuadInstruction.ILSS,
        Dtype.FLOAT: QuadInstruction.RLSS
    },
    QuadInstructionType.GRT: {
        Dtype.INT: QuadInstruction.IGRT,
        Dtype.FLOAT: QuadInstruction.RGRT
    },
    QuadInstructionType.ADD: {
        Dtype.INT: QuadInstruction.IADD,
        Dtype.FLOAT: QuadInstruction.RADD
    },
    QuadInstructionType.SUB:  {
        Dtype.INT: QuadInstruction.ISUB,
        Dtype.FLOAT: QuadInstruction.RSUB
    },
    QuadInstructionType.MLT: {
        Dtype.INT: QuadInstruction.IMLT,
        Dtype.FLOAT: QuadInstruction.RMLT
    },
    QuadInstructionType.DIV: {
        Dtype.INT: QuadInstruction.IDIV,
        Dtype.FLOAT: QuadInstruction.RDIV
    },
}
"""This is map from instruction type to instruction,
with the affective type of the arguments reference."""