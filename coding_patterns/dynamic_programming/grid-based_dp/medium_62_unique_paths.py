class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        The time complexity is O(n * m).
        The space complexity is O(n * m).
        """
        dp = [[1] * n] * m
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        return dp[m - 1][n - 1]
