from typing import List

class Solution:
    def flipAndInvertImage(self, image: List[List[int]]) -> List[List[int]]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        for row in image:
            for i in range((len(row) + 1) // 2):
                row[i], row[~i] = row[~i] ^ 1, row[i] ^ 1
        return image


class Solution:
    def flipAndInvertImage(self, image: List[List[int]]) -> List[List[int]]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        for row in image:
            i, j = 0, len(row) - 1
            while i <= j:
                row[i], row[j] = row[j] ^ 1, row[i] ^ 1
                i, j = i + 1, j - 1
        return image
