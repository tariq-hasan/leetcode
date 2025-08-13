# LeetCode 664: Strange Printer
# 
# Problem: There is a strange printer with the following two special properties:
# 1. The printer can only print a sequence of the same character each time.
# 2. At each turn, the printer can print new characters starting from and ending 
#    at any place and will cover the original existing characters.
# Return the minimum number of turns the printer needed to print it.

class Solution:
    def strangePrinter(self, s: str) -> int:
        """
        Solution 1: Top-Down DP with Memoization
        Time: O(n^3), Space: O(n^2)
        Most intuitive approach for interviews
        """
        if not s:
            return 0
        
        # Remove consecutive duplicates for optimization
        s = self._remove_duplicates(s)
        n = len(s)
        
        # Memoization cache
        memo = {}
        
        def dp(i, j):
            # Base case: single character or invalid range
            if i > j:
                return 0
            if i == j:
                return 1
            
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Case 1: Print s[i] first, then handle the rest
            # This gives us at least dp(i+1, j) + 1 operations
            result = dp(i + 1, j) + 1
            
            # Case 2: Try to merge printing operations
            # If s[i] == s[k] for some k > i, we can print s[i] to s[k]
            # in one operation, potentially saving operations
            for k in range(i + 1, j + 1):
                if s[i] == s[k]:
                    # Print from i to k with character s[i]
                    # This covers positions i and k in one operation
                    # Then we need dp(i+1, k-1) + dp(k+1, j) operations
                    result = min(result, dp(i + 1, k - 1) + dp(k + 1, j))
            
            memo[(i, j)] = result
            return result
        
        return dp(0, n - 1)
    
    def _remove_duplicates(self, s):
        """Remove consecutive duplicate characters"""
        if not s:
            return s
        
        result = [s[0]]
        for i in range(1, len(s)):
            if s[i] != s[i-1]:
                result.append(s[i])
        return ''.join(result)

class SolutionBottomUp:
    def strangePrinter(self, s: str) -> int:
        """
        Solution 2: Bottom-Up DP (Iterative)
        Time: O(n^3), Space: O(n^2)
        More optimized for production use
        """
        if not s:
            return 0
        
        # Remove consecutive duplicates
        s = self._remove_duplicates(s)
        n = len(s)
        
        # dp[i][j] = minimum operations to print s[i:j+1]
        dp = [[0] * n for _ in range(n)]
        
        # Base case: single characters
        for i in range(n):
            dp[i][i] = 1
        
        # Fill for all lengths from 2 to n
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                # Initialize with worst case: print each character separately
                dp[i][j] = dp[i + 1][j] + 1
                
                # Try to optimize by merging operations
                for k in range(i + 1, j + 1):
                    if s[i] == s[k]:
                        left_cost = 0 if i + 1 > k - 1 else dp[i + 1][k - 1]
                        right_cost = 0 if k + 1 > j else dp[k + 1][j]
                        dp[i][j] = min(dp[i][j], left_cost + right_cost)
        
        return dp[0][n - 1]
    
    def _remove_duplicates(self, s):
        """Remove consecutive duplicate characters"""
        if not s:
            return s
        
        result = []
        for char in s:
            if not result or result[-1] != char:
                result.append(char)
        return ''.join(result)

class SolutionOptimized:
    def strangePrinter(self, s: str) -> int:
        """
        Solution 3: Optimized with Better State Definition
        Time: O(n^3), Space: O(n^2)
        Best approach for interviews - cleaner logic
        """
        if not s:
            return 0
        
        # Preprocess: remove consecutive duplicates
        chars = []
        for c in s:
            if not chars or chars[-1] != c:
                chars.append(c)
        
        n = len(chars)
        if n == 1:
            return 1
        
        # dp[i][j] = min operations to print chars[i:j+1]
        dp = [[float('inf')] * n for _ in range(n)]
        
        # Base cases
        for i in range(n):
            dp[i][i] = 1
        
        # Fill dp table
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                # Option 1: Print chars[i] separately
                dp[i][j] = min(dp[i][j], dp[i + 1][j] + 1)
                
                # Option 2: Find matching characters and merge
                for k in range(i + 1, j + 1):
                    if chars[i] == chars[k]:
                        # Print chars[i] and chars[k] together
                        left = dp[i + 1][k - 1] if i + 1 <= k - 1 else 0
                        right = dp[k + 1][j] if k + 1 <= j else 0
                        dp[i][j] = min(dp[i][j], left + right)
        
        return dp[0][n - 1]

class SolutionWithExplanation:
    def strangePrinter(self, s: str) -> int:
        """
        Solution 4: Detailed explanation version for interview discussion
        Time: O(n^3), Space: O(n^2)
        """
        if not s:
            return 0
        
        # Step 1: Preprocessing - remove consecutive duplicates
        # "aaabbbccc" -> "abc" (no change in minimum operations needed)
        processed = self._preprocess(s)
        n = len(processed)
        
        # Step 2: Initialize memoization
        memo = {}
        
        def solve(start, end):
            """
            Returns minimum operations to print processed[start:end+1]
            
            Key insight: When we print a character, we can print it across
            any range where it eventually needs to appear, potentially
            saving operations by "preparing" future positions.
            """
            # Base cases
            if start > end:
                return 0
            if start == end:
                return 1
            
            if (start, end) in memo:
                return memo[(start, end)]
            
            # Strategy 1: Print processed[start] by itself
            # Then solve the remaining substring
            min_ops = solve(start + 1, end) + 1
            
            # Strategy 2: Look for the same character later in the string
            # If processed[start] == processed[k], we can print both positions
            # in a single operation by printing processed[start] from start to k
            for k in range(start + 1, end + 1):
                if processed[start] == processed[k]:
                    # Print processed[start] from position start to k
                    # This handles both start and k positions
                    # We need to solve: [start+1, k-1] and [k+1, end]
                    left_cost = solve(start + 1, k - 1)
                    right_cost = solve(k + 1, end)
                    min_ops = min(min_ops, left_cost + right_cost)
            
            memo[(start, end)] = min_ops
            return min_ops
        
        return solve(0, n - 1)
    
    def _preprocess(self, s):
        """Remove consecutive duplicates to optimize"""
        result = []
        for char in s:
            if not result or result[-1] != char:
                result.append(char)
        return result

# Test cases and comprehensive analysis
def test_solutions():
    solutions = [
        Solution(), 
        SolutionBottomUp(), 
        SolutionOptimized(), 
        SolutionWithExplanation()
    ]
    
    test_cases = [
        ("aaabbb", 2),      # "aaa" then "bbb"
        ("aba", 2),         # "aaa" then "b" (overwrite middle)
        ("abcabc", 5),      # Each character needs separate operation mostly
        ("", 0),            # Empty string
        ("a", 1),           # Single character
        ("abcdef", 6),      # No optimization possible
        ("ababa", 3),       # "aaaaa" then "bbb" then "aaa" 
        ("abcabcabc", 7),   # Complex case
    ]
    
    print("Testing all solutions:")
    print("=" * 60)
    
    for i, sol in enumerate(solutions, 1):
        class_name = sol.__class__.__name__
        print(f"\nSolution {i} ({class_name}):")
        
        for s, expected in test_cases:
            try:
                result = sol.strangePrinter(s)
                status = "✓" if result == expected else "✗"
                print(f"  {status} strangePrinter('{s}') = {result} (expected {expected})")
            except Exception as e:
                print(f"  ✗ Error with '{s}': {e}")

def explain_algorithm():
    print("\n" + "=" * 60)
    print("ALGORITHM EXPLANATION")
    print("=" * 60)
    
    print("""
Key Insights:
1. This is an interval DP problem - we solve subproblems on ranges [i,j]

2. For any range [i,j], we have two main strategies:
   - Print s[i] separately: cost = 1 + dp(i+1, j)
   - Find matching s[k] where s[i] == s[k]: print s[i] from i to k in one operation
     Then solve subproblems: dp(i+1, k-1) + dp(k+1, j)

3. The key optimization: when we print a character, we can print it across
   any range where it will eventually need to appear.

4. Preprocessing removes consecutive duplicates since "aaa" and "a" take
   the same number of operations.

Time Complexity: O(n³)
- Three nested loops: range length, start position, split position
- Each state computed once due to memoization

Space Complexity: O(n²)
- DP table or memoization cache stores results for all ranges [i,j]

Example walkthrough for "aba":
- We can print "aaa" first (1 operation)  
- Then print "b" in the middle (1 operation, overwrites middle 'a')
- Total: 2 operations instead of naive 3
    """)

def interview_tips():
    print("\n" + "=" * 60)
    print("INTERVIEW STRATEGY")
    print("=" * 60)
    
    print("""
1. PROBLEM RECOGNITION:
   - Interval DP pattern: solving on ranges [i,j]
   - Optimization problem with overlapping subproblems
   - "Covering" strategy suggests thinking about ranges

2. APPROACH PROGRESSION:
   - Start with brute force: print each character separately
   - Identify optimization: same characters can be printed together
   - Formalize with DP: define state and transitions

3. KEY POINTS TO MENTION:
   - Preprocessing optimization (remove consecutive duplicates)
   - State definition: dp[i][j] = min operations for range [i,j]
   - Two strategies: separate vs. merged printing
   - Why we check s[i] == s[k]: can print both positions in one operation

4. EDGE CASES:
   - Empty string → 0
   - Single character → 1  
   - All same characters → 1
   - All different characters → n

5. FOLLOW-UP QUESTIONS:
   - What if we could print backwards?
   - What if we had multiple printers?
   - How to find the actual sequence of operations?
    """)

if __name__ == "__main__":
    test_solutions()
    explain_algorithm()
    interview_tips()
