from typing import Dict, Optional

class MemTable:
    def __init__(self):
        self.table: Dict[str, bytes] = {}

    def put(self, key: str, value: bytes) -> None:
        # Implement in-memory put
        pass

    def get(self, key: str) -> Optional[bytes]:
        # Implement in-memory get
        pass

    def remove(self, key: str) -> None:
        # Implement in-memory delete
        pass