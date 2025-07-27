"""
LeetCode 1: Two Sum

Problem: Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

This is the most fundamental problem in coding interviews and often the first one asked.
The key insight is to use a hash map to achieve O(n) time complexity.

Time Complexity: O(n) for optimal solution
Space Complexity: O(n) for hash map
"""

class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """
        OPTIMAL SOLUTION - Hash Map (One Pass)
        
        Key insight: For each number, check if (target - number) exists in hash map
        If it exists, we found our pair. If not, add current number to hash map.
        
        Time: O(n), Space: O(n)
        This is what 99% of interviewers expect to see.
        """
        # Hash map to store {value: index}
        num_to_index = {}
        
        for i, num in enumerate(nums):
            complement = target - num
            
            # If complement exists in map, we found the pair
            if complement in num_to_index:
                return [num_to_index[complement], i]
            
            # Add current number to map
            num_to_index[num] = i
        
        # Should never reach here given problem constraints
        return []
    
    def twoSumTwoPass(self, nums: list[int], target: int) -> list[int]:
        """
        TWO-PASS HASH MAP - Less optimal but shows understanding
        
        First pass: build the hash map
        Second pass: look for complements
        
        Time: O(n), Space: O(n)
        Same complexity but requires two passes
        """
        # First pass: build hash map
        num_to_index = {}
        for i, num in enumerate(nums):
            num_to_index[num] = i
        
        # Second pass: look for complements
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index and num_to_index[complement] != i:
                return [i, num_to_index[complement]]
        
        return []
    
    def twoSumBruteForce(self, nums: list[int], target: int) -> list[int]:
        """
        BRUTE FORCE SOLUTION - Mention but don't use in interviews
        
        Check every pair of numbers to see if they sum to target
        
        Time: O(n²), Space: O(1)
        Good to mention as the naive approach, then optimize to hash map
        """
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
    
    def twoSumSorted(self, nums: list[int], target: int) -> list[int]:
        """
        TWO-POINTER SOLUTION - Only works if we can modify input
        
        If we're allowed to sort the array, we can use two pointers
        But we need to track original indices, which complicates things
        
        Time: O(n log n), Space: O(n)
        Generally not preferred for this problem due to sorting overhead
        """
        # Create list of (value, original_index) pairs
        indexed_nums = [(num, i) for i, num in enumerate(nums)]
        
        # Sort by value
        indexed_nums.sort()
        
        left, right = 0, len(indexed_nums) - 1
        
        while left < right:
            current_sum = indexed_nums[left][0] + indexed_nums[right][0]
            
            if current_sum == target:
                return [indexed_nums[left][1], indexed_nums[right][1]]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return []
    
    def twoSumWithDuplicates(self, nums: list[int], target: int) -> list[int]:
        """
        HANDLING DUPLICATES - More robust version
        
        Handle edge case where target = 2 * num (same number twice)
        Uses list to store all indices for duplicate values
        
        Time: O(n), Space: O(n)
        """
        from collections import defaultdict
        
        # Map value to list of indices
        num_to_indices = defaultdict(list)
        
        for i, num in enumerate(nums):
            num_to_indices[num].append(i)
        
        for num in num_to_indices:
            complement = target - num
            
            if complement in num_to_indices:
                if complement == num:
                    # Need at least 2 occurrences of the same number
                    if len(num_to_indices[num]) >= 2:
                        return num_to_indices[num][:2]
                else:
                    # Different numbers
                    return [num_to_indices[num][0], num_to_indices[complement][0]]
        
        return []


def test_solution():
    """Comprehensive test cases for interview practice"""
    sol = Solution()
    
    test_cases = [
        # (nums, target, expected_description)
        ([2, 7, 11, 15], 9, "Basic example: 2 + 7 = 9"),
        ([3, 2, 4], 6, "3 + 3 would be same element twice, so 2 + 4 = 6"),
        ([3, 3], 6, "Same number twice: 3 + 3 = 6"),
        ([1, 2, 3, 4, 5], 9, "4 + 5 = 9"),
        ([1, 5, 2, 8, 3], 10, "2 + 8 = 10"),
        ([-1, -2, -3, -4, -5], -8, "Negative numbers: -3 + -5 = -8"),
        ([0, 4, 3, 0], 0, "Zero sum: 0 + 0 = 0"),
        ([-3, 4, 3, 90], 0, "Negative + positive = 0"),
        ([1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1], 11, "Many duplicates"),
    ]
    
    print("Testing Two Sum Solutions:")
    print("=" * 60)
    
    for i, (nums, target, description) in enumerate(test_cases):
        print(f"Test {i+1}: {description}")
        print(f"  Input: nums = {nums}, target = {target}")
        
        # Test optimal solution
        result = sol.twoSum(nums.copy(), target)
        
        # Verify result
        if len(result) == 2:
            idx1, idx2 = result
            if 0 <= idx1 < len(nums) and 0 <= idx2 < len(nums) and idx1 != idx2:
                sum_check = nums[idx1] + nums[idx2]
                if sum_check == target:
                    status = "✓"
                    print(f"  Result: {status} indices [{idx1}, {idx2}] -> {nums[idx1]} + {nums[idx2]} = {sum_check}")
                else:
                    status = "✗"
                    print(f"  Result: {status} indices [{idx1}, {idx2}] -> {nums[idx1]} + {nums[idx2]} = {sum_check} ≠ {target}")
            else:
                status = "✗"
                print(f"  Result: {status} invalid indices {result}")
        else:
            status = "✗"
            print(f"  Result: {status} invalid result {result}")
        
        # Test other approaches for comparison
        brute_result = sol.twoSumBruteForce(nums.copy(), target)
        two_pass_result = sol.twoSumTwoPass(nums.copy(), target)
        
        # Results might have different orders but should be valid
        print(f"  Brute force: {brute_result}")
        print(f"  Two-pass: {two_pass_result}")
        print()

def demonstrate_approaches():
    """Show different approaches and their trade-offs"""
    print("Approach Comparison:")
    print("=" * 50)
    
    approaches = [
        ("Brute Force", "O(n²)", "O(1)", "Check all pairs"),
        ("Hash Map (One Pass)", "O(n)", "O(n)", "✓ Optimal - use this!"),
        ("Hash Map (Two Pass)", "O(n)", "O(n)", "Same complexity, more passes"),
        ("Two Pointer (Sorted)", "O(n log n)", "O(n)", "Need to sort first"),
    ]
    
    print(f"{'Approach':<20} {'Time':<12} {'Space':<8} {'Notes'}")
    print("-" * 60)
    
    for approach, time_comp, space_comp, notes in approaches:
        marker = "⭐" if "Optimal" in notes else "  "
        print(f"{marker} {approach:<18} {time_comp:<12} {space_comp:<8} {notes}")

if __name__ == "__main__":
    test_solution()
    print()
    demonstrate_approaches()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Return INDICES, not the values themselves
   - Exactly one solution guaranteed
   - Cannot use same element twice (different indices OK for same value)
   - Can return indices in any order

2. APPROACH EVOLUTION:
   - Start with brute force (O(n²)) to show understanding
   - Optimize to hash map (O(n)) - this is the expected solution
   - Explain why hash map works: complement lookup is O(1)

3. KEY INSIGHT - HASH MAP:
   - For each number, check if (target - number) exists
   - If yes, return indices. If no, add current number to map
   - One pass is sufficient - no need to build entire map first

4. COMPLEXITY ANALYSIS:
   - Time: O(n) - single pass through array
   - Space: O(n) - hash map can store up to n elements
   - Trade space for time - classic algorithm optimization

5. EDGE CASES TO DISCUSS:
   - Duplicate numbers in array
   - Target is twice a number (need same value twice)
   - Negative numbers
   - Zero values
   - Very large/small numbers

6. IMPLEMENTATION DETAILS:
   - Use dictionary/hash map for O(1) lookup
   - Check complement before adding to avoid same index
   - Return as soon as pair found
   - Handle case where same value appears twice

7. COMMON MISTAKES:
   - Returning values instead of indices
   - Using same element twice (same index)
   - Not handling duplicates correctly
   - Forgetting to check complement before adding to map

8. FOLLOW-UP QUESTIONS:
   - "What if no solution exists?" → Return empty array or raise exception
   - "What if multiple solutions exist?" → Return any valid pair
   - "What if array is sorted?" → Two-pointer approach possible
   - "What about 3Sum or 4Sum?" → Extensions of this problem

9. OPTIMIZATION NOTES:
   - One-pass is more efficient than two-pass
   - Hash map lookup is average O(1), worst case O(n)
   - Space-time tradeoff: O(n) space for O(n) time

10. RELATED PROBLEMS:
    - Two Sum II (sorted array) - use two pointers
    - 3Sum (15) - extends this concept
    - 4Sum (18) - further extension
    - Two Sum BST (653) - tree version

INTERVIEW STRATEGY:
1. **Clarify requirements**: "I need to return indices of two numbers that sum to target"
2. **Start with brute force**: "Naive approach would be O(n²)..."
3. **Optimize to hash map**: "I can use a hash map to get O(n) time"
4. **Explain the insight**: "For each number, I check if its complement exists"
5. **Code the one-pass solution**: This is what they want to see
6. **Walk through example**: Show how it works step by step
7. **Discuss edge cases**: Mention duplicates, negatives, etc.

CRITICAL SUCCESS FACTORS:
- Code the optimal O(n) solution quickly and correctly
- Explain the hash map insight clearly
- Handle the complement check properly
- Test with a simple example
- Discuss time/space complexity

This problem sets the tone for the entire interview - nail it confidently!
"""
