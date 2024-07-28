from KeyValueStore import KeyValueStore

class CLI:
    def __init__(self, store: KeyValueStore):
        self.store = store

    def run(self) -> None:
        while True:
            command = input("Enter command (put/get/delete/exit): ").strip().lower()
            if command == "exit":
                break
            elif command == "put":
                self.handle_put()
            elif command == "get":
                self.handle_get()
            elif command == "delete":
                self.handle_delete()
            else:
                print("Invalid command")

    def handle_put(self) -> None:
        key = input("Enter key: ")
        value = input("Enter value: ").encode()
        self.store.put(key, value)
        print("Value stored successfully")

    def handle_get(self) -> None:
        key = input("Enter key: ")
        value = self.store.get(key)
        if value is not None:
            print(f"Value: {value.decode()}")
        else:
            print("Key not found")

    def handle_delete(self) -> None:
        key = input("Enter key: ")
        self.store.delete(key)
        print("Key deleted successfully")