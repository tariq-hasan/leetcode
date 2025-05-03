class Solution:
    def minPathSum(self, grid):
        """
        The time complexity is O(m * n).
        The space complexity is O(n).
        """
        dp = [0 for _ in range(len(grid[0]))]
        for i in range(len(grid) - 1, -1, -1):
            for j in range(len(grid[0]) - 1, -1, -1):
                if i == len(grid) - 1 and j != len(grid[0]) - 1:
                    dp[j] = grid[i][j] + dp[j + 1]
                elif j == len(grid[0]) - 1 and i != len(grid) - 1:
                    dp[j] = grid[i][j] + dp[j]
                elif i != len(grid) - 1 and j != len(grid[0]) - 1:
                    dp[j] = grid[i][j] + min(dp[j], dp[j + 1])
                else:
                    dp[j] = grid[i][j]
        return dp[0]


class Solution:
    def minPathSum(self, grid):
        """
        The time complexity is O(m * n).
        The space complexity is O(1).
        """
        for i in reversed(range(len(grid))):
            for j in reversed(range(len(grid[0]))):
                if i == len(grid) - 1 and j != len(grid[0]) - 1:
                    grid[i][j] += grid[i][j + 1]
                elif j == len(grid[0]) - 1 and i != len(grid) - 1:
                    grid[i][j] += grid[i + 1][j]
                elif j != len(grid[0]) - 1 and i != len(grid) - 1:
                    grid[i][j] += min(grid[i + 1][j], grid[i][j + 1])
        return grid[0][0]
