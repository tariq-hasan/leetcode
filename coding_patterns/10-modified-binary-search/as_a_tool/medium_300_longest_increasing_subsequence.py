from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        The time complexity is O(n^2).
        The space complexity is O(n).
        """
        dp = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        The time complexity is O(n^2).
        The space complexity is O(n).
        """
        sub = [nums[0]]
        for num in nums[1:]:
            if num > sub[-1]:
                sub.append(num)
            else:
                i = 0
                while num > sub[i]:
                    i = i + 1
                sub[i] = num
        return len(sub)


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        sub = []
        for num in nums:
            left, right = 0, len(sub) - 1
            while left <= right:
                mid = left + (right - left) // 2
                if sub[mid] < num:
                    left = mid + 1
                else:
                    right = mid - 1
            if left == len(sub):
                sub.append(num)
            else:
                sub[left] = num
        return len(sub)
