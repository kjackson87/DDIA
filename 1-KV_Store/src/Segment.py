class Segment:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.offset = 0

    def append(self, key: str, value: bytes) -> int:
        # Implement append operation
        pass

    def read(self, offset: int) -> tuple[str, bytes]:
        # Implement read operation
        pass

    def iterate_entries(self):
        # Implement iteration over all entries
        pass