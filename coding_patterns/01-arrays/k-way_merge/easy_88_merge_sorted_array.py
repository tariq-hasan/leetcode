from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        The time complexity is O(m + n).
        The space complexity is O(n).
        """
        i, j = m - 1, n - 1
        for k in range(m + n - 1, -1, -1):
            if j < 0:
                break
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i = i - 1
            else:
                nums1[k] = nums2[j]
                j = j - 1
