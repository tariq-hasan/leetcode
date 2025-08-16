"""
LeetCode 1463: Cherry Pickup II

Problem: You have two robots that can collect cherries from a grid. Both robots start 
at the top row (robot1 at (0,0), robot2 at (0,cols-1)) and can only move down.
Each robot can move to one of three positions: down-left, down, or down-right.
Return the maximum number of cherries both robots can collect.

Key Insights:
1. Both robots move simultaneously row by row
2. If both robots are at the same cell, count cherries only once
3. Use 3D DP: dp[row][col1][col2] = max cherries when robot1 is at col1 and robot2 is at col2
4. Each robot has 3 possible moves, so 9 combinations total per step

Time Complexity: O(rows * cols^2)
Space Complexity: O(rows * cols^2) -> can be optimized to O(cols^2)
"""

class Solution:
    def cherryPickup(self, grid: list[list[int]]) -> int:
        """
        Main solution using 3D DP with memoization.
        
        State: (row, col1, col2) where col1 and col2 are positions of robot1 and robot2
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        memo = {}
        
        def dp(row: int, col1: int, col2: int) -> int:
            """
            Returns maximum cherries from current state to bottom
            
            Args:
                row: current row (both robots are always on same row)
                col1: column of robot1
                col2: column of robot2
            """
            # Base case: out of bounds
            if (row >= rows or col1 < 0 or col1 >= cols or 
                col2 < 0 or col2 >= cols):
                return 0
            
            # Memoization check
            if (row, col1, col2) in memo:
                return memo[(row, col1, col2)]
            
            # Collect cherries from current position
            cherries = grid[row][col1]
            if col1 != col2:  # Different positions
                cherries += grid[row][col2]
            
            # Base case: reached last row
            if row == rows - 1:
                memo[(row, col1, col2)] = cherries
                return cherries
            
            # Try all 9 possible combinations of moves (3 for each robot)
            max_future = 0
            moves = [-1, 0, 1]  # left, stay, right relative moves
            
            for move1 in moves:
                for move2 in moves:
                    next_col1 = col1 + move1
                    next_col2 = col2 + move2
                    max_future = max(max_future, 
                                   dp(row + 1, next_col1, next_col2))
            
            result = cherries + max_future
            memo[(row, col1, col2)] = result
            return result
        
        # Start: robot1 at (0,0), robot2 at (0,cols-1)
        return dp(0, 0, cols - 1)


class SolutionBottomUp:
    def cherryPickup(self, grid: list[list[int]]) -> int:
        """
        Bottom-up DP solution for better space complexity understanding.
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        
        # dp[r][c1][c2] = max cherries from row r to bottom with robots at c1, c2
        dp = [[[-1 for _ in range(cols)] for _ in range(cols)] for _ in range(rows)]
        
        # Initialize last row
        for c1 in range(cols):
            for c2 in range(cols):
                if c1 == c2:
                    dp[rows-1][c1][c2] = grid[rows-1][c1]
                else:
                    dp[rows-1][c1][c2] = grid[rows-1][c1] + grid[rows-1][c2]
        
        # Fill DP table from bottom to top
        for row in range(rows - 2, -1, -1):
            for c1 in range(cols):
                for c2 in range(cols):
                    # Current cherries
                    cherries = grid[row][c1]
                    if c1 != c2:
                        cherries += grid[row][c2]
                    
                    # Find maximum from next row
                    max_next = 0
                    moves = [-1, 0, 1]
                    
                    for move1 in moves:
                        for move2 in moves:
                            nc1, nc2 = c1 + move1, c2 + move2
                            if (0 <= nc1 < cols and 0 <= nc2 < cols):
                                max_next = max(max_next, dp[row + 1][nc1][nc2])
                    
                    dp[row][c1][c2] = cherries + max_next
        
        return dp[0][0][cols - 1]


class SolutionSpaceOptimized:
    def cherryPickup(self, grid: list[list[int]]) -> int:
        """
        Space-optimized version using only 2D arrays.
        Space: O(cols^2) instead of O(rows * cols^2)
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        
        # Only need current and next row
        prev = [[-1 for _ in range(cols)] for _ in range(cols)]
        curr = [[-1 for _ in range(cols)] for _ in range(cols)]
        
        # Initialize last row
        for c1 in range(cols):
            for c2 in range(cols):
                if c1 == c2:
                    prev[c1][c2] = grid[rows-1][c1]
                else:
                    prev[c1][c2] = grid[rows-1][c1] + grid[rows-1][c2]
        
        # Process from bottom to top
        for row in range(rows - 2, -1, -1):
            for c1 in range(cols):
                for c2 in range(cols):
                    cherries = grid[row][c1]
                    if c1 != c2:
                        cherries += grid[row][c2]
                    
                    max_next = 0
                    moves = [-1, 0, 1]
                    
                    for move1 in moves:
                        for move2 in moves:
                            nc1, nc2 = c1 + move1, c2 + move2
                            if (0 <= nc1 < cols and 0 <= nc2 < cols):
                                max_next = max(max_next, prev[nc1][nc2])
                    
                    curr[c1][c2] = cherries + max_next
            
            # Swap arrays
            prev, curr = curr, prev
        
        return prev[0][cols - 1]


def test_solutions():
    """Comprehensive test cases"""
    
    # Test case 1
    grid1 = [
        [3,1,1],
        [2,5,1],
        [1,5,5],
        [2,1,1]
    ]
    # Expected: 24
    # Path: Robot1: (0,0)->(1,1)->(2,1)->(3,1), Robot2: (0,2)->(1,1)->(2,2)->(3,2)
    
    # Test case 2
    grid2 = [
        [1,0,0,0,0,0,1],
        [2,0,0,0,0,3,0],
        [2,0,9,0,0,0,0],
        [0,3,0,5,4,0,0],
        [1,0,2,3,0,0,6]
    ]
    # Expected: 28
    
    # Test case 3 - Edge case
    grid3 = [[1,1],[1,1]]
    # Expected: 4
    
    solutions = [
        ("Top-down DP", Solution()),
        ("Bottom-up DP", SolutionBottomUp()), 
        ("Space Optimized", SolutionSpaceOptimized())
    ]
    
    test_cases = [
        ("Test 1", grid1, 24),
        ("Test 2", grid2, 28), 
        ("Test 3", grid3, 4)
    ]
    
    for name, grid, expected in test_cases:
        print(f"\n{name} (Expected: {expected}):")
        for sol_name, solution in solutions:
            result = solution.cherryPickup(grid)
            status = "✓" if result == expected else "✗"
            print(f"  {sol_name}: {result} {status}")


def visualize_solution_path():
    """Helper to understand the problem better"""
    grid = [
        [3,1,1],
        [2,5,1], 
        [1,5,5],
        [2,1,1]
    ]
    
    print("\nGrid visualization:")
    print("Robot1 starts at (0,0), Robot2 starts at (0,2)")
    print("Both robots move down simultaneously")
    print("\nOptimal path example:")
    print("Row 0: R1=(0,0)=3, R2=(0,2)=1 -> Total: 4")
    print("Row 1: R1=(1,1)=5, R2=(1,1)=5 -> Total: 5 (same cell)")  
    print("Row 2: R1=(2,1)=5, R2=(2,2)=5 -> Total: 10")
    print("Row 3: R1=(3,1)=1, R2=(3,2)=1 -> Total: 2")
    print("Grand Total: 4 + 5 + 10 + 2 = 21")


# Interview talking points and complexity analysis
"""
INTERVIEW DISCUSSION POINTS:

1. Problem Breakdown:
   - Two robots move simultaneously from top corners
   - Each robot has 3 choices per move (9 total combinations)
   - Key insight: robots are always on the same row

2. State Definition:
   - dp[row][col1][col2] = max cherries from this state to end
   - Only need to track columns since row is always same for both robots

3. Transition:
   - Current cherries = grid[row][col1] + (grid[row][col2] if col1 != col2 else 0)
   - Try all 9 combinations of next moves
   - Take maximum of all valid transitions

4. Base Cases:
   - Out of bounds: return 0
   - Last row: return current cherries

5. Optimizations:
   - Memoization for top-down
   - Space optimization: O(cols^2) instead of O(rows * cols^2)

6. Edge Cases:
   - Single row/column
   - Robots meet at same cell
   - All zeros vs all ones

7. Alternative Approaches:
   - Could model as single robot making two passes (more complex)
   - Graph theory approach (overkill for this problem)

8. Follow-up Questions:
   - What if robots can move in any direction?
   - What if we have k robots?
   - What if grid has obstacles?

Time Complexity: O(rows * cols^2 * 9) = O(rows * cols^2)
Space Complexity: O(rows * cols^2) unoptimized, O(cols^2) optimized
"""

if __name__ == "__main__":
    test_solutions()
    visualize_solution_path()
