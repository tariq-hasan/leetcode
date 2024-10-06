# """
# This is ArrayReader's API interface.
# You should not implement it, or speculate about its implementation
# """
#class ArrayReader:
#    def get(self, index: int) -> int:

class Solution:
    def search(self, reader: 'ArrayReader', target: int) -> int:
        """
        The time complexity is O(log T), where T is the index of target value.
        The space complexity is O(1).
        """
        if reader.get(0) == target:
            return 0

        left, right = 0, 1
        while reader.get(right) < target:
            left = right
            right = right << 1

        while left <= right:
            mid = left + (right - left) // 2
            if reader.get(mid) < target:
                left = mid + 1
            elif reader.get(mid) == (2 ** 31) - 1 or reader.get(mid) > target:
                right = mid - 1
            else:
                return mid
        return -1
