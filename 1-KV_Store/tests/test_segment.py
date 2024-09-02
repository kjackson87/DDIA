import pytest
import shutil
from src.log_structured_kvstore.segment import Segment

@pytest.fixture
def temp_dir(tmpdir):
    yield tmpdir
    shutil.rmtree(tmpdir)

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
