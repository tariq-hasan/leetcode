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
        i = j = 0
        for num in nums[::-1]:
            i, j = max(i, j + num), i
        return i
