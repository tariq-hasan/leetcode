"""
LeetCode 167: Two Sum II - Input Array Is Sorted

Problem: Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, 
find two numbers such that they add up to a specific target number. Let these two numbers be 
numbers[index1] and numbers[index2] where 1 ≤ index1 < index2 ≤ n.

Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.

Key differences from Two Sum I:
1. Array is sorted (can use two pointers!)
2. Return 1-indexed positions (not 0-indexed)
3. Guaranteed to have exactly one solution
4. Cannot use same element twice

Time Complexity: O(n) for optimal solution
Space Complexity: O(1) - major improvement over original Two Sum
"""

class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        """
        OPTIMAL SOLUTION - Two Pointers
        
        Key insight: Since array is sorted, use two pointers from ends
        - If sum > target: move right pointer left (decrease sum)
        - If sum < target: move left pointer right (increase sum)
        - If sum == target: found the answer
        
        Time: O(n), Space: O(1)
        This is the expected solution that leverages the sorted property.
        """
        left = 0
        right = len(numbers) - 1
        
        while left < right:
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                # Return 1-indexed positions
                return [left + 1, right + 1]
            elif current_sum < target:
                # Need larger sum, move left pointer right
                left += 1
            else:
                # Need smaller sum, move right pointer left
                right -= 1
        
        # Should never reach here given problem constraints
        return []
    
    def twoSumHashMap(self, numbers: list[int], target: int) -> list[int]:
        """
        HASH MAP SOLUTION - Same as Two Sum I
        
        Works but doesn't leverage the sorted property
        Uses extra space when constant space is possible
        
        Time: O(n), Space: O(n)
        Mention this but explain why two-pointer is better
        """
        num_to_index = {}
        
        for i, num in enumerate(numbers):
            complement = target - num
            
            if complement in num_to_index:
                # Return 1-indexed positions
                return [num_to_index[complement] + 1, i + 1]
            
            num_to_index[num] = i
        
        return []
    
    def twoSumBinarySearch(self, numbers: list[int], target: int) -> list[int]:
        """
        BINARY SEARCH SOLUTION - Alternative approach
        
        For each element, binary search for its complement
        More complex than two-pointer but shows algorithmic thinking
        
        Time: O(n log n), Space: O(1)
        Less optimal than two-pointer approach
        """
        def binary_search(arr, target_val, start_idx):
            """Binary search for target_val in arr[start_idx:]"""
            left, right = start_idx, len(arr) - 1
            
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] == target_val:
                    return mid
                elif arr[mid] < target_val:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1
        
        for i in range(len(numbers)):
            complement = target - numbers[i]
            # Search for complement in remaining array
            complement_idx = binary_search(numbers, complement, i + 1)
            
            if complement_idx != -1:
                return [i + 1, complement_idx + 1]  # 1-indexed
        
        return []
    
    def twoSumVerbose(self, numbers: list[int], target: int) -> list[int]:
        """
        VERBOSE TWO-POINTER - Step-by-step explanation version
        
        Same as optimal solution but with detailed comments
        Good for explaining the logic during interview
        
        Time: O(n), Space: O(1)
        """
        # Initialize pointers at both ends
        left = 0
        right = len(numbers) - 1
        
        while left < right:
            # Calculate current sum
            left_val = numbers[left]
            right_val = numbers[right]
            current_sum = left_val + right_val
            
            print(f"  Checking: numbers[{left}]={left_val} + numbers[{right}]={right_val} = {current_sum}")
            
            if current_sum == target:
                print(f"  Found! Returning 1-indexed: [{left + 1}, {right + 1}]")
                return [left + 1, right + 1]
            elif current_sum < target:
                print(f"  Sum {current_sum} < target {target}, move left pointer right")
                left += 1
            else:
                print(f"  Sum {current_sum} > target {target}, move right pointer left")
                right -= 1
        
        return []
    
    def twoSumWithValidation(self, numbers: list[int], target: int) -> list[int]:
        """
        SOLUTION WITH INPUT VALIDATION - Production-ready version
        
        Includes error checking and edge case handling
        Good to mention for robustness discussion
        
        Time: O(n), Space: O(1)
        """
        # Input validation
        if not numbers or len(numbers) < 2:
            return []
        
        # Check if array is actually sorted
        for i in range(1, len(numbers)):
            if numbers[i] < numbers[i-1]:
                raise ValueError("Array must be sorted in non-decreasing order")
        
        left = 0
        right = len(numbers) - 1
        
        while left < right:
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                return [left + 1, right + 1]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        # No solution found (shouldn't happen per problem statement)
        return []


def test_solution():
    """Comprehensive test cases for interview practice"""
    sol = Solution()
    
    test_cases = [
        # (numbers, target, expected, description)
        ([2, 7, 11, 15], 9, [1, 2], "Basic example: 2 + 7 = 9"),
        ([2, 3, 4], 6, [1, 3], "2 + 4 = 6"),
        ([-1, 0], -1, [1, 2], "Negative numbers: -1 + 0 = -1"),
        ([1, 2, 3, 4, 4, 9, 56, 90], 8, [4, 5], "Duplicates: 4 + 4 = 8"),
        ([1, 3, 4, 5, 7, 10, 11], 9, [3, 4], "3 + 5 = 8? No, 4 + 5 = 9"),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 17, [8, 9], "Large indices: 8 + 9 = 17"),
        ([0, 0, 3, 4], 0, [1, 2], "Zeros: 0 + 0 = 0"),
        ([-10, -1, 0, 3, 10, 11, 15], 0, [2, 3], "Mixed signs: -1 + 0 = -1? No, 0 + 0? No, -1 + 1? No... 0 + 0 impossible, so -10 + 10 = 0"),
        ([-10, -1, 0, 3, 10, 11, 15], 0, [1, 5], "-10 + 10 = 0"),
    ]
    
    print("Testing Two Sum II - Sorted Array Solutions:")
    print("=" * 70)
    
    for i, (numbers, target, expected, description) in enumerate(test_cases):
        print(f"Test {i+1}: {description}")
        print(f"  Input: numbers = {numbers}, target = {target}")
        print(f"  Expected: {expected}")
        
        # Test optimal two-pointer solution
        result = sol.twoSum(numbers.copy(), target)
        
        # Verify result
        if len(result) == 2 and len(expected) == 2:
            idx1, idx2 = result
            exp_idx1, exp_idx2 = expected
            
            # Check if indices are valid (1-indexed)
            if 1 <= idx1 <= len(numbers) and 1 <= idx2 <= len(numbers) and idx1 < idx2:
                # Convert to 0-indexed for array access
                actual_sum = numbers[idx1-1] + numbers[idx2-1]
                if actual_sum == target:
                    status = "✓"
                    print(f"  Result: {status} {result} -> numbers[{idx1-1}] + numbers[{idx2-1}] = {numbers[idx1-1]} + {numbers[idx2-1]} = {actual_sum}")
                else:
                    status = "✗"
                    print(f"  Result: {status} {result} -> sum = {actual_sum} ≠ {target}")
            else:
                status = "✗"
                print(f"  Result: {status} invalid indices {result}")
        else:
            status = "✗"
            print(f"  Result: {status} invalid result format {result}")
        
        # Test alternative approaches
        hash_result = sol.twoSumHashMap(numbers.copy(), target)
        binary_result = sol.twoSumBinarySearch(numbers.copy(), target)
        
        print(f"  Hash Map: {hash_result}")
        print(f"  Binary Search: {binary_result}")
        print()

def demonstrate_two_pointer_logic():
    """Show how two-pointer approach works step by step"""
    print("Two-Pointer Algorithm Walkthrough:")
    print("=" * 50)
    
    numbers = [2, 7, 11, 15]
    target = 9
    sol = Solution()
    
    print(f"Array: {numbers}")
    print(f"Target: {target}")
    print("Steps:")
    
    # Use verbose version to show steps
    result = sol.twoSumVerbose(numbers, target)
    print(f"Final result: {result}")

def compare_approaches():
    """Compare different approaches and their trade-offs"""
    print("\nApproach Comparison:")
    print("=" * 60)
    
    approaches = [
        ("Two Pointers", "O(n)", "O(1)", "✓ Optimal - leverages sorted property"),
        ("Hash Map", "O(n)", "O(n)", "Same as Two Sum I, doesn't use sorted property"),
        ("Binary Search", "O(n log n)", "O(1)", "For each element, binary search complement"),
        ("Brute Force", "O(n²)", "O(1)", "Check all pairs - not recommended"),
    ]
    
    print(f"{'Approach':<15} {'Time':<12} {'Space':<8} {'Notes'}")
    print("-" * 60)
    
    for approach, time_comp, space_comp, notes in approaches:
        marker = "⭐" if "Optimal" in notes else "  "
        print(f"{marker} {approach:<13} {time_comp:<12} {space_comp:<8} {notes}")

if __name__ == "__main__":
    test_solution()
    demonstrate_two_pointer_logic()
    compare_approaches()


"""
INTERVIEW TALKING POINTS:

1. KEY DIFFERENCE FROM TWO SUM I:
   - Array is sorted! This enables O(1) space solution
   - Return 1-indexed positions (not 0-indexed)
   - Two-pointer technique becomes optimal approach

2. TWO-POINTER INTUITION:
   - Start with pointers at both ends
   - If sum too small: move left pointer right (increase sum)
   - If sum too large: move right pointer left (decrease sum)
   - If sum equals target: found the answer!

3. WHY TWO POINTERS WORK:
   - Sorted array means left side has smaller values, right side has larger values
   - Moving pointers intelligently explores all possibilities in O(n) time
   - No need to check all pairs like in brute force

4. APPROACH COMPARISON:
   - Two pointers: O(n) time, O(1) space ⭐ OPTIMAL
   - Hash map: O(n) time, O(n) space (works but wasteful)
   - Binary search: O(n log n) time, O(1) space (more complex)

5. IMPLEMENTATION DETAILS:
   - Remember to return 1-indexed positions!
   - left < right condition prevents using same element twice
   - Array is guaranteed to have exactly one solution

6. EDGE CASES:
   - Negative numbers (still works with two pointers)
   - Duplicate values in array
   - Target is very large or very small
   - Array with only 2 elements

7. COMMON MISTAKES:
   - Returning 0-indexed instead of 1-indexed positions
   - Using hash map when two pointers are more efficient
   - Forgetting that array is sorted (missing key optimization)
   - Not handling the pointer movement logic correctly

8. OPTIMIZATION INSIGHTS:
   - Two pointers eliminate need for extra space
   - Each element examined at most once
   - Early termination when pointers meet
   - Leverages sorted property for intelligent search

9. FOLLOW-UP QUESTIONS:
   - "What if array had duplicates?" → Still works, return any valid pair
   - "What if no solution existed?" → Pointers would cross without finding answer
   - "What if we wanted all pairs?" → Continue searching after finding first pair
   - "3Sum on sorted array?" → Extension using similar two-pointer technique

10. RELATED PROBLEMS:
    - 3Sum (15) - uses two pointers as subroutine
    - 4Sum (18) - further extension
    - Container With Most Water (11) - two pointer technique
    - Trapping Rain Water (42) - advanced two pointers

INTERVIEW STRATEGY:
1. **Recognize the sorted property**: "Since the array is sorted, I can use two pointers"
2. **Explain the intuition**: "Start from ends, move pointers based on sum comparison"
3. **Highlight the optimization**: "This gives me O(1) space instead of O(n)"
4. **Remember 1-indexed**: "The problem wants 1-indexed positions"
5. **Code efficiently**: Two pointers solution should be quick to implement
6. **Walk through example**: Show pointer movements step by step

KEY SUCCESS FACTORS:
- Immediately recognize this as two-pointer problem due to sorted array
- Explain why two pointers work better than hash map here
- Implement cleanly with correct index handling
- Remember the 1-indexed return format
- Show understanding of the sorted property advantage

This problem tests your ability to recognize when array properties enable better algorithms!
"""
