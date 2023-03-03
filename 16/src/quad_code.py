
from typing import Dict, List, Optional, Tuple
from consts import QuadInstruction, QuadInstructionType, Dtype

class QuadCode:
    def __init__(self) -> None:
        self.code: List[Tuple] = []
        self.code_lines = 1
        self.labels: Dict[str, int] = {}
        self.symbols: Dict[str, Dtype] = {}
        self.temp_var_counter = 0
        self.label_counter = 0
        self.break_scopes_stack: List[str] = []
        """ This property holds the stack of break (where to go) labels. """
    
    def add_symbol(self, name: str, dtype: Dtype) -> None:
        if name in self.symbols:
            raise Exception(f"Symbol {name} already exists")
        self.symbols[name] = dtype
    
    def emitlabel(self, label: str) -> str:
        self.labels[label] = self.code_lines
    
    def emit(self, op: QuadInstruction,
             arg1: Optional[str] = None,
             arg2: Optional[str] = None,
             arg3: Optional[str] = None) -> None:
        """ 
        This method adds a code line to the QUAD output code.
        """
        self.code.append((op, arg1, arg2, arg3))
        self.code_lines += 1
    
    def newlabel(self) -> str:
        self.label_counter += 1
        return f"Label{self.label_counter}"
    
    def newtemp(self, dtype: Dtype) -> str:
        self.temp_var_counter += 1
        tname = f"temp{self.temp_var_counter}"
        self.symbols[tname] = dtype
        return tname
    
    def auto_cast(self, dest_type: Dtype, *args: str) -> None:
        """ This method adds cast for all the arguments to the dest_type, if needed. """
        for to_cast in args:
            to_cast_dtype = self.symbols[to_cast]
            if to_cast_dtype == dest_type:
                continue
            if to_cast_dtype == Dtype.INT and dest_type == Dtype.FLOAT:
                self.emit(QuadInstruction.ITOR, to_cast, to_cast)
            else:
                raise ValueError(f"Cannot implicitly cast {to_cast} "+
                                 f"of type {to_cast_dtype} to type {dest_type}!")
    
    def emit_op_temp(self, op: QuadInstructionType,
                arg1: str,
                arg2: str) -> Tuple[str, Dtype]:
        """ 
        This method generates a temporary variable for the result of the required operation,
        and emits the relevant code for the execution. 
        """
        # Checks the real dtype of the result, and create temp variable.
        affective_type = self.symbols[arg1].affective_type(self.symbols[arg2])
        temp = self.newtemp(affective_type)
        # Generate the instructions.
        self.emit_op_dest(op,(temp, affective_type), arg1, arg2)
        return temp, affective_type

    def emit_op_dest(self, op: QuadInstructionType,
                dest_name: str,
                *args: str) -> None:

        try:
            dest = (dest_name, self.symbols[dest_name])
        except KeyError:
            raise ValueError(f"Cannot find symbol {dest_name} in the symbol table!")

        if args:
            self.auto_cast(dest[1], tuple(args))
        self.emit(op.get_bytype(dest[1]), dest, *[arg[0] for arg in args])
    
    def apply_labels(self) -> None:
        for i, (op, arg1, arg2, arg3) in enumerate(self.code):
            if arg1 in self.labels:
                self.code[i] = (op, self.labels[arg1], arg2, arg3)

    def push_break_scope(self, label: str) -> None:
        self.break_scopes_stack.append(label)

    def pop_break_scope(self) -> str:
        return self.break_scopes_stack.pop()

    def peek_break_scope(self) -> str:
        return self.break_scopes_stack[-1]

    def write(self, filename: str) -> None:
        self.apply_labels()
        with open(filename, 'w') as f:
            for line in self.code:
                f.write(f"{line[0].name} {line[1]} {line[2]} {line[3]}")