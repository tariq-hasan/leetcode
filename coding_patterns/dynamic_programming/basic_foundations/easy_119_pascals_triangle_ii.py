from typing import List


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        """
        The time complexity is O(n^2).
        The space complexity is O(1).
        """
        out = [1] * (rowIndex + 1)
        for i in range(rowIndex - 1):
            for j in range(i, -1, -1):
                out[j + 1] = out[j] + out[j + 1]
        return out
