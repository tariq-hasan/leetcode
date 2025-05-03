from typing import List


class Solution:
    def countNegatives(self, grid: List[List[int]]) -> int:
        """
        The time complexity is O(m + n).
        The space complexity is O(1).
        """
        count = 0
        size = len(grid[0])
        index_last_positive = size - 1

        for row in grid:
            while index_last_positive >= 0 and row[index_last_positive] < 0:
                index_last_positive = index_last_positive - 1
            count = count + (size - (index_last_positive + 1))
        return count
