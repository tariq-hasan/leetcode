import math
from typing import List


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        """
        The time complexity is O(n^2).
        The space complexity is O(n).
        """
        dp = [0] * len(triangle)
        dp[0] = triangle[0][0]
        for row in triangle[1:]:
            for i in range(len(row) - 1, -1, -1):
                if i == len(row) - 1:
                    dp[i] = dp[i - 1] + row[i]
                elif i == 0:
                    dp[i] = dp[i] + row[i]
                else:
                    dp[i] = min(dp[i] + row[i], dp[i - 1] + row[i])
        return min(dp)


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        """
        The time complexity is O(n^2).
        The space complexity is O(1).
        """
        for row in range(1, len(triangle)):
            for col in range(row + 1):
                smallest_above = math.inf
                if col > 0:
                    smallest_above = triangle[row - 1][col - 1]
                if col < row:
                    smallest_above = min(smallest_above, triangle[row - 1][col])
                triangle[row][col] += smallest_above
        return min(triangle[-1])


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        """
        The time complexity is O(n^2).
        The space complexity is O(n).
        """
        prev_row = triangle[0]
        for row in range(1, len(triangle)):
            curr_row = []
            for col in range(row + 1):
                smallest_above = math.inf
                if col > 0:
                    smallest_above = prev_row[col - 1]
                if col < row:
                    smallest_above = min(smallest_above, prev_row[col])
                curr_row.append(triangle[row][col] + smallest_above)
            prev_row = curr_row
        return min(prev_row)
