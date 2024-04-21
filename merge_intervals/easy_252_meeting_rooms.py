from typing import List

class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        """
        The time complexity is O(n log n).
        The space complexity is O(1).
        """
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i - 1][1] > intervals[i][0]:
                return False
        return True
