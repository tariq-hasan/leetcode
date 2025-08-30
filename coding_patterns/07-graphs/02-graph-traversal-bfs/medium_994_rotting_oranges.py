"""
LeetCode 994: Rotting Oranges
Problem: Given a grid with fresh oranges (1), rotten oranges (2), and empty cells (0),
determine minimum time for all oranges to rot. Rotten oranges spread to adjacent
fresh oranges every minute (4-directional).

Time Complexity: O(m*n) where m, n are grid dimensions
Space Complexity: O(m*n) for the queue in worst case
"""

from collections import deque
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Solution 1: Multi-source BFS (Standard approach)
        Start BFS from all initially rotten oranges simultaneously
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0
        
        # Find all initially rotten oranges and count fresh ones
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c, 0))  # (row, col, time)
                elif grid[r][c] == 1:
                    fresh_count += 1
        
        # If no fresh oranges, return 0
        if fresh_count == 0:
            return 0
        
        # 4-directional movement
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        max_time = 0
        
        while queue:
            row, col, time = queue.popleft()
            max_time = max(max_time, time)
            
            # Check all 4 adjacent cells
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check bounds and if cell contains fresh orange
                if (0 <= new_row < rows and 0 <= new_col < cols and 
                    grid[new_row][new_col] == 1):
                    
                    # Rot the fresh orange
                    grid[new_row][new_col] = 2
                    fresh_count -= 1
                    queue.append((new_row, new_col, time + 1))
        
        # Return time if all oranges rotted, else -1
        return max_time if fresh_count == 0 else -1

    def orangesRotting_layered_bfs(self, grid: List[List[int]]) -> int:
        """
        Solution 2: Layer-by-layer BFS
        Process all oranges at current time level before moving to next
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0
        
        # Initialize queue with all rotten oranges
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh_count += 1
        
        if fresh_count == 0:
            return 0
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        minutes = 0
        
        # Process level by level
        while queue and fresh_count > 0:
            minutes += 1
            # Process all oranges that are rotten at current minute
            for _ in range(len(queue)):
                row, col = queue.popleft()
                
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    
                    if (0 <= new_row < rows and 0 <= new_col < cols and 
                        grid[new_row][new_col] == 1):
                        
                        grid[new_row][new_col] = 2
                        fresh_count -= 1
                        queue.append((new_row, new_col))
        
        return minutes if fresh_count == 0 else -1

    def orangesRotting_with_visited(self, grid: List[List[int]]) -> int:
        """
        Solution 3: BFS with separate visited array
        Preserves original grid, uses visited array to track processed cells
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0
        visited = [[False] * cols for _ in range(rows)]
        
        # Find initial rotten oranges
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c, 0))
                    visited[r][c] = True
                elif grid[r][c] == 1:
                    fresh_count += 1
        
        if fresh_count == 0:
            return 0
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        max_time = 0
        
        while queue:
            row, col, time = queue.popleft()
            max_time = max(max_time, time)
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < rows and 0 <= new_col < cols and 
                    not visited[new_row][new_col] and grid[new_row][new_col] == 1):
                    
                    visited[new_row][new_col] = True
                    fresh_count -= 1
                    queue.append((new_row, new_col, time + 1))
        
        return max_time if fresh_count == 0 else -1

    def orangesRotting_optimized_space(self, grid: List[List[int]]) -> int:
        """
        Solution 4: Space-optimized version
        Uses the grid itself to mark visited cells with a special value
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0
        
        # Count fresh oranges and add rotten ones to queue
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    fresh_count += 1
                elif grid[r][c] == 2:
                    queue.append((r, c))
        
        if fresh_count == 0:
            return 0
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        minutes = 0
        
        while queue and fresh_count > 0:
            minutes += 1
            
            # Process current level
            for _ in range(len(queue)):
                row, col = queue.popleft()
                
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    
                    if (0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1):
                        grid[nr][nc] = 2  # Mark as rotten
                        fresh_count -= 1
                        queue.append((nr, nc))
        
        return minutes if fresh_count == 0 else -1

# Test cases for interview demonstration
def test_solutions():
    sol = Solution()
    
    # Test case 1: Normal case
    grid1 = [[2,1,1],[1,1,0],[0,1,1]]
    print(f"Test 1: {sol.orangesRotting(grid1)}")  # Expected: 4
    
    # Test case 2: Impossible case
    grid2 = [[2,1,1],[0,1,1],[1,0,1]]
    print(f"Test 2: {sol.orangesRotting(grid2)}")  # Expected: -1
    
    # Test case 3: All already rotten or empty
    grid3 = [[0,2]]
    print(f"Test 3: {sol.orangesRotting(grid3)}")  # Expected: 0
    
    # Test case 4: Single fresh orange, no rotten
    grid4 = [[1]]
    print(f"Test 4: {sol.orangesRotting(grid4)}")  # Expected: -1
    
    # Test case 5: All fresh oranges are isolated
    grid5 = [[1,0,1],[0,2,0],[1,0,1]]
    print(f"Test 5: {sol.orangesRotting(grid5)}")  # Expected: -1

if __name__ == "__main__":
    test_solutions()

"""
Interview Discussion Points:

1. **Why Multi-source BFS?**
   - All initially rotten oranges spread simultaneously
   - Single-source BFS would be incorrect (sequential spreading)
   - Need to process all current rotten oranges before moving to next minute

2. **Key Insights**:
   - This is a multi-source BFS problem
   - Track fresh orange count to determine if all can be rotted
   - Use level-by-level processing or time tracking

3. **Edge Cases**:
   - No fresh oranges initially → return 0
   - No rotten oranges but fresh exist → return -1
   - Isolated fresh oranges → return -1
   - Empty grid → return 0

4. **Time/Space Complexity**:
   - Time: O(m*n) - visit each cell at most once
   - Space: O(m*n) - queue can contain all cells in worst case

5. **Implementation Variations**:
   - Time tracking vs level-by-level processing
   - In-place modification vs separate visited array
   - Different ways to handle the "minute" counting

6. **Common Mistakes**:
   - Using single-source BFS instead of multi-source
   - Not handling the case where some oranges can't be reached
   - Off-by-one errors in time calculation
   - Forgetting to check if all fresh oranges were processed

7. **Follow-up Questions**:
   - What if oranges could rot diagonally? (8-directional)
   - What if different rotten oranges had different spread rates?
   - How to track which orange caused each infection?
"""
