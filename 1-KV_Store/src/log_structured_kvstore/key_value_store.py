from abc import ABC, abstractmethod
from typing import Optional

class KeyValueStore(ABC):
    @abstractmethod
    def put(self, key: str, value: bytes) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[bytes]:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass