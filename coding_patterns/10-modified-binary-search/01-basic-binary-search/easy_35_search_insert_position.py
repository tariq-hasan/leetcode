"""
LeetCode 35. Search Insert Position
Problem: Given a sorted array of distinct integers and a target value, 
return the index if the target is found. If not, return the index where 
it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

Example:
Input: nums = [1,3,5,6], target = 5
Output: 2

Input: nums = [1,3,5,6], target = 2
Output: 1

Input: nums = [1,3,5,6], target = 7
Output: 4

Key Insights:
1. This is a classic binary search problem
2. We're looking for the leftmost position where target can be inserted
3. If target exists, return its index; if not, return insertion position
"""

from typing import List

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        Approach 1: Standard Binary Search
        Time: O(log n)
        Space: O(1)
        
        This is the most straightforward approach that most candidates should use.
        """
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = left + (right - left) // 2  # Avoid overflow
            
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        # If target not found, left is the insertion position
        return left

    def searchInsert_v2(self, nums: List[int], target: int) -> int:
        """
        Approach 2: Binary Search - Find leftmost position
        Time: O(log n)
        Space: O(1)
        
        This approach directly finds the leftmost position where target 
        should be inserted, treating it as a "lower bound" problem.
        """
        left, right = 0, len(nums)
        
        while left < right:
            mid = left + (right - left) // 2
            
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        
        return left

    def searchInsert_v3(self, nums: List[int], target: int) -> int:
        """
        Approach 3: Using Python's bisect module (for reference)
        Time: O(log n)
        Space: O(1)
        
        This shows the built-in solution, but you should implement it yourself.
        """
        import bisect
        return bisect.bisect_left(nums, target)

    def searchInsert_linear(self, nums: List[int], target: int) -> int:
        """
        Approach 4: Linear Search (Not optimal - O(n) time)
        Time: O(n)
        Space: O(1)
        
        This is the brute force approach. Don't use this in an interview
        unless specifically asked, but good to mention as baseline.
        """
        for i in range(len(nums)):
            if nums[i] >= target:
                return i
        return len(nums)

    def searchInsert_recursive(self, nums: List[int], target: int) -> int:
        """
        Approach 5: Recursive Binary Search
        Time: O(log n)
        Space: O(log n) due to recursion stack
        
        Recursive version - good to know but iterative is preferred.
        """
        def binary_search(left, right):
            if left > right:
                return left
            
            mid = left + (right - left) // 2
            
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                return binary_search(mid + 1, right)
            else:
                return binary_search(left, mid - 1)
        
        return binary_search(0, len(nums) - 1)

# Test the solutions
def test_solutions():
    solution = Solution()
    
    test_cases = [
        ([1, 3, 5, 6], 5, 2),  # target found
        ([1, 3, 5, 6], 2, 1),  # insert in middle
        ([1, 3, 5, 6], 7, 4),  # insert at end
        ([1, 3, 5, 6], 0, 0),  # insert at beginning
        ([1], 1, 0),           # single element, found
        ([1], 0, 0),           # single element, insert before
        ([1], 2, 1),           # single element, insert after
        ([], 1, 0),            # empty array
    ]
    
    for nums, target, expected in test_cases:
        result1 = solution.searchInsert(nums, target)
        result2 = solution.searchInsert_v2(nums, target)
        
        print(f"nums: {nums}, target: {target}")
        print(f"Expected: {expected}, Got: {result1}, {result2}")
        print(f"Correct: {result1 == expected and result2 == expected}")
        print()

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW TALKING POINTS:

1. Problem Analysis:
   - This is a classic binary search problem
   - We need to find either the exact position or the insertion position
   - The key insight is that after binary search, 'left' pointer gives us the answer

2. Why Binary Search Works:
   - Array is sorted, so we can eliminate half the search space each time
   - We're essentially finding the "lower bound" - first position >= target
   - If target exists, we find it; if not, we find where it should go

3. Edge Cases to Consider:
   - Empty array
   - Target smaller than all elements (insert at beginning)
   - Target larger than all elements (insert at end)  
   - Target equals an existing element
   - Single element array

4. Common Pitfalls:
   - Off-by-one errors in loop conditions
   - Integer overflow in mid calculation (use left + (right-left)//2)
   - Forgetting that 'left' gives the insertion position when target not found

5. Time Complexity: O(log n) - required by problem statement
   Space Complexity: O(1) for iterative, O(log n) for recursive

6. Follow-up Questions:
   - What if array has duplicates? (Find leftmost/rightmost position)
   - What if we want to find the rightmost insertion position?
   - How would you modify for a rotated sorted array?

7. Template Recognition:
   - This is the "lower bound" binary search template
   - Very similar to bisect_left in Python
   - Useful pattern for many other problems

RECOMMENDED APPROACH FOR INTERVIEW:
- Start with Approach 1 (standard binary search) as it's most intuitive
- Explain the logic clearly: why 'left' gives us the answer
- Walk through examples, especially edge cases
- Mention Approach 2 if you have time (cleaner template)
"""
