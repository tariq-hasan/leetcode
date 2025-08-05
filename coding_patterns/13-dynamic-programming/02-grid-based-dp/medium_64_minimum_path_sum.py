"""
LeetCode 64: Minimum Path Sum

Problem Statement:
Given a m x n grid filled with non-negative numbers, find a path from top left 
to bottom right, which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 200
- 0 <= grid[i][j] <= 200

Examples:
Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
Output: 7
Explanation: Path 1 -> 3 -> 1 -> 1 -> 1 minimizes the sum.

Input: grid = [[1,2,3],[4,5,6]]
Output: 12
Explanation: Path 1 -> 2 -> 3 -> 6 minimizes the sum.

Input: grid = [[1]]
Output: 1
"""

from typing import List

class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        """
        Solution 1: 2D Dynamic Programming (Most Intuitive)
        
        Key Insight: dp[i][j] represents minimum path sum to reach cell (i,j)
        from the starting position (0,0).
        
        Recurrence relation: dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
        - To reach (i,j), we can come from above (i-1,j) or from left (i,j-1)
        - Choose the path with minimum sum and add current cell value
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        
        This is the most straightforward approach for interviews.
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        
        # Create DP table
        dp = [[0] * n for _ in range(m)]
        
        # Initialize starting point
        dp[0][0] = grid[0][0]
        
        # Initialize first column (can only come from above)
        for i in range(1, m):
            dp[i][0] = dp[i-1][0] + grid[i][0]
        
        # Initialize first row (can only come from left)
        for j in range(1, n):
            dp[0][j] = dp[0][j-1] + grid[0][j]
        
        # Fill the DP table
        for i in range(1, m):
            for j in range(1, n):
                # Choose minimum path: from above or from left
                dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
        
        return dp[m-1][n-1]

    def minPathSum_optimized_space(self, grid: List[List[int]]) -> int:
        """
        Solution 2: Space-Optimized DP (1D Array)
        
        Key Insight: We only need the previous row to calculate current row.
        Use a 1D array and update it in-place.
        
        Time Complexity: O(m * n)
        Space Complexity: O(n)
        
        Great optimization to show in interviews after the 2D approach.
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        
        # dp[j] represents minimum sum to reach column j in current row
        dp = [0] * n
        
        # Initialize first row
        dp[0] = grid[0][0]
        for j in range(1, n):
            dp[j] = dp[j-1] + grid[0][j]
        
        # Process each subsequent row
        for i in range(1, m):
            # Update first column (can only come from above)
            dp[0] += grid[i][0]
            
            # Update rest of the row
            for j in range(1, n):
                # dp[j] = from above, dp[j-1] = from left
                dp[j] = grid[i][j] + min(dp[j], dp[j-1])
        
        return dp[n-1]

    def minPathSum_in_place(self, grid: List[List[int]]) -> int:
        """
        Solution 3: In-Place DP (Modify Input Grid)
        
        Key Insight: Use the input grid itself as DP table.
        Modify each cell to store the minimum path sum to reach it.
        
        Time Complexity: O(m * n)
        Space Complexity: O(1)
        
        Most space-efficient but modifies input (ask interviewer first).
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        
        # Initialize first column
        for i in range(1, m):
            grid[i][0] += grid[i-1][0]
        
        # Initialize first row
        for j in range(1, n):
            grid[0][j] += grid[0][j-1]
        
        # Fill the rest of the grid
        for i in range(1, m):
            for j in range(1, n):
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])
        
        return grid[m-1][n-1]

    def minPathSum_recursive_memoized(self, grid: List[List[int]]) -> int:
        """
        Solution 4: Recursive with Memoization (Top-Down DP)
        
        Good to show understanding of recursion and memoization.
        Less efficient than bottom-up but demonstrates the recursive nature.
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        memo = {}
        
        def dfs(i: int, j: int) -> int:
            # Base cases
            if i >= m or j >= n:
                return float('inf')  # Out of bounds
            
            if i == m-1 and j == n-1:
                return grid[i][j]  # Reached destination
            
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Recursive case: go right or go down
            right = dfs(i, j+1)
            down = dfs(i+1, j)
            
            memo[(i, j)] = grid[i][j] + min(right, down)
            return memo[(i, j)]
        
        return dfs(0, 0)

    def minPathSum_dijkstra(self, grid: List[List[int]]) -> int:
        """
        Solution 5: Dijkstra's Algorithm (Over-engineered but Educational)
        
        Treats the problem as shortest path in a weighted graph.
        Overkill for this problem but shows graph algorithm knowledge.
        
        Time Complexity: O(mn * log(mn))
        Space Complexity: O(mn)
        
        NOT recommended for interviews - DP is much better!
        """
        import heapq
        
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        
        # Priority queue: (cost, row, col)
        pq = [(grid[0][0], 0, 0)]
        visited = set()
        
        directions = [(0, 1), (1, 0)]  # right, down
        
        while pq:
            cost, row, col = heapq.heappop(pq)
            
            if (row, col) in visited:
                continue
                
            visited.add((row, col))
            
            # Reached destination
            if row == m-1 and col == n-1:
                return cost
            
            # Explore neighbors
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < m and 0 <= new_col < n and 
                    (new_row, new_col) not in visited):
                    new_cost = cost + grid[new_row][new_col]
                    heapq.heappush(pq, (new_cost, new_row, new_col))
        
        return -1  # Should never reach here

    def minPathSum_brute_force(self, grid: List[List[int]]) -> int:
        """
        Solution 6: Brute Force Recursion (For Understanding Only)
        
        Exponential time complexity - NOT for interviews!
        Included only to show the recursive structure of the problem.
        
        Time Complexity: O(2^(m+n))
        Space Complexity: O(m + n) - recursion stack
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        
        def dfs(i: int, j: int) -> int:
            # Base cases
            if i >= m or j >= n:
                return float('inf')
            
            if i == m-1 and j == n-1:
                return grid[i][j]
            
            # Recursive case: go right or go down
            right = dfs(i, j+1)
            down = dfs(i+1, j)
            
            return grid[i][j] + min(right, down)
        
        return dfs(0, 0)


# Test cases for verification
def test_solutions():
    solution = Solution()
    
    test_cases = [
        # Test case 1: Basic example
        ([[1,3,1],[1,5,1],[4,2,1]], 7),
        
        # Test case 2: Simple 2x3 grid
        ([[1,2,3],[4,5,6]], 12),
        
        # Test case 3: Single cell
        ([[1]], 1),
        
        # Test case 4: Single row
        ([[1,2,3,4]], 10),
        
        # Test case 5: Single column
        ([[1],[2],[3],[4]], 10),
        
        # Test case 6: All zeros
        ([[0,0,0],[0,0,0]], 0),
        
        # Test case 7: Larger grid
        ([[1,2,3,4],[5,6,7,8],[9,10,11,12]], 26),
        
        # Test case 8: Prefer down over right
        ([[5,1,2],[1,1,2],[1,1,2]], 8)
    ]
    
    methods = [
        ("2D DP", solution.minPathSum),
        ("Optimized DP", solution.minPathSum_optimized_space),
        ("Memoized", solution.minPathSum_recursive_memoized)
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
   - Path-finding problem with optimization (minimum sum)
   - 2D grid traversal with movement restrictions (right/down only)
   - Classic Dynamic Programming problem
   - Similar to Unique Paths but optimizing for cost instead of counting paths

2. Approach Evolution (Show this progression):
   
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
      - Time: O(m*n), Space: O(n)
      - Great optimization to demonstrate
   
   e) In-Place DP:
      - Use input grid as DP table
      - Time: O(m*n), Space: O(1)
      - Most space-efficient but modifies input

3. Key DP Insights:
   - State definition: dp[i][j] = minimum path sum to reach (i,j)
   - Base cases: dp[0][0] = grid[0][0], first row/column have single path
   - Recurrence: dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
   - Optimal substructure: optimal path to (i,j) uses optimal paths to neighbors
   - Final answer: dp[m-1][n-1]

4. Comparison with Related Problems:
   - Unique Paths (62): Count paths → dp[i][j] = dp[i-1][j] + dp[i][j-1]
   - Unique Paths II (63): Count paths with obstacles → add obstacle check
   - Minimum Path Sum (64): Minimize cost → dp[i][j] = cost + min(neighbors)
   - All share same movement pattern and DP structure

5. Edge Cases:
   - Single cell grid: return grid[0][0]
   - Single row/column: cumulative sum
   - All zeros: return 0
   - Large values: ensure no integer overflow

6. Follow-up Questions You Might Get:
   - "What if you can move in all 4 directions?" → Use Dijkstra's algorithm
   - "What if there are obstacles?" → Combine with Unique Paths II logic
   - "What if you want the actual path?" → Store parent pointers or backtrack
   - "What if grid is too large for memory?" → Use rolling array or divide-and-conquer
   - "What about maximum path sum?" → Change min to max in recurrence

7. Interview Strategy:
   - Start by connecting to Unique Paths problems
   - Identify key difference: optimization vs counting
   - Implement 2D DP solution first (most intuitive)
   - Optimize space if time permits
   - Discuss time/space trade-offs

8. Time/Space Analysis:
   - Time: O(m * n) - visit each cell once
   - Space: O(m * n) for 2D DP, O(n) for optimized, O(1) for in-place
   - Cannot do better than O(m * n) time since we need to consider all cells

9. Common Mistakes to Avoid:
   - Confusing with shortest path (this is minimum sum, not minimum steps)
   - Incorrect base case initialization
   - Off-by-one errors in loop boundaries
   - Not handling edge cases (empty grid, single cell)
   - Forgetting to add current cell value to minimum of neighbors

10. Alternative Approaches:
    - Dijkstra's Algorithm: Overkill but shows graph knowledge (O(mn log mn))
    - A* Algorithm: Also overkill for this specific problem
    - Recursive backtracking: Exponential time, not practical

11. Pattern Recognition:
    - Grid-based DP with path optimization
    - 2D state space with local decisions
    - Optimal substructure property
    - Bottom-up computation from smaller subproblems
"""
