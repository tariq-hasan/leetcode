"""
LeetCode 1091: Shortest Path in Binary Matrix
Problem: Find shortest path from top-left to bottom-right in binary matrix
where 0 represents open cell and 1 represents blocked cell.
Can move in 8 directions (including diagonals).

Time Complexity: O(n²) where n is the side length of the matrix
Space Complexity: O(n²) for the queue and visited set
"""

from collections import deque
from typing import List

class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        """
        Solution 1: Standard BFS with visited set
        Most readable and commonly expected in interviews
        """
        n = len(grid)
        
        # Edge cases
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        
        if n == 1:
            return 1
        
        # 8 directions: up, down, left, right, and 4 diagonals
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        queue = deque([(0, 0, 1)])  # (row, col, path_length)
        visited = {(0, 0)}
        
        while queue:
            row, col, path_len = queue.popleft()
            
            # Check if we reached the destination
            if row == n-1 and col == n-1:
                return path_len
            
            # Explore all 8 directions
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check bounds and if cell is valid and unvisited
                if (0 <= new_row < n and 0 <= new_col < n and 
                    grid[new_row][new_col] == 0 and 
                    (new_row, new_col) not in visited):
                    
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, path_len + 1))
        
        return -1

    def shortestPathBinaryMatrix_optimized(self, grid: List[List[int]]) -> int:
        """
        Solution 2: BFS with in-place marking (space optimized)
        Modifies the grid to mark visited cells, saves space
        """
        n = len(grid)
        
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        
        if n == 1:
            return 1
        
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        queue = deque([(0, 0, 1)])
        grid[0][0] = 1  # Mark as visited
        
        while queue:
            row, col, path_len = queue.popleft()
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < n and 0 <= new_col < n and 
                    grid[new_row][new_col] == 0):
                    
                    # Check if we reached destination before marking
                    if new_row == n-1 and new_col == n-1:
                        return path_len + 1
                    
                    grid[new_row][new_col] = 1  # Mark as visited
                    queue.append((new_row, new_col, path_len + 1))
        
        return -1

    def shortestPathBinaryMatrix_astar(self, grid: List[List[int]]) -> int:
        """
        Solution 3: A* algorithm with Manhattan distance heuristic
        More advanced solution showing algorithmic knowledge
        """
        import heapq
        
        n = len(grid)
        
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        
        if n == 1:
            return 1
        
        def heuristic(row, col):
            # Chebyshev distance (max of horizontal/vertical distance)
            # More accurate for 8-directional movement
            return max(abs(row - (n-1)), abs(col - (n-1)))
        
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        # Priority queue: (f_score, g_score, row, col)
        heap = [(1 + heuristic(0, 0), 1, 0, 0)]
        visited = set()
        
        while heap:
            f_score, g_score, row, col = heapq.heappop(heap)
            
            if (row, col) in visited:
                continue
                
            visited.add((row, col))
            
            if row == n-1 and col == n-1:
                return g_score
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < n and 0 <= new_col < n and 
                    grid[new_row][new_col] == 0 and 
                    (new_row, new_col) not in visited):
                    
                    new_g = g_score + 1
                    new_f = new_g + heuristic(new_row, new_col)
                    heapq.heappush(heap, (new_f, new_g, new_row, new_col))
        
        return -1

# Test cases for interview demonstration
def test_solutions():
    sol = Solution()
    
    # Test case 1: Basic valid path
    grid1 = [[0,0,0],[1,1,0],[1,1,0]]
    print(f"Test 1: {sol.shortestPathBinaryMatrix(grid1)}")  # Expected: 4
    
    # Test case 2: No path available
    grid2 = [[0,1],[1,0]]
    print(f"Test 2: {sol.shortestPathBinaryMatrix(grid2)}")  # Expected: -1
    
    # Test case 3: Single cell
    grid3 = [[0]]
    print(f"Test 3: {sol.shortestPathBinaryMatrix(grid3)}")  # Expected: 1
    
    # Test case 4: Start or end blocked
    grid4 = [[1,0,0],[1,1,0],[1,1,0]]
    print(f"Test 4: {sol.shortestPathBinaryMatrix(grid4)}")  # Expected: -1

if __name__ == "__main__":
    test_solutions()

"""
Interview Discussion Points:

1. **Algorithm Choice**: BFS is optimal for unweighted shortest path problems
   - Why not DFS? DFS doesn't guarantee shortest path
   - Why not Dijkstra? All edges have weight 1, BFS is simpler

2. **Time/Space Complexity**: 
   - Time: O(n²) - worst case visit all cells
   - Space: O(n²) - queue and visited set

3. **Edge Cases to Consider**:
   - Start or destination blocked
   - Single cell grid
   - No valid path exists
   - Empty grid (though problem constraints prevent this)

4. **Optimizations**:
   - In-place marking saves O(n²) space
   - Early termination when destination found
   - A* for theoretical improvement (though overkill for this problem)

5. **8-Directional Movement**:
   - Include all 8 directions including diagonals
   - Common mistake: forgetting diagonal movements

6. **Implementation Details**:
   - Use deque for O(1) append/popleft operations
   - Check bounds carefully
   - Mark visited before adding to queue to prevent duplicates
"""
