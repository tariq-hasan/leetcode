"""
LeetCode 47. Permutations II

Problem: Given a collection of numbers that might contain duplicates, 
return all the possible unique permutations in any order.

Key Insight: We need to avoid generating duplicate permutations when input has duplicates.

Time Complexity: O(n! * n) in worst case, but pruning reduces actual runtime
Space Complexity: O(n! * n) for output + O(n) recursion depth

The critical insight is proper duplicate handling through sorting + skipping.
"""

# Approach 1: Backtracking with Sorting (Most Common & Recommended)
def permuteUnique_v1(nums):
    """
    Standard approach: Sort first, then skip duplicates intelligently
    """
    result = []
    nums.sort()  # CRITICAL: Sort to group duplicates together
    used = [False] * len(nums)
    current = []
    
    def backtrack():
        if len(current) == len(nums):
            result.append(current[:])
            return
        
        for i in range(len(nums)):
            # Skip if already used
            if used[i]:
                continue
                
            # CRITICAL DUPLICATE HANDLING:
            # Skip duplicates: if current number equals previous number
            # and previous number hasn't been used yet, skip current
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            
            # Choose
            current.append(nums[i])
            used[i] = True
            
            # Explore
            backtrack()
            
            # Unchoose
            current.pop()
            used[i] = False
    
    backtrack()
    return result

# Approach 2: Backtracking with Counter (Alternative)
from collections import Counter

def permuteUnique_v2(nums):
    """
    Using Counter to track available numbers - cleaner duplicate handling
    """
    result = []
    counter = Counter(nums)
    current = []
    
    def backtrack():
        if len(current) == len(nums):
            result.append(current[:])
            return
        
        # Try each unique number
        for num in counter:
            if counter[num] > 0:
                # Choose
                current.append(num)
                counter[num] -= 1
                
                # Explore
                backtrack()
                
                # Unchoose
                current.pop()
                counter[num] += 1
    
    backtrack()
    return result

# Approach 3: Swapping with Set (Less Efficient but Intuitive)
def permuteUnique_v3(nums):
    """
    Generate all permutations, then use set to remove duplicates
    Not optimal but shows the naive approach
    """
    result = []
    
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        
        # Use set to avoid duplicate swaps at each level
        seen = set()
        for i in range(start, len(nums)):
            if nums[i] not in seen:
                seen.add(nums[i])
                
                # Swap
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                # Swap back
                nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return result

# Approach 4: Iterative with Set Deduplication
def permuteUnique_v4(nums):
    """
    Build permutations iteratively, use set for deduplication
    """
    result = [tuple()]  # Start with empty tuple for hashing
    
    for num in nums:
        new_result = set()  # Use set to automatically handle duplicates
        for perm in result:
            for i in range(len(perm) + 1):
                new_perm = perm[:i] + (num,) + perm[i:]
                new_result.add(new_perm)
        result = list(new_result)
    
    return [list(perm) for perm in result]

# Detailed explanation version for interviews
def permuteUnique_explained(nums):
    """
    Version with detailed comments explaining the duplicate handling logic
    """
    result = []
    nums.sort()  # Step 1: Sort to group identical elements
    used = [False] * len(nums)
    current = []
    
    def backtrack(depth=0):
        indent = "  " * depth
        print(f"{indent}Current permutation: {current}")
        
        if len(current) == len(nums):
            print(f"{indent}✓ Found complete permutation: {current}")
            result.append(current[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                print(f"{indent}Skip nums[{i}]={nums[i]} (already used)")
                continue
            
            # The key insight: Skip duplicate elements intelligently
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                print(f"{indent}Skip nums[{i}]={nums[i]} (duplicate, prev not used)")
                continue
            
            print(f"{indent}Choose nums[{i}]={nums[i]}")
            
            # Choose
            current.append(nums[i])
            used[i] = True
            
            # Explore
            backtrack(depth + 1)
            
            # Unchoose
            current.pop()
            used[i] = False
            print(f"{indent}Backtrack from nums[{i}]={nums[i]}")
    
    backtrack()
    return result

def test_permutations_ii():
    """Test cases covering various scenarios"""
    test_cases = [
        [1, 1, 2],        # Basic duplicates
        [1, 2, 1, 1],     # Multiple duplicates
        [1, 2, 3],        # No duplicates
        [2, 2, 1, 1],     # Two pairs of duplicates
        [1],              # Single element
        [1, 1, 1],        # All same
        []                # Empty array
    ]
    
    for nums in test_cases:
        print(f"\nInput: {nums}")
        
        # Test main approach
        result1 = permuteUnique_v1(nums[:])
        result2 = permuteUnique_v2(nums[:])
        
        print(f"Sorted + Skip approach: {len(result1)} unique permutations")
        print(f"Counter approach: {len(result2)} unique permutations")
        
        # Show results for small inputs
        if len(nums) <= 4:
            print(f"All unique permutations: {sorted(result1)}")
        
        # Verify both approaches give same results
        assert sorted(result1) == sorted(result2), "Approaches don't match!"

def why_sorting_works():
    """
    Explain why the sorting + skipping approach works
    """
    print("Why does 'if nums[i] == nums[i-1] and not used[i-1]: continue' work?")
    print()
    print("Example: [1, 1, 2] after sorting")
    print("Positions: [0, 1, 2] with values [1, 1, 2]")
    print()
    print("Without the condition, we'd generate:")
    print("- [1(pos0), 1(pos1), 2] and [1(pos1), 1(pos0), 2] <- DUPLICATES!")
    print()
    print("With the condition:")
    print("- When we try pos1 before pos0, we skip it")
    print("- This ensures we always use duplicates in sorted order")
    print("- Only [1(pos0), 1(pos1), 2] gets generated")
    print()
    print("The key insight: For any group of duplicates, always use them")
    print("in the order they appear after sorting!")

if __name__ == "__main__":
    print("=== Testing Permutations II Solutions ===")
    test_permutations_ii()
    
    print("\n=== Detailed Walkthrough for [1, 1, 2] ===")
    result = permuteUnique_explained([1, 1, 2])
    print(f"Final result: {result}")
    
    print("\n=== Why Sorting Works ===")
    why_sorting_works()

"""
Critical Interview Discussion Points:

1. **The Core Challenge**:
   - Input has duplicates, but output should have unique permutations only
   - Naive approach generates duplicates, then removes them (inefficient)
   - Smart approach: prevent duplicate generation during backtracking

2. **Why Sorting is Critical**:
   - Groups identical elements together
   - Enables the "skip duplicate" condition to work correctly
   - Without sorting, the skip condition fails

3. **The Magic Skip Condition**:
   ```python
   if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
       continue
   ```
   - Skip current duplicate if previous duplicate hasn't been used
   - Ensures we always use duplicates in sorted order
   - Prevents generating permutations that differ only in duplicate ordering

4. **Alternative Approaches**:
   - Counter approach: More intuitive but slightly more complex
   - Set-based approaches: Less efficient but easier to understand
   - Can mention but focus on sorted + skip approach

5. **Complexity Analysis**:
   - Time: Still O(n! * n) worst case, but pruning significantly helps
   - Space: O(n! * n) for unique permutations + O(n) recursion
   - Much better than generate-all-then-deduplicate approach

6. **Common Mistakes**:
   - Forgetting to sort the input array
   - Wrong duplicate skip condition
   - Using set for deduplication (works but inefficient)

7. **Follow-up Questions**:
   - What if we want only k-length permutations?
   - Can we optimize space by generating one permutation at a time?
   - How would you handle this iteratively?

8. **Why This Pattern Matters**:
   - Same technique used in Subsets II, Combination Sum II
   - General pattern for avoiding duplicates in backtracking problems
"""
