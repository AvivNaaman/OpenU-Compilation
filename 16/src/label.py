
from typing import List


class Labels:
    """
    This class is responsible for replacing sematic labels with jump destinations.
    """
    def __init__(self):
        self._labels: List[str] = []
        self._label_counter = 0
    
    def next_label(self):
        self._label_counter += 1
        label = f'LABEL_{self._label_counter}'
        self._labels.append(label)
        return label
    
    def enqueue(self, num: int = 1):
        for _ in range(num):
            self._labels.append(self.next_label())
    
    def pop(self) -> str:
        return self._labels.pop()
        
    def dequeue(self) -> str:
        return self._labels.pop(0)
    
    def __getitem__(self, index: int) -> str:
        return self._labels[index]
    