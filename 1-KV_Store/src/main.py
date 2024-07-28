import os
from .LogStructuredStore import LogStructuredStore
from .CLI import CLI

def main():
    store_directory = "store"
    os.makedirs(store_directory, exist_ok=True)
    store = LogStructuredStore(store_directory)
    cli = CLI(store)
    cli.run()

if __name__ == "__main__":
    main()