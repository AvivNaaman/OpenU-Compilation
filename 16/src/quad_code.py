"""
This module implements the final code generation from CPL to Quad,
And is used by the AST nodes to generate the final code.
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from consts import QuadInstruction, QuadInstructionType, Dtype, SemanticError

ArgumentType = Union[str, int, float]
class BreakLabelScope:
    """ 
    This class helps managing the stack of break statement jump-outside labels.
    To make managing jump destinations outside of loops/switches easier, we push a new
    scope for each loop/switch, and pop it when we exit the loop/switch. 
    The scope is the label to jump to when we encounter a break statement.
    """
    def __init__(self) -> None:
        self._stack: List[str] = []
    
    def push(self, label: str) -> None:
        """ 
        Pushes a new scope for break statement jump-outside label.
        """
        self._stack.append(label)

    def pop(self) -> str:
        """
        Pops the top of the break statement jump-outside label stack.
        """
        return self._stack.pop()

    def peek(self) -> str:
        """ 
        Returns the label for the current break statement jump-outside scope.
        """
        return self._stack[-1]

class QuadCode:
    """ This class contains useful methods for creation of the final code,
    including generation of temporary variables, labels, symbol management,
    code emission and type checking. """
    def __init__(self) -> None:
        self.code: List[Tuple] = []
        self.code_lines = 1
        self.labels: Dict[str, int] = {}
        self.symbols: Dict[str, Dtype] = {}
        self.temp_var_counter = 1
        self.label_counter = 1
        self._label_scope = BreakLabelScope()
        """ This property holds the stack of break (where to go) labels. """
    
    @property
    def label_scope(self) -> BreakLabelScope:
        return self._label_scope
    
    def add_symbol(self, name: str, dtype: Dtype) -> None:
        """
        This method adds a new symbol to the symbol table.
        Such symbols should only be added as a result of a user-defined variable declaration.
        The method raises an error if the symbol already exists.
        """
        if name in self.symbols:
            raise ValueError(f"Symbol {name} of type {self.symbols[name]} already exists!")
        self.symbols[name] = dtype
    
    def emitlabel(self, label: str) -> None:
        """ 
        This method adds a label to the QUAD output code.
        The label points to the next line of code.
        It will be replaced with the line number when the code is written to a file,
        and may not be re-defined.
        """
        if label in self.labels:
            raise Exception(f"Label {label} re-emitted!")
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
    
    LABEL_PFX = "Label"
    """ Prefix for labels' names. """
    
    def newlabel(self) -> str:
        """ Generates a new distinct semantic label. """
        lname =  f"{self.LABEL_PFX}{self.label_counter}"
        # Avoid name collisions with existing symbols (non-temps)
        # Such collision will cause a major issue during label replacement later.
        while lname in self.symbols:
            self.label_counter += 1
            lname =  f"{self.LABEL_PFX}{self.label_counter}"
        self.label_counter += 1
        return lname
    
    TEMP_VAR_PFX = "temp"
    """ Prefix for temporary variables' names. """
    
    def newtemp(self, dtype: Dtype) -> str:
        """ Generates a new distinct temporary variable with the specified data type. """
        tname = f"{self.TEMP_VAR_PFX}{self.temp_var_counter}"
        # Avoid name collisions with existing symbols (non-temps)
        while tname in self.symbols:
            self.temp_var_counter += 1
            tname = f"{self.TEMP_VAR_PFX}{self.temp_var_counter}"
        self.symbols[tname] = dtype
        self.temp_var_counter += 1
        return tname
    
    def auto_cast(self, dest_type: Dtype, *args: ArgumentType) -> Dict[ArgumentType, str]:
        """ This method adds cast for all the arguments to the dest_type, if needed. """
        results = {}
        for to_cast in args:
            to_cast_dtype = self.get_type(to_cast)
                
            # Cast is unnecessary.    
            if to_cast_dtype == dest_type:
                continue
            
            # Auto cast int --> float
            if to_cast_dtype == Dtype.INT and dest_type == Dtype.FLOAT:
                results[to_cast] = self.newtemp(dest_type)
                self.emit(QuadInstruction.ITOR, results[to_cast], to_cast)
            # Disable casting float --> int (required static_cast in source code)
            else:
                raise SemanticError(f"Cannot implicitly cast {to_cast} "+
                                 f"of type {to_cast_dtype} to type {dest_type}!")
        return results
    
    def get_type(self, arg: ArgumentType) -> Dtype:
        """ 
        Returns the data type of an emit method argument.
        Raises a KeyError if the argument is a string (identifier) and is not in the symbol table,
        meaning it's a non-existing variable or temporary variable.
        """
        # If argument to cast is a string - it's an identifier,
        if isinstance(arg, str):
            # So it has to be in the symbol table
            return self.symbols[arg]
        # Determine data type of number: according to the presence of '.'
        # lexer parses numbers' pythonic data types as int or float
        return Dtype.INT if isinstance(arg, int) else Dtype.FLOAT
    
    def emit_to_temp(self, op: QuadInstructionType,
                arg1: ArgumentType,
                arg2: ArgumentType) -> str:
        """ 
        Emits an operation with a destination variable created automatically as a temp variable.
        """
        # Checks the real dtype of the result, and create temp variable.
        affective_type = self.get_type(arg1).affective_type(self.get_type(arg2))
        temp = self.newtemp(affective_type)
        # Generate the instructions.
        self.emit_op_dest(op, temp, arg1, arg2)
        return temp

    def emit_op_dest(self, op: QuadInstructionType,
                dest_name: ArgumentType,
                *args: ArgumentType) -> None:
        """ Emits an operation with a destination variable specified. """

        dest_dtype = self.get_type(dest_name)

        # Apply implicit casts, and check for required explicit casts.
        results = self.auto_cast(dest_dtype, *args)
        updated_args = [
            results.get(a, a) for a in args
        ]
        self.emit(op.get_bytype(dest_dtype), dest_name, *updated_args)
    
    def apply_labels(self) -> None:
        """ Replaces instances of a semantic label in the code with it's emitted line number. """
        for i, (op, arg1, arg2, arg3) in enumerate(self.code):
            # TODO: Identify labels as labels, mixup with variables might occur!
            if arg1 in self.labels:
                self.code[i] = (op, self.labels[arg1], arg2, arg3)
            if arg2 in self.labels:
                self.code[i] = (op, arg1, self.labels[arg2], arg3)


    @staticmethod
    def _printable(val: Optional[Union[str, int, float, QuadInstruction]]) -> Optional[str]:
        """ Returns a printable string representation of an argument to a final code generation. """
        if val is None:
            return None
        if isinstance(val, str):
            return val
        if isinstance(val, QuadInstruction):
            return val.name
        return str(val)
    
    def write(self, dest: Union[str, Path], epilogue: Optional[str] = None) -> None:
        """ Writes the final code to an output raw file. """
        self.apply_labels()
        with open(dest, 'w', encoding='utf-8') as output_file:
            for line in self.code:
                output_file.write(" ".join(filter(None, [self._printable(j) for j in line])) + '\n')
            if epilogue:
                output_file.write(epilogue)
