from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        ans = cur_end = cur_far = 0
        for i in range(len(nums) - 1):
            cur_far = max(cur_far, i + nums[i])
            if i == cur_end:
                ans = ans + 1
                cur_end = cur_far
        return ans
