from enum import Enum, auto
from typing import Dict

class SupportedDtype(Enum):
    INT = 1
    FLOAT = auto()
    
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

class QuadInstructionFetcher:
    _arg_map: Dict[QuadInstructionType, Dict[SupportedDtype, QuadInstruction]] = {
        QuadInstructionType.ASN: {SupportedDtype.INT: QuadInstruction.IASN, SupportedDtype.FLOAT: QuadInstruction.RASN},
        QuadInstructionType.PRT: {SupportedDtype.INT: QuadInstruction.IPRT, SupportedDtype.FLOAT: QuadInstruction.RPRT},
        QuadInstructionType.INP: {SupportedDtype.INT: QuadInstruction.IINP, SupportedDtype.FLOAT: QuadInstruction.RINP},
        QuadInstructionType.EQL: {SupportedDtype.INT: QuadInstruction.IEQL, SupportedDtype.FLOAT: QuadInstruction.REQL},
        QuadInstructionType.NQL: {SupportedDtype.INT: QuadInstruction.INQL, SupportedDtype.FLOAT: QuadInstruction.RNQL},
        QuadInstructionType.LSS: {SupportedDtype.INT: QuadInstruction.ILSS, SupportedDtype.FLOAT: QuadInstruction.RLSS},
        QuadInstructionType.GRT: {SupportedDtype.INT: QuadInstruction.IGRT, SupportedDtype.FLOAT: QuadInstruction.RGRT},
        QuadInstructionType.ADD: {SupportedDtype.INT: QuadInstruction.IADD, SupportedDtype.FLOAT: QuadInstruction.RADD},
        QuadInstructionType.SUB: {SupportedDtype.INT: QuadInstruction.ISUB, SupportedDtype.FLOAT: QuadInstruction.RSUB},
        QuadInstructionType.MLT: {SupportedDtype.INT: QuadInstruction.IMLT, SupportedDtype.FLOAT: QuadInstruction.RMLT},
        QuadInstructionType.DIV: {SupportedDtype.INT: QuadInstruction.IDIV, SupportedDtype.FLOAT: QuadInstruction.RDIV},
    }
    
    @staticmethod
    def get_by2args(type: QuadInstructionType, arg1: SupportedDtype, arg2: SupportedDtype) -> QuadInstruction:
        major_dtype: SupportedDtype = SupportedDtype.FLOAT \
            if arg1 == SupportedDtype.FLOAT or arg2 == SupportedDtype.FLOAT \
            else SupportedDtype.INT
        return QuadInstructionFetcher._arg_map[type][major_dtype]
    
    @staticmethod
    def get_by1arg(type: QuadInstructionType, arg: SupportedDtype) -> QuadInstruction:
        return QuadInstructionFetcher._arg_map[type][arg]
        