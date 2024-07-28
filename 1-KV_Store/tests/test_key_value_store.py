import pytest
import shutil
from src.LogStructuredStore import LogStructuredStore
from src.MemTable import MemTable
from src.Segment import Segment

@pytest.fixture
def temp_dir(tmpdir):
    yield tmpdir
    shutil.rmtree(tmpdir)

class TestLogStructuredStore:
    def test_put_and_get(self, temp_dir):
        store = LogStructuredStore(str(temp_dir))
        store.put("key1", b"value1")
        assert store.get("key1") == b"value1"

    def test_delete(self, temp_dir):
        store = LogStructuredStore(str(temp_dir))
        store.put("key2", b"value2")
        store.delete("key2")
        assert store.get("key2") is None

    def test_nonexistent_key(self, temp_dir):
        store = LogStructuredStore(str(temp_dir))
        assert store.get("nonexistent") is None

class TestMemTable:
    def test_put_and_get(self):
        memtable = MemTable()
        memtable.put("key1", b"value1")
        assert memtable.get("key1") == b"value1"

    def test_remove(self):
        memtable = MemTable()
        memtable.put("key2", b"value2")
        memtable.remove("key2")
        assert memtable.get("key2") is None

class TestSegment:
    def test_write_and_read(self, temp_dir):
        segment_file = temp_dir.join("segment.log")
        segment = Segment(str(segment_file))
        segment.write("key1", b"value1", 0)
        assert segment.read("key1") == b"value1"

    def test_read_nonexistent(self, temp_dir):
        segment_file = temp_dir.join("segment.log")
        segment = Segment(str(segment_file))
        assert segment.read("nonexistent") is None

def test_end_to_end(temp_dir):
    store = LogStructuredStore(str(temp_dir))

    # Test put and get
    store.put("key1", b"value1")
    store.put("key2", b"value2")
    assert store.get("key1") == b"value1"
    assert store.get("key2") == b"value2"

    # Test update
    store.put("key1", b"new_value1")
    assert store.get("key1") == b"new_value1"

    # Test delete
    store.delete("key2")
    assert store.get("key2") is None

    # Test nonexistent key
    assert store.get("key3") is None

# Additional tests students should implement:
# - Test compaction
# - Test recovery after crash
# - Test with large number of entries
# - Test concurrent access (if implemented)
# - Test edge cases (empty keys, large values, etc.)
# - Test performance (time taken for operations)