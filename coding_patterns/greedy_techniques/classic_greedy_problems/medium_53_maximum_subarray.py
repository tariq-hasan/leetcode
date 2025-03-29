import math
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out, total = - math.inf, 0
        for num in nums:
            total = total + num
            out = max(out, total)
            total = 0 if total < 0 else total
        return out
