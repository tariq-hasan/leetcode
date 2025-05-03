from typing import List


class Solution:
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        def sliding_window_at_most(nums: List[int], distinct_k: int) -> int:
            i = out = 0
            freq = {}
            for j in range(len(nums)):
                freq[nums[j]] = freq.get(nums[j], 0) + 1
                while len(freq) > distinct_k:
                    freq[nums[i]] = freq[nums[i]] - 1
                    if freq[nums[i]] == 0:
                        del freq[nums[i]]
                    i = i + 1
                out = out + j - i + 1
            return out

        return sliding_window_at_most(nums, k) - sliding_window_at_most(nums, k - 1)
