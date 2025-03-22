from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = j = 0
        for num in nums:
            i, j = j, max(num + i, j)
        return j


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = j = k = 0
        for num in nums:
            i, j, k = j, k, max(i, j) + num
        return max(j, k)
