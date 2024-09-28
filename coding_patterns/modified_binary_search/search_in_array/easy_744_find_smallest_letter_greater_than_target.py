from typing import List


class Solution:
    def nextGreatestLetter(self, letters: List[str], target: str) -> str:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        left, right = 0, len(letters) - 1
        while left <= right:
            mid = (left + right) // 2
            if letters[mid] <= target:
                left = mid + 1
            else:
                right = mid - 1
        return letters[0] if left == len(letters) else letters[left]
