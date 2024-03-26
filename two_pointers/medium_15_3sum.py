class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        The time complexity is O(n^2).
        The space complexity is O(log n) or O(n)
        depending on the implementation of the sorting algorithm.
        """
        res = []
        nums.sort()
        for i in range(len(nums)):
            if nums[i] > 0: break
            if i == 0 or nums[i - 1] != nums[i]:
                j, k = i + 1, len(nums) - 1
                while j < k:
                    if nums[i] + nums[j] + nums[k] < 0: j = j + 1
                    elif nums[i] + nums[j] + nums[k] > 0: k = k - 1
                    else:
                        res.append([nums[i], nums[j], nums[k]])
                        j, k = j + 1, k - 1
                        while j < k and nums[j - 1] == nums[j]:
                            j = j + 1
        return res
