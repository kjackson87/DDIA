import pytest
import shutil
from src.log_structured_kvstore.write_ahead_log import WriteAheadLog

@pytest.fixture
def temp_dir(tmpdir):
    yield tmpdir
    shutil.rmtree(tmpdir)

class TestWriteAheadLog:
    def test_append_and_recover(self, temp_dir):
        wal = WriteAheadLog(str(temp_dir))
        wal.append("put", "key1", b"value1")
        wal.append("delete", "key2")
        recovered = wal.recover()
        assert recovered == [("put", "key1", b"value1"), ("delete", "key2", None)]

    def test_append_many_entries(self, temp_dir):
        wal = WriteAheadLog(str(temp_dir))
        for i in range(1000):
            wal.append("put", f"key{i}", f"value{i}".encode())
        recovered = wal.recover()
        assert len(recovered) == 1000
        assert recovered[500] == ("put", "key500", b"value500")

    def test_recover_after_crash(self, temp_dir):
        wal1 = WriteAheadLog(str(temp_dir))
        for i in range(100):
            wal1.append("put", f"key{i}", f"value{i}".encode())

        # Simulate a crash by creating a new WAL instance
        wal2 = WriteAheadLog(str(temp_dir))
        recovered = wal2.recover()
        assert len(recovered) == 100
        assert recovered[50] == ("put", "key50", b"value50")
