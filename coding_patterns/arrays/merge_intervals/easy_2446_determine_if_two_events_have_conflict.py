from typing import List


class Solution:
    def haveConflict(self, event1: List[str], event2: List[str]) -> bool:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        if event1[0] <= event2[0] <= event1[1]:
            return True

        if event2[0] <= event1[0] <= event2[1]:
            return True

        return False
