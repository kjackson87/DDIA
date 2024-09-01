import os
import argparse
from .log_structured_store import LogStructuredStore
from .cli import CLI
from .config import Config

def main():
    parser = argparse.ArgumentParser(description="Log-Structured Key-Value Store")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    parser.add_argument("--segment-size", type=int, help="Segment size in bytes")
    parser.add_argument("--compaction-threshold", type=int, help="Number of segments before compaction")
    parser.add_argument("--bloom-filter-size", type=int, help="Size of Bloom filter in bits")
    args = parser.parse_args()

    config = Config.from_args(args) if args.config is None else Config(args.config)

    store_directory = "store"
    os.makedirs(store_directory, exist_ok=True)
    store = LogStructuredStore(store_directory, config)
    cli = CLI(store, config)
    cli.run()

if __name__ == "__main__":
    main()