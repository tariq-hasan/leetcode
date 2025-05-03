from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        The time complexity is O(n log m), where m is the maximum number of bananas in a single pile from piles.
        The space complexity is O(1).
        """
        left, right = 1, max(piles)
        while left < right:
            mid = left + (right - left) // 2
            hour_spent = sum([math.ceil(pile / mid) for pile in piles])
            if hour_spent > h:
                left = mid + 1
            else:
                right = mid
        return left
