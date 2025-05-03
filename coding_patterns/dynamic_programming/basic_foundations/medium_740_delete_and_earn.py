from typing import List


class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        """
        Determine the maximum points you can earn by performing the following operation:

        1. Take any nums[i] and earn nums[i] points
        2. Delete every element equal to nums[i] - 1 and nums[i] + 1
        3. Repeat until array becomes empty

        This can be transformed into a house robber problem where:
        - For each unique number, we sum its total points
        - We can't take adjacent numbers, similar to not robbing adjacent houses

        Args:
            nums: A list of integers

        Returns:
            The maximum points you can earn

        Time Complexity: O(n + k) - Where k is the maximum value in nums
        Space Complexity: O(k) - We need to store points for each unique value
        """
        # Transform the problem into a house robber problem
        # Create an array where index i contains total points from value i
        max_num = max(nums)
        points = [0] * (max_num + 1)

        # Sum up points for each number
        for num in nums:
            points[num] += num

        # Apply house robber algorithm on the points array
        prev_max = curr_max = 0
        for point in points:
            # For each value, we either take it (and skip the previous value)
            # or skip it (and keep the previous maximum)
            prev_max, curr_max = curr_max, max(point + prev_max, curr_max)

        return curr_max
