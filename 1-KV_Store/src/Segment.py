from typing import Dict, Optional

class Segment:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.index: Dict[str, int] = {}

    def write(self, key: str, value: bytes, offset: int) -> None:
        # Write entry to segment file
        pass

    def read(self, key: str) -> Optional[bytes]:
        # Read entry from segment file
        pass