from typing import List

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = len(nums)
        for i, num in enumerate(nums):
            out = out ^ i ^ num
        return out
