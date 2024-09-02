import pytest
import shutil
import os
from src.log_structured_kvstore.log_structured_store import LogStructuredStore
from src.log_structured_kvstore.config import Config

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