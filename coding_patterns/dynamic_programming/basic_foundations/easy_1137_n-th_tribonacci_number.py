class Solution:
    def tribonacci(self, n: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if n < 2:
            return n

        i, j, k = 0, 1, 1
        for _ in range(n - 2):
            i, j, k = j, k, i + j + k

        return k
