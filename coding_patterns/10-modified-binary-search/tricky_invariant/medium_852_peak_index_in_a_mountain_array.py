from typing import List


class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        left, right = 0, len(arr) - 1
        while left < right:
            mid = (left + right) // 2
            if arr[mid] < arr[mid + 1]:
                left = mid + 1
            else:
                right = mid
        return left
