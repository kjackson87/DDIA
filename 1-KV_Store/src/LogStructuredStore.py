from typing import Dict, Optional
from .KeyValueStore import KeyValueStore
from .Segment import Segment

class LogStructuredStore(KeyValueStore):
    def __init__(self, directory: str):
        self.directory = directory
        self.index: Dict[str, int] = {}
        self.segment_counter = 0
        self.active_segment = Segment(f"{self.directory}/{self.segment_counter}")
        self.active_segment_offset = 0

    def put(self, key: str, value: bytes) -> None:
        # Implement put operation
        offset = self.active_segment.append(key, value)
        self.index[key] = offset

    def get(self, key: str) -> Optional[bytes]:
        # Implement get operation
        if key not in self.index: return None
        key, val = self.active_segment.read(self.index[key])
        return val

    def delete(self, key: str) -> None:
        # Implement delete operation
        self.put(key, b"")
        del self.index[key]

    def compact(self) -> None:
        # Implement log compaction
        pass

    def recover(self) -> None:
        # Implement recovery from crash
        pass