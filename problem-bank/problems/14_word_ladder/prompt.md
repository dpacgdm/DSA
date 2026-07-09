# Word Ladder length (LC 127 simplified)

Return the number of words in the shortest transformation sequence from `begin_word` to `end_word`,
where each step changes exactly one letter and every intermediate word is in `word_list`.
Return `0` if no such sequence exists.

`begin_word` does not need to be in `word_list`. `end_word` must be reachable via `word_list`.

## API

```python
def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int
```
