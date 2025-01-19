from typing import List


class Solution:
    def circularArrayLoop(self, nums: List[int]) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        def next_idx(nums, idx, direction):
            if idx == -1 or (nums[idx] > 0) != direction:
                return -1

            next_idx = (idx + nums[idx]) % len(nums)
            if next_idx < 0:
                next_idx = next_idx + len(nums)
            return -1 if next_idx == idx else next_idx

        for i in range(len(nums)):
            if nums[i] == 0:
                continue

            direction = nums[i] > 0
            slow = fast = i
            while nums[slow] or nums[fast]:
                slow = next_idx(nums, slow, direction)
                fast = next_idx(nums, next_idx(nums, fast, direction), direction)
                if slow == -1 or fast == -1:
                    break
                elif slow == fast:
                    return True

            slow = i
            while next_idx(nums, slow, direction) != -1:
                nums[slow], slow = 0, next_idx(nums, slow, direction)

        return False
