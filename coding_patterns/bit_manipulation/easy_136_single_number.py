from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        res = 0
        for num in nums:
            res = res ^ num
        return res
