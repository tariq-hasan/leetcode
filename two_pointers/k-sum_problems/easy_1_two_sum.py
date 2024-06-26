from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        map_index = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in map_index:
                return [i, map_index[complement]]
            map_index[nums[i]] = i
