from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = 0
        for num in nums:
            out = out ^ num
        return out
