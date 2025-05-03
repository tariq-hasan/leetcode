from typing import List


class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        intervals.sort(key = lambda x: (x[0], -x[1]))
        out = 0
        prev_end = 0
        for _, end in intervals:
            if end > prev_end:
                out = out + 1
                prev_end = end
        return out
