from typing import List


class Solution:
    def minAvailableDuration(self, slots1: List[List[int]], slots2: List[List[int]], duration: int) -> List[int]:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        slots1, slots2 = sorted(slots1), sorted(slots2)
        i = j = 0
        while i < len(slots1) and j < len(slots2):
            start = max(slots1[i][0], slots2[j][0])
            end = min(slots1[i][1], slots2[j][1])
            if end - start > duration:
                return [start, start + duration]
            if slots1[i][1] < slots2[j][1]:
                i = i + 1
            else:
                j = j + 1
        return []
