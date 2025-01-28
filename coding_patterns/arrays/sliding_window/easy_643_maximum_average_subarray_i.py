from typing import List

class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        total = 0
        for i in range(k):
            total = total + nums[i]

        out = total
        for i in range(k, len(nums)):
            total = total + nums[i] - nums[i - k]
            out = max(out, total)
        return out / k
