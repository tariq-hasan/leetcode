class Solution:
    def minWindow(self, s1: str, s2: str) -> str:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        dp = [[1000000000] * (len(s2) + 1) for i in range(len(s1) + 1)]
        dp[0][0] = 0
        end = 0
        length = len(s1) + 1
        for i in range(1, len(s1) + 1):
            dp[i][0] = 0
            for j in range(1, len(s2) + 1):
                dp[i][j] = 1 + (dp[i - 1][j - 1] if s1[i - 1] == s2[j - 1]
                                else dp[i - 1][j])
            if dp[i][len(s2)] < length:
                length = dp[i][len(s2)]
                end = i
        return "" if length > len(s1) else s1[end - length:end]
