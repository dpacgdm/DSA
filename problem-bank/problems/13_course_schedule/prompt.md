# Course Schedule (LC 207)

There are `num_courses` labeled `0` to `num_courses - 1`.
`prerequisites[i] = [a, b]` means you must take course `b` before `a`.

Return `True` if you can finish all courses, else `False` (detect cycle).

## API

```python
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool
```
