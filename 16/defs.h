#ifndef _DEFS_H
#define _DEFS_H

typedef enum cpl_dtype {
    CPL_DTYPE_INT = 0,
    CPL_DTYPE_FLOAT = 1,
} cpl_dtype;

typedef enum quad_instructions {
    IASN = 0,
    IPRT, IINP,
    IEQL, INLQ, ILSS,  IGRT,
    IADD, ISUB, IMUL, IDIV,

    RASN,
    RPRT, RINP,
    REQL, RNLQ,
    RLSS, RGRT,
    RADD, RSUB, RMUL, RDIV,

    ITOR, RTOI,

    JUMP, JMPZ,

    HALT
} quad_instructions;
#endif // _DEFS_H