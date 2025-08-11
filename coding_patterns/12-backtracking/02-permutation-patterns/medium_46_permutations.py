"""
LeetCode 46. Permutations

Problem: Given an array nums of distinct integers, return all the possible permutations.

Time Complexity: O(n! * n) - n! permutations, each takes O(n) to build
Space Complexity: O(n! * n) - storing all permutations + O(n) recursion depth

Multiple approaches shown below for interview flexibility
"""

# Approach 1: Backtracking with Used Array (Most Common)
def permute_v1(nums):
    """
    Standard backtracking approach using a used array
    """
    result = []
    used = [False] * len(nums)
    current = []
    
    def backtrack():
        # Base case: we've built a complete permutation
        if len(current) == len(nums):
            result.append(current[:])  # Important: make a copy!
            return
        
        # Try each unused number
        for i in range(len(nums)):
            if not used[i]:
                # Choose
                current.append(nums[i])
                used[i] = True
                
                # Explore
                backtrack()
                
                # Unchoose (backtrack)
                current.pop()
                used[i] = False
    
    backtrack()
    return result

# Approach 2: Backtracking with Index Swapping (More Efficient)
def permute_v2(nums):
    """
    Backtracking by swapping elements - avoids extra space for tracking used elements
    """
    result = []
    
    def backtrack(start):
        # Base case: we've fixed all positions
        if start == len(nums):
            result.append(nums[:])  # Make a copy
            return
        
        # Try each element as the next element in permutation
        for i in range(start, len(nums)):
            # Choose: swap current element to the start position
            nums[start], nums[i] = nums[i], nums[start]
            
            # Explore: recurse with next position
            backtrack(start + 1)
            
            # Unchoose: swap back to restore original state
            nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return result

# Approach 3: Iterative Building (Bottom-up)
def permute_v3(nums):
    """
    Build permutations iteratively by inserting each new number
    at all possible positions in existing permutations
    """
    result = [[]]  # Start with empty permutation
    
    for num in nums:
        new_result = []
        for perm in result:
            # Insert num at each possible position in current permutation
            for i in range(len(perm) + 1):
                new_result.append(perm[:i] + [num] + perm[i:])
        result = new_result
    
    return result

# Approach 4: Using Python's itertools (For Reference Only)
from itertools import permutations

def permute_v4(nums):
    """
    Using built-in library - mention but don't use in interview
    """
    return list(map(list, permutations(nums)))

# Approach 5: Lexicographic Generation (Advanced)
def permute_v5(nums):
    """
    Generate permutations in lexicographic order using next_permutation logic
    """
    def next_permutation(arr):
        # Find pivot
        i = len(arr) - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1
        
        if i == -1:
            return False  # No next permutation
        
        # Find successor
        j = len(arr) - 1
        while arr[j] <= arr[i]:
            j -= 1
        
        # Swap and reverse
        arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1:] = reversed(arr[i + 1:])
        return True
    
    result = []
    nums.sort()  # Start with smallest permutation
    
    while True:
        result.append(nums[:])
        if not next_permutation(nums):
            break
    
    return result

# Test function
def test_permutations():
    test_cases = [
        [1, 2, 3],
        [0, 1],
        [1],
        [1, 2, 3, 4]
    ]
    
    for nums in test_cases:
        print(f"Input: {nums}")
        
        # Test different approaches
        result1 = permute_v1(nums[:])
        result2 = permute_v2(nums[:])
        result3 = permute_v3(nums[:])
        
        print(f"Backtracking (used array): {len(result1)} permutations")
        print(f"Backtracking (swapping): {len(result2)} permutations")
        print(f"Iterative building: {len(result3)} permutations")
        
        # Show first few permutations for small inputs
        if len(nums) <= 3:
            print(f"All permutations: {sorted(result1)}")
        
        print("-" * 50)

# Detailed walkthrough for interview explanation
def permute_with_explanation(nums):
    """
    Version with detailed logging for interview explanation
    """
    result = []
    current = []
    used = [False] * len(nums)
    
    def backtrack(depth=0):
        # Visualization for interview
        indent = "  " * depth
        print(f"{indent}Entering backtrack, current = {current}")
        
        if len(current) == len(nums):
            print(f"{indent}Found complete permutation: {current}")
            result.append(current[:])
            return
        
        for i in range(len(nums)):
            if not used[i]:
                print(f"{indent}Trying nums[{i}] = {nums[i]}")
                
                # Choose
                current.append(nums[i])
                used[i] = True
                
                # Explore
                backtrack(depth + 1)
                
                # Unchoose
                current.pop()
                used[i] = False
                print(f"{indent}Backtracked, current = {current}")
    
    backtrack()
    return result

if __name__ == "__main__":
    print("=== Testing Permutations Solutions ===")
    test_permutations()
    
    print("\n=== Detailed Walkthrough for [1, 2] ===")
    result = permute_with_explanation([1, 2])
    print(f"Final result: {result}")

"""
Interview Discussion Points:

1. **Algorithm Choice**:
   - Backtracking is the most intuitive and commonly expected
   - Mention other approaches to show algorithmic breadth
   - Swapping approach is more space-efficient

2. **Complexity Analysis**:
   - Time: O(n! * n) - n! permutations, O(n) to build each
   - Space: O(n! * n) for output + O(n) recursion depth
   - Can't do better than O(n!) since that's the size of output

3. **Key Implementation Details**:
   - Always make copies when adding to result (current[:])
   - Proper backtracking: undo all changes
   - Base case: when permutation is complete

4. **Edge Cases**:
   - Empty array: return [[]]
   - Single element: return [[element]]
   - All elements distinct (given in problem)

5. **Follow-up Questions**:
   - What if array has duplicates? (leads to Permutations II)
   - Can you generate kth permutation? (leads to different approach)
   - Memory optimization? (generate one at a time)

6. **Common Mistakes**:
   - Forgetting to make copies (result.append(current) vs result.append(current[:]))
   - Not properly backtracking
   - Off-by-one errors in swapping approach
"""
