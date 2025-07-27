"""
LeetCode 77: Combinations

Problem: Given two integers n and k, return all possible combinations of k numbers 
chosen from the range [1, n].

Key Insights:
1. Classic backtracking problem with fixed combination size
2. Use start_index to avoid duplicates and maintain lexicographic order
3. Prune early when remaining slots > remaining numbers

Time Complexity: O(C(n,k) * k) = O(n!/(k!(n-k)!) * k)
Space Complexity: O(k) for recursion depth + O(C(n,k) * k) for result storage
"""

class Solution:
    def combine(self, n, k):
        """
        Standard Backtracking Solution - Most intuitive for interviews
        """
        result = []
        
        def backtrack(start, current_combination):
            # Base case: we have k numbers in our combination
            if len(current_combination) == k:
                result.append(current_combination[:])  # Make a copy
                return
            
            # Try numbers from start to n
            for i in range(start, n + 1):
                # Choose: add current number
                current_combination.append(i)
                
                # Recurse: continue with next number
                backtrack(i + 1, current_combination)
                
                # Backtrack: remove current number
                current_combination.pop()
        
        backtrack(1, [])
        return result

    def combineOptimized(self, n, k):
        """
        Optimized with early pruning - Important optimization to mention
        """
        result = []
        
        def backtrack(start, current_combination):
            # Base case
            if len(current_combination) == k:
                result.append(current_combination[:])
                return
            
            # Calculate how many more numbers we need
            needed = k - len(current_combination)
            
            # Pruning: if remaining numbers < needed, no point continuing
            # Available numbers from i to n: (n - i + 1)
            for i in range(start, n + 1):
                # Early pruning: not enough numbers left
                if n - i + 1 < needed:
                    break
                
                current_combination.append(i)
                backtrack(i + 1, current_combination)
                current_combination.pop()
        
        backtrack(1, [])
        return result

    def combineIterative(self, n, k):
        """
        Iterative solution using stack - Good alternative approach
        """
        if k == 0:
            return [[]]
        
        result = []
        # Stack stores: (start_index, current_combination)
        stack = [(1, [])]
        
        while stack:
            start, current_combination = stack.pop()
            
            # If we have k numbers, add to result
            if len(current_combination) == k:
                result.append(current_combination)
                continue
            
            # Try all numbers from start to n
            for i in range(start, n + 1):
                new_combination = current_combination + [i]
                
                # Only continue if we can still reach k numbers
                needed = k - len(new_combination)
                available = n - i
                
                if available >= needed:
                    stack.append((i + 1, new_combination))
        
        return result

    def combineMathematical(self, n, k):
        """
        Mathematical approach using lexicographic generation
        Advanced technique - good for follow-up discussion
        """
        import math
        
        def get_combination_by_index(n, k, index):
            """Generate the index-th combination in lexicographic order"""
            combination = []
            remaining_k = k
            
            for i in range(1, n + 1):
                if remaining_k == 0:
                    break
                
                # Calculate combinations if we don't include i
                combinations_without_i = math.comb(n - i, remaining_k - 1) if remaining_k > 0 else 0
                
                if index < combinations_without_i:
                    # Include i in combination
                    combination.append(i)
                    remaining_k -= 1
                else:
                    # Skip i, adjust index
                    index -= combinations_without_i
            
            return combination
        
        total_combinations = math.comb(n, k)
        result = []
        
        for i in range(total_combinations):
            result.append(get_combination_by_index(n, k, i))
        
        return result

    def combineBuiltIn(self, n, k):
        """
        Using itertools.combinations - Elegant but may not be allowed
        """
        import itertools
        return list(map(list, itertools.combinations(range(1, n + 1), k)))

    def combineBFS(self, n, k):
        """
        BFS approach - Build combinations level by level
        """
        from collections import deque
        
        if k == 0:
            return [[]]
        
        # Start with all single numbers
        queue = deque([[i] for i in range(1, n + 1)])
        
        # Build combinations level by level
        for level in range(2, k + 1):
            next_queue = deque()
            
            while queue:
                current_combination = queue.popleft()
                last_number = current_combination[-1]
                
                # Add numbers greater than last number
                for next_number in range(last_number + 1, n + 1):
                    new_combination = current_combination + [next_number]
                    
                    if level == k:
                        next_queue.append(new_combination)
                    else:
                        # Check if we can still reach k numbers
                        needed = k - len(new_combination)
                        available = n - next_number
                        if available >= needed:
                            next_queue.append(new_combination)
            
            queue = next_queue
        
        return list(queue)

    def combineRecursiveFormula(self, n, k):
        """
        Recursive mathematical approach
        C(n,k) = C(n-1,k-1) + C(n-1,k)
        """
        def generate_combinations(n, k):
            # Base cases
            if k == 0:
                return [[]]
            if k > n or n <= 0:
                return []
            if k == n:
                return [list(range(1, n + 1))]
            
            # Include n: choose k-1 from first n-1 numbers, then add n
            with_n = []
            for combo in generate_combinations(n - 1, k - 1):
                with_n.append(combo + [n])
            
            # Exclude n: choose k from first n-1 numbers
            without_n = generate_combinations(n - 1, k)
            
            return with_n + without_n
        
        return generate_combinations(n, k)


# Test cases for interview
def test_combinations():
    solution = Solution()
    
    # Test case 1: Standard case
    n1, k1 = 4, 2
    result1 = solution.combine(n1, k1)
    print(f"Test 1 - C({n1},{k1}): {result1}")
    # Expected: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
    
    # Test case 2: Edge case - k=1
    n2, k2 = 3, 1
    result2 = solution.combine(n2, k2)
    print(f"Test 2 - C({n2},{k2}): {result2}")
    # Expected: [[1],[2],[3]]
    
    # Test case 3: Edge case - k=n
    n3, k3 = 3, 3
    result3 = solution.combine(n3, k3)
    print(f"Test 3 - C({n3},{k3}): {result3}")
    # Expected: [[1,2,3]]
    
    # Test case 4: Larger example
    n4, k4 = 5, 3
    result4 = solution.combine(n4, k4)
    print(f"Test 4 - C({n4},{k4}): Count = {len(result4)}")
    print(f"First few: {result4[:5]}")
    # Expected: 10 combinations total
    
    # Test case 5: Edge case - k=0
    n5, k5 = 3, 0
    result5 = [[]] if k5 == 0 else solution.combine(n5, k5)
    print(f"Test 5 - C({n5},{k5}): {result5}")
    # Expected: [[]]
    
    # Verify with mathematical formula
    import math
    expected_count = math.comb(n4, k4)
    print(f"Mathematical verification: C({n4},{k4}) = {expected_count}")

if __name__ == "__main__":
    test_combinations()


"""
Key Interview Points to Discuss:

1. PROBLEM UNDERSTANDING:
   - Generate all combinations of k numbers from range [1, n]
   - Order within each combination follows lexicographic order
   - This is pure combinations (not permutations)
   - Fixed size k (unlike variable-size subset problems)

2. CORE BACKTRACKING APPROACH:
   - Base case: len(current_combination) == k
   - Choice: try numbers from start to n
   - Constraint: use start_index to avoid duplicates
   - Recurse: move to next index (i+1, no reuse)

3. WHY START_INDEX WORKS:
   - Ensures lexicographic order: [1,2] before [1,3]
   - Prevents duplicates: won't generate both [1,2] and [2,1]
   - Natural for combinations (order doesn't matter)
   - More efficient than generating permutations then filtering

4. CRITICAL OPTIMIZATION - PRUNING:
   ```python
   needed = k - len(current_combination)
   available = n - i + 1
   if available < needed:
       break  # Not enough numbers left
   ```
   - Dramatically reduces unnecessary recursion
   - Essential for larger inputs

5. EDGE CASES TO MENTION:
   - k = 0: return [[]] (one way to choose nothing)
   - k > n: return [] (impossible)
   - k = 1: return [[1], [2], ..., [n]]
   - k = n: return [[1,2,...,n]] (only one way)
   - n = 1: depends on k

6. TIME/SPACE COMPLEXITY:
   - Time: O(C(n,k) * k) = O(n!/(k!(n-k)!) * k)
   - The k factor comes from copying each combination
   - Space: O(k) recursion depth + O(C(n,k) * k) result storage
   - With pruning: significantly better in practice

7. MATHEMATICAL INSIGHT:
   - Total combinations: C(n,k) = n!/(k!(n-k)!)
   - Recursive formula: C(n,k) = C(n-1,k-1) + C(n-1,k)
   - Can verify answer using math.comb(n,k)

8. FOLLOW-UP QUESTIONS TO EXPECT:
   - "Can you optimize this?" → Pruning technique
   - "Iterative solution?" → Stack or BFS approach
   - "Generate kth combination directly?" → Mathematical indexing
   - "What if k is very large?" → Generate C(n,n-k) and complement
   - "Memory constraints?" → Generator approach

9. COMPARISON WITH SIMILAR PROBLEMS:
   - Subsets: All possible sizes vs. fixed size k
   - Permutations: Order matters vs. order doesn't matter
   - Combination Sum: Target sum vs. fixed count
   - Letter Combinations: Cartesian product vs. choose k from n

10. ALTERNATIVE APPROACHES:
    - BFS: Build combinations level by level
    - Mathematical: Direct generation using combinatorial indexing
    - Recursive formula: C(n,k) = include nth + exclude nth
    - Itertools: itertools.combinations (if allowed)

11. OPTIMIZATION TECHNIQUES:
    - Early pruning when impossible to reach k
    - Start from larger numbers and work down (sometimes better)
    - Iterative to avoid recursion overhead
    - Generate in specific order if needed

12. REAL-WORLD APPLICATIONS:
    - Team selection (choose k people from n candidates)
    - Lottery number generation
    - Feature selection in machine learning
    - Chemical compound combinations
    - Tournament bracket generation

13. INTERVIEW CODING TIPS:
    - Start with basic backtracking template
    - Add pruning optimization
    - Handle edge cases (k=0, k=n, k>n)
    - Use descriptive variable names
    - Mention time complexity with mathematical formula

14. DEBUGGING TECHNIQUES:
    - Trace through small example (n=4, k=2)
    - Verify count matches C(n,k) formula
    - Check lexicographic ordering
    - Ensure no duplicates in result

15. ADVANCED DISCUSSIONS:
    - Gray code generation for combinations
    - Generating combinations in different orders
    - Memory-efficient streaming generation
    - Parallel generation for large inputs
    - Connection to binomial coefficients and Pascal's triangle
"""
