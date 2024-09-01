import configparser
import argparse
from typing import Dict, Any

class Config:
    def __init__(self):
        self.segment_size: int = 1024 * 1024  # Default: 1MB
        self.compaction_threshold: int = 4  # Default: compact after 4 segments
        self.bloom_filter_size: int = 10000  # Default: 10,000 bits
        self.max_memtable_size: int = 1024 * 1024  # Default: 1MB
        self.wal_directory: str = "wal"  # Default: 'wal' subdirectory

    @classmethod
    def from_file(cls, config_file: str) -> 'Config':
        config = cls()
        parser = configparser.ConfigParser()
        parser.read(config_file)

        if 'DEFAULT' in parser:
            config.segment_size = parser.getint('DEFAULT', 'segment_size', fallback=config.segment_size)
            config.compaction_threshold = parser.getint('DEFAULT', 'compaction_threshold', fallback=config.compaction_threshold)
            config.bloom_filter_size = parser.getint('DEFAULT', 'bloom_filter_size', fallback=config.bloom_filter_size)
            config.max_memtable_size = parser.getint('DEFAULT', 'max_memtable_size', fallback=config.max_memtable_size)
            config.wal_directory = parser.get('DEFAULT', 'wal_directory', fallback=config.wal_directory)

        return config

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        config = cls()
        config.segment_size = config_dict.get('segment_size', config.segment_size)
        config.compaction_threshold = config_dict.get('compaction_threshold', config.compaction_threshold)
        config.bloom_filter_size = config_dict.get('bloom_filter_size', config.bloom_filter_size)
        config.max_memtable_size = config_dict.get('max_memtable_size', config.max_memtable_size)
        config.wal_directory = config_dict.get('wal_directory', config.wal_directory)
        return config

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> 'Config':
        config = cls()
        if args.config:
            return cls.from_file(args.config)

        if hasattr(args, 'segment_size') and args.segment_size is not None:
            config.segment_size = args.segment_size
        if hasattr(args, 'compaction_threshold') and args.compaction_threshold is not None:
            config.compaction_threshold = args.compaction_threshold
        if hasattr(args, 'bloom_filter_size') and args.bloom_filter_size is not None:
            config.bloom_filter_size = args.bloom_filter_size
        if hasattr(args, 'max_memtable_size') and args.max_memtable_size is not None:
            config.max_memtable_size = args.max_memtable_size
        if hasattr(args, 'wal_directory') and args.wal_directory is not None:
            config.wal_directory = args.wal_directory

        return config

    def to_dict(self) -> Dict[str, Any]:
        return {
            'segment_size': self.segment_size,
            'compaction_threshold': self.compaction_threshold,
            'bloom_filter_size': self.bloom_filter_size,
            'max_memtable_size': self.max_memtable_size,
            'wal_directory': self.wal_directory
        }

    def __str__(self) -> str:
        return f"""Config:
    Segment Size: {self.segment_size} bytes
    Compaction Threshold: {self.compaction_threshold} segments
    Bloom Filter Size: {self.bloom_filter_size} bits
    Max MemTable Size: {self.max_memtable_size} bytes
    WAL Directory: {self.wal_directory}
"""

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Log-Structured Key-Value Store Configuration")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    parser.add_argument("--segment-size", type=int, help="Segment size in bytes")
    parser.add_argument("--compaction-threshold", type=int, help="Number of segments before compaction")
    parser.add_argument("--bloom-filter-size", type=int, help="Size of Bloom filter in bits")
    parser.add_argument("--max-memtable-size", type=int, help="Maximum size of MemTable in bytes")
    parser.add_argument("--wal-directory", type=str, help="Directory for Write-Ahead Log files")
    return parser

# Example usage
if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()
    config = Config.from_args(args)
    print(config)