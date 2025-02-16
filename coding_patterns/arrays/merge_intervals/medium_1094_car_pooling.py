from typing import List


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        timestamp = []
        for trip in trips:
            timestamp.append([trip[1], trip[0]])
            timestamp.append([trip[2], -trip[0]])

        timestamp.sort()

        used_capacity = 0
        for _, passenger_change in timestamp:
            used_capacity = used_capacity + passenger_change
            if used_capacity > capacity:
                return False

        return True


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        timestamp = [0] * 1001
        for trip in trips:
            timestamp[trip[1]] += trip[0]
            timestamp[trip[2]] -= trip[0]

        used_capacity = 0
        for passenger_change in timestamp:
            used_capacity = used_capacity + passenger_change
            if used_capacity > capacity:
                return False

        return True
