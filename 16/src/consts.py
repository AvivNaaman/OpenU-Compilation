from __future__ import annotations
from enum import Enum, auto
from typing import Dict, Tuple
from typing import Self

class Dtype(Enum):
    INT = 1
    FLOAT = auto()
    
    def affective_type(self, other: Self) -> Self:
        if self == Dtype.FLOAT or other == Dtype.FLOAT:
            return Dtype.FLOAT
        return Dtype.INT
    

class QuadInstruction(Enum):
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
        Converts the CplBinaryOp to the QuadInstructionType,
        with an optional boolean value to indicate whether flipping the operand order is required. 
        """
        return {
            self.ADD: (QuadInstructionType.ADD, False),
            self.MLT: (QuadInstructionType.MLT, False),
            self.DIV: (QuadInstructionType.DIV, False),
            self.EQL: (QuadInstructionType.EQL, False),
            self.NQL: (QuadInstructionType.NQL, False),
            self.LSS: (QuadInstructionType.LSS, False),
            self.GRT: (QuadInstructionType.GRT, False),
            self.GRTEQ: (QuadInstructionType.LSS, True),
            self.LSSEQ: (QuadInstructionType.GRT, True),
        }[self]



class QuadInstructionType(Enum):
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
    

    def get_bytype(self: Self, arg: Dtype) -> QuadInstruction:
        print(self, arg)
        return _arg_map[self][arg]


# This is map from instruction type to instruction,
# with the affective type of the arguments reference.
_arg_map: Dict[Self, Dict[Dtype, QuadInstruction]] = {
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