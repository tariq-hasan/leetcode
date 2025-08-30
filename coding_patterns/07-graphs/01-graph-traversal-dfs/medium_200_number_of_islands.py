"""
LeetCode 200: Number of Islands

Problem: Given a 2D binary grid which represents a map of '1's (land) and '0's (water),
return the number of islands. An island is surrounded by water and is formed by 
connecting adjacent lands horizontally or vertically.

Key Insight: Each connected component of '1's forms one island.
Use graph traversal to mark visited lands and count components.

Time Complexity: O(M*N) where M and N are grid dimensions
Space Complexity: O(min(M,N)) to O(M*N) depending on approach
"""

class Solution:
    def numIslands(self, grid):
        """
        DFS Solution - Most popular and intuitive for interviews
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        islands = 0
        
        def dfs(r, c):
            # Base cases: out of bounds or water/visited
            if (r < 0 or r >= rows or c < 0 or c >= cols or 
                grid[r][c] != '1'):
                return
            
            # Mark as visited by sinking the island
            grid[r][c] = '0'
            
            # Explore all 4 directions
            dfs(r + 1, c)  # down
            dfs(r - 1, c)  # up
            dfs(r, c + 1)  # right
            dfs(r, c - 1)  # left
        
        # Scan the entire grid
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    islands += 1
                    dfs(r, c)  # Sink the entire island
        
        return islands

    def numIslandsBFS(self, grid):
        """
        BFS Solution - Better for very wide grids to avoid stack overflow
        """
        if not grid or not grid[0]:
            return 0
        
        from collections import deque
        
        rows, cols = len(grid), len(grid[0])
        islands = 0
        
        def bfs(start_r, start_c):
            queue = deque([(start_r, start_c)])
            grid[start_r][start_c] = '0'  # Mark as visited
            
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            while queue:
                r, c = queue.popleft()
                
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and 
                        grid[nr][nc] == '1'):
                        grid[nr][nc] = '0'  # Mark as visited
                        queue.append((nr, nc))
        
        # Scan the entire grid
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    islands += 1
                    bfs(r, c)
        
        return islands

    def numIslandsUnionFind(self, grid):
        """
        Union-Find Solution - Great for follow-up discussions
        Especially useful when grid is dynamic (adding/removing lands)
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        
        class UnionFind:
            def __init__(self):
                self.parent = {}
                self.rank = {}
                self.count = 0
            
            def add(self, x):
                if x not in self.parent:
                    self.parent[x] = x
                    self.rank[x] = 0
                    self.count += 1
            
            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])
                return self.parent[x]
            
            def union(self, x, y):
                px, py = self.find(x), self.find(y)
                if px == py:
                    return
                
                # Union by rank
                if self.rank[px] < self.rank[py]:
                    px, py = py, px
                
                self.parent[py] = px
                if self.rank[px] == self.rank[py]:
                    self.rank[px] += 1
                
                self.count -= 1
        
        uf = UnionFind()
        
        # Add all land cells to Union-Find
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    uf.add((r, c))
        
        # Union adjacent land cells
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < rows and 0 <= nc < cols and 
                            grid[nr][nc] == '1'):
                            uf.union((r, c), (nr, nc))
        
        return uf.count

    def numIslandsPreserveGrid(self, grid):
        """
        DFS Solution that preserves original grid using visited set
        Good when you can't modify the input
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set()
        islands = 0
        
        def dfs(r, c):
            if ((r, c) in visited or r < 0 or r >= rows or 
                c < 0 or c >= cols or grid[r][c] != '1'):
                return
            
            visited.add((r, c))
            
            # Explore all 4 directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(r + dr, c + dc)
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1' and (r, c) not in visited:
                    islands += 1
                    dfs(r, c)
        
        return islands

    def numIslandsIterativeDFS(self, grid):
        """
        Iterative DFS to avoid recursion stack overflow
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        islands = 0
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    islands += 1
                    
                    # Iterative DFS using stack
                    stack = [(r, c)]
                    while stack:
                        curr_r, curr_c = stack.pop()
                        
                        if (curr_r < 0 or curr_r >= rows or 
                            curr_c < 0 or curr_c >= cols or 
                            grid[curr_r][curr_c] != '1'):
                            continue
                        
                        grid[curr_r][curr_c] = '0'  # Mark as visited
                        
                        # Add neighbors to stack
                        stack.extend([
                            (curr_r + 1, curr_c),
                            (curr_r - 1, curr_c),
                            (curr_r, curr_c + 1),
                            (curr_r, curr_c - 1)
                        ])
        
        return islands


# Test cases for interview
def test_number_of_islands():
    solution = Solution()
    
    # Test case 1: Standard case
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    print(f"Test 1: {solution.numIslands([row[:] for row in grid1])}")  # Expected: 1
    
    # Test case 2: Multiple islands
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    print(f"Test 2: {solution.numIslands([row[:] for row in grid2])}")  # Expected: 3
    
    # Test case 3: No islands
    grid3 = [
        ["0","0","0"],
        ["0","0","0"],
        ["0","0","0"]
    ]
    print(f"Test 3: {solution.numIslands([row[:] for row in grid3])}")  # Expected: 0
    
    # Test case 4: Single cell
    grid4 = [["1"]]
    print(f"Test 4: {solution.numIslands([row[:] for row in grid4])}")  # Expected: 1
    
    # Test case 5: All land
    grid5 = [
        ["1","1"],
        ["1","1"]
    ]
    print(f"Test 5: {solution.numIslands([row[:] for row in grid5])}")  # Expected: 1

if __name__ == "__main__":
    test_number_of_islands()


"""
Key Interview Points to Discuss:

1. PROBLEM UNDERSTANDING:
   - Connected components problem in a 2D grid
   - Each island is a connected component of '1's
   - 4-directional connectivity (not diagonal)
   - Need to avoid double-counting same island

2. CORE ALGORITHM:
   - Iterate through entire grid
   - When find unvisited '1', increment island count
   - Use DFS/BFS to mark entire connected component as visited
   - Continue until grid is fully processed

3. MARKING STRATEGIES:
   - Sink islands: Change '1' to '0' (modifies input)
   - Visited set: Track coordinates (preserves input)
   - Temporary marker: Use different character (can restore)

4. EDGE CASES TO MENTION:
   - Empty grid
   - All water (no islands)
   - All land (one big island)
   - Single cell
   - Linear arrangements (rows/columns)

5. TIME/SPACE COMPLEXITY:
   - Time: O(M*N) - each cell visited at most once
   - Space: O(min(M,N)) for BFS queue, O(M*N) worst case for DFS recursion

6. FOLLOW-UP QUESTIONS TO EXPECT:
   - "What if grid is very large?" -> BFS or iterative DFS
   - "Can't modify input?" -> Use visited set
   - "Dynamic updates?" -> Union-Find approach
   - "Find largest island?" -> Track sizes during traversal
   - "8-directional connectivity?" -> Add diagonal directions
   - "Different shapes?" -> Modify neighbor directions

7. COMPARISON WITH RELATED PROBLEMS:
   - Flood Fill: Similar traversal, different goal
   - Surrounded Regions: Mark safe regions vs count components
   - Max Area of Island: Track area during traversal

8. OPTIMIZATION OPPORTUNITIES:
   - Early termination if only counting
   - Parallel processing for independent regions
   - Compressed representations for sparse grids

9. REAL-WORLD APPLICATIONS:
   - Image processing (connected components)
   - Network analysis (isolated clusters)
   - Geographic information systems
   - Game development (terrain analysis)
"""
