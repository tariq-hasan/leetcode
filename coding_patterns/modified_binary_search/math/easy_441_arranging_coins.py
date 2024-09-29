class Solution:
    def arrangeCoins(self, n: int) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        left, right = 1, n
        while left <= right:
            mid = left + (right - left) // 2
            total = ((mid) * (mid + 1)) / 2
            if total < n:
                left = mid + 1
            elif total > n:
                right = mid - 1
            else:
                return mid
        return right
