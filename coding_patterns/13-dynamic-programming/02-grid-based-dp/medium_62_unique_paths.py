"""
LeetCode 62: Unique Paths

Problem Statement:
There is a robot on an m x n grid. The robot is initially located at the top-left 
corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner 
(i.e., grid[m-1][n-1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that 
the robot can take to reach the bottom-right corner.

Constraints:
- 1 <= m, n <= 100

Examples:
Input: m = 3, n = 7
Output: 28

Input: m = 3, n = 2
Output: 3
Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Right -> Down  
3. Down -> Down -> Right

Input: m = 1, n = 1
Output: 1
"""

from typing import List
import math

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Solution 1: 2D Dynamic Programming (Most Intuitive)
        
        Key Insight: dp[i][j] represents number of unique paths to reach cell (i,j)
        from the starting position (0,0).
        
        Recurrence relation: dp[i][j] = dp[i-1][j] + dp[i][j-1]
        - Can reach (i,j) from above (i-1,j) or from left (i,j-1)
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        
        This is the most straightforward approach for interviews.
        """
        # Create DP table
        dp = [[0] * n for _ in range(m)]
        
        # Initialize base cases
        # First row: only one way (all right moves)
        for j in range(n):
            dp[0][j] = 1
        
        # First column: only one way (all down moves)
        for i in range(m):
            dp[i][0] = 1
        
        # Fill the DP table
        for i in range(1, m):
            for j in range(1, n):
                # Can come from above or from left
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        return dp[m-1][n-1]

    def uniquePaths_optimized_space(self, m: int, n: int) -> int:
        """
        Solution 2: 1D Dynamic Programming (Space Optimized)
        
        Key Insight: We only need the previous row to calculate current row.
        Use a 1D array and update it in-place.
        
        Time Complexity: O(m * n)
        Space Complexity: O(n)
        
        Great optimization to show in interviews after the 2D approach.
        """
        # Use smaller dimension for space optimization
        if m > n:
            m, n = n, m
        
        # dp[j] represents number of paths to reach column j in current row
        dp = [1] * n
        
        # Process each row (starting from row 1)
        for i in range(1, m):
            for j in range(1, n):
                # dp[j] = dp[j] (from above) + dp[j-1] (from left)
                dp[j] += dp[j-1]
        
        return dp[n-1]

    def uniquePaths_combinatorics(self, m: int, n: int) -> int:
        """
        Solution 3: Combinatorics (Mathematical)
        
        Key Insight: To reach (m-1, n-1) from (0, 0):
        - Need exactly (m-1) down moves and (n-1) right moves
        - Total moves = (m-1) + (n-1) = m + n - 2
        - Choose (m-1) positions for down moves from total positions
        - Answer = C(m+n-2, m-1) = (m+n-2)! / ((m-1)! * (n-1)!)
        
        Time Complexity: O(min(m, n))
        Space Complexity: O(1)
        
        Most efficient but requires combinatorics knowledge.
        """
        # Total moves needed
        total_moves = m + n - 2
        
        # Choose the smaller of (m-1) or (n-1) for efficiency
        choose = min(m - 1, n - 1)
        
        # Calculate C(total_moves, choose) = total_moves! / (choose! * (total_moves-choose)!)
        # Use the formula: C(n,k) = n*(n-1)*...*(n-k+1) / k!
        result = 1
        for i in range(choose):
            result = result * (total_moves - i) // (i + 1)
        
        return result

    def uniquePaths_recursive_memoized(self, m: int, n: int) -> int:
        """
        Solution 4: Recursive with Memoization (Top-Down DP)
        
        Good to show understanding of recursion and memoization.
        Less efficient than bottom-up but demonstrates the recursive nature.
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        memo = {}
        
        def dfs(i: int, j: int) -> int:
            # Base cases
            if i == 0 or j == 0:
                return 1
            
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Recursive case
            memo[(i, j)] = dfs(i-1, j) + dfs(i, j-1)
            return memo[(i, j)]
        
        return dfs(m-1, n-1)

    def uniquePaths_brute_force(self, m: int, n: int) -> int:
        """
        Solution 5: Brute Force Recursion (For Understanding Only)
        
        Exponential time complexity - NOT for interviews!
        Included only to show the recursive structure of the problem.
        
        Time Complexity: O(2^(m+n))
        Space Complexity: O(m + n) - recursion stack
        """
        def dfs(i: int, j: int) -> int:
            # Base cases
            if i == m-1 and j == n-1:
                return 1
            if i >= m or j >= n:
                return 0
            
            # Recursive case: go right or go down
            return dfs(i+1, j) + dfs(i, j+1)
        
        return dfs(0, 0)

    def uniquePaths_bottom_up_alternative(self, m: int, n: int) -> int:
        """
        Solution 6: Bottom-Up DP (Alternative Implementation)
        
        Another way to think about the DP approach.
        Build from destination back to source.
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        dp = [[1] * n for _ in range(m)]
        
        # Work backwards from bottom-right
        for i in range(m-2, -1, -1):
            for j in range(n-2, -1, -1):
                dp[i][j] = dp[i+1][j] + dp[i][j+1]
        
        return dp[0][0]


# Test cases for verification
def test_solutions():
    solution = Solution()
    
    test_cases = [
        (3, 7, 28),
        (3, 2, 3),
        (1, 1, 1),
        (2, 2, 2),
        (4, 4, 20),
        (1, 10, 1),
        (10, 1, 1)
    ]
    
    methods = [
        ("2D DP", solution.uniquePaths),
        ("1D DP", solution.uniquePaths_optimized_space),
        ("Combinatorics", solution.uniquePaths_combinatorics),
        ("Memoized", solution.uniquePaths_recursive_memoized)
    ]
    
    for m, n, expected in test_cases:
        print(f"\nTest case: m={m}, n={n}, expected={expected}")
        for method_name, method in methods:
            result = method(m, n)
            status = "PASS" if result == expected else "FAIL"
            print(f"  {method_name}: {result} ({status})")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW DISCUSSION POINTS:

1. Problem Recognition:
   - Classic 2D grid traversal problem
   - Only rightward and downward movement allowed
   - Counting paths (not finding shortest path)
   - Perfect candidate for Dynamic Programming

2. Approach Evolution (Show this progression in interview):
   
   a) Brute Force Recursion:
      - Try all possible paths recursively
      - Exponential time complexity O(2^(m+n))
      - Not acceptable for large inputs
   
   b) Memoized Recursion (Top-Down DP):
      - Add memoization to avoid recomputing subproblems
      - Time: O(m*n), Space: O(m*n)
      - Good to show understanding of recursion → DP transition
   
   c) Bottom-Up DP (2D array):
      - Build solution iteratively from base cases
      - Time: O(m*n), Space: O(m*n)
      - Most intuitive and commonly expected
   
   d) Space-Optimized DP (1D array):
      - Only need previous row to compute current row
      - Time: O(m*n), Space: O(min(m,n))
      - Great optimization to demonstrate
   
   e) Mathematical Solution:
      - Recognize as combinatorics problem
      - Time: O(min(m,n)), Space: O(1)
      - Most efficient but requires math insight

3. Key DP Insights:
   - State definition: dp[i][j] = number of paths to reach (i,j)
   - Base cases: dp[0][j] = 1 and dp[i][0] = 1 (edges of grid)
   - Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]
   - Final answer: dp[m-1][n-1]

4. Mathematical Insight:
   - Total moves needed: (m-1) down + (n-1) right = m+n-2 moves
   - Problem reduces to: "Choose (m-1) positions for down moves"
   - Answer = C(m+n-2, m-1) = (m+n-2)! / ((m-1)! * (n-1)!)

5. Edge Cases:
   - 1x1 grid: Only 1 path (stay at start)
   - 1×n or n×1 grid: Only 1 path (straight line)
   - Large values of m, n: Test efficiency

6. Follow-up Questions You Might Get:
   - "What if there are obstacles?" → LeetCode 63 (Unique Paths II)
   - "What if we can move in all 4 directions?" → Different problem entirely
   - "What if we want to find the actual paths, not just count?" → Backtracking
   - "What if movements have different costs?" → Minimum path sum variant

7. Interview Strategy:
   - Start with brute force to show problem understanding
   - Identify overlapping subproblems → suggest DP
   - Implement 2D DP solution first (most straightforward)
   - Optimize space if time permits
   - Mention mathematical solution as bonus

8. Common Mistakes to Avoid:
   - Confusing indices (0-based vs 1-based)
   - Incorrect base case initialization
   - Off-by-one errors in loop boundaries  
   - Not handling edge cases (m=1 or n=1)
   - Forgetting that we can only move right or down

9. Time/Space Trade-offs:
   - 2D DP: Clear and intuitive, O(mn) space
   - 1D DP: More complex but O(min(m,n)) space
   - Combinatorics: Requires math knowledge but O(1) space
"""
