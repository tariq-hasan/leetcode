"""
LeetCode 90. Subsets II
Problem: Given an integer array nums that may contain duplicates, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.

Example:
Input: nums = [1,2,2]
Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]

Key Insights:
1. Need to handle duplicates to avoid duplicate subsets
2. Sort the array first to group duplicates together
3. Skip duplicates at the same recursion level
"""

from typing import List

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 1: Backtracking with Skip Duplicates
        Time: O(2^n * n) where n is length of nums
        Space: O(n) for recursion depth
        """
        result = []
        nums.sort()  # Sort to group duplicates together
        
        def backtrack(start, path):
            # Add current subset to result
            result.append(path[:])  # Make a copy of current path
            
            for i in range(start, len(nums)):
                # Skip duplicates: if current element equals previous element
                # and we're not at the start position, skip it
                if i > start and nums[i] == nums[i-1]:
                    continue
                
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()  # backtrack
        
        backtrack(0, [])
        return result

    def subsetsWithDup_v2(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 2: Iterative approach
        Time: O(2^n * n)
        Space: O(2^n * n) for storing all subsets
        """
        nums.sort()
        result = [[]]
        
        for i, num in enumerate(nums):
            # If current number is duplicate, only add to subsets 
            # that were created in the previous iteration
            if i > 0 and nums[i] == nums[i-1]:
                # Only extend subsets from previous iteration
                start_idx = prev_size
            else:
                # Extend all existing subsets
                start_idx = 0
            
            prev_size = len(result)
            
            # Add current number to existing subsets
            for j in range(start_idx, prev_size):
                result.append(result[j] + [num])
        
        return result

    def subsetsWithDup_v3(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 3: Using set to handle duplicates (less efficient)
        Time: O(2^n * n * log(2^n)) due to set operations
        Space: O(2^n * n)
        """
        result = []
        nums.sort()
        
        def backtrack(start, path):
            result.append(path[:])
            
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()
        
        backtrack(0, [])
        
        # Remove duplicates using set (convert lists to tuples)
        unique_subsets = set()
        for subset in result:
            unique_subsets.add(tuple(subset))
        
        return [list(subset) for subset in unique_subsets]

# Test the solutions
def test_solutions():
    solution = Solution()
    
    # Test case 1
    nums1 = [1, 2, 2]
    print("Input:", nums1)
    print("Output (Backtracking):", solution.subsetsWithDup(nums1))
    print("Output (Iterative):", solution.subsetsWithDup_v2(nums1))
    print()
    
    # Test case 2
    nums2 = [0]
    print("Input:", nums2)
    print("Output:", solution.subsetsWithDup(nums2))
    print()
    
    # Test case 3
    nums3 = [1, 2, 2, 3]
    print("Input:", nums3)
    print("Output:", solution.subsetsWithDup(nums3))

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW TALKING POINTS:

1. Problem Analysis:
   - This is a variation of the classic "Subsets" problem with duplicates
   - Key challenge: avoiding duplicate subsets in the result
   - Need to systematically generate all possible combinations

2. Approach Explanation:
   - Sort the array first to group duplicates together
   - Use backtracking to generate all subsets
   - Skip duplicates at the same recursion level to avoid duplicate subsets
   
3. The Skip Logic:
   - "if i > start and nums[i] == nums[i-1]: continue"
   - This ensures we only skip duplicates when they're not the first choice at a level
   - We can choose the first occurrence of a duplicate but skip subsequent ones

4. Time/Space Complexity:
   - Time: O(2^n * n) - 2^n subsets, each taking O(n) time to copy
   - Space: O(n) for recursion depth (not counting output space)

5. Edge Cases to Consider:
   - Empty array
   - Array with all duplicates
   - Array with no duplicates
   - Single element array

6. Alternative Approaches:
   - Iterative approach (shown in v2)
   - Using set for deduplication (less efficient, shown in v3)
   - Bit manipulation (possible but more complex with duplicates)
"""
