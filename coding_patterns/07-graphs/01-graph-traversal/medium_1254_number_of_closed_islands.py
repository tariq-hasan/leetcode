"""
LeetCode 1254. Number of Closed Islands
Problem: Given a 2D grid consists of 0s (land) and 1s (water), an island is a group of 1s 
(representing water) and is surrounded by 0s (representing land). An island is closed if the 
island is completely surrounded by water (1s) and is not touching the boundary of the grid.
Return the number of closed islands.

Wait - there's a common confusion here! Let me clarify:
Actually, in this problem:
- 0 represents LAND
- 1 represents WATER  
- A closed island is a group of 0s (land) completely surrounded by 1s (water)
- Islands touching the boundary are NOT closed

Examples:
- Input: grid = [[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]
  Output: 2 (there are 2 closed islands of land)

Key insight: Remove all land connected to boundary first, then count remaining land islands.
"""

# SOLUTION 1: DFS - Remove Boundary Islands First (PREFERRED)
# Time: O(m*n), Space: O(m*n) for recursion stack
def closedIsland(grid):
    """
    DFS approach: Remove all land (0s) connected to boundary, then count remaining islands
    1. Mark all boundary-connected land as water (flip 0->1)
    2. Count remaining land islands using standard island counting
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    
    def dfs(i, j):
        # Base case: out of bounds or already water
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 1:
            return
        
        # Mark current land as water (visited)
        grid[i][j] = 1
        
        # Explore all 4 directions
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    
    # Phase 1: Remove all boundary-connected land
    # Top and bottom rows
    for j in range(n):
        if grid[0][j] == 0:
            dfs(0, j)
        if grid[m-1][j] == 0:
            dfs(m-1, j)
    
    # Left and right columns
    for i in range(m):
        if grid[i][0] == 0:
            dfs(i, 0)
        if grid[i][n-1] == 0:
            dfs(i, n-1)
    
    # Phase 2: Count remaining land islands
    closed_islands = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:  # Found unvisited land
                dfs(i, j)  # Mark entire island as visited
                closed_islands += 1
    
    return closed_islands


# SOLUTION 2: DFS with Boolean Return (Alternative approach)
# Time: O(m*n), Space: O(m*n)
def closedIsland_boolean(grid):
    """
    DFS that returns boolean indicating if island is closed
    For each land cell, check if its entire island is closed
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    
    def dfs(i, j):
        # Out of bounds means not closed (touches boundary)
        if i < 0 or i >= m or j < 0 or j >= n:
            return False
        
        # Water or already visited
        if grid[i][j] == 1 or visited[i][j]:
            return True
        
        # Mark as visited
        visited[i][j] = True
        
        # Check if all 4 directions are closed
        up = dfs(i - 1, j)
        down = dfs(i + 1, j)
        left = dfs(i, j - 1)
        right = dfs(i, j + 1)
        
        # Island is closed only if all directions are closed
        return up and down and left and right
    
    closed_islands = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0 and not visited[i][j]:
                if dfs(i, j):
                    closed_islands += 1
    
    return closed_islands


# SOLUTION 3: BFS Approach
# Time: O(m*n), Space: O(m*n)
def closedIsland_bfs(grid):
    """
    BFS approach: Same logic as DFS but using queue
    Good alternative if worried about recursion stack overflow
    """
    if not grid or not grid[0]:
        return 0
    
    from collections import deque
    
    m, n = len(grid), len(grid[0])
    
    def bfs_mark(start_i, start_j):
        queue = deque([(start_i, start_j)])
        grid[start_i][start_j] = 1
        
        while queue:
            i, j = queue.popleft()
            
            # Check all 4 directions
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 0:
                    grid[ni][nj] = 1  # Mark as water
                    queue.append((ni, nj))
    
    # Phase 1: Remove boundary-connected land using BFS
    for j in range(n):
        if grid[0][j] == 0:
            bfs_mark(0, j)
        if grid[m-1][j] == 0:
            bfs_mark(m-1, j)
    
    for i in range(1, m-1):  # Skip corners already handled
        if grid[i][0] == 0:
            bfs_mark(i, 0)
        if grid[i][n-1] == 0:
            bfs_mark(i, n-1)
    
    # Phase 2: Count remaining islands
    closed_islands = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:
                bfs_mark(i, j)
                closed_islands += 1
    
    return closed_islands


# SOLUTION 4: Union-Find Approach (Advanced)
# Time: O(m*n*α(m*n)), Space: O(m*n)
def closedIsland_unionfind(grid):
    """
    Union-Find approach: Connect all land cells, check boundary connections
    Advanced solution showing data structure knowledge
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    
    class UnionFind:
        def __init__(self, size):
            self.parent = list(range(size))
            self.rank = [0] * size
            self.components = size
        
        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        
        def union(self, x, y):
            px, py = self.find(x), self.find(y)
            if px == py:
                return False
            
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            
            self.components -= 1
            return True
    
    # Create virtual boundary node
    boundary_node = m * n
    uf = UnionFind(m * n + 1)
    
    def get_index(i, j):
        return i * n + j
    
    # Union all land cells
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:  # Land cell
                # Connect boundary land to boundary node
                if i == 0 or i == m-1 or j == 0 or j == n-1:
                    uf.union(get_index(i, j), boundary_node)
                
                # Connect to adjacent land cells
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if (0 <= ni < m and 0 <= nj < n and 
                        grid[ni][nj] == 0):
                        uf.union(get_index(i, j), get_index(ni, nj))
    
    # Count land components not connected to boundary
    boundary_root = uf.find(boundary_node)
    land_components = set()
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:
                root = uf.find(get_index(i, j))
                if root != boundary_root:
                    land_components.add(root)
    
    return len(land_components)


# SOLUTION 5: Non-destructive DFS (Preserves original grid)
# Time: O(m*n), Space: O(m*n)
def closedIsland_nondestructive(grid):
    """
    DFS approach that doesn't modify the original grid
    Uses visited set to track processed cells
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    boundary_connected = set()
    
    def dfs_boundary(i, j):
        if (i < 0 or i >= m or j < 0 or j >= n or 
            grid[i][j] == 1 or (i, j) in boundary_connected):
            return
        
        boundary_connected.add((i, j))
        
        # Explore all 4 directions
        dfs_boundary(i + 1, j)
        dfs_boundary(i - 1, j)
        dfs_boundary(i, j + 1)
        dfs_boundary(i, j - 1)
    
    # Mark all boundary-connected land
    for j in range(n):
        if grid[0][j] == 0:
            dfs_boundary(0, j)
        if grid[m-1][j] == 0:
            dfs_boundary(m-1, j)
    
    for i in range(m):
        if grid[i][0] == 0:
            dfs_boundary(i, 0)
        if grid[i][n-1] == 0:
            dfs_boundary(i, n-1)
    
    # Count closed islands
    visited = set()
    
    def dfs_island(i, j):
        if (i < 0 or i >= m or j < 0 or j >= n or 
            grid[i][j] == 1 or (i, j) in visited):
            return
        
        visited.add((i, j))
        
        dfs_island(i + 1, j)
        dfs_island(i - 1, j)
        dfs_island(i, j + 1)
        dfs_island(i, j - 1)
    
    closed_islands = 0
    for i in range(m):
        for j in range(n):
            if (grid[i][j] == 0 and (i, j) not in visited and 
                (i, j) not in boundary_connected):
                dfs_island(i, j)
                closed_islands += 1
    
    return closed_islands


# Test cases
def test_solutions():
    # Test case 1
    grid1 = [
        [1,1,1,1,1,1,1,0],
        [1,0,0,0,0,1,1,0],
        [1,0,1,0,1,1,1,0],
        [1,0,0,0,0,1,0,1],
        [1,1,1,1,1,1,1,0]
    ]
    
    # Test case 2
    grid2 = [
        [0,0,1,0,0],
        [0,1,0,1,0],
        [0,1,1,1,0]
    ]
    
    # Test case 3 - all boundary
    grid3 = [
        [0,0,1,1,0],
        [1,1,1,1,1],
        [0,0,1,1,0]
    ]
    
    test_cases = [grid1, grid2, grid3]
    expected = [2, 1, 0]
    
    print("Testing all solutions:")
    for i, grid in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print("Grid (0=land, 1=water):")
        for row in grid:
            print(row)
        
        # Test each solution (need deep copy since some modify grid)
        import copy
        
        result1 = closedIsland(copy.deepcopy(grid))
        result2 = closedIsland_boolean(copy.deepcopy(grid))
        result3 = closedIsland_bfs(copy.deepcopy(grid))
        result4 = closedIsland_unionfind(copy.deepcopy(grid))
        result5 = closedIsland_nondestructive(copy.deepcopy(grid))
        
        print(f"DFS (boundary removal):  {result1}")
        print(f"DFS (boolean return):    {result2}")
        print(f"BFS:                     {result3}")
        print(f"Union-Find:              {result4}")
        print(f"Non-destructive DFS:     {result5}")
        print(f"Expected:                {expected[i]}")
        print(f"All correct: {all(r == expected[i] for r in [result1, result2, result3, result4, result5])}")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING (CRITICAL - CLARIFY FIRST):
   - "Let me confirm: 0 = land, 1 = water, we want closed land islands"
   - "Closed island = land completely surrounded by water, not touching boundary"
   - "This is opposite of typical island problems where 1 = land"

2. START WITH BOUNDARY REMOVAL DFS (PREFERRED):
   - "Strategy: Remove all land connected to boundary, count remaining islands"
   - "Two phases: 1) Eliminate boundary-connected land, 2) Count remaining islands"
   - "More efficient than checking each island individually"
   - Time: O(m*n), Space: O(m*n) for recursion stack

3. KEY INSIGHTS:
   - "Any land touching boundary cannot be a closed island"
   - "Reverse approach: eliminate invalid islands first, then count valid ones"
   - "Similar to 'Number of Enclaves' but counting islands instead of cells"

4. IMPLEMENTATION DETAILS:
   - "First DFS: start from boundary, mark all connected land as water"
   - "Second pass: standard island counting on remaining land"
   - "Can modify grid in-place or use visited sets"

5. ALTERNATIVE APPROACHES:
   - Boolean DFS: "Check if each island touches boundary during traversal"
   - BFS: "Same logic but iterative - good for stack overflow concerns"
   - Union-Find: "Advanced approach using virtual boundary node"

6. EDGE CASES:
   - Empty grid → return 0
   - All water → return 0
   - All land touching boundary → return 0
   - Single cell grids → check if it's boundary

7. COMMON CONFUSION POINTS:
   - "Remember: 0=land, 1=water (opposite of typical problems)"
   - "Closed means NOT touching boundary (completely surrounded)"
   - "Count islands, not individual land cells"

8. FOLLOW-UP QUESTIONS:
   - "How to preserve original grid?" → Use visited set approach
   - "What about very large grids?" → BFS to avoid stack overflow
   - "How to find actual island coordinates?" → Return list of island cell sets

RECOMMENDED INTERVIEW FLOW:
1. **CLARIFY PROBLEM FIRST**: "Just to confirm, 0=land, 1=water, and we want land islands not touching boundary?"
2. Explain strategy: "Remove boundary-connected land first, then count remaining islands"
3. Code two-phase DFS solution
4. Test with example (trace through boundary removal, then counting)
5. Discuss complexity: O(m*n) time and space
6. Handle edge cases and mention alternatives

KEY INSIGHT TO COMMUNICATE:
"The key insight is that any land connected to the boundary cannot be closed. So we eliminate all boundary-connected land first, then count the remaining separate land components."

CRITICAL INTERVIEW MISTAKE TO AVOID:
- **Misunderstanding the problem**: This is the #1 issue. Make sure you clarify that 0=land, 1=water
- Many candidates assume 1=land and get completely wrong approach

COMMON CODING MISTAKES:
- Forgetting to handle all 4 boundary sides
- Not properly implementing two-phase approach
- Off-by-one errors in boundary traversal
- Confusing land (0) vs water (1) in conditions
"""
