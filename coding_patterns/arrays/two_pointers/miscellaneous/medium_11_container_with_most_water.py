from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i, j = 0, len(height) - 1
        max_area = 0
        while i < j:
            area = (j - i) * min(height[i], height[j])
            max_area = max(area, max_area)
            if height[i] < height[j]:
                i = i + 1
            else:
                j = j - 1
        return max_area
