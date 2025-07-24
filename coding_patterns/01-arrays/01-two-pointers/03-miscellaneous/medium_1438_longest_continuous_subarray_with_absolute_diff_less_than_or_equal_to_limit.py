import heapq
from typing import List


class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        max_heap, min_heap = [], []
        i = out = 0
        for j in range(len(nums)):
            heapq.heappush(max_heap, (-nums[j], j))
            heapq.heappush(min_heap, (nums[j], j))
            while -max_heap[0][0] - min_heap[0][0] > limit:
                i = min(max_heap[0][1], min_heap[0][1]) + 1
                while max_heap[0][1] < i:
                    heapq.heappop(max_heap)
                while min_heap[0][1] < i:
                    heapq.heappop(min_heap)
            out = max(out, j - i + 1)
        return out
