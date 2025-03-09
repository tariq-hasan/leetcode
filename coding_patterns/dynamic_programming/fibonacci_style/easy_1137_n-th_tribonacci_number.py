class Solution:
    def tribonacci(self, n: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if n < 3:
            return 1 if n else 0
        i, j, k = 0, 1, 1
        for _ in range(n - 2):
            i, j, k = j, k, i + j + k
        return k
