from typing import List


class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        """
        The time complexity is O(log n) + k.
        The space complexity is O(1).
        """
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] <= x:
                left = mid + 1
            elif arr[mid] > x:
                right = mid - 1

        left = left - 2 if arr[left - 1] == x else left - 1
        right = left + 1
        while right - left - 1 < k:
            if left == -1:
                right = right + 1
                continue
            if right == len(arr) or abs(arr[left] - x) <= abs(arr[right] - x):
                left = left - 1
            else:
                right = right + 1

        return arr[left + 1:right]


class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        """
        The time complexity is O(log(n − k) + k).
        The space complexity is O(1).
        """
        left, right = 0, len(arr) - k
        while left < right:
            mid = left + (right - left) // 2
            if x - arr[mid] > arr[mid + k] - x:
                left = mid + 1
            else:
                right = mid

        return arr[left:left + k]
