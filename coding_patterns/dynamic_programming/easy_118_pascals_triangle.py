from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        """
        The time complexity is O(n^2).
        The space complexity is O(1).
        """
        out = []
        for i in range(numRows):
            row = [None for _ in range(i + 1)]
            row[0], row[-1] = 1, 1
            for j in range(1, len(row) - 1):
                row[j] = out[i - 1][j - 1] + out[i - 1][j]
            out.append(row)
        return out
