class MinStack:
    def __init__(self):
        self.st = []
        self.mins = []
    def push(self, val: int) -> None:
        self.st.append(val)
        self.mins.append(val if not self.mins else min(val, self.mins[-1]))
    def pop(self) -> None:
        self.st.pop(); self.mins.pop()
    def top(self) -> int:
        return self.st[-1]
    def get_min(self) -> int:
        return self.mins[-1]
