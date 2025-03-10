class Solution:
    def fib(self, n: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if n < 2:
            return n
        i, j = 0, 1
        for _ in range(n - 1):
            i, j = j, i + j
        return j
