# Log-Structured Key-Value Store Project

## Overview
This project involves implementing a simple key-value store with a log-structured storage engine. You'll be working with concepts from Chapters 1-3 of "Designing Data-Intensive Applications" by Martin Kleppmann.

## Objectives
- Implement a basic key-value store
- Develop a log-structured storage engine
- Gain hands-on experience with data persistence and retrieval
- Understand trade-offs in storage engine design
- Implement additional features like Bloom filters and Write-Ahead Logging
- Visualize the state of the key-value store

## Project Structure
```
key_value_store/
│
├── src/
│   ├── log_structured_kvstore/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── cli.py
│   │   ├── config.py
│   │   ├── key_value_store.py
│   │   ├── log_structured_store.py
│   │   ├── memtable.py
│   │   ├── segment.py
│   │   ├── bloom_filter.py
│   │   └── write_ahead_log.py
│   │
│   └── scripts/
│       └── visualize.py
│
├── tests/
│   ├── __init__.py
│   ├── test_key_value_store.py
│   ├── test_log_structured_store.py
│   ├── test_memtable.py
│   ├── test_segment.py
│   ├── test_bloom_filter.py
│   └── test_write_ahead_log.py
│
├── data/
│   └── .gitkeep
│
├── docs/
│   ├── design.md
│   └── usage.md
│
├── pyproject.toml
├── .gitignore
└── README.md
```

## Tasks
1. Implement the `put`, `get`, and `delete` methods in `LogStructuredStore`.
2. Develop the `MemTable` class for in-memory operations.
3. Implement file I/O operations in the `Segment` class.
4. Add log compaction functionality to manage log size.
5. Implement crash recovery mechanism using `WriteAheadLog`.
6. Develop a `BloomFilter` class for efficient key lookups.
7. Enhance the CLI for better user interaction.
8. Implement the visualization tool in `scripts/visualize.py`.
9. Add comprehensive error handling and logging.
10. Write unit tests for all implemented functionality.
11. Document your design decisions and usage instructions in the `docs/` directory.

## Implementation Guidelines
- Use append-only logs for write operations.
- Implement an in-memory index for fast key lookups.
- Ensure data persistence across program restarts.
- Implement efficient file I/O operations.
- Use the `Config` class to manage configuration settings.
- Follow Python best practices and PEP 8 style guide.

## New Components

### Config
- Implement the `Config` class in `config.py` to manage all configuration settings.
- Use this class throughout your project to access configuration parameters.

### BloomFilter
- Implement a Bloom filter in `bloom_filter.py` to optimize key lookups.
- Integrate the Bloom filter into your `LogStructuredStore` implementation.

### WriteAheadLog
- Implement a Write-Ahead Log in `write_ahead_log.py` for crash recovery.
- Use the WAL in `LogStructuredStore` to ensure data durability.

### Visualization
- Implement the visualization tool in `scripts/visualize.py`.
- The tool should create a graphical representation of the key-value store's segments.

## Getting Started

You can choose either venv (Python's built-in virtual environment) or Conda for your development environment. Both methods will use pip for package management.

### Option 1: Using venv

1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
4. Install the project in editable mode with development dependencies:
   `pip install -e ".[dev]"`

### Option 2: Using Conda

1. Clone this repository.
2. Install Miniconda or Anaconda if you haven't already.
3. Create a new Conda environment:
   `conda env create -f environment.yml`
4. Activate the Conda environment:
   `conda activate log_structured_kvstore`
5. Install the project in editable mode with development dependencies:
   `pip install -e ".[dev]"`

After setting up your environment (either with venv or Conda):

6. Implement the components in the `src/log_structured_kvstore/` directory.
7. Run the program: `python -m log_structured_kvstore.main`

## Testing
- Navigate to the project root directory.
- Run tests using pytest: `pytest`
- For more verbose output: `pytest -v`
- To run a specific test file: `pytest tests/test_key_value_store.py`

## Visualization
After implementing the visualization tool:
1. Ensure your key-value store has some data.
2. Run the visualization script: `python src/scripts/visualize.py`
3. Analyze the graphical representation of your store's segments.

## Documentation
- Update `docs/design.md` with your design decisions and rationale.
- Keep `docs/usage.md` updated with instructions on how to use your key-value store.

## Evaluation Criteria
- Correctness: The key-value store should correctly handle put, get, and delete operations.
- Persistence: Data should survive program restarts.
- Efficiency: Read and write operations should be reasonably fast, even with a large number of entries.
- Crash Recovery: The system should be able to recover from crashes without data loss.
- Bloom Filter: Implement and demonstrate the effectiveness of the Bloom filter.
- Visualization: The visualization tool should accurately represent the state of the store.
- Code Quality: Well-organized, commented, and following Python best practices.
- Testing: Comprehensive unit tests and integration tests.
- Documentation: Clear and concise documentation of design decisions and usage instructions.

## Resources
- "Designing Data-Intensive Applications" by Martin Kleppmann (Chapters 1-3)
- Python documentation: https://docs.python.org/3/
- Pytest documentation: https://docs.pytest.org/

Good luck, and happy coding!