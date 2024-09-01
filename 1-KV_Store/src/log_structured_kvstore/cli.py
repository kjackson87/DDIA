from .key_value_store import KeyValueStore
from .config import Config
from typing import List

class CLI:
    def __init__(self, store: KeyValueStore, config: Config):
        self.store = store
        self.config = config

    def run(self) -> None:
        print("Welcome to the Log-Structured Key-Value Store!")
        print("Type 'help' for a list of commands.")

        while True:
            try:
                command = input("Enter command: ").strip().lower()
                if command == "exit":
                    print("Goodbye!")
                    break
                elif command == "help":
                    self.print_help()
                elif command == "put":
                    self.handle_put()
                elif command == "get":
                    self.handle_get()
                elif command == "delete":
                    self.handle_delete()
                elif command == "list":
                    self.handle_list()
                elif command == "stats":
                    self.handle_stats()
                elif command == "compact":
                    self.handle_compact()
                else:
                    print("Invalid command. Type 'help' for a list of commands.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def print_help(self) -> None:
        print("\nAvailable commands:")
        print("  put     - Store a key-value pair")
        print("  get     - Retrieve a value by key")
        print("  delete  - Delete a key-value pair")
        print("  list    - List all keys in the store")
        print("  stats   - Show store statistics")
        print("  compact - Trigger log compaction")
        print("  help    - Show this help message")
        print("  exit    - Exit the program")

    def handle_put(self) -> None:
        key = input("Enter key: ").strip()
        value = input("Enter value: ").encode()
        self.store.put(key, value)
        print(f"Stored key '{key}' with value '{value.decode()}'")

    def handle_get(self) -> None:
        key = input("Enter key: ").strip()
        value = self.store.get(key)
        if value is not None:
            print(f"Value for key '{key}': {value.decode()}")
        else:
            print(f"No value found for key '{key}'")

    def handle_delete(self) -> None:
        key = input("Enter key to delete: ").strip()
        self.store.delete(key)
        print(f"Deleted key '{key}'")

    def handle_list(self) -> None:
        keys = self.get_all_keys()
        if keys:
            print("Keys in the store:")
            for key in keys:
                print(f"  {key}")
        else:
            print("The store is empty.")

    def handle_stats(self) -> None:
        stats = self.store.get_statistics()
        print("\nStore Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    def handle_compact(self) -> None:
        print("Triggering log compaction...")
        self.store.compact()
        print("Log compaction completed.")

    def get_all_keys(self) -> List[str]:
        # This method assumes that the store has a way to iterate over all keys.
        # If not, you may need to implement this functionality in the LogStructuredStore class.
        # For now, we'll return an empty list as a placeholder.
        return []

# Note: The actual implementation of get_all_keys() will depend on how
# the LogStructuredStore is implemented. Students will need to add this
# functionality to the LogStructuredStore class.