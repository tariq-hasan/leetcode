class Solution:
    def firstBadVersion(self, n: int) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        left, right = 1, n
        while left <= right:
            mid = left + (right - left) // 2
            if isBadVersion(mid):
                right = mid - 1
            else:
                left = mid + 1
        return right + 1
