"""
LeetCode 1020. Number of Enclaves
Problem: You are given an m x n binary matrix grid, where 0 represents a sea cell and 1 represents a land cell.
A move consists of walking from one land cell to another adjacent (4-directionally) land cell or walking off the boundary of the grid.
Return the number of land cells in grid for which we cannot walk off the boundary of the grid in any number of moves.

Examples:
- Input: grid = [[0,0,0,0],[1,1,0,1],[0,1,1,0],[0,0,0,0]]
  Output: 3 (the middle land cells cannot reach boundary)

Key insight: Land cells that can reach boundary are NOT enclaves.
Strategy: Mark all land cells connected to boundary, then count remaining land cells.
"""

# SOLUTION 1: DFS from Boundary (PREFERRED for interviews)
# Time: O(m*n), Space: O(m*n) for recursion stack
def numEnclaves(grid):
    """
    DFS approach: Mark all land cells reachable from boundary, count the rest
    1. Start DFS from all boundary land cells
    2. Mark all connected land cells as visited (set to 0)
    3. Count remaining land cells (these are enclaves)
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    
    def dfs(i, j):
        # Mark current cell as water (visited)
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
            return
        
        grid[i][j] = 0  # Mark as visited by converting to water
        
        # Explore all 4 directions
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    
    # Start DFS from all boundary cells
    # Top and bottom rows
    for j in range(n):
        if grid[0][j] == 1:
            dfs(0, j)
        if grid[m-1][j] == 1:
            dfs(m-1, j)
    
    # Left and right columns
    for i in range(m):
        if grid[i][0] == 1:
            dfs(i, 0)
        if grid[i][n-1] == 1:
            dfs(i, n-1)
    
    # Count remaining land cells (enclaves)
    enclaves = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                enclaves += 1
    
    return enclaves


# SOLUTION 2: BFS from Boundary (Alternative approach)
# Time: O(m*n), Space: O(m*n) for queue
def numEnclaves_bfs(grid):
    """
    BFS approach: Same logic as DFS but using queue
    Useful if worried about recursion stack overflow
    """
    if not grid or not grid[0]:
        return 0
    
    from collections import deque
    
    m, n = len(grid), len(grid[0])
    queue = deque()
    
    # Add all boundary land cells to queue
    for j in range(n):
        if grid[0][j] == 1:
            queue.append((0, j))
            grid[0][j] = 0
        if grid[m-1][j] == 1:
            queue.append((m-1, j))
            grid[m-1][j] = 0
    
    for i in range(1, m-1):  # Skip corners (already handled)
        if grid[i][0] == 1:
            queue.append((i, 0))
            grid[i][0] = 0
        if grid[i][n-1] == 1:
            queue.append((i, n-1))
            grid[i][n-1] = 0
    
    # BFS to mark all connected land cells
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        x, y = queue.popleft()
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                grid[nx][ny] = 0
                queue.append((nx, ny))
    
    # Count remaining land cells
    return sum(sum(row) for row in grid)


# SOLUTION 3: DFS with Visited Set (Non-destructive)
# Time: O(m*n), Space: O(m*n)
def numEnclaves_nondestructive(grid):
    """
    DFS approach that doesn't modify original grid
    Uses separate visited set to track boundary-connected cells
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    visited = set()
    
    def dfs(i, j):
        if (i < 0 or i >= m or j < 0 or j >= n or 
            grid[i][j] == 0 or (i, j) in visited):
            return
        
        visited.add((i, j))
        
        # Explore all 4 directions
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    
    # Mark all boundary-connected land cells
    for j in range(n):
        if grid[0][j] == 1:
            dfs(0, j)
        if grid[m-1][j] == 1:
            dfs(m-1, j)
    
    for i in range(m):
        if grid[i][0] == 1:
            dfs(i, 0)
        if grid[i][n-1] == 1:
            dfs(i, n-1)
    
    # Count land cells not connected to boundary
    enclaves = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1 and (i, j) not in visited:
                enclaves += 1
    
    return enclaves


# SOLUTION 4: Union-Find (Advanced approach)
# Time: O(m*n*α(m*n)), Space: O(m*n)
def numEnclaves_unionfind(grid):
    """
    Union-Find approach: Connect all land cells, then check boundary connections
    More complex but shows advanced data structure knowledge
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    
    class UnionFind:
        def __init__(self, size):
            self.parent = list(range(size))
            self.rank = [0] * size
        
        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        
        def union(self, x, y):
            px, py = self.find(x), self.find(y)
            if px == py:
                return
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
    
    # Create virtual boundary node
    boundary_node = m * n
    uf = UnionFind(m * n + 1)
    
    # Convert 2D coordinates to 1D index
    def get_index(i, j):
        return i * n + j
    
    # Connect all adjacent land cells
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                # Connect to boundary if on edge
                if i == 0 or i == m-1 or j == 0 or j == n-1:
                    uf.union(get_index(i, j), boundary_node)
                
                # Connect to adjacent land cells
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if (0 <= ni < m and 0 <= nj < n and 
                        grid[ni][nj] == 1):
                        uf.union(get_index(i, j), get_index(ni, nj))
    
    # Count land cells not connected to boundary
    boundary_root = uf.find(boundary_node)
    enclaves = 0
    
    for i in range(m):
        for j in range(n):
            if (grid[i][j] == 1 and 
                uf.find(get_index(i, j)) != boundary_root):
                enclaves += 1
    
    return enclaves


# SOLUTION 5: Two-Pass Algorithm
# Time: O(m*n), Space: O(1) additional space
def numEnclaves_twopass(grid):
    """
    Two-pass algorithm: 
    1. First pass: mark all boundary-connected cells
    2. Second pass: count unmarked land cells
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    
    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != 1:
            return
        
        grid[i][j] = -1  # Mark as boundary-connected
        
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    
    # First pass: mark all boundary-connected land cells
    for j in range(n):
        dfs(0, j)
        dfs(m-1, j)
    
    for i in range(m):
        dfs(i, 0)
        dfs(i, n-1)
    
    # Second pass: count enclaves and restore grid
    enclaves = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                enclaves += 1
            elif grid[i][j] == -1:
                grid[i][j] = 1  # Restore original value
    
    return enclaves


# Test cases
def test_solutions():
    # Test case 1
    grid1 = [
        [0,0,0,0],
        [1,1,0,1],
        [0,1,1,0],
        [0,0,0,0]
    ]
    
    # Test case 2
    grid2 = [
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,0,0]
    ]
    
    test_cases = [grid1, grid2]
    expected = [3, 0]
    
    print("Testing all solutions:")
    for i, grid in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print("Grid:")
        for row in grid:
            print(row)
        
        # Test each solution (need to copy grid since some modify it)
        import copy
        
        result1 = numEnclaves(copy.deepcopy(grid))
        result2 = numEnclaves_bfs(copy.deepcopy(grid))
        result3 = numEnclaves_nondestructive(copy.deepcopy(grid))
        result4 = numEnclaves_unionfind(copy.deepcopy(grid))
        result5 = numEnclaves_twopass(copy.deepcopy(grid))
        
        print(f"DFS (destructive):     {result1}")
        print(f"BFS:                   {result2}")
        print(f"DFS (non-destructive): {result3}")
        print(f"Union-Find:            {result4}")
        print(f"Two-Pass:              {result5}")
        print(f"Expected:              {expected[i]}")
        print(f"All correct: {all(r == expected[i] for r in [result1, result2, result3, result4, result5])}")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - "Enclaves are land cells that cannot reach the boundary"
   - "Strategy: Find all land cells connected to boundary, count the rest"
   - "This is essentially a graph connectivity problem"

2. START WITH DFS FROM BOUNDARY (PREFERRED):
   - "Start DFS from all boundary land cells"
   - "Mark all reachable land cells (these can escape)"
   - "Count remaining unmarked land cells (these are enclaves)"
   - Time: O(m*n), Space: O(m*n) for recursion stack

3. KEY INSIGHTS:
   - "Instead of checking if each cell can reach boundary, we reverse the approach"
   - "Start from boundary and mark all reachable cells - much more efficient"
   - "This avoids redundant DFS calls from interior cells"

4. IMPLEMENTATION DETAILS:
   - "Can modify grid in-place (set reachable land to 0) or use visited set"
   - "Need to handle all 4 boundary sides: top, bottom, left, right"
   - "Be careful with corner cells - don't double-count"

5. ALTERNATIVE APPROACHES:
   - BFS: "Same logic but iterative - good if worried about stack overflow"
   - Union-Find: "Advanced approach connecting land cells to virtual boundary node"
   - Two-pass: "More explicit separation of marking and counting phases"

6. EDGE CASES:
   - Empty grid or no land cells → return 0
   - All land cells on boundary → return 0  
   - Grid with single row/column → handle boundary correctly
   - All land cells are enclaves → count all

7. OPTIMIZATION DISCUSSIONS:
   - "Can use BFS instead of DFS to avoid stack overflow for large grids"
   - "In-place modification saves space but destroys original grid"
   - "Union-Find has worse time complexity but shows advanced knowledge"

8. FOLLOW-UP QUESTIONS:
   - "What if we want to preserve original grid?" → Use visited set
   - "How to handle very large grids?" → BFS to avoid stack overflow
   - "What if we want to find actual enclave regions?" → Return list of coordinates

RECOMMENDED INTERVIEW FLOW:
1. Clarify problem: "Find land cells that cannot reach boundary"
2. Explain strategy: "Reverse approach - start from boundary, mark reachable"
3. Code DFS solution with boundary traversal
4. Test with example grid
5. Discuss time/space complexity: O(m*n) for both
6. Mention BFS alternative if asked about stack overflow
7. Handle edge cases

KEY INSIGHT TO COMMUNICATE:
"Instead of checking each cell individually, we reverse the problem: start from the boundary and mark everything reachable. What's left unmarked are the enclaves."

COMMON MISTAKES TO AVOID:
- Forgetting to check all 4 boundary sides
- Double-counting corner cells
- Not handling empty grid edge case
- Stack overflow with deep recursion (mention BFS alternative)
- Off-by-one errors in boundary iteration
"""
