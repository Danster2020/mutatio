# messages.py
from textual.message import Message

class TransformRequested(Message):
    """User requested a transformation (e.g. replace '_' with space)."""
    def __init__(self):
        super().__init__()

class ResetRequested(Message):
    """User requested a reset of names."""
    def __init__(self):
        super().__init__()