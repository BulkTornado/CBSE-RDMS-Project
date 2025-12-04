import random

class StringUtilities:
    
    """Provides various string operations with history tracking."""

    def __init__(self, max_history: int | None = None):
        """Initialises a list of tuples for history.
        :param max_history: Optional limit on history length.
        """
        self.history: list[tuple[str, str, str]] = []
        self.max_history = max_history

    def __len__(self) -> int:
        """Returns number of operations recorded."""
        return len(self.history)

    def __str__(self) -> str:
        """Returns the history in readable format."""
        return ",\n".join([f"{name}('{inp}' -> '{out}')" for name, inp, out in self.history])

    def __repr__(self) -> str:
        """Returns debugging representation."""
        return (f"StringOperation("
                f"history={self.history}, "
                f"max_history={self.max_history})")
    
    def _record(self, op_name: str, inp: str, out: str) -> None:
        """Updates the history for each operation call.
        
        If :param max_history has been passed, removes the oldest element when len(history) > max_history."""
        self.history.append((op_name, inp, out))
        if self.max_history and len(self.history) > self.max_history:
            self.history.pop(0)  # remove oldest

    def randomCase(self, string: str) -> str:
        """Randomly switch case of each character."""
        result = "".join(char.upper() if random.randint(0, 10) in (1, 6, 7) else char.lower() for char in string)
        self._record("randomCase", string, result)
        return result

    def swapCase(self, string: str) -> str:
        """Swap the case of each character."""
        result = "".join(char.lower() if char.isupper() else char.upper() for char in string)
        self._record("swapCase", string, result)
        return result
    
    def charCount(self, string: str) -> dict:
        frequency = {}
        for char in string:
            if char not in frequency:
                frequency.update({char: 1})
            else:
                frequency[char] += 1
        self._record("charCount", string, str(frequency))
        
        return frequency
    
    def maxFrequency(self, string: str) -> tuple[str, int]:
        """Returns the char in string that
        has the maximum frequency, and the
        frequency of that char."""
        
        frequency = StringUtilities.charCount(self, string)
        frequency = {v:k for k,v in frequency.items()}
        
        max_frequency= max(list(frequency.keys()))
        char = frequency.get(max_frequency, "")
        self._record("maxFrequency", char, str(max_frequency))
        return char, max_frequency


# Operation variable

def main():
    op = StringUtilities()
    print(op.randomCase("Hello, World!"))
    print(op.swapCase("Goodbye, World!"))
    print(op.maxFrequency("Hello, World!. Goodbye, World!"))
    print(op.charCount("Hello, World!. Goodbye, World!"))
    print(op)

if __name__ == "__main__":
    main()