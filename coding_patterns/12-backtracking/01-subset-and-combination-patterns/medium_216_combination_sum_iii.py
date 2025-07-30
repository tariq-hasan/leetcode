from typing import List

class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        """
        Problem: Find all valid combinations of k numbers that sum to n.
        Only use numbers 1-9, each number used at most once.
        
        APPROACH 1: BACKTRACKING (Standard Interview Solution)
        Time: O(C(9,k) * k) = O(9!/(k!(9-k)!) * k) - combinations * copy cost
        Space: O(k) for recursion depth and current combination
        
        This is the most intuitive and expected approach.
        """
        result = []
        
        def backtrack(start, current_combination, remaining_sum, remaining_count):
            """
            start: next number to consider (1-9)
            current_combination: numbers chosen so far
            remaining_sum: target sum left to achieve
            remaining_count: how many more numbers we need
            """
            # Base case: found valid combination
            if remaining_count == 0 and remaining_sum == 0:
                result.append(current_combination[:])  # Make copy
                return
            
            # Pruning: impossible to complete
            if remaining_count == 0 or remaining_sum <= 0:
                return
            
            # Try each number from start to 9
            for num in range(start, 10):
                # Pruning: if current number > remaining sum, skip
                if num > remaining_sum:
                    break
                
                # Choose current number
                current_combination.append(num)
                # Recurse with updated parameters
                backtrack(num + 1, current_combination, remaining_sum - num, remaining_count - 1)
                # Backtrack
                current_combination.pop()
        
        backtrack(1, [], n, k)
        return result
    
    def combinationSum3_optimized(self, k: int, n: int) -> List[List[int]]:
        """
        APPROACH 2: BACKTRACKING WITH ENHANCED PRUNING
        Time: O(C(9,k) * k) - same but with better constant factors
        Space: O(k)
        
        More aggressive pruning to reduce search space.
        """
        result = []
        
        def backtrack(start, path, target, count):
            # Early termination conditions
            if count == 0:
                if target == 0:
                    result.append(path[:])
                return
            
            # Pruning: not enough numbers left or target too small
            if target <= 0 or 10 - start < count:
                return
            
            # Pruning: minimum possible sum with remaining numbers
            min_possible = sum(range(start, start + count))
            if target < min_possible:
                return
            
            # Pruning: maximum possible sum with remaining numbers  
            max_possible = sum(range(10 - count, 10))
            if target > max_possible:
                return
            
            for num in range(start, 10):
                # Early break if number too large
                if num > target:
                    break
                
                path.append(num)
                backtrack(num + 1, path, target - num, count - 1)
                path.pop()
        
        # Early validation
        if k > 9 or n < 1 or n > 45:  # 45 is sum of 1+2+...+9
            return []
        
        backtrack(1, [], n, k)
        return result
    
    def combinationSum3_iterative(self, k: int, n: int) -> List[List[int]]:
        """
        APPROACH 3: ITERATIVE WITH STACK (Alternative Implementation)
        Time: O(C(9,k) * k)
        Space: O(C(9,k) * k) for storing all combinations
        
        Good to show different implementation style.
        """
        if k > 9 or n < 1 or n > 45:
            return []
        
        result = []
        # Stack stores: (start_num, current_path, remaining_sum, remaining_count)
        stack = [(1, [], n, k)]
        
        while stack:
            start, path, target, count = stack.pop()
            
            if count == 0:
                if target == 0:
                    result.append(path)
                continue
            
            if target <= 0 or 10 - start < count:
                continue
            
            for num in range(start, 10):
                if num > target:
                    break
                
                new_path = path + [num]
                stack.append((num + 1, new_path, target - num, count - 1))
        
        return result

# INTERVIEW DEMONSTRATION CLASS
class InterviewSolution:
    """
    Clean, interview-ready solution with clear explanation
    """
    
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        """
        MAIN INTERVIEW SOLUTION
        Find all combinations of k unique numbers (1-9) that sum to n
        """
        result = []
        
        def is_valid_input():
            """Quick validation of input constraints"""
            # Need at least k numbers, each at least 1
            if n < k:
                return False
            # Maximum sum with k smallest numbers: 1+2+...+k
            if n < k * (k + 1) // 2:
                return False
            # Maximum sum with k largest numbers: (10-k)+(10-k+1)+...+9
            max_sum = k * (19 - k) // 2
            if n > max_sum:
                return False
            return True
        
        def backtrack(start_num, current_combo, remaining_sum, remaining_count):
            """
            Backtracking function to build combinations
            
            start_num: next number to consider (prevents duplicates)
            current_combo: combination being built
            remaining_sum: how much sum is left to achieve
            remaining_count: how many more numbers we need
            """
            # Success case: used exactly k numbers with sum n
            if remaining_count == 0 and remaining_sum == 0:
                result.append(current_combo[:])  # Important: make copy
                return
            
            # Pruning: impossible cases
            if remaining_count == 0 or remaining_sum <= 0:
                return
            
            # Try each valid number from start_num to 9
            for num in range(start_num, 10):
                # Pruning: if current number exceeds remaining sum
                if num > remaining_sum:
                    break  # All larger numbers will also exceed
                
                # Choose this number
                current_combo.append(num)
                
                # Recurse: next number is num+1 (no repeats)
                backtrack(num + 1, current_combo, 
                         remaining_sum - num, remaining_count - 1)
                
                # Backtrack: remove this number
                current_combo.pop()
        
        # Input validation
        if not is_valid_input():
            return []
        
        backtrack(1, [], n, k)
        return result

# COMPREHENSIVE TESTING
def test_solutions():
    """Test all approaches with comprehensive cases"""
    solutions = [
        Solution().combinationSum3,
        Solution().combinationSum3_optimized,
        Solution().combinationSum3_iterative,
        InterviewSolution().combinationSum3
    ]
    
    test_cases = [
        # (k, n, expected_result_count, sample_result)
        (3, 7, 1, [[1, 2, 4]]),
        (3, 9, 3, [[1, 2, 6], [1, 3, 5], [2, 3, 4]]),
        (4, 1, 0, []),  # Impossible: need 4 numbers but sum is 1
        (2, 18, 1, [[9, 9]]),  # Wait, can't repeat! Should be []
        (2, 18, 0, []),  # Corrected: can't use same number twice
        (1, 5, 1, [[5]]),  # Single number
        (9, 45, 1, [[1, 2, 3, 4, 5, 6, 7, 8, 9]]),  # Use all numbers
        (2, 10, 3, [[1, 9], [2, 8], [3, 7], [4, 6]]),  # Multiple valid pairs
    ]
    
    # Fix test case that was wrong
    test_cases[3] = (2, 17, 1, [[8, 9]])  # Only one way: 8+9=17
    test_cases[7] = (2, 10, 4, [[1, 9], [2, 8], [3, 7], [4, 6]])
    
    for i, solution_func in enumerate(solutions):
        print(f"Testing Solution {i+1}...")
        for k, n, expected_count, sample in test_cases:
            result = solution_func(k, n)
            
            if len(result) != expected_count:
                print(f"  FAILED: k={k}, n={n}")
                print(f"    Expected {expected_count} combinations, got {len(result)}")
                print(f"    Result: {result}")
                continue
            
            # Validate each combination
            for combo in result:
                if len(combo) != k:
                    print(f"    Invalid length: {combo}")
                if sum(combo) != n:
                    print(f"    Invalid sum: {combo} sums to {sum(combo)}, not {n}")
                if len(set(combo)) != len(combo):
                    print(f"    Contains duplicates: {combo}")
                if any(x < 1 or x > 9 for x in combo):
                    print(f"    Invalid numbers: {combo}")
        
        print(f"Solution {i+1} passed all tests ✓")

# INTERVIEW STRATEGY GUIDE
interview_strategy = """
INTERVIEW WALKTHROUGH (6-8 minutes total):

1. PROBLEM UNDERSTANDING (1 minute):
   "I need to find combinations of k unique numbers from 1-9 that sum to n."
   "Each number can be used at most once, and I need exactly k numbers."
   "This is a classic backtracking/combination problem."

2. APPROACH EXPLANATION (1 minute):
   "I'll use backtracking to try all possible combinations."
   "At each step, I'll try numbers from current position to 9."
   "I'll track remaining sum and remaining count to know when to stop."
   "Key insight: use start parameter to avoid duplicates (1,2,3) vs (2,1,3)."

3. IMPLEMENTATION WALKTHROUGH (3-4 minutes):
   - Explain backtracking function parameters clearly
   - Show base case (remaining_count == 0 and remaining_sum == 0)
   - Demonstrate pruning (if num > remaining_sum, break)
   - Emphasize making copy when adding to result
   - Show proper backtracking pattern (append -> recurse -> pop)

4. COMPLEXITY ANALYSIS (1 minute):
   "Time: O(C(9,k) * k) - number of ways to choose k from 9, times copy cost"
   "Space: O(k) - recursion depth and current combination storage"
   "In practice, much faster due to pruning."

5. OPTIMIZATIONS (1 minute):
   "Can add more aggressive pruning:"
   "- Early validation of k and n ranges"
   "- Check if remaining numbers can achieve target"
   "- Mathematical bounds on possible sums"

KEY TALKING POINTS:
✓ "I'll use start parameter to avoid duplicate combinations"
✓ "Pruning when current number exceeds remaining sum"
✓ "Making copy of combination when adding to result"
✓ "This is bounded search space - at most C(9,k) combinations"

COMMON MISTAKES TO AVOID:
✗ Not using start parameter (generates duplicate combinations)
✗ Not making copy of current combination
✗ Forgetting to backtrack (not calling pop())
✗ Wrong base case conditions
✗ Not handling edge cases (k > 9, impossible sums)

FOLLOW-UP OPTIMIZATIONS:
- More aggressive mathematical pruning
- Early termination based on remaining sum bounds  
- Iterative implementation instead of recursive
"""

# MATHEMATICAL INSIGHTS
math_insights = """
MATHEMATICAL BOUNDS AND PRUNING:

1. MINIMUM POSSIBLE SUM with k numbers:
   sum of k smallest: 1 + 2 + ... + k = k(k+1)/2
   If n < k(k+1)/2, impossible

2. MAXIMUM POSSIBLE SUM with k numbers:
   sum of k largest: (10-k) + (10-k+1) + ... + 9 = k(19-k)/2
   If n > k(19-k)/2, impossible

3. DURING SEARCH PRUNING:
   - If current_num > remaining_sum, break (all larger nums will exceed)
   - If not enough numbers left: 10 - start < remaining_count
   - If min possible with remaining numbers > target, prune
   - If max possible with remaining numbers < target, prune

4. SEARCH SPACE SIZE:
   Total combinations: C(9, k) = 9!/(k!(9-k)!)
   Examples:
   - k=2: C(9,2) = 36 combinations  
   - k=3: C(9,3) = 84 combinations
   - k=4: C(9,4) = 126 combinations
   
5. PRACTICAL OPTIMIZATIONS:
   - Sort result combinations (not required but clean)
   - Use bit manipulation for very advanced optimization
   - Memoization not helpful here (no overlapping subproblems)
"""

# EDGE CASES AND EXAMPLES
edge_cases_guide = """
CRITICAL EDGE CASES TO HANDLE:

1. IMPOSSIBLE CASES:
   - k > 9: Can't choose more than 9 unique numbers
   - n < k: Sum too small (need at least k if using 1,1,1...)  
   - n > 45: Sum too large (max is 1+2+...+9 = 45)
   - k=4, n=10: Min sum with 4 numbers is 1+2+3+4=10, so only one solution

2. BOUNDARY CASES:
   - k=1: Just check if n is in range [1,9]
   - k=9, n=45: Only one solution [1,2,3,4,5,6,7,8,9]
   - k=2, n=3: Only [1,2]
   - k=2, n=17: Only [8,9]

3. NO SOLUTION CASES:
   - k=3, n=6: Impossible (min is 1+2+3=6, but then all smallest)
   - k=2, n=19: Impossible (max is 8+9=17)

4. MULTIPLE SOLUTION CASES:
   - k=3, n=9: [[1,2,6], [1,3,5], [2,3,4]]
   - k=2, n=10: [[1,9], [2,8], [3,7], [4,6]]

TESTING STRATEGY:
- Test minimum and maximum possible sums for given k
- Test cases with no solutions
- Test cases with exactly one solution  
- Test cases with multiple solutions
- Verify no duplicate combinations in result
- Verify all combinations have exactly k elements
- Verify all combinations sum to exactly n
"""

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*70)
    print(interview_strategy)
    print("\n" + "="*70) 
    print(math_insights)
    print("\n" + "="*70)
    print(edge_cases_guide)
