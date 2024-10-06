from typing import List


class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(1).
        """
        left, right = max(weights), sum(weights)
        while left < right:
            mid = left + (right - left) // 2
            days_to_ship, total_weight = 1, mid
            for weight in weights:
                if total_weight < weight:
                    days_to_ship, total_weight, = days_to_ship + 1, mid
                total_weight = total_weight - weight
            if days_to_ship > days:
                left = mid + 1
            else:
                right = mid
        return left
