from typing import List


class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        total = [0] * (max(nums) + 1)
        for num in nums:
            total[num] = total[num] + num

        i = j = 0
        for num in total:
            i, j = j, max(j, i + num)

        return j
