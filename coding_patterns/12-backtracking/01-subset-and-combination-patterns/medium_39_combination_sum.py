"""
LeetCode 39: Combination Sum

Problem: Given an array of distinct integers 'candidates' and a target integer 'target', 
return a list of all unique combinations of 'candidates' where the chosen numbers sum to 'target'. 
The same number may be chosen from 'candidates' an unlimited number of times.

Key Insights:
1. This is a classic backtracking problem with repetition allowed
2. To avoid duplicates, we use index-based approach (don't go backwards)
3. Early termination when current sum exceeds target (pruning)

Time Complexity: O(N^(T/M)) where N = len(candidates), T = target, M = minimal candidate
Space Complexity: O(T/M) for recursion depth + space for storing results
"""

class Solution:
    def combinationSum(self, candidates, target):
        """
        Backtracking Solution - Most intuitive and popular for interviews
        """
        result = []
        
        def backtrack(start_index, current_combination, remaining_target):
            # Base cases
            if remaining_target == 0:
                result.append(current_combination[:])  # Found valid combination
                return
            
            if remaining_target < 0:
                return  # Exceeded target, backtrack
            
            # Try each candidate starting from start_index
            for i in range(start_index, len(candidates)):
                candidate = candidates[i]
                
                # Choose: add candidate to current combination
                current_combination.append(candidate)
                
                # Recurse: same index (can reuse same number)
                backtrack(i, current_combination, remaining_target - candidate)
                
                # Unchoose: remove candidate for backtracking
                current_combination.pop()
        
        backtrack(0, [], target)
        return result

    def combinationSumOptimized(self, candidates, target):
        """
        Optimized backtracking with early pruning
        Sort candidates first for better pruning
        """
        candidates.sort()  # Sort for early termination
        result = []
        
        def backtrack(start_index, current_combination, remaining_target):
            if remaining_target == 0:
                result.append(current_combination[:])
                return
            
            for i in range(start_index, len(candidates)):
                candidate = candidates[i]
                
                # Early termination: if current candidate > remaining, 
                # all subsequent candidates will also exceed (since sorted)
                if candidate > remaining_target:
                    break
                
                current_combination.append(candidate)
                backtrack(i, current_combination, remaining_target - candidate)
                current_combination.pop()
        
        backtrack(0, [], target)
        return result

    def combinationSumIterative(self, candidates, target):
        """
        Iterative solution using stack (DFS simulation)
        Good alternative to show non-recursive thinking
        """
        result = []
        # Stack stores: (start_index, current_combination, remaining_target)
        stack = [(0, [], target)]
        
        while stack:
            start_index, current_combination, remaining_target = stack.pop()
            
            if remaining_target == 0:
                result.append(current_combination)
                continue
            
            if remaining_target < 0:
                continue
            
            for i in range(start_index, len(candidates)):
                candidate = candidates[i]
                
                if candidate <= remaining_target:
                    # Create new combination (avoid reference issues)
                    new_combination = current_combination + [candidate]
                    stack.append((i, new_combination, remaining_target - candidate))
        
        return result

    def combinationSumDP(self, candidates, target):
        """
        Dynamic Programming approach - less intuitive but shows different thinking
        dp[i] = all combinations that sum to i
        """
        dp = [[] for _ in range(target + 1)]
        dp[0] = [[]]  # One way to make 0: empty combination
        
        for i in range(1, target + 1):
            for candidate in candidates:
                if candidate <= i and dp[i - candidate]:
                    # Add candidate to all combinations that sum to (i - candidate)
                    for combination in dp[i - candidate]:
                        dp[i].append(combination + [candidate])
        
        return dp[target]

    def combinationSumMemoized(self, candidates, target):
        """
        Backtracking with memoization
        Cache results for same (start_index, remaining_target) pairs
        """
        memo = {}
        
        def backtrack(start_index, remaining_target):
            # Check memo
            if (start_index, remaining_target) in memo:
                return memo[(start_index, remaining_target)]
            
            # Base cases
            if remaining_target == 0:
                return [[]]
            
            if remaining_target < 0 or start_index >= len(candidates):
                return []
            
            result = []
            
            # Try each candidate from start_index
            for i in range(start_index, len(candidates)):
                candidate = candidates[i]
                
                if candidate <= remaining_target:
                    # Get all combinations for remaining target
                    sub_combinations = backtrack(i, remaining_target - candidate)
                    
                    # Add current candidate to each sub-combination
                    for combo in sub_combinations:
                        result.append([candidate] + combo)
            
            memo[(start_index, remaining_target)] = result
            return result
        
        return backtrack(0, target)

    def combinationSumConcise(self, candidates, target):
        """
        Most concise backtracking solution
        """
        def backtrack(start, path, remaining):
            if remaining == 0:
                return [path]
            
            result = []
            for i in range(start, len(candidates)):
                if candidates[i] <= remaining:
                    result.extend(backtrack(i, path + [candidates[i]], remaining - candidates[i]))
            
            return result
        
        return backtrack(0, [], target)


# Test cases for interview
def test_combination_sum():
    solution = Solution()
    
    # Test case 1: Standard case
    candidates1 = [2, 3, 6, 7]
    target1 = 7
    result1 = solution.combinationSum(candidates1, target1)
    print(f"Test 1 - candidates: {candidates1}, target: {target1}")
    print(f"Result: {result1}")
    # Expected: [[2,2,3],[7]]
    
    # Test case 2: Multiple solutions
    candidates2 = [2, 3, 5]
    target2 = 8
    result2 = solution.combinationSum(candidates2, target2)
    print(f"\nTest 2 - candidates: {candidates2}, target: {target2}")
    print(f"Result: {result2}")
    # Expected: [[2,2,2,2],[2,3,3],[3,5]]
    
    # Test case 3: No solution
    candidates3 = [2]
    target3 = 1
    result3 = solution.combinationSum(candidates3, target3)
    print(f"\nTest 3 - candidates: {candidates3}, target: {target3}")
    print(f"Result: {result3}")
    # Expected: []
    
    # Test case 4: Single element solution
    candidates4 = [1]
    target4 = 1
    result4 = solution.combinationSum(candidates4, target4)
    print(f"\nTest 4 - candidates: {candidates4}, target: {target4}")
    print(f"Result: {result4}")
    # Expected: [[1]]
    
    # Test case 5: Large target
    candidates5 = [2, 3, 5]
    target5 = 12
    result5 = solution.combinationSum(candidates5, target5)
    print(f"\nTest 5 - candidates: {candidates5}, target: {target5}")
    print(f"Result count: {len(result5)}")

if __name__ == "__main__":
    test_combination_sum()


"""
Key Interview Points to Discuss:

1. PROBLEM UNDERSTANDING:
   - Find all unique combinations that sum to target
   - Numbers can be reused unlimited times
   - Same combination in different order should appear only once
   - This is backtracking with repetition allowed

2. KEY INSIGHT - AVOID DUPLICATES:
   - Use start_index to ensure we don't consider previous elements
   - This prevents generating [2,3] and [3,2] as separate combinations
   - Always move forward or stay at same index (for reuse)

3. BACKTRACKING TEMPLATE:
   - Base case: remaining_target == 0 (found solution)
   - Pruning: remaining_target < 0 (exceeded target)
   - Choice: try each candidate from start_index onwards
   - Recurse: same index (reuse allowed) with updated remaining
   - Backtrack: remove choice and try next

4. WHY START_INDEX APPROACH WORKS:
   - Ensures lexicographic order
   - Prevents duplicate combinations
   - [2,2,3] will be found, but [3,2,2] won't be generated
   - Natural way to handle "combinations with repetition"

5. EDGE CASES TO MENTION:
   - Empty candidates array
   - Target is 0 (return [[]])
   - No valid combinations exist
   - Target smaller than smallest candidate
   - All candidates larger than target

6. TIME/SPACE COMPLEXITY:
   - Time: O(N^(T/M)) where N=candidates, T=target, M=min candidate
   - Worst case: T/M depth, N choices at each level
   - Space: O(T/M) recursion depth + space for storing results
   - Result space can be exponential in worst case

7. OPTIMIZATION TECHNIQUES:
   - Sort candidates for early termination
   - Prune when candidate > remaining_target
   - Use memoization for overlapping subproblems
   - Iterative approach to avoid recursion overhead

8. FOLLOW-UP QUESTIONS TO EXPECT:
   - "Can you optimize?" -> Sort + early termination
   - "What if candidates have duplicates?" -> Combination Sum II (different problem)
   - "Iterative solution?" -> Stack-based DFS
   - "DP approach?" -> Bottom-up combination building
   - "Memory constraints?" -> Generator approach

9. COMPARISON WITH SIMILAR PROBLEMS:
   - Combination Sum II: Candidates have duplicates, each used once
   - Combination Sum III: Fixed number of elements
   - Letter Combinations: Cartesian product vs. sum constraint
   - Subsets: All possible combinations vs. target sum

10. REAL-WORLD APPLICATIONS:
    - Making change problem (coin combinations)
    - Resource allocation with constraints
    - Recipe ingredient combinations
    - Portfolio optimization

11. DEBUGGING TIPS:
    - Draw recursion tree for small example
    - Verify start_index logic prevents duplicates
    - Check base cases handle edge conditions
    - Ensure proper backtracking (pop after recursion)

12. INTERVIEW CODING TIPS:
    - Start with basic backtracking template
    - Mention optimizations but code simple version first
    - Use descriptive variable names (remaining_target vs. target)
    - Add comments for base cases and key logic
    - Test with simple example during coding

13. ALTERNATIVE PERSPECTIVES:
    - Think of it as "unlimited knapsack" problem
    - Graph traversal where each node is a partial sum
    - Tree generation where each path represents a combination
    - Recursive decomposition: solve(target) = solve(target-candidate) + [candidate]
"""
