"""
LeetCode 78: Subsets

Problem: Given an integer array nums of unique elements, return all possible subsets 
(the power set). The solution set must not contain duplicate subsets.

Key Insights:
1. Generate all possible combinations of all sizes (0 to n)
2. Multiple approaches: backtracking, bit manipulation, iterative building
3. Total subsets: 2^n (each element can be included or excluded)

Time Complexity: O(N * 2^N) where N = len(nums)
Space Complexity: O(N) for recursion depth + O(N * 2^N) for result storage
"""

class Solution:
    def subsets(self, nums):
        """
        Backtracking Solution - Most intuitive and popular for interviews
        """
        result = []
        
        def backtrack(start_index, current_subset):
            # Add current subset to result (every recursive call is valid)
            result.append(current_subset[:])  # Make a copy
            
            # Try adding each remaining element
            for i in range(start_index, len(nums)):
                # Choose: add nums[i] to current subset
                current_subset.append(nums[i])
                
                # Recurse: continue with remaining elements
                backtrack(i + 1, current_subset)
                
                # Backtrack: remove nums[i] for next iteration
                current_subset.pop()
        
        backtrack(0, [])
        return result

    def subsetsBitManipulation(self, nums):
        """
        Bit Manipulation Solution - Elegant mathematical approach
        Each subset corresponds to a binary number where bit i indicates
        whether nums[i] is included
        """
        n = len(nums)
        result = []
        
        # Generate all numbers from 0 to 2^n - 1
        for i in range(2 ** n):
            subset = []
            
            # Check each bit position
            for j in range(n):
                # If jth bit is set, include nums[j]
                if i & (1 << j):
                    subset.append(nums[j])
            
            result.append(subset)
        
        return result

    def subsetsIterative(self, nums):
        """
        Iterative Solution - Build subsets incrementally
        Start with empty set, add each new element to existing subsets
        """
        result = [[]]  # Start with empty subset
        
        for num in nums:
            # For each existing subset, create new subset by adding current number
            new_subsets = []
            for existing_subset in result:
                new_subsets.append(existing_subset + [num])
            
            # Add all new subsets to result
            result.extend(new_subsets)
        
        return result

    def subsetsIterativeOptimized(self, nums):
        """
        Optimized iterative - modify result in place
        """
        result = [[]]
        
        for num in nums:
            # Get current size to avoid infinite loop
            current_size = len(result)
            
            # Add current number to each existing subset
            for i in range(current_size):
                result.append(result[i] + [num])
        
        return result

    def subsetsRecursiveChoice(self, nums):
        """
        Recursive Choice Solution - For each element, decide include or exclude
        Classic divide and conquer approach
        """
        def generate_subsets(index):
            # Base case: processed all elements
            if index == len(nums):
                return [[]]
            
            # Get all subsets without current element
            subsets_without = generate_subsets(index + 1)
            
            # Create subsets with current element
            subsets_with = []
            for subset in subsets_without:
                subsets_with.append([nums[index]] + subset)
            
            # Return both possibilities
            return subsets_without + subsets_with
        
        return generate_subsets(0)

    def subsetsDFS(self, nums):
        """
        DFS with explicit stack - Non-recursive backtracking
        """
        result = []
        # Stack stores: (start_index, current_subset)
        stack = [(0, [])]
        
        while stack:
            start_index, current_subset = stack.pop()
            
            # Add current subset to result
            result.append(current_subset)
            
            # Add choices for remaining elements
            for i in range(start_index, len(nums)):
                new_subset = current_subset + [nums[i]]
                stack.append((i + 1, new_subset))
        
        return result

    def subsetsBFS(self, nums):
        """
        BFS Solution - Build subsets level by level
        """
        from collections import deque
        
        # Queue stores subsets, start with empty subset
        queue = deque([[]])
        result = []
        
        for num in nums:
            # Process all subsets at current level
            level_size = len(queue)
            
            for _ in range(level_size):
                current_subset = queue.popleft()
                result.append(current_subset)
                
                # Add subset with current number
                queue.append(current_subset + [num])
        
        # Add remaining subsets (those with all elements)
        while queue:
            result.append(queue.popleft())
        
        return result

    def subsetsBuiltIn(self, nums):
        """
        Using itertools.combinations - Elegant but may not be allowed
        """
        import itertools
        
        result = []
        n = len(nums)
        
        # Generate combinations of all possible sizes
        for size in range(n + 1):
            for combo in itertools.combinations(nums, size):
                result.append(list(combo))
        
        return result

    def subsetsGenerator(self, nums):
        """
        Generator approach - Memory efficient for large inputs
        Good for follow-up discussion
        """
        def generate_subsets():
            n = len(nums)
            
            # Use bit manipulation to generate all subsets
            for i in range(2 ** n):
                subset = []
                for j in range(n):
                    if i & (1 << j):
                        subset.append(nums[j])
                yield subset
        
        return list(generate_subsets())


# Test cases for interview
def test_subsets():
    solution = Solution()
    
    # Test case 1: Standard case
    nums1 = [1, 2, 3]
    result1 = solution.subsets(nums1)
    print(f"Test 1 - nums: {nums1}")
    print(f"Result: {result1}")
    print(f"Count: {len(result1)} (expected: {2**len(nums1)})")
    # Expected: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
    
    # Test case 2: Single element
    nums2 = [0]
    result2 = solution.subsets(nums2)
    print(f"\nTest 2 - nums: {nums2}")
    print(f"Result: {result2}")
    # Expected: [[],[0]]
    
    # Test case 3: Empty array
    nums3 = []
    result3 = solution.subsets(nums3)
    print(f"\nTest 3 - nums: {nums3}")
    print(f"Result: {result3}")
    # Expected: [[]]
    
    # Test case 4: Two elements
    nums4 = [1, 2]
    result4 = solution.subsets(nums4)
    print(f"\nTest 4 - nums: {nums4}")
    print(f"Result: {result4}")
    # Expected: [[],[1],[2],[1,2]]
    
    # Compare different approaches
    print(f"\nComparison for {nums1}:")
    print(f"Backtracking: {len(solution.subsets(nums1))} subsets")
    print(f"Bit manipulation: {len(solution.subsetsBitManipulation(nums1))} subsets")
    print(f"Iterative: {len(solution.subsetsIterative(nums1))} subsets")

if __name__ == "__main__":
    test_subsets()


"""
Key Interview Points to Discuss:

1. PROBLEM UNDERSTANDING:
   - Generate all possible subsets (power set) of given array
   - Include empty set and the set itself
   - No duplicate subsets (input has unique elements)
   - Total subsets: 2^n (each element included or excluded)

2. BACKTRACKING APPROACH:
   - Key insight: Every recursive call represents a valid subset
   - Add current subset to result before exploring further
   - Use start_index to maintain order and avoid duplicates
   - Most intuitive and commonly expected in interviews

3. BIT MANIPULATION INSIGHT:
   - Each subset maps to a binary number 0 to 2^n-1
   - Bit i set means nums[i] is included in subset
   - Very elegant and shows mathematical thinking
   - Example: nums=[1,2,3], binary 101 → subset [1,3]

4. ITERATIVE BUILDING APPROACH:
   - Start with [[]] (empty subset)
   - For each new element, double the subsets by adding element to each existing subset
   - Natural way humans might solve the problem
   - Easy to understand and implement

5. RECURSIVE CHOICE PATTERN:
   - For each element: include it or don't include it
   - Classic divide and conquer thinking
   - Subsets(nums) = Subsets(nums[1:]) + [nums[0] + s for s in Subsets(nums[1:])]

6. TIME/SPACE COMPLEXITY:
   - Time: O(N * 2^N) - generate 2^N subsets, each takes O(N) to copy
   - Space: O(N * 2^N) for storing all subsets + O(N) recursion depth
   - Cannot be improved significantly as we must generate 2^N subsets

7. EDGE CASES TO MENTION:
   - Empty array: return [[]]
   - Single element: return [[], [element]]
   - Large arrays: exponential explosion (2^10 = 1024, 2^20 ≈ 1M)

8. FOLLOW-UP QUESTIONS TO EXPECT:
   - "Can you optimize?" → Complexity is optimal for generating all subsets
   - "Iterative solution?" → Show iterative building approach
   - "Bit manipulation?" → Demonstrate mathematical approach
   - "Memory constraints?" → Generator approach or streaming
   - "What if array has duplicates?" → Subsets II (different problem)

9. COMPARISON WITH SIMILAR PROBLEMS:
   - Combinations: Fixed size k vs. all sizes
   - Permutations: Order matters vs. order doesn't matter
   - Subsets II: Has duplicates vs. unique elements
   - Power set: Same problem, different name

10. REAL-WORLD APPLICATIONS:
    - Feature selection in machine learning
    - Analyzing all possible configurations
    - Boolean satisfiability problems
    - Set operations in databases
    - Combinatorial optimization

11. OPTIMIZATION TECHNIQUES:
    - Bit manipulation for compact representation
    - Iterative to avoid recursion overhead  
    - Generator for memory efficiency
    - Early termination if only specific subsets needed

12. MATHEMATICAL CONNECTIONS:
    - Power set cardinality: |P(S)| = 2^|S|
    - Binary representation correspondence
    - Binomial theorem: (1+x)^n expansion coefficients
    - Gray code generation for efficient enumeration

13. INTERVIEW STRATEGY:
    - Start with backtracking (most expected)
    - Mention bit manipulation as elegant alternative
    - Show iterative approach for completeness
    - Discuss complexity and why it can't be improved
    - Handle edge cases properly

14. DEBUGGING TECHNIQUES:
    - Verify count equals 2^n
    - Check empty set is included
    - Ensure no duplicate subsets
    - Trace through small example step by step

15. ADVANCED DISCUSSIONS:
    - Lexicographic ordering of subsets
    - Gray code generation for minimal changes
    - Parallel generation for large inputs
    - Compressed representations
    - Subset enumeration in specific orders

16. COMMON MISTAKES TO AVOID:
    - Forgetting to include empty subset
    - Not making copies of current subset
    - Wrong range in bit manipulation (0 to 2^n, not 2^n-1)
    - Infinite loops in iterative approach

17. PATTERN RECOGNITION:
    This problem teaches the fundamental "generate all combinations" pattern:
    ```python
    def backtrack(start, current):
        result.append(current[:])  # Process current state
        for i in range(start, len(choices)):
            current.append(choices[i])   # Choose
            backtrack(i + 1, current)   # Recurse
            current.pop()               # Backtrack
    ```
"""
