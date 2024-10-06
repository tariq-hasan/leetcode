from typing import List


class Solution:
    def twoSumLessThanK(self, nums: List[int], k: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(log n) to O(n), depending on the implementation of the sorting algorithm.
        """
        nums.sort()
        max_num = -1
        left, right = 0, len(nums) - 1
        while left < right:
            total = nums[left] + nums[right]
            if total < k:
                max_num = max(max_num, total)
                left = left + 1
            else:
                right = right - 1
        return max_num


class Solution:
    def twoSumLessThanK(self, nums: List[int], k: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(log n) to O(n), depending on the implementation of the sorting algorithm.
        """
        nums.sort()
        max_num = -1
        for i in range(len(nums)):
            left, right = i + 1, len(nums) - 1
            while left <= right:
                mid = left + (right - left) // 2
                total = nums[i] + nums[mid]
                if total < k:
                    max_num = max(max_num, total)
                    left = mid + 1
                elif total >= k:
                    right = mid - 1
        return max_num


class Solution:
    def twoSumLessThanK(self, nums: List[int], k: int) -> int:
        """
        The time complexity is O(n + m) where m corresponds to the range of values in the input array.
        The space complexity is O(m) to count each value.
        """
        max_num = -1
        count = [0] * 1001
        for num in nums:
            count[num] = count[num] + 1
        low, high = 1, 1000
        while low <= high:
            if low + high >= k or count[high] == 0:
                high = high - 1
            else:
                if count[low] > (0 if low < high else 1):
                    max_num = max(max_num, low + high)
                low = low + 1
        return max_num
