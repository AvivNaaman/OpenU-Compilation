
from typing import Dict, List, Tuple
from consts import QuadInstruction

class QuadCode:
    def __init__(self) -> None:
        self.code: List[Tuple] = []
        self.code_lines = 1
        self.labels: Dict[str, int] = {}
        
    def genlabel(self, label: str) -> str:
        self.labels[label] = self.code_lines
    
    def emit(self, op: QuadInstruction, arg1: str, arg2: str, arg3: str) -> None:
        self.code.append((op, arg1, arg2, arg3))
        self.code_lines += 1
        
    def emit
        
    def apply_labels(self) -> None:
        for i, (op, arg1, arg2, arg3) in enumerate(self.code):
            if arg1 in self.labels:
                self.code[i] = (op, self.labels[arg1], arg2, arg3)
    
    def write(self, filename: str) -> None:
        self.apply_labels()
        with open(filename, 'w') as f:
            for line in self.code:
                f.write(f"{line[0].name} {line[1]} {line[2]} {line[3]}")