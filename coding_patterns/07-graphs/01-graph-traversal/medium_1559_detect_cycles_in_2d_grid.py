"""
LeetCode 1559. Detect Cycles in 2D Grid
Problem: Given a 2D array of characters grid of size m x n, you need to find if there exists any cycle 
consisting of the same value in grid.

A cycle is a path of length 4 or more in the grid that starts and ends at the same cell. 
From a cell, you can move to one of the cells adjacent to it - in one of the four directions (up, down, left, right), 
if it has the same value of the current cell.

Also, you cannot move to the cell that you visited in the previous move.

Examples:
- Input: grid = [["a","a","a","a"],["a","b","b","a"],["a","b","b","a"],["a","a","a","a"]]
  Output: true (there's a cycle of 'a's around the border)
  
- Input: grid = [["c","c","c","a"],["c","d","c","c"],["c","c","e","c"],["f","c","c","c"]]
  Output: true (there's a cycle of 'c's)

Key insights: 
1. This is cycle detection in an undirected graph
2. Cannot revisit the parent cell (immediate previous cell)
3. Need DFS with parent tracking
4. Cycle exists if we reach a visited cell that's not our parent
"""

# SOLUTION 1: DFS with Parent Tracking (PREFERRED for interviews)
# Time: O(m*n), Space: O(m*n) for recursion stack and visited array
def containsCycle(grid):
    """
    DFS approach with parent tracking - most intuitive solution
    For each unvisited cell, start DFS and check for cycles
    """
    if not grid or not grid[0]:
        return False
    
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    
    def dfs(x, y, parent_x, parent_y, char):
        """
        DFS to detect cycle starting from (x, y)
        parent_x, parent_y: coordinates of the cell we came from
        char: the character value we're looking for in the cycle
        """
        visited[x][y] = True
        
        # Check all 4 directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check bounds and same character
            if (0 <= nx < m and 0 <= ny < n and 
                grid[nx][ny] == char):
                
                # Skip the parent cell (can't go back immediately)
                if nx == parent_x and ny == parent_y:
                    continue
                
                # If we've visited this cell before, we found a cycle
                if visited[nx][ny]:
                    return True
                
                # Continue DFS
                if dfs(nx, ny, x, y, char):
                    return True
        
        return False
    
    # Try starting DFS from each unvisited cell
    for i in range(m):
        for j in range(n):
            if not visited[i][j]:
                if dfs(i, j, -1, -1, grid[i][j]):
                    return True
    
    return False


# SOLUTION 2: DFS with Path Tracking (Alternative approach)
# Time: O(m*n), Space: O(m*n)
def containsCycle_path(grid):
    """
    DFS with path tracking - keeps track of current path
    Cycle detected when we revisit a cell in current path
    """
    if not grid or not grid[0]:
        return False
    
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    in_path = [[False] * n for _ in range(m)]
    
    def dfs(x, y, parent_x, parent_y, char):
        visited[x][y] = True
        in_path[x][y] = True
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < m and 0 <= ny < n and 
                grid[nx][ny] == char and 
                not (nx == parent_x and ny == parent_y)):
                
                # If in current path, we found a cycle
                if in_path[nx][ny]:
                    return True
                
                # If not visited, continue DFS
                if not visited[nx][ny] and dfs(nx, ny, x, y, char):
                    return True
        
        in_path[x][y] = False  # Remove from current path
        return False
    
    for i in range(m):
        for j in range(n):
            if not visited[i][j]:
                if dfs(i, j, -1, -1, grid[i][j]):
                    return True
    
    return False


# SOLUTION 3: Union-Find Approach (Advanced)
# Time: O(m*n*α(m*n)), Space: O(m*n)
def containsCycle_unionfind(grid):
    """
    Union-Find approach for cycle detection
    Connect adjacent same-character cells, detect cycle when union fails
    """
    if not grid or not grid[0]:
        return False
    
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
                return False  # Already connected - cycle detected
            
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            
            return True
    
    def get_index(i, j):
        return i * n + j
    
    uf = UnionFind(m * n)
    
    # Process each cell and try to union with right and down neighbors
    for i in range(m):
        for j in range(n):
            # Check right neighbor
            if j + 1 < n and grid[i][j] == grid[i][j + 1]:
                if not uf.union(get_index(i, j), get_index(i, j + 1)):
                    return True
            
            # Check down neighbor
            if i + 1 < m and grid[i][j] == grid[i + 1][j]:
                if not uf.union(get_index(i, j), get_index(i + 1, j)):
                    return True
    
    return False


# SOLUTION 4: BFS with Parent Tracking
# Time: O(m*n), Space: O(m*n)
def containsCycle_bfs(grid):
    """
    BFS approach with parent tracking
    Alternative to DFS if worried about recursion stack
    """
    if not grid or not grid[0]:
        return False
    
    from collections import deque
    
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    
    def bfs(start_x, start_y, char):
        queue = deque([(start_x, start_y, -1, -1)])  # (x, y, parent_x, parent_y)
        visited[start_x][start_y] = True
        
        while queue:
            x, y, parent_x, parent_y = queue.popleft()
            
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < m and 0 <= ny < n and 
                    grid[nx][ny] == char and 
                    not (nx == parent_x and ny == parent_y)):
                    
                    if visited[nx][ny]:
                        return True  # Cycle found
                    
                    visited[nx][ny] = True
                    queue.append((nx, ny, x, y))
        
        return False
    
    for i in range(m):
        for j in range(n):
            if not visited[i][j]:
                if bfs(i, j, grid[i][j]):
                    return True
    
    return False


# SOLUTION 5: DFS with Color States (Advanced)
# Time: O(m*n), Space: O(m*n)
def containsCycle_colors(grid):
    """
    DFS with 3 color states: WHITE (unvisited), GRAY (in progress), BLACK (finished)
    Cycle detected when we encounter a GRAY cell
    """
    if not grid or not grid[0]:
        return False
    
    m, n = len(grid), len(grid[0])
    
    # Color states: 0=WHITE (unvisited), 1=GRAY (in progress), 2=BLACK (finished)
    color = [[0] * n for _ in range(m)]
    
    def dfs(x, y, parent_x, parent_y, char):
        color[x][y] = 1  # Mark as GRAY (in progress)
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < m and 0 <= ny < n and 
                grid[nx][ny] == char and 
                not (nx == parent_x and ny == parent_y)):
                
                if color[nx][ny] == 1:  # Found GRAY cell - cycle detected
                    return True
                
                if color[nx][ny] == 0 and dfs(nx, ny, x, y, char):
                    return True
        
        color[x][y] = 2  # Mark as BLACK (finished)
        return False
    
    for i in range(m):
        for j in range(n):
            if color[i][j] == 0:
                if dfs(i, j, -1, -1, grid[i][j]):
                    return True
    
    return False


# Test cases
def test_solutions():
    # Test case 1: Has cycle
    grid1 = [
        ["a","a","a","a"],
        ["a","b","b","a"],
        ["a","b","b","a"],
        ["a","a","a","a"]
    ]
    
    # Test case 2: Has cycle
    grid2 = [
        ["c","c","c","a"],
        ["c","d","c","c"],
        ["c","c","e","c"],
        ["f","c","c","c"]
    ]
    
    # Test case 3: No cycle
    grid3 = [
        ["a","b","b"],
        ["b","z","b"],
        ["b","b","a"]
    ]
    
    test_cases = [grid1, grid2, grid3]
    expected = [True, True, False]
    
    print("Testing all solutions:")
    for i, grid in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print("Grid:")
        for row in grid:
            print(row)
        
        result1 = containsCycle(grid)
        result2 = containsCycle_path(grid)
        result3 = containsCycle_unionfind(grid)
        result4 = containsCycle_bfs(grid)
        result5 = containsCycle_colors(grid)
        
        print(f"DFS (parent tracking):   {result1}")
        print(f"DFS (path tracking):     {result2}")
        print(f"Union-Find:              {result3}")
        print(f"BFS:                     {result4}")
        print(f"DFS (color states):      {result5}")
        print(f"Expected:                {expected[i]}")
        print(f"All correct: {all(r == expected[i] for r in [result1, result2, result3, result4, result5])}")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - "This is cycle detection in an undirected graph represented as a 2D grid"
   - "Each cell is a node, edges exist between adjacent cells with same character"
   - "Key constraint: cannot return to immediate parent (previous cell)"
   - "Minimum cycle length is 4 due to grid structure"

2. START WITH DFS + PARENT TRACKING (PREFERRED):
   - "Use DFS to explore connected components of same characters"
   - "Track parent to avoid immediate backtracking"
   - "Cycle found when we reach a visited cell that's not our parent"
   - Time: O(m*n), Space: O(m*n) for visited array and recursion

3. KEY INSIGHTS:
   - "This is different from directed graph cycle detection"
   - "Must prevent immediate backtracking to parent"
   - "Each connected component of same characters forms a subgraph"
   - "Only need to find one cycle to return true"

4. IMPLEMENTATION DETAILS:
   - "For each unvisited cell, start DFS with that character"
   - "Pass parent coordinates to avoid going back"
   - "If we reach visited cell (not parent), cycle found"
   - "Use directions array for clean 4-directional movement"

5. ALTERNATIVE APPROACHES:
   - Union-Find: "Connect same-character neighbors, cycle when union fails"
   - BFS: "Same logic as DFS but iterative - good for stack overflow concerns"
   - Color states: "WHITE/GRAY/BLACK coloring for cycle detection"

6. EDGE CASES:
   - Single cell grid → False (minimum cycle length is 4)
   - All different characters → False
   - 2x2 grid of same character → True (forms a 4-cycle)
   - Linear path → False

7. OPTIMIZATION DISCUSSIONS:
   - "Can early terminate as soon as we find one cycle"
   - "Union-Find has worse time complexity but elegant for this problem"
   - "BFS alternative if recursion depth is a concern"

8. FOLLOW-UP QUESTIONS:
   - "What's minimum cycle length?" → 4 due to grid structure and parent constraint
   - "How to find all cycles?" → Continue search instead of early return
   - "What about diagonal movement?" → Would change minimum cycle length to 3

RECOMMENDED INTERVIEW FLOW:
1. Clarify problem: "Find cycle of same characters, can't return to immediate parent"
2. Explain approach: "DFS with parent tracking for cycle detection"
3. Code DFS solution with clean parent handling
4. Test with example: trace through DFS showing cycle detection
5. Discuss complexity: O(m*n) time and space
6. Mention alternatives: Union-Find, BFS, color states
7. Handle edge cases

KEY INSIGHT TO COMMUNICATE:
"This is undirected graph cycle detection where we must track the parent to prevent immediate backtracking. The key is recognizing when we reach a visited cell that's not our immediate parent."

COMMON MISTAKES TO AVOID:
- Forgetting parent tracking (allowing immediate backtrack)
- Not handling bounds checking properly
- Confusing with directed graph cycle detection
- Forgetting that minimum cycle length is 4
- Not checking character equality before moving

CRITICAL INTERVIEW POINTS:
- "Cannot return to immediate parent" - this is the key constraint
- "Each connected component of same characters is a separate subgraph"
- "DFS with parent tracking is most intuitive approach"
- "Union-Find also works elegantly - when union fails, cycle exists"
"""
