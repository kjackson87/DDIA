from typing import List, Optional, Tuple

class WriteAheadLog:
    def __init__(self, directory: str):
        # TODO: Initialize WAL in the given directory
        pass

    def append(self, operation: str, key: str, value: Optional[bytes] = None) -> None:
        # TODO: Append operation to WAL
        pass

    def recover(self) -> List[Tuple[str, str, Optional[bytes]]]:
        # TODO: Read WAL and return list of operations for recovery
        pass