# Insert Delete GetRandom O(1) (LC 380)

Design a data structure that supports insert, remove, and getRandom in average O(1):

- `insert(val)` → True if not present
- `remove(val)` → True if present
- `get_random()` → random element uniformly among current elements

## API

```python
class RandomizedSet:
    def insert(self, val: int) -> bool: ...
    def remove(self, val: int) -> bool: ...
    def get_random(self) -> int: ...
```
