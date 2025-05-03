from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        The time complexity is O(n log n).
        The space complexity is O(log n).
        """
        intervals.sort(key=lambda x: x[0])
        out = []
        for interval in intervals:
            if not out or out[-1][1] < interval[0]:
                out.append(interval)
            else:
                out[-1][1] = max(out[-1][1], interval[1])
        return out
