from typing import Dict, Optional

class MemTable:
    def __init__(self):
        self.table: Dict[str, bytes] = {}

    def put(self, key: str, value: bytes) -> None:
        self.table[key] = value

    def get(self, key: str) -> Optional[bytes]:
        return self.table.get(key)

    def remove(self, key: str) -> None:
        del self.table[key]