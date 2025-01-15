from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i, j = 0, len(nums) - 1
        res = []
        while i <= j:
            if abs(nums[i]) >= abs(nums[j]):
                res.append(nums[i] * nums[i])
                i = i + 1
            else:
                res.append(nums[j] * nums[j])
                j = j - 1
        return res[::-1]


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        res = [0] * len(nums)
        i, j = 0, len(nums) - 1
        for k in range(len(nums) - 1, -1, -1):
            if abs(nums[i]) >= abs(nums[j]):
                res[k] = nums[i] * nums[i]
                i = i + 1
            else:
                res[k] = nums[j] * nums[j]
                j = j - 1
        return res
