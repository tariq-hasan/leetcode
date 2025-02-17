from typing import List


class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = 0
        out = []

        while i < len(intervals) and intervals[i][1] < newInterval[0]:
            out.append(intervals[i])
            i = i + 1

        while i < len(intervals) and newInterval[1] >= intervals[i][0]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i = i + 1
        out.append(newInterval)

        while i < len(intervals):
            out.append(intervals[i])
            i = i + 1

        return out
