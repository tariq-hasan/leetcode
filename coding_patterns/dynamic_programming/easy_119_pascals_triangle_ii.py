from typing import List


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        """
        The time complexity is O(n^2).
        The space complexity is O(1).
        """
        out = [1] * (rowIndex + 1)
        for i in range(1, rowIndex):
            for j in range(i, 0, -1):
                out[j] = out[j] + out[j - 1]
        return out
