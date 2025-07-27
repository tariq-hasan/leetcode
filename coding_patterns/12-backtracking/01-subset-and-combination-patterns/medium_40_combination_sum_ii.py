"""
LeetCode 40: Combination Sum II

Problem: Given a collection of candidate numbers (candidates) and a target number (target), 
find all unique combinations in candidates where the candidate numbers sum to target.
Each number in candidates may only be used ONCE in the combination.

Key Differences from Combination Sum I:
1. Candidates array may contain duplicates
2. Each candidate can only be used once (not unlimited times)
3. Must handle duplicate combinations caused by duplicate candidates

Key Insight: Sort first, then skip duplicates at the same recursion level
to avoid generating duplicate combinations.

Time Complexity: O(2^N) in worst case where N = len(candidates)
Space Complexity: O(N) for recursion depth + space for storing results
"""

class Solution:
    def combinationSum2(self, candidates, target):
        """
        Backtracking with duplicate skipping - Most important solution for interviews
        """
        candidates.sort()  # CRITICAL: Sort to group duplicates together
        result = []
        
        def backtrack(start_index, current_combination, remaining_target):
            # Base cases
            if remaining_target == 0:
                result.append(current_combination[:])
                return
            
            if remaining_target < 0:
                return
            
            for i in range(start_index, len(candidates)):
                candidate = candidates[i]
                
                # KEY INSIGHT: Skip duplicates at the same level
                # Only skip if i > start_index (not the first element at this level)
                if i > start_index and candidates[i] == candidates[i-1]:
                    continue
                
                # Early termination optimization
                if candidate > remaining_target:
                    break
                
                # Choose
                current_combination.append(candidate)
                
                # Recurse with i+1 (each element used only once)
                backtrack(i + 1, current_combination, remaining_target - candidate)
                
                # Backtrack
                current_combination.pop()
        
        backtrack(0, [], target)
        return result

    def combinationSum2Verbose(self, candidates, target):
        """
        More verbose version with detailed comments for explanation
        """
        candidates.sort()
        result = []
        
        def backtrack(start_index, current_combination, remaining_target):
            # Base case: found valid combination
            if remaining_target == 0:
                result.append(current_combination[:])  # Make a copy
                return
            
            # Pruning: exceeded target
            if remaining_target < 0:
                return
            
            for i in range(start_index, len(candidates)):
                candidate = candidates[i]
                
                # Skip duplicates at the same recursion level
                # This is the key to avoiding duplicate combinations
                # We allow first occurrence but skip subsequent duplicates
                if i > start_index and candidates[i] == candidates[i-1]:
                    print(f"Skipping duplicate {candidates[i]} at position {i}")
                    continue
                
                # Early termination since array is sorted
                if candidate > remaining_target:
                    print(f"Early termination: {candidate} > {remaining_target}")
                    break
                
                print(f"Trying candidate {candidate} at level {len(current_combination)}")
                
                # Make choice
                current_combination.append(candidate)
                
                # Recurse: move to next index (no reuse allowed)
                backtrack(i + 1, current_combination, remaining_target - candidate)
                
                # Backtrack
                current_combination.pop()
                print(f"Backtracked from {candidate}")
        
        backtrack(0, [], target)
        return result

    def combinationSum2Alternative(self, candidates, target):
        """
        Alternative approach using set to avoid duplicates
        Less efficient but shows different thinking
        """
        candidates.sort()
        result = []
        seen_combinations = set()
        
        def backtrack(start_index, current_combination, remaining_target):
            if remaining_target == 0:
                combo_tuple = tuple(current_combination)
                if combo_tuple not in seen_combinations:
                    seen_combinations.add(combo_tuple)
                    result.append(current_combination[:])
                return
            
            if remaining_target < 0:
                return
            
            for i in range(start_index, len(candidates)):
                candidate = candidates[i]
                
                if candidate > remaining_target:
                    break
                
                current_combination.append(candidate)
                backtrack(i + 1, current_combination, remaining_target - candidate)
                current_combination.pop()
        
        backtrack(0, [], target)
        return result

    def combinationSum2Iterative(self, candidates, target):
        """
        Iterative solution using stack
        """
        candidates.sort()
        result = []
        # Stack: (start_index, current_combination, remaining_target)
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
                
                # Skip duplicates at same level
                if i > start_index and candidates[i] == candidates[i-1]:
                    continue
                
                if candidate > remaining_target:
                    break
                
                new_combination = current_combination + [candidate]
                stack.append((i + 1, new_combination, remaining_target - candidate))
        
        return result

    def combinationSum2Optimized(self, candidates, target):
        """
        Optimized version with frequency counting
        Good for arrays with many duplicates
        """
        from collections import Counter
        counter = Counter(candidates)
        unique_candidates = sorted(counter.keys())
        result = []
        
        def backtrack(index, current_combination, remaining_target):
            if remaining_target == 0:
                result.append(current_combination[:])
                return
            
            if index >= len(unique_candidates) or remaining_target < 0:
                return
            
            candidate = unique_candidates[index]
            max_count = min(counter[candidate], remaining_target // candidate)
            
            # Try using 0 to max_count of current candidate
            for count in range(max_count + 1):
                # Add 'count' copies of current candidate
                current_combination.extend([candidate] * count)
                
                # Recurse to next unique candidate
                backtrack(index + 1, current_combination, remaining_target - candidate * count)
                
                # Remove 'count' copies for backtracking
                for _ in range(count):
                    current_combination.pop()
        
        backtrack(0, [], target)
        return result

    def combinationSum2Concise(self, candidates, target):
        """
        Most concise version
        """
        candidates.sort()
        
        def backtrack(start, path, remaining):
            if remaining == 0:
                return [path]
            
            result = []
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i-1]:
                    continue
                if candidates[i] > remaining:
                    break
                result.extend(backtrack(i + 1, path + [candidates[i]], remaining - candidates[i]))
            
            return result
        
        return backtrack(0, [], target)


# Test cases for interview
def test_combination_sum2():
    solution = Solution()
    
    # Test case 1: Standard case with duplicates
    candidates1 = [10, 1, 2, 7, 6, 1, 5]
    target1 = 8
    result1 = solution.combinationSum2(candidates1, target1)
    print(f"Test 1 - candidates: {candidates1}, target: {target1}")
    print(f"Result: {result1}")
    # Expected: [[1,1,6],[1,2,5],[1,7],[2,6]]
    
    # Test case 2: Multiple duplicates
    candidates2 = [2, 5, 2, 1, 2]
    target2 = 5
    result2 = solution.combinationSum2(candidates2, target2)
    print(f"\nTest 2 - candidates: {candidates2}, target: {target2}")
    print(f"Result: {result2}")
    # Expected: [[1,2,2],[5]]
    
    # Test case 3: No solution
    candidates3 = [2, 3, 5]
    target3 = 1
    result3 = solution.combinationSum2(candidates3, target3)
    print(f"\nTest 3 - candidates: {candidates3}, target: {target3}")
    print(f"Result: {result3}")
    # Expected: []
    
    # Test case 4: All same numbers
    candidates4 = [1, 1, 1, 1]
    target4 = 2
    result4 = solution.combinationSum2(candidates4, target4)
    print(f"\nTest 4 - candidates: {candidates4}, target: {target4}")
    print(f"Result: {result4}")
    # Expected: [[1,1]]
    
    # Test case 5: Single element
    candidates5 = [1]
    target5 = 1
    result5 = solution.combinationSum2(candidates5, target5)
    print(f"\nTest 5 - candidates: {candidates5}, target: {target5}")
    print(f"Result: {result5}")
    # Expected: [[1]]

if __name__ == "__main__":
    test_combination_sum2()


"""
Key Interview Points to Discuss:

1. PROBLEM UNDERSTANDING:
   - Each candidate used AT MOST once (vs. unlimited in Combination Sum I)
   - Candidates array may contain duplicates
   - Must avoid duplicate combinations in result
   - More constrained than Combination Sum I

2. KEY CHALLENGE - HANDLING DUPLICATES:
   - Input: [1,1,2], target: 3
   - Without handling: might generate [1,2] twice (using different 1's)
   - Solution: Sort first, then skip duplicates at same recursion level

3. CRITICAL INSIGHT - DUPLICATE SKIPPING LOGIC:
   ```python
   if i > start_index and candidates[i] == candidates[i-1]:
       continue  # Skip duplicate
   ```
   - Only skip if i > start_index (not the first at this level)
   - This allows first occurrence but skips subsequent duplicates
   - Prevents generating same combination multiple ways

4. WHY SORTING IS ESSENTIAL:
   - Groups duplicate values together
   - Enables the duplicate skipping logic
   - Allows early termination optimization
   - Makes duplicate detection O(1)

5. DIFFERENCE FROM COMBINATION SUM I:
   - Recursion: backtrack(i+1, ...) vs. backtrack(i, ...)
   - No reuse: each element used at most once
   - Duplicate handling: additional logic needed
   - Input constraints: may have duplicates

6. EDGE CASES TO MENTION:
   - All duplicates: [1,1,1,1], target=2 → [[1,1]]
   - No solution possible
   - Target equals single candidate
   - Empty candidates array
   - Single element array

7. TIME/SPACE COMPLEXITY:
   - Time: O(2^N) worst case - each element included or not
   - Sorting: O(N log N) preprocessing
   - Space: O(N) recursion depth + exponential result storage
   - Better than naive O(N!) approach

8. OPTIMIZATION TECHNIQUES:
   - Sort for duplicate grouping and early termination
   - Skip duplicates at same level
   - Early pruning when candidate > remaining
   - Frequency counting for many duplicates

9. FOLLOW-UP QUESTIONS TO EXPECT:
   - "Why not use a set to avoid duplicates?" → Less efficient, still need sorting
   - "What if array has many duplicates?" → Frequency counting approach
   - "Can you solve iteratively?" → Stack-based solution
   - "How to modify for k elements?" → Add counter parameter

10. DEBUGGING THE DUPLICATE LOGIC:
    Walk through example: [1,1,2], target=3
    - Level 0: try candidates[0]=1, candidates[1]=1 (skip), candidates[2]=2
    - When candidates[0]=1: recurse with [2] at level 1
    - Skip candidates[1]=1 because it's duplicate at same level
    - This prevents generating [1,2] twice

11. COMPARISON WITH RELATED PROBLEMS:
    - Combination Sum I: Unlimited reuse vs. single use
    - Combination Sum III: Fixed count constraint
    - Subsets II: All combinations vs. target sum constraint
    - Permutations II: Order matters vs. combinations

12. REAL-WORLD APPLICATIONS:
    - Resource allocation with limited quantities
    - Team selection with constraints
    - Portfolio construction with asset limits
    - Recipe variations with ingredient constraints

13. INTERVIEW STRATEGY:
    - Start by explaining difference from Combination Sum I
    - Draw example showing duplicate issue: [1,1,2] → why [1,2] appears twice
    - Code the duplicate skipping logic carefully
    - Explain why i > start_index condition is crucial
    - Test with duplicate-heavy example

14. COMMON MISTAKES TO AVOID:
    - Forgetting to sort the array first
    - Wrong duplicate skipping condition (i > 0 vs. i > start_index)
    - Using i instead of i+1 in recursion (allows reuse)
    - Not handling empty result case properly
"""
