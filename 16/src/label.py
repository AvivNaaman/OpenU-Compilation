
from typing import List


class Labels:
    """
    This class is responsible for replacing sematic labels with jump destinations.
    """
    def __init__(self):
        self._label_counter = 0
    
    def new_label(self) -> str:
        """
        Returns a new label.
        """
        self._label_counter += 1
        return f"Label{self._label_counter}"