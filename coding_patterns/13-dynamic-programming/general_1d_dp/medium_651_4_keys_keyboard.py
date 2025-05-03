class Solution:
    def maxA(self, n: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        dp = list(range(n + 1))
        for i in range(n - 2):
            for j in range(i + 3, min(n, i + 6) + 1):
                dp[j] = max(dp[j], (j - i - 1) * dp[i])
        return dp[n]
