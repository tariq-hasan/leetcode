"""
LeetCode 2328: Number of Increasing Paths in a Grid

Problem: Given an m x n integer matrix grid, return the number of strictly 
increasing paths in the grid. A path can start from any cell and end at any cell.

Time Complexity: O(m * n)
Space Complexity: O(m * n)
"""

class Solution:
    def countPaths(self, grid: list[list[int]]) -> int:
        """
        Main solution using DFS with memoization.
        
        Key insights:
        1. For each cell, we can move to 4 adjacent cells if the value is strictly greater
        2. Use DFS with memoization to avoid recalculating paths from the same cell
        3. Each cell contributes at least 1 path (itself)
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        MOD = 10**9 + 7
        
        # Memoization table: memo[i][j] = number of paths starting from cell (i,j)
        memo = {}
        
        def dfs(i: int, j: int) -> int:
            """DFS to count paths starting from cell (i, j)"""
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Base case: single cell path
            paths = 1
            
            # Explore all 4 directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            
            for di, dj in directions:
                ni, nj = i + di, j + dj
                
                # Check bounds and increasing condition
                if (0 <= ni < m and 0 <= nj < n and 
                    grid[ni][nj] > grid[i][j]):
                    paths = (paths + dfs(ni, nj)) % MOD
            
            memo[(i, j)] = paths
            return paths
        
        # Count paths starting from each cell
        total_paths = 0
        for i in range(m):
            for j in range(n):
                total_paths = (total_paths + dfs(i, j)) % MOD
        
        return total_paths


class SolutionIterative:
    def countPaths(self, grid: list[list[int]]) -> int:
        """
        Alternative iterative solution using topological sort approach.
        
        This approach processes cells in order of their values, which ensures
        that when we process a cell, all cells with smaller values have been processed.
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        MOD = 10**9 + 7
        
        # Create list of all cells with their values
        cells = []
        for i in range(m):
            for j in range(n):
                cells.append((grid[i][j], i, j))
        
        # Sort by value (ascending order)
        cells.sort()
        
        # DP table: dp[i][j] = number of paths starting from cell (i,j)
        dp = [[1] * n for _ in range(m)]
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Process cells in order of increasing value
        for val, i, j in cells:
            for di, dj in directions:
                ni, nj = i + di, j + dj
                
                # If neighbor has larger value, add current cell's paths to neighbor
                if (0 <= ni < m and 0 <= nj < n and 
                    grid[ni][nj] > grid[i][j]):
                    dp[ni][nj] = (dp[ni][nj] + dp[i][j]) % MOD
        
        # Sum all paths
        total_paths = 0
        for i in range(m):
            for j in range(n):
                total_paths = (total_paths + dp[i][j]) % MOD
        
        return total_paths


def test_solutions():
    """Test cases for validation"""
    
    # Test case 1
    grid1 = [[1, 1], [3, 4]]
    # Expected: 8
    # Paths: [1], [1], [3], [4], [1,3], [1,4], [3,4], [1,3,4]
    
    # Test case 2  
    grid2 = [[1], [2]]
    # Expected: 3
    # Paths: [1], [2], [1,2]
    
    sol1 = Solution()
    sol2 = SolutionIterative()
    
    print("Test Case 1:")
    print(f"DFS Solution: {sol1.countPaths(grid1)}")
    print(f"Iterative Solution: {sol2.countPaths(grid1)}")
    
    print("\nTest Case 2:")
    print(f"DFS Solution: {sol1.countPaths(grid2)}")
    print(f"Iterative Solution: {sol2.countPaths(grid2)}")


# Interview talking points:
"""
Key Interview Discussion Points:

1. Problem Understanding:
   - We need to count ALL strictly increasing paths, not just longest ones
   - A path can start and end at any cell
   - Each single cell counts as a path of length 1

2. Approach Analysis:
   - DFS with memoization: Natural recursive thinking
   - Topological sort: More optimal for understanding dependencies
   - Both have same time/space complexity but different perspectives

3. Edge Cases:
   - Empty grid
   - Single cell grid  
   - All cells have same value (answer = m*n)
   - Grid with decreasing values only

4. Optimization Considerations:
   - Memoization prevents recalculation
   - MOD operation for large results
   - Space optimization possible but not necessary given constraints

5. Follow-up Questions:
   - What if we want longest path instead of count?
   - What if diagonal moves are allowed?
   - Memory optimization for very large grids?
"""

if __name__ == "__main__":
    test_solutions()
