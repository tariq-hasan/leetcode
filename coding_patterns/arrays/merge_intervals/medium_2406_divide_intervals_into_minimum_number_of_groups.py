from typing import List


class Solution:
    def minGroups(self, intervals: List[List[int]]) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        events = []
        for interval in intervals:
            events.append((interval[0], 1))
            events.append((interval[1] + 1, -1))
        events.sort(key=lambda x: (x[0], x[1]))

        concurrent_intervals = out = 0
        for event in events:
            concurrent_intervals = concurrent_intervals + event[1]
            out = max(out, concurrent_intervals)
        return out



