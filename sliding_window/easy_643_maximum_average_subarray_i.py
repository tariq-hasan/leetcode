from typing import List

class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        total = sum(nums[:k])
        max_total = total
        for j in range(len(nums) - k):
            total = total - nums[j] + nums[j + k]
            max_total = max(max_total, total)
        return max_total / k
