"""
LeetCode 63: Unique Paths II

Problem Statement:
You are given an m x n integer array grid. There is a robot initially located at 
the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right 
corner (i.e., grid[m-1][n-1]). The robot can only move either down or right at any 
point in time.

An obstacle and space are marked as 1 and 0 respectively in grid. A path that the 
robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the 
bottom-right corner.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 100
- grid[i][j] is 0 or 1

Examples:
Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
Output: 2
Explanation: There is one obstacle in the middle of the 3x3 grid above.
There are two ways to reach the bottom-right corner:
1. Right -> Right -> Down -> Down
2. Down -> Down -> Right -> Right

Input: obstacleGrid = [[0,1],[0,0]]
Output: 1

Input: obstacleGrid = [[1]]
Output: 0

Input: obstacleGrid = [[0]]
Output: 1
"""

from typing import List

class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        """
        Solution 1: 2D Dynamic Programming (Most Intuitive)
        
        Key Insight: Similar to Unique Paths I, but obstacles block paths.
        dp[i][j] = number of unique paths to reach cell (i,j)
        
        Recurrence relation:
        - If obstacleGrid[i][j] == 1: dp[i][j] = 0 (blocked)
        - Else: dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        
        This is the most straightforward approach for interviews.
        """
        if not obstacleGrid or not obstacleGrid[0] or obstacleGrid[0][0] == 1:
            return 0
        
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        # Create DP table
        dp = [[0] * n for _ in range(m)]
        
        # Initialize starting point
        dp[0][0] = 1
        
        # Initialize first column
        for i in range(1, m):
            if obstacleGrid[i][0] == 0:
                dp[i][0] = dp[i-1][0]  # Copy from above if no obstacle
            else:
                dp[i][0] = 0  # Obstacle blocks all paths below
        
        # Initialize first row
        for j in range(1, n):
            if obstacleGrid[0][j] == 0:
                dp[0][j] = dp[0][j-1]  # Copy from left if no obstacle
            else:
                dp[0][j] = 0  # Obstacle blocks all paths to the right
        
        # Fill the DP table
        for i in range(1, m):
            for j in range(1, n):
                if obstacleGrid[i][j] == 0:  # No obstacle
                    dp[i][j] = dp[i-1][j] + dp[i][j-1]
                else:  # Obstacle present
                    dp[i][j] = 0
        
        return dp[m-1][n-1]

    def uniquePathsWithObstacles_optimized(self, obstacleGrid: List[List[int]]) -> int:
        """
        Solution 2: Space-Optimized DP (1D Array)
        
        Key Insight: Only need previous row values to compute current row.
        Use single array and update in-place.
        
        Time Complexity: O(m * n)
        Space Complexity: O(n)
        
        Great optimization to show after the 2D approach.
        """
        if not obstacleGrid or not obstacleGrid[0] or obstacleGrid[0][0] == 1:
            return 0
        
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        # dp[j] represents number of paths to reach column j in current row
        dp = [0] * n
        dp[0] = 1  # Starting point
        
        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0  # Obstacle blocks all paths
                elif j > 0:
                    dp[j] += dp[j-1]  # Add paths from left
        
        return dp[n-1]

    def uniquePathsWithObstacles_in_place(self, obstacleGrid: List[List[int]]) -> int:
        """
        Solution 3: In-Place DP (Modify Input Grid)
        
        Key Insight: Use the input grid itself as DP table.
        Modify obstacles (1) to 0 and paths to their path count.
        
        Time Complexity: O(m * n)
        Space Complexity: O(1)
        
        Most space-efficient but modifies input (ask interviewer first).
        """
        if not obstacleGrid or not obstacleGrid[0] or obstacleGrid[0][0] == 1:
            return 0
        
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        # Convert obstacles to 0 and set starting point
        obstacleGrid[0][0] = 1
        
        # Process first row
        for j in range(1, n):
            if obstacleGrid[0][j] == 0:
                obstacleGrid[0][j] = obstacleGrid[0][j-1]
            else:
                obstacleGrid[0][j] = 0
        
        # Process first column
        for i in range(1, m):
            if obstacleGrid[i][0] == 0:
                obstacleGrid[i][0] = obstacleGrid[i-1][0]
            else:
                obstacleGrid[i][0] = 0
        
        # Fill the rest of the grid
        for i in range(1, m):
            for j in range(1, n):
                if obstacleGrid[i][j] == 0:
                    obstacleGrid[i][j] = obstacleGrid[i-1][j] + obstacleGrid[i][j-1]
                else:
                    obstacleGrid[i][j] = 0
        
        return obstacleGrid[m-1][n-1]

    def uniquePathsWithObstacles_recursive_memo(self, obstacleGrid: List[List[int]]) -> int:
        """
        Solution 4: Recursive with Memoization (Top-Down DP)
        
        Good to show understanding of recursion → DP transition.
        Less efficient than bottom-up but demonstrates recursive thinking.
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        if not obstacleGrid or not obstacleGrid[0] or obstacleGrid[0][0] == 1:
            return 0
        
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        memo = {}
        
        def dfs(i: int, j: int) -> int:
            # Base cases
            if i >= m or j >= n or obstacleGrid[i][j] == 1:
                return 0
            
            if i == m-1 and j == n-1:
                return 1
            
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Recursive case: go right or go down
            memo[(i, j)] = dfs(i+1, j) + dfs(i, j+1)
            return memo[(i, j)]
        
        return dfs(0, 0)

    def uniquePathsWithObstacles_cleaner(self, obstacleGrid: List[List[int]]) -> int:
        """
        Solution 5: Cleaner 2D DP Implementation
        
        Alternative implementation with cleaner initialization logic.
        Shows different ways to handle base cases.
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        # Create DP table
        dp = [[0] * n for _ in range(m)]
        
        # Initialize first cell if not blocked
        if obstacleGrid[0][0] == 0:
            dp[0][0] = 1
        
        # Fill entire DP table in one go
        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0  # Obstacle
                elif i == 0 and j == 0:
                    continue  # Already initialized
                else:
                    # Add paths from above
                    if i > 0:
                        dp[i][j] += dp[i-1][j]
                    # Add paths from left
                    if j > 0:
                        dp[i][j] += dp[i][j-1]
        
        return dp[m-1][n-1]


# Test cases for verification
def test_solutions():
    solution = Solution()
    
    test_cases = [
        # Test case 1: Basic obstacle in middle
        ([[0,0,0],[0,1,0],[0,0,0]], 2),
        
        # Test case 2: Obstacle in top row
        ([[0,1],[0,0]], 1),
        
        # Test case 3: Starting point blocked
        ([[1]], 0),
        
        # Test case 4: Single cell, no obstacle
        ([[0]], 1),
        
        # Test case 5: All obstacles except start and end
        ([[0,0],[1,0]], 1),
        
        # Test case 6: Path completely blocked
        ([[0,1],[1,0]], 0),
        
        # Test case 7: No obstacles (like original Unique Paths)
        ([[0,0,0],[0,0,0],[0,0,0]], 6),
        
        # Test case 8: Complex case
        ([[0,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,1,0],[0,0,0,0]], 7)
    ]
    
    methods = [
        ("2D DP", solution.uniquePathsWithObstacles),
        ("Optimized DP", solution.uniquePathsWithObstacles_optimized),
        ("Memoized", solution.uniquePathsWithObstacles_recursive_memo),
        ("Cleaner DP", solution.uniquePathsWithObstacles_cleaner)
    ]
    
    for i, (grid, expected) in enumerate(test_cases, 1):
        print(f"\nTest case {i}: Grid = {grid}, Expected = {expected}")
        for method_name, method in methods:
            # Create a copy for methods that might modify input
            grid_copy = [row[:] for row in grid]
            result = method(grid_copy)
            status = "PASS" if result == expected else "FAIL"
            print(f"  {method_name}: {result} ({status})")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW DISCUSSION POINTS:

1. Problem Recognition:
   - Extension of Unique Paths I with obstacles
   - Still a 2D grid traversal problem with DP
   - Key difference: obstacles (1) block paths, empty spaces (0) allow movement
   - Cannot pass through or count paths through obstacles

2. Approach Evolution (Show this progression):
   
   a) Understand Base Problem:
      - Same as Unique Paths I: only right/down movement
      - dp[i][j] = number of paths to reach cell (i,j)
   
   b) Handle Obstacles:
      - If cell has obstacle: dp[i][j] = 0 (no paths through obstacles)
      - If cell is empty: dp[i][j] = dp[i-1][j] + dp[i][j-1]
   
   c) Base Cases with Obstacles:
      - First row: paths blocked after first obstacle
      - First column: paths blocked after first obstacle
      - Starting point: if blocked, return 0 immediately

3. Key DP Insights:
   - State definition: dp[i][j] = number of paths to reach (i,j) avoiding obstacles
   - Base cases: Handle first row/column carefully with obstacles
   - Recurrence: Same as Unique Paths I, but with obstacle check
   - Obstacles act as "path blockers" - set dp value to 0

4. Critical Edge Cases:
   - Starting point (0,0) is blocked → return 0
   - Destination is blocked → return 0
   - Path completely blocked by obstacles → return 0
   - No obstacles → same as original Unique Paths problem
   - Single cell with/without obstacle

5. Implementation Variations:
   
   a) 2D DP Array (Most Intuitive):
      - Separate DP table, clear logic
      - Easy to understand and debug
   
   b) Space-Optimized (1D Array):
      - Only need previous row for current row
      - O(n) space instead of O(m*n)
   
   c) In-Place Modification:
      - Use input grid as DP table
      - O(1) extra space but modifies input
   
   d) Recursive + Memoization:
      - Top-down approach
      - Good for showing recursion understanding

6. Obstacle Handling Strategy:
   - Check for obstacle BEFORE computing paths
   - Obstacles propagate blocking effect in first row/column
   - Obstacles in middle only affect that specific cell

7. Follow-up Questions You Might Get:
   - "What if robot can move in all 4 directions?" → Different problem (shortest path)
   - "What if obstacles can be removed?" → State becomes (i,j,obstacles_removed)
   - "What if we want the actual paths?" → Backtracking needed
   - "What about minimum cost path?" → Different DP state (cost instead of count)

8. Interview Strategy:
   - Start by comparing to Unique Paths I
   - Identify key difference: obstacles block paths
   - Implement 2D DP first (most clear)
   - Optimize space if time permits
   - Test with edge cases, especially obstacle at start/end

9. Common Mistakes to Avoid:
   - Not checking if starting point is blocked
   - Incorrect handling of first row/column with obstacles
   - Forgetting that obstacles completely block paths (set to 0)
   - Index out of bounds when checking neighbors
   - Not handling empty grid or single cell cases

10. Complexity Analysis:
    - Time: O(m * n) - visit each cell once
    - Space: O(m * n) for 2D DP, O(n) for optimized, O(1) for in-place
    - Same time complexity as Unique Paths I, but with obstacle checks

11. Testing Strategy:
    - Normal cases with obstacles in middle
    - Edge cases: start/end blocked, path completely blocked
    - Compare with Unique Paths I (when no obstacles)
    - Single row/column with obstacles
"""
