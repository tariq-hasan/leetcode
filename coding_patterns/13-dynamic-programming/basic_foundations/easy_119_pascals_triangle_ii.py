from typing import List


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        """
        Returns the rowIndex-th row of Pascal's Triangle.

        In Pascal's Triangle, each number is the sum of the two numbers directly above it.

        Args:
            rowIndex: The zero-indexed row to return

        Returns:
            A list representing the requested row of Pascal's Triangle

        Time Complexity: O(rowIndex²) - We compute each element once
        Space Complexity: O(rowIndex) - We only store one row at a time
        """
        row = [1] * (rowIndex + 1)

        for i in range(1, rowIndex + 1):
            # Update from right to left to avoid overwriting values needed later
            for j in range(i - 1, 0, -1):
                row[j] = row[j] + row[j - 1]

        return row
