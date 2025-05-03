from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        The time complexity is O(n * 2^n).
        The space complexity is O(n * 2^n).
        """
        out = [[]]

        for num in nums:
            out += [curr + [num] for curr in out]

        return out


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        The time complexity is O(n * 2^n).
        The space complexity is O(n).
        """
        def backtrack(first, curr):
            if len(curr) == k:
                subsets.append(curr[:])
                return

            for i in range(first, len(nums)):
                curr.append(nums[i])
                backtrack(i + 1, curr)
                curr.pop()

        subsets = []
        for k in range(len(nums) + 1):
            backtrack(0, [])
        return subsets
