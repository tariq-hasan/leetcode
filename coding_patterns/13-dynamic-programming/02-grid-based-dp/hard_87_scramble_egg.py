# LeetCode 87: Scramble String
# 
# Problem: Given two strings s1 and s2 of the same length, return true if s2 is a scrambled string of s1.
# A string is scrambled by recursively splitting it into non-empty parts and swapping them.

class Solution:
    def isScramble(self, s1: str, s2: str) -> bool:
        """
        Solution 1: Recursive with Memoization (Top-Down DP)
        Time: O(n^4), Space: O(n^3)
        """
        if len(s1) != len(s2):
            return False
        
        memo = {}
        
        def dfs(s1, s2):
            # Base cases
            if s1 == s2:
                return True
            if len(s1) <= 1:
                return s1 == s2
            
            # Check memoization
            key = (s1, s2)
            if key in memo:
                return memo[key]
            
            # Early pruning: check if characters match
            if sorted(s1) != sorted(s2):
                memo[key] = False
                return False
            
            n = len(s1)
            # Try all possible split points
            for i in range(1, n):
                # Case 1: No swap - s1[:i] matches s2[:i] and s1[i:] matches s2[i:]
                if dfs(s1[:i], s2[:i]) and dfs(s1[i:], s2[i:]):
                    memo[key] = True
                    return True
                
                # Case 2: With swap - s1[:i] matches s2[n-i:] and s1[i:] matches s2[:n-i]
                if dfs(s1[:i], s2[n-i:]) and dfs(s1[i:], s2[:n-i]):
                    memo[key] = True
                    return True
            
            memo[key] = False
            return False
        
        return dfs(s1, s2)

class SolutionDP:
    def isScramble(self, s1: str, s2: str) -> bool:
        """
        Solution 2: 3D Dynamic Programming (Bottom-Up)
        Time: O(n^4), Space: O(n^3)
        More optimized for interview coding
        """
        if len(s1) != len(s2):
            return False
        if s1 == s2:
            return True
        
        n = len(s1)
        # dp[i][j][k] = True if s1[i:i+k] can be scrambled to s2[j:j+k]
        dp = [[[False] * (n + 1) for _ in range(n)] for _ in range(n)]
        
        # Base case: single characters
        for i in range(n):
            for j in range(n):
                dp[i][j][1] = (s1[i] == s2[j])
        
        # Fill for lengths 2 to n
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                for j in range(n - length + 1):
                    # Try all possible split points
                    for k in range(1, length):
                        # Case 1: No swap
                        if dp[i][j][k] and dp[i + k][j + k][length - k]:
                            dp[i][j][length] = True
                            break
                        
                        # Case 2: With swap
                        if dp[i][j + length - k][k] and dp[i + k][j][length - k]:
                            dp[i][j][length] = True
                            break
        
        return dp[0][0][n]

class SolutionOptimized:
    def isScramble(self, s1: str, s2: str) -> bool:
        """
        Solution 3: Optimized Recursive with Character Count Pruning
        Time: O(n^4), Space: O(n^3)
        Best for interviews - clean and efficient
        """
        if len(s1) != len(s2):
            return False
        
        memo = {}
        
        def canScramble(i1, i2, length):
            # Base case
            if length == 1:
                return s1[i1] == s2[i2]
            
            # Check memo
            key = (i1, i2, length)
            if key in memo:
                return memo[key]
            
            # Character count pruning
            if sorted(s1[i1:i1+length]) != sorted(s2[i2:i2+length]):
                memo[key] = False
                return False
            
            # Try all split points
            for k in range(1, length):
                # No swap: left with left, right with right
                if (canScramble(i1, i2, k) and 
                    canScramble(i1 + k, i2 + k, length - k)):
                    memo[key] = True
                    return True
                
                # Swap: left with right, right with left
                if (canScramble(i1, i2 + length - k, k) and 
                    canScramble(i1 + k, i2, length - k)):
                    memo[key] = True
                    return True
            
            memo[key] = False
            return False
        
        return canScramble(0, 0, len(s1))

# Test cases
def test_solutions():
    solutions = [Solution(), SolutionDP(), SolutionOptimized()]
    
    test_cases = [
        ("great", "rgeat", True),   # Example 1
        ("abcde", "caebd", False), # Example 2
        ("a", "a", True),          # Single character
        ("abc", "acb", True),      # Simple swap
        ("hwareg", "grhwae", True) # Complex case
    ]
    
    for i, sol in enumerate(solutions, 1):
        print(f"Solution {i} Results:")
        for s1, s2, expected in test_cases:
            result = sol.isScramble(s1, s2)
            status = "✓" if result == expected else "✗"
            print(f"  {status} isScramble('{s1}', '{s2}') = {result}")
        print()

if __name__ == "__main__":
    test_solutions()

# Interview Tips:
# 1. Start with the recursive approach - it's more intuitive
# 2. Explain the two cases: swap and no-swap at each split
# 3. Mention memoization to avoid recalculating subproblems
# 4. Character count pruning is a good optimization to mention
# 5. Time complexity: O(n^4), Space: O(n^3) for all approaches
