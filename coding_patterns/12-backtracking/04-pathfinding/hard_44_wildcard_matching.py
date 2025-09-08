"""
LeetCode 44: Wildcard Matching
Hard Difficulty

Problem:
Given an input string (s) and a pattern (p), implement wildcard pattern matching 
with support for '?' and '*'.

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).

Examples:
s = "aa", p = "a" -> false (entire string not covered)
s = "aa", p = "*" -> true ('*' matches "aa")
s = "cb", p = "?a" -> false ('?' matches 'c', but 'b' != 'a')
s = "adceb", p = "*a*b*" -> true (first '*' matches "ad", second '*' matches "ce")

Time Complexity: O(S * P) where S = len(s), P = len(p)
Space Complexity: O(S * P) for 2D DP, O(P) for optimized version
"""

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Optimal Dynamic Programming approach with 2D table
        
        dp[i][j] = True if s[0:i] matches p[0:j]
        
        Recurrence relation:
        - If p[j-1] == '*': dp[i][j] = dp[i-1][j] OR dp[i][j-1]
          - dp[i-1][j]: '*' matches current character in s
          - dp[i][j-1]: '*' matches empty sequence
        - If p[j-1] == '?' or s[i-1] == p[j-1]: dp[i][j] = dp[i-1][j-1]
        - Else: dp[i][j] = False
        """
        m, n = len(s), len(p)
        
        # dp[i][j] represents if s[0:i] matches p[0:j]
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        
        # Base case: empty string matches empty pattern
        dp[0][0] = True
        
        # Handle patterns like "***" that can match empty string
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 1]
        
        # Fill the DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '*':
                    # '*' can match empty sequence OR any character
                    dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
                elif p[j - 1] == '?' or s[i - 1] == p[j - 1]:
                    # Exact match or wildcard '?'
                    dp[i][j] = dp[i - 1][j - 1]
                # else: dp[i][j] = False (already initialized)
        
        return dp[m][n]


class SpaceOptimizedSolution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Space-optimized DP using only O(P) space
        
        Since each dp[i][j] only depends on dp[i-1][j-1], dp[i-1][j], and dp[i][j-1],
        we can use just two rows instead of the full 2D table.
        """
        m, n = len(s), len(p)
        
        # Use two arrays to represent current and previous rows
        prev = [False] * (n + 1)
        curr = [False] * (n + 1)
        
        # Base case
        prev[0] = True
        
        # Handle patterns like "***"
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                prev[j] = prev[j - 1]
        
        # Process each character in string
        for i in range(1, m + 1):
            curr[0] = False  # Non-empty string can't match empty pattern
            
            for j in range(1, n + 1):
                if p[j - 1] == '*':
                    curr[j] = curr[j - 1] or prev[j]
                elif p[j - 1] == '?' or s[i - 1] == p[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = False
            
            # Swap arrays for next iteration
            prev, curr = curr, prev
        
        return prev[n]


class RecursiveSolution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Recursive approach with memoization
        Good for understanding the problem structure
        """
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def dp(i, j):
            # Base cases
            if j == len(p):
                return i == len(s)
            
            if i == len(s):
                # Check if remaining pattern consists only of '*'
                return all(c == '*' for c in p[j:])
            
            # Current characters
            if p[j] == '*':
                # '*' can match empty sequence OR any character
                return dp(i, j + 1) or dp(i + 1, j)
            elif p[j] == '?' or s[i] == p[j]:
                # Exact match or wildcard match
                return dp(i + 1, j + 1)
            else:
                # No match possible
                return False
        
        return dp(0, 0)


class GreedyOptimizedSolution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Greedy approach with backtracking
        Most space-efficient solution - O(1) space
        
        Key insight: When we see '*', we try to match as few characters as possible
        initially, and backtrack if needed.
        """
        s_idx = p_idx = 0
        star_idx = s_match = -1
        
        while s_idx < len(s):
            # Characters match
            if p_idx < len(p) and (p[p_idx] == '?' or s[s_idx] == p[p_idx]):
                s_idx += 1
                p_idx += 1
            # Found '*' in pattern
            elif p_idx < len(p) and p[p_idx] == '*':
                star_idx = p_idx  # Remember position of '*'
                s_match = s_idx   # Remember position in string
                p_idx += 1
            # No match, but we have seen '*' before
            elif star_idx != -1:
                p_idx = star_idx + 1  # Go back to after '*'
                s_match += 1          # Try matching one more character with '*'
                s_idx = s_match
            # No match and no '*' to backtrack
            else:
                return False
        
        # Skip any remaining '*' in pattern
        while p_idx < len(p) and p[p_idx] == '*':
            p_idx += 1
        
        return p_idx == len(p)


class PatternPreprocessingSolution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Solution with pattern preprocessing to handle consecutive '*'
        Optimization: multiple consecutive '*' are equivalent to single '*'
        """
        # Preprocess pattern to remove consecutive '*'
        if not p:
            return not s
        
        # Remove consecutive stars
        processed_pattern = []
        for char in p:
            if char == '*' and processed_pattern and processed_pattern[-1] == '*':
                continue
            processed_pattern.append(char)
        
        p = ''.join(processed_pattern)
        m, n = len(s), len(p)
        
        # Use standard DP approach on preprocessed pattern
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        
        # Handle leading stars
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 1]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '*':
                    dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
                elif p[j - 1] == '?' or s[i - 1] == p[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
        
        return dp[m][n]


class DetailedTracingSolution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Solution with detailed tracing for interview explanation
        """
        m, n = len(s), len(p)
        print(f"Matching string: '{s}' with pattern: '{p}'")
        
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        
        # Initialize first row
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 1]
        
        # Fill DP table with tracing
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '*':
                    dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
                    print(f"dp[{i}][{j}]: '*' at pattern[{j-1}] -> {dp[i][j]}")
                elif p[j - 1] == '?' or s[i - 1] == p[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                    print(f"dp[{i}][{j}]: Match '{s[i-1]}' with '{p[j-1]}' -> {dp[i][j]}")
                else:
                    print(f"dp[{i}][{j}]: No match '{s[i-1]}' with '{p[j-1]}' -> False")
        
        self._print_dp_table(dp, s, p)
        return dp[m][n]
    
    def _print_dp_table(self, dp, s, p):
        print("\nDP Table:")
        print("    ", end="")
        print("ε".rjust(3), end="")
        for char in p:
            print(char.rjust(3), end="")
        print()
        
        for i in range(len(dp)):
            if i == 0:
                print("ε".rjust(3), end=" ")
            else:
                print(s[i-1].rjust(3), end=" ")
            
            for j in range(len(dp[0])):
                print("T" if dp[i][j] else "F", end="  ")
            print()


def test_solutions():
    """Test all solutions with comprehensive test cases"""
    test_cases = [
        ("aa", "a", False),
        ("aa", "*", True),
        ("cb", "?a", False),
        ("adceb", "*a*b*", True),
        ("acdcb", "a*c?b", False),
        ("", "*", True),
        ("", "", True),
        ("a", "", False),
        ("mississippi", "m??*ss*?i*pi", False),
        ("abcabczzzde", "*abc???de*", True),
        ("aaaa", "***a", True),
        ("", "?", False)
    ]
    
    solutions = [
        ("2D DP", Solution()),
        ("Space Optimized", SpaceOptimizedSolution()),
        ("Recursive + Memo", RecursiveSolution()),
        ("Greedy", GreedyOptimizedSolution()),
        ("Preprocessed", PatternPreprocessingSolution())
    ]
    
    print("Wildcard Matching Test Results:")
    print("-" * 60)
    
    all_correct = True
    for s, p, expected in test_cases:
        print(f"s='{s}', p='{p}' -> Expected: {expected}")
        
        for name, sol in solutions:
            try:
                result = sol.isMatch(s, p)
                status = "✓" if result == expected else "✗"
                if result != expected:
                    all_correct = False
                print(f"  {name:20}: {result} {status}")
            except Exception as e:
                print(f"  {name:20}: ERROR - {e}")
                all_correct = False
        print()
    
    print(f"All tests passed: {all_correct}")


def trace_detailed_example():
    """Trace through a complex example"""
    print("Detailed trace for: s='adceb', p='*a*b*'")
    print("=" * 50)
    
    sol = DetailedTracingSolution()
    result = sol.isMatch("adceb", "*a*b*")
    print(f"\nFinal result: {result}")


def performance_analysis():
    """Analyze performance of different approaches"""
    import time
    
    # Test with larger inputs
    long_string = "a" * 1000 + "b" * 1000 + "c" * 1000
    long_pattern = "*" + "a" * 500 + "*" + "b" * 500 + "*" + "c" * 500 + "*"
    
    solutions = [
        ("2D DP", Solution()),
        ("Space Optimized", SpaceOptimizedSolution()),
        ("Greedy", GreedyOptimizedSolution())
    ]
    
    print("Performance Analysis (large input):")
    print("-" * 40)
    
    for name, sol in solutions:
        start_time = time.time()
        result = sol.isMatch(long_string, long_pattern)
        end_time = time.time()
        
        print(f"{name:20}: {end_time - start_time:.6f}s -> {result}")


"""
Interview Strategy and Key Points:

1. **Problem Recognition**:
   "This is a classic dynamic programming problem similar to regex matching.
   Key insight: we need to handle '*' which can match any sequence of characters."

2. **Approach Progression**:
   - Recursive solution with memoization (understanding)
   - 2D DP bottom-up (standard approach)
   - Space-optimized DP (optimization)
   - Greedy approach (advanced optimization)

3. **DP State Definition**:
   "dp[i][j] = True if s[0:i] matches p[0:j]"
   
4. **Recurrence Relation**:
   - If p[j-1] == '*': dp[i][j] = dp[i-1][j] OR dp[i][j-1]
   - If p[j-1] == '?' or s[i-1] == p[j-1]: dp[i][j] = dp[i-1][j-1]
   - Else: dp[i][j] = False

5. **Key Insights**:
   - '*' can match empty sequence (dp[i][j-1]) OR any character (dp[i-1][j])
   - Base cases: empty string matches empty pattern and patterns with only '*'
   - Order of operations matters in DP

6. **Complexity Analysis**:
   - Time: O(S * P) for DP approaches, O(S + P) average for greedy
   - Space: O(S * P) for 2D DP, O(P) for space-optimized, O(1) for greedy

7. **Optimizations**:
   - Space optimization: use only two rows instead of full 2D table
   - Pattern preprocessing: remove consecutive '*'
   - Greedy approach: O(1) space with backtracking

8. **Edge Cases**:
   - Empty string and empty pattern
   - Pattern with only '*'
   - String longer than pattern without '*'
   - No wildcard characters

9. **Common Pitfalls**:
   - Forgetting to handle consecutive '*' properly
   - Incorrect base case initialization
   - Off-by-one errors in indexing

10. **Follow-up Questions**:
    - "Can you optimize space?" -> Show space-optimized version
    - "What about time complexity?" -> Discuss greedy approach
    - "How is this different from regex matching?" -> Compare with problem 10
"""

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*60 + "\n")
    trace_detailed_example()
    print("\n" + "="*60 + "\n")
    performance_analysis()
