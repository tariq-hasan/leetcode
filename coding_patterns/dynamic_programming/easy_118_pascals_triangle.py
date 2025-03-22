from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        """
        The time complexity is O(n^2).
        The space complexity is O(1).
        """
        out = []
        for i in range(numRows):
            row = [1] * (i + 1)
            for j in range(1, len(row) - 1):
                row[j] = out[-1][j - 1] + out[-1][j]
            out.append(row)
        return out
