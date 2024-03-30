from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i, j = 0, len(numbers) - 1
        while i < j:
            total = numbers[i] + numbers[j]
            if total < target:
                i = i + 1
            elif total > target:
                j = j - 1
            else:
                return [i + 1, j + 1]
