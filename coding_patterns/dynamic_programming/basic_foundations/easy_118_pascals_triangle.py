from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        """
        The time complexity is O(n^2).
        The space complexity is O(1).
        """
        out = []
        for i in range(numRows):
            arr = [1] * (i + 1)
            for j in range(i - 1):
                arr[j + 1] = out[-1][j] + out[-1][j + 1]
            out.append(arr)
        return out
