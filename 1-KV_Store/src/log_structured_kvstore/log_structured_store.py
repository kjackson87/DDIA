from typing import Dict, Optional
from .key_value_store import KeyValueStore
from .bloom_filter import BloomFilter
from .write_ahead_log import WriteAheadLog
from .config import Config

class LogStructuredStore(KeyValueStore):
    def __init__(self, directory: str, config: Config):
        self.directory = directory
        self.config = config
        self.index: Dict[str, int] = {}
        self.active_segment = None
        self.active_segment_offset = 0
        self.bloom_filter = BloomFilter(config.bloom_filter_size)
        self.wal = WriteAheadLog(directory)

    def put(self, key: str, value: bytes) -> None:
        # TODO: Implement put operation
        # Don't forget to update the WAL and Bloom filter
        pass

    def get(self, key: str) -> Optional[bytes]:
        # TODO: Implement get operation
        # Use Bloom filter for optimization
        pass

    def delete(self, key: str) -> None:
        # TODO: Implement delete operation
        # Don't forget to update the WAL
        pass

    def compact(self) -> None:
        # TODO: Implement log compaction
        # Consider using self.config.compaction_threshold
        pass

    def recover(self) -> None:
        # TODO: Implement recovery from crash
        # Use the WAL for crash recovery
        pass

    def get_statistics(self) -> Dict[str, any]:
        # TODO: Implement method to return store statistics
        pass