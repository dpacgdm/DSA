# LRU Cache (LC 146)

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement `LRUCache` class:
- `LRUCache(int capacity)`
- `int get(int key)` — return value or -1
- `void put(int key, int value)` — insert/update; evict LRU if over capacity

All operations must be O(1) average time.

## API

```python
class LRUCache:
    def __init__(self, capacity: int): ...
    def get(self, key: int) -> int: ...
    def put(self, key: int, value: int) -> None: ...
```
