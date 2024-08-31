class Segment:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.offset = 0

    def append(self, key: str, value: bytes) -> int:
        # Implement append operation
        with open(self.file_path, "ab") as f:
            byteString = key.encode() + b"\0" + value + b"\0"
            f.write(byteString)
        appended_offset = self.offset
        self.offset += len(byteString)
        return appended_offset

    def read(self, offset: int) -> tuple[str, bytes]:
        # Implement read operation
        with open(self.file_path, "rb") as f:
            f.seek(offset)
            key = b""
            while True:
                b = f.read(1)
                if b == b"\0":
                    break
                key += b
            value = b""
            while True:
                b = f.read(1)
                if b == b"\0":
                    break
                value += b
        return key.decode(), value

    def iterate_entries(self):
        # Implement iteration over all entries
        pass