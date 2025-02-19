from typing import List

class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = []
        i = 0
        while i < len(nums): 
            start = nums[i]
            while i + 1 < len(nums) and nums[i] + 1 == nums[i + 1]:
                i = i + 1
            if start != nums[i]:
                out.append(str(start) + "->" + str(nums[i]))
            else:
                out.append(str(nums[i]))
            i = i + 1
        return out
