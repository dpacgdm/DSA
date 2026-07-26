# Sliding-Window Rate Limiter

`allow()` returns True if an event is permitted under: at most `limit`
events in any rolling window of `window_seconds` ending now.
Use injectable `time_fn`.

## API
```python
class SlidingWindowLogLimiter:
    def __init__(self, limit: int, window_seconds: float, time_fn): ...
    def allow(self) -> bool: ...
```
