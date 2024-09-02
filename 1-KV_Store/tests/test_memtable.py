from src.log_structured_kvstore.memtable import MemTable
class TestMemTable:
    def test_put_and_get(self):
        memtable = MemTable()
        memtable.put("key1", b"value1")
        assert memtable.get("key1") == b"value1"

    def test_update(self):
        memtable = MemTable()
        memtable.put("key2", b"value2")
        memtable.put("key2", b"new_value2")
        assert memtable.get("key2") == b"new_value2"

    def test_delete(self):
        memtable = MemTable()
        memtable.put("key3", b"value3")
        memtable.delete("key3")
        assert memtable.get("key3") is None

    def test_nonexistent_key(self):
        memtable = MemTable()
        assert memtable.get("nonexistent") is None