from typing import List

class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        ranges = []
        i = 0
        for j in range(len(nums)):
            if (j < len(nums) - 1 and nums[j] + 1 != nums[j + 1]) or (j == len(nums) - 1):
                if i == j:
                    ranges.append(f"{nums[i]}")
                else:
                    ranges.append(f"{nums[i]}->{nums[j]}")
                i = j + 1
        return ranges
