
from typing import Dict, List, Optional, Tuple, Union
from consts import QuadInstruction, QuadInstructionType, Dtype

ArgumentType = Union[str, int, float]
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
    
    def emitlabel(self, label: str) -> None:
        self.labels[label] = self.code_lines
    
    def emit(self, op: QuadInstruction,
             arg1: Optional[ArgumentType] = None,
             arg2: Optional[ArgumentType] = None,
             arg3: Optional[ArgumentType] = None) -> None:
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
    
    def auto_cast(self, dest_type: Dtype, *args: ArgumentType) -> None:
        """ This method adds cast for all the arguments to the dest_type, if needed. """
        for to_cast in args:
            
            if isinstance(to_cast, str):
                to_cast_dtype = self.symbols[to_cast]
            else:
                to_cast_dtype = Dtype.INT if isinstance(to_cast, int) else Dtype.FLOAT
                
            if to_cast_dtype == dest_type:
                continue
            if to_cast_dtype == Dtype.INT and dest_type == Dtype.FLOAT:
                self.emit(QuadInstruction.ITOR, to_cast, to_cast)
            else:
                raise ValueError(f"Cannot implicitly cast {to_cast} "+
                                 f"of type {to_cast_dtype} to type {dest_type}!")
    
    def _arg_type(self, arg: ArgumentType) -> Dtype:
        if isinstance(arg, str):
            return self.symbols[arg]
        return Dtype.INT if isinstance(arg, int) else Dtype.FLOAT
    
    def emit_to_temp(self, op: QuadInstructionType,
                arg1: ArgumentType,
                arg2: ArgumentType) -> str:
        """ 
        This method generates a temporary variable for the result of the required operation,
        and emits the relevant code for the execution. 
        """
        # Checks the real dtype of the result, and create temp variable.
        affective_type = self._arg_type(arg1).affective_type(self._arg_type(arg2))
        temp = self.newtemp(affective_type)
        # Generate the instructions.
        self.emit_op_dest(op, temp, arg1, arg2)
        return temp

    def emit_op_dest(self, op: QuadInstructionType,
                dest_name: ArgumentType,
                *args: ArgumentType) -> None:

        dest_dtype = self._arg_type(dest_name)

        if args:
            self.auto_cast(dest_dtype, *args)
        self.emit(op.get_bytype(dest_dtype), dest_name, *args)
    
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

    @staticmethod
    def _printable(val: Union[str, int, float, QuadInstruction]) -> str:
        if isinstance(val, str):
            return val
        elif isinstance(val, QuadInstruction):
            return val.name
        return str(val)
    
    def write(self, filename: str) -> None:
        self.apply_labels()
        with open(filename, 'w') as f:
            for line in self.code:
                f.write(" ".join([self._printable(j) for j in line]))
