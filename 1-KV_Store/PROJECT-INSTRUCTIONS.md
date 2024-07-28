# Key-Value Store Project

## Overview
This project involves implementing a simple key-value store with a log-structured storage engine. You'll be working with concepts from Chapters 1-3 of "Designing Data-Intensive Applications" by Martin Kleppmann.

## Objectives
- Implement a basic key-value store
- Develop a log-structured storage engine
- Gain hands-on experience with data persistence and retrieval
- Understand trade-offs in storage engine design

## Project Structure
- `KeyValueStore.py`: Abstract base class defining the key-value store interface
- `LogStructuredStore.py`: Main class implementing the key-value store
- `MemTable.py`: In-memory structure for efficient reads and writes
- `Segment.py`: Represents a segment file in the log-structured store
- `CLI.py`: Command-line interface for interacting with the store
- `main.py`: Entry point of the application

## Tasks
1. Implement the `put`, `get`, and `delete` methods in `LogStructuredStore`.
2. Develop the `MemTable` class for in-memory operations.
3. Implement file I/O operations in the `Segment` class.
4. Add log compaction functionality to manage log size.
5. Implement crash recovery mechanism.
6. Enhance the CLI for better user interaction.
7. Add comprehensive error handling and logging.
8. Write unit tests for all implemented functionality.

## Implementation Guidelines
- Use append-only logs for write operations.
- Implement an in-memory index for fast key lookups.
- Ensure data persistence across program restarts.
- Implement efficient file I/O operations.
- Follow Python best practices and PEP 8 style guide.

## Getting Started
1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
4. Install required packages: `pip install -r requirements.txt`
5. Run the program: `python main.py`

## Testing
- Navigate to the project root directory.
- Run tests using pytest: `PYTHONPATH=. pytest`
- For more verbose output: `PYTHONPATH=. pytest -v`
- To run a specific test file: `PYTHONPATH=. pytest tests/test_key_value_store.py`

## Initial Tests

We've provided some basic tests in `tests/test_key_value_store.py`. These tests cover:

- Basic functionality of LogStructuredStore
- MemTable operations
- Segment file operations
- An end-to-end test of the key-value store

To run these tests:

1. Ensure you're in the project root directory
2. Run `pytest tests/test_key_value_store.py`

You are expected to:

1. Ensure all provided tests pass as you implement the functionality
2. Add more detailed tests to cover edge cases, error conditions, and additional functionality
3. Implement the suggested additional tests mentioned in the test file comments

Remember, thorough testing is crucial for ensuring the reliability and correctness of your key-value store implementation.

## Running the Program
From the project root directory:
`python -m src.main`

## Evaluation Criteria
- Correctness: The key-value store should correctly handle put, get, and delete operations.
- Persistence: Data should survive program restarts.
- Efficiency: Read and write operations should be reasonably fast, even with a large number of entries.
- Code Quality: Well-organized, commented, and following Python best practices.
- Testing: Comprehensive unit tests and integration tests.

## Resources
- "Designing Data-Intensive Applications" by Martin Kleppmann (Chapters 1-3)
- Python documentation: https://docs.python.org/3/
- Pytest documentation: https://docs.pytest.org/

Good luck, and happy coding!