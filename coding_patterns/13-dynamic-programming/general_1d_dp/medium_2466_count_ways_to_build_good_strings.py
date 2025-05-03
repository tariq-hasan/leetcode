class Solution:
    def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        dp = [1] + [0] * (high)
        mod = 10 ** 9 + 7

        for i in range(1, high + 1):
            if i >= zero:
                dp[i] = dp[i] + dp[i - zero]
            if i >= one:
                dp[i] = dp[i] + dp[i - one]
            dp[i] = dp[i] % mod

        return sum(dp[low : high + 1]) % mod


class Solution:
    def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        dp = [1] + [-1] * (high)
        mod = 10 ** 9 + 7

        def dfs(i):
            if dp[i] != -1:
                return dp[i]
            count = 0
            if i >= zero:
                count = count + dfs(i - zero)
            if i >= one:
                count = count + dfs(i - one)
            dp[i] = count % mod
            return dp[i]

        return sum(dfs(i) for i in range(low, high + 1)) % mod
