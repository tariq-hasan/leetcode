from typing import List


class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        answer = [0] * (n + 1)
        for booking in bookings:
            start, end, seats = booking
            answer[start - 1] = answer[start - 1] + seats
            answer[end] = answer[end] - seats
        for i in range(1, len(answer)):
            answer[i] = answer[i - 1] + answer[i]
        return answer[:-1]
