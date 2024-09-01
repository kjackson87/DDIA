import pytest
import shutil
import os
from src.log_structured_kvstore.log_structured_store import LogStructuredStore
from src.log_structured_kvstore.memtable import MemTable
from src.log_structured_kvstore.segment import Segment
from src.log_structured_kvstore.config import Config
from src.log_structured_kvstore.bloom_filter import BloomFilter
from src.log_structured_kvstore.write_ahead_log import WriteAheadLog

@pytest.fixture
def temp_dir(tmpdir):
    yield tmpdir
    shutil.rmtree(tmpdir)

@pytest.fixture
def config():
    return Config.from_dict({
        "segment_size": 1024,
        "compaction_threshold": 2,
        "bloom_filter_size": 1000
    })

class TestLogStructuredStore:
    def test_put_and_get(self, temp_dir, config):
        store = LogStructuredStore(str(temp_dir), config)
        store.put("key1", b"value1")
        assert store.get("key1") == b"value1"

    def test_delete(self, temp_dir, config):
        store = LogStructuredStore(str(temp_dir), config)
        store.put("key2", b"value2")
        store.delete("key2")
        assert store.get("key2") is None

    def test_nonexistent_key(self, temp_dir, config):
        store = LogStructuredStore(str(temp_dir), config)
        assert store.get("nonexistent") is None

    def test_update_existing_key(self, temp_dir, config):
        store = LogStructuredStore(str(temp_dir), config)
        store.put("key3", b"value3")
        store.put("key3", b"new_value3")
        assert store.get("key3") == b"new_value3"

    def test_large_value(self, temp_dir, config):
        store = LogStructuredStore(str(temp_dir), config)
        large_value = b"x" * 1000000  # 1MB value
        store.put("large_key", large_value)
        assert store.get("large_key") == large_value

    def test_many_keys(self, temp_dir, config):
        store = LogStructuredStore(str(temp_dir), config)
        for i in range(1000):
            store.put(f"key{i}", f"value{i}".encode())
        for i in range(1000):
            assert store.get(f"key{i}") == f"value{i}".encode()

    def test_compaction(self, temp_dir, config):
        store = LogStructuredStore(str(temp_dir), config)
        for i in range(100):
            store.put(f"key{i}", f"value{i}".encode())

        # Update some keys to create tombstones
        for i in range(0, 100, 2):
            store.delete(f"key{i}")

        initial_segment_count = len(os.listdir(temp_dir))
        store.compact()
        final_segment_count = len(os.listdir(temp_dir))

        assert final_segment_count < initial_segment_count

        # Check that compaction didn't lose any data
        for i in range(1, 100, 2):
            assert store.get(f"key{i}") == f"value{i}".encode()
        for i in range(0, 100, 2):
            assert store.get(f"key{i}") is None

    def test_crash_recovery(self, temp_dir, config):
        store1 = LogStructuredStore(str(temp_dir), config)
        for i in range(100):
            store1.put(f"key{i}", f"value{i}".encode())

        # Simulate a crash by creating a new store instance
        store2 = LogStructuredStore(str(temp_dir), config)
        store2.recover()

        for i in range(100):
            assert store2.get(f"key{i}") == f"value{i}".encode()

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

class TestSegment:
    def test_write_and_read(self, temp_dir):
        segment_file = temp_dir.join("segment.log")
        segment = Segment(str(segment_file))
        segment.append("key1", b"value1")
        assert segment.read("key1") == b"value1"

    def test_multiple_entries(self, temp_dir):
        segment_file = temp_dir.join("segment.log")
        segment = Segment(str(segment_file))
        segment.append("key1", b"value1")
        segment.append("key2", b"value2")
        assert segment.read("key1") == b"value1"
        assert segment.read("key2") == b"value2"

    def test_update_entry(self, temp_dir):
        segment_file = temp_dir.join("segment.log")
        segment = Segment(str(segment_file))
        segment.append("key1", b"value1")
        segment.append("key1", b"new_value1")
        assert segment.read("key1") == b"new_value1"

    def test_delete_entry(self, temp_dir):
        segment_file = temp_dir.join("segment.log")
        segment = Segment(str(segment_file))
        segment.append("key1", b"value1")
        segment.append("key1", None)  # Delete operation
        assert segment.read("key1") is None

    def test_iterate_entries(self, temp_dir):
        segment_file = temp_dir.join("segment.log")
        segment = Segment(str(segment_file))
        entries = [("key1", b"value1"), ("key2", b"value2"), ("key3", b"value3")]
        for key, value in entries:
            segment.append(key, value)

        assert list(segment.iterate_entries()) == entries

class TestBloomFilter:
    def test_add_and_check(self):
        bf = BloomFilter(1000)
        bf.add("test_key")
        assert bf.may_contain("test_key") == True
        assert bf.may_contain("non_existent_key") == False

    def test_false_positive_rate(self):
        bf = BloomFilter(1000)
        for i in range(100):
            bf.add(f"key{i}")

        false_positives = 0
        for i in range(100, 200):
            if bf.may_contain(f"key{i}"):
                false_positives += 1

        # False positive rate should be relatively low
        assert false_positives / 100 < 0.1

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

class TestConfig:
    def test_load_from_file(self, temp_dir):
        config_file = temp_dir.join("config.ini")
        with open(config_file, "w") as f:
            f.write("[DEFAULT]\n")
            f.write("segment_size = 2097152\n")
            f.write("compaction_threshold = 8\n")
            f.write("bloom_filter_size = 20000\n")

        config = Config(str(config_file))
        assert config.segment_size == 2097152
        assert config.compaction_threshold == 8
        assert config.bloom_filter_size == 20000

    def test_from_dict(self):
        config_dict = {
            "segment_size": 1048576,
            "compaction_threshold": 4,
            "bloom_filter_size": 10000
        }
        config = Config.from_dict(config_dict)
        assert config.segment_size == 1048576
        assert config.compaction_threshold == 4
        assert config.bloom_filter_size == 10000

    def test_default_values(self):
        config = Config.from_dict({})
        assert config.segment_size == 1024 * 1024  # Default: 1MB
        assert config.compaction_threshold == 4  # Default: compact after 4 segments
        assert config.bloom_filter_size == 10000  # Default: 10,000 bits

# TODO: Add property-based tests using Hypothesis library
# This will help test the system with a wide range of inputs
# Example (uncomment and implement):
# from hypothesis import given, strategies as st
#
# class TestPropertyBased:
#     @given(key=st.text(), value=st.binary())
#     def test_put_get_property(self, temp_dir, config, key, value):
#         store = LogStructuredStore(str(temp_dir), config)
#         store.put(key, value)
#         assert store.get(key) == value