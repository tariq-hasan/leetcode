class Solution:
    def numTilings(self, n: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        MOD = 1_000_000_007
        if n <= 2:
            return n

        i, j, k = 1, 2, 1
        for _ in range(3, n + 1):
            tmp = j
            i, j, k = j, (i + j + (2 * k)) % MOD, (i + k) % MOD
        return j
